import fs from "fs-extra";
import path from "node:path";
import { randomUUID } from "node:crypto";

import { LedgerEntry } from "../types";

const dataDir = path.resolve(process.cwd(), "data");
const ledgerFile = path.join(dataDir, "ledger.jsonl");

async function ensureDataDir(): Promise<void> {
  await fs.ensureDir(dataDir);
  if (!(await fs.pathExists(ledgerFile))) {
    await fs.writeFile(ledgerFile, "", "utf8");
  }
}

export async function appendLedgerEntry(partial: Omit<LedgerEntry, "id" | "createdAt">): Promise<LedgerEntry> {
  await ensureDataDir();
  const entry: LedgerEntry = {
    id: randomUUID(),
    createdAt: new Date().toISOString(),
    ...partial,
  };
  await fs.appendFile(ledgerFile, `${JSON.stringify(entry)}\n`);
  return entry;
}

export async function readLedgerEntries(limit = 200): Promise<LedgerEntry[]> {
  await ensureDataDir();
  const content = await fs.readFile(ledgerFile, "utf8");
  return content
    .split("\n")
    .filter(Boolean)
    .slice(-limit)
    .map((line) => JSON.parse(line) as LedgerEntry);
}

export async function totalRevenue(): Promise<number> {
  const entries = await readLedgerEntries(2000);
  return entries.reduce((acc, entry) => acc + (entry.amountUsd || 0), 0);
}

export async function recordMonetizableEvent(eventType: LedgerEntry["eventType"], userId: string, amountUsd: number, metadata: Record<string, unknown> = {}): Promise<LedgerEntry> {
  return appendLedgerEntry({ eventType, userId, amountUsd, metadata });
}

export function getLedgerFilePath(): string {
  return ledgerFile;
}
