import fs from "fs-extra";
import path from "node:path";

import { readLedgerEntries } from "./ledger";

const outputFile = path.resolve(process.cwd(), "data", "telemetry-dataset.json");

export async function runTelemetryAggregation(): Promise<{ file: string; checksum: string }> {
  const entries = await readLedgerEntries(5000);
  const byType = entries.reduce<Record<string, number>>((acc, entry) => {
    acc[entry.eventType] = (acc[entry.eventType] || 0) + 1;
    return acc;
  }, {});

  const summary = {
    generatedAt: new Date().toISOString(),
    totalEvents: entries.length,
    byType,
  };

  await fs.ensureDir(path.dirname(outputFile));
  await fs.writeJson(outputFile, summary, { spaces: 2 });
  const checksum = Buffer.from(JSON.stringify(summary)).toString("base64");
  return { file: outputFile, checksum };
}

export async function getDatasetCatalog(): Promise<{ file: string; generatedAt: string }> {
  try {
    const content = await fs.readJson(outputFile);
    return { file: outputFile, generatedAt: content.generatedAt };
  } catch {
    return { file: outputFile, generatedAt: "pending" };
  }
}
