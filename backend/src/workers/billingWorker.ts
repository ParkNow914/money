import cron from "node-cron";
import fs from "fs-extra";
import path from "node:path";
import { randomUUID } from "node:crypto";

import { readLedgerEntries } from "../services/ledger";

const invoicesDir = path.resolve(process.cwd(), "data", "invoices");

export function scheduleBillingWorker(): void {
  cron.schedule("*/30 * * * *", async () => {
    await runBillingCycle();
  });
}

export async function runBillingCycle(): Promise<void> {
  await fs.ensureDir(invoicesDir);
  const entries = await readLedgerEntries(500);
  const amountUsd = entries.reduce((acc, entry) => acc + entry.amountUsd, 0);
  const invoice = {
    id: randomUUID(),
    createdAt: new Date().toISOString(),
    amountUsd,
    items: entries.slice(-20),
  };

  if (process.env.STRIPE_KEY) {
    console.info("[billing] Stripe key detected. Capture flow would run here.");
  } else {
    const file = path.join(invoicesDir, `${invoice.id}.json`);
    await fs.writeJson(file, invoice, { spaces: 2 });
    console.info("[billing] Invoice salvo localmente", file);
  }
}
