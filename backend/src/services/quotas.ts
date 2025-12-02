import fs from "fs-extra";
import path from "node:path";

const storageFile = path.resolve(process.cwd(), "data", "quotas.json");

interface UsageRecord {
  [date: string]: number;
}

const usageCache: Record<string, UsageRecord> = {};
let warnedDb = false;

async function ensureStorage(): Promise<void> {
  await fs.ensureDir(path.dirname(storageFile));
  if (!(await fs.pathExists(storageFile))) {
    await fs.writeJson(storageFile, {});
  }
}

async function loadUsage(): Promise<void> {
  if (Object.keys(usageCache).length) return;
  await ensureStorage();
  const data = await fs.readJson(storageFile);
  Object.assign(usageCache, data as Record<string, UsageRecord>);
}

async function persist(): Promise<void> {
  await fs.writeJson(storageFile, usageCache, { spaces: 2 });
}

function getTodayKey(): string {
  return new Date().toISOString().slice(0, 10);
}

export function getQuotaLimit(userId: string, isPartner = false): number {
  if (userId.startsWith("admin")) {
    return 10000;
  }
  if (isPartner) {
    return 2000;
  }
  return 100;
}

export async function incrementUsage(userId: string, incrementBy = 1): Promise<number> {
  if ((process.env.DATABASE_URL || process.env.SUPABASE_URL) && !warnedDb) {
    console.info("[quotas] DATABASE_URL detectado. Usando fallback em arquivo até configurar DB");
    warnedDb = true;
  }
  await loadUsage();
  const key = getTodayKey();
  usageCache[userId] = usageCache[userId] || {};
  usageCache[userId][key] = (usageCache[userId][key] || 0) + incrementBy;
  await persist();
  return usageCache[userId][key];
}

export async function getUsage(userId: string): Promise<number> {
  await loadUsage();
  const key = getTodayKey();
  return usageCache[userId]?.[key] ?? 0;
}
