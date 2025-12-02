# Monitoring & Alerts

This stack ships with hooks for Sentry (application layer) and AWS CloudWatch (infrastructure). Use this guide to wire them up quickly.

## 1. Sentry (application errors and traces)

1. Create a project in Sentry (Platform: **Node.js**).
2. Copy the DSN and set the variables below in `.env` (or in your hosting provider):
   - `SENTRY_DSN`
   - `SENTRY_ENVIRONMENT` (optional, e.g. `production`, `staging`)
   - `SENTRY_TRACES_SAMPLE_RATE` (0–1; default 0.1 for the backend)
3. Deploy the backend. The initialization already exists in `backend/src/index.ts`; no code changes needed.
4. Verify events by hitting `/api/v1/ia` with invalid payloads and checking Sentry for the captured exception + request fingerprint.

### Recommended alerts

- **Error spike**: alert if events/minute exceed baseline for 5 minutes.
- **APEX fallback**: create a metric alert based on the tag `ia-provider` (set in `services/iaAdapter.ts`) when the provider equals `deterministic` more than 30% of the time.

## 2. CloudWatch (infrastructure)

Terraform already provisions:

- ECS cluster logs to `/aws/ecs/${project_slug}-api`.
- Application Load Balancer metrics.
- Container Insights for CPU/memory.

### Dashboards

Use the snippet below as a starting point (replace the region/ARNs with the outputs from `infra/terraform`):

```bash
aws cloudwatch put-dashboard \
  --dashboard-name always-free-api \
  --dashboard-body "$(cat <<'JSON'
{
  "widgets": [
    {
      "type": "metric",
      "width": 12,
      "height": 6,
      "properties": {
        "metrics": [
          [ "AWS/ApplicationELB", "RequestCount", "LoadBalancer", "${alb_arn_suffix}" ],
          [ ".", "HTTPCode_Target_5XX_Count", ".", "." ]
        ],
        "region": "${aws_region}",
        "stat": "Sum",
        "title": "ALB traffic"
      }
    },
    {
      "type": "metric",
      "width": 12,
      "height": 6,
      "properties": {
        "metrics": [
          [ "ECS/ContainerInsights", "CpuUtilized", "ClusterName", "${cluster_name}", "ServiceName", "${service_name}" ],
          [ ".", "MemoryUtilized", ".", ".", ".", "." ]
        ],
        "region": "${aws_region}",
        "title": "ECS Utilization"
      }
    }
  ]
}
JSON
)"
```

### Alarms

Create at least two alarms:

1. **ALB 5xx burst**

  ```bash
   aws cloudwatch put-metric-alarm \
     --alarm-name alb-5xx-spike \
     --metric-name HTTPCode_Target_5XX_Count \
     --namespace AWS/ApplicationELB \
     --stat Sum --period 60 --threshold 5 --comparison-operator GreaterThanThreshold \
     --dimensions Name=LoadBalancer,Value=${alb_arn_suffix} \
     --evaluation-periods 1 --alarm-actions arn:aws:sns:...:alert-topic
  ```

1. **ECS CPU saturation**

  ```bash
   aws cloudwatch put-metric-alarm \
     --alarm-name ecs-cpu-90 \
     --metric-name CpuUtilized --namespace ECS/ContainerInsights \
     --stat Average --period 60 --threshold 90 --comparison-operator GreaterThanThreshold \
     --dimensions Name=ClusterName,Value=${cluster_name} Name=ServiceName,Value=${service_name} \
     --evaluation-periods 5 --alarm-actions arn:aws:sns:...:alert-topic
  ```

## 3. Log shipping (optional)

- Subscribe the CloudWatch log group to a Lambda or Kinesis Firehose if you need logs in Datadog/Splunk.
- Configure log retention via the `aws_cloudwatch_log_group.api` resource in Terraform (default 14 days).

## 4. Runbook checklist

| Symptom | Checks | Next Action |
| --- | --- | --- |
| High IA latency | Inspect `services/iaAdapter.ts` logs for provider fallbacks | Increase HF quota or deploy private cluster (see roadmap) |
| Many 5xx from ALB | Open Sentry event, correlate with ECS task logs | Roll back release or restart service with `aws ecs update-service` |
| Memory pressure | Container Insights `MemoryUtilized` > 85% | Scale `desired_count` or `container_memory` variables and re-apply Terraform |
| Dataset export failing | Check ETL worker logs (`data/telemetry-dataset.json` timestamp) | Rerun worker locally with `npm run dev` or schedule via cron |

Keep this file close to on-call rotations so everyone knows how to triage issues quickly.
