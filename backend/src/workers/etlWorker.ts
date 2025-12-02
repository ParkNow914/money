import cron from "node-cron";

import { runTelemetryAggregation } from "../services/etl";

export function scheduleEtlWorker(): void {
  cron.schedule("0 1 * * *", async () => {
    const result = await runTelemetryAggregation();
    console.info("[etlWorker] Dataset atualizado", result);
  });
}

export async function runEtlNow(): Promise<void> {
  await runTelemetryAggregation();
}
