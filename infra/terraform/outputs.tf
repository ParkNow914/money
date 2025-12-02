output "region" {
  value       = var.aws_region
  description = "AWS region used for the stack"
}

output "alb_dns" {
  value       = aws_lb.api.dns_name
  description = "Public endpoint for the backend"
}

output "ecs_cluster_name" {
  value       = aws_ecs_cluster.backend.name
  description = "ECS cluster where the API runs"
}

output "ecs_service_name" {
  value       = aws_ecs_service.api.name
  description = "Service managing Fargate tasks"
}

output "cloudwatch_log_group" {
  value       = aws_cloudwatch_log_group.api.name
  description = "Log group streaming container logs"
}

output "s3_dataset_bucket" {
  value       = aws_s3_bucket.datasets.bucket
  description = "Bucket for datasets/static assets"
}

output "rds_endpoint" {
  value       = aws_db_instance.ledger.address
  description = "Postgres endpoint for Supabase-compatible workloads"
}

output "vpc_id" {
  value       = module.vpc.vpc_id
  description = "ID of the provisioned VPC"
}

output "private_subnets" {
  value       = module.vpc.private_subnets
  description = "Private subnets used by ECS/RDS"
}
