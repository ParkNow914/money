import fs from "fs-extra";
import path from "node:path";
import { randomUUID } from "node:crypto";

import { MarketplaceItem } from "../types";
import { appendLedgerEntry } from "./ledger";

const storagePath = path.resolve(process.cwd(), "data", "marketplace.json");

async function ensureStorage(): Promise<void> {
  await fs.ensureDir(path.dirname(storagePath));
  if (!(await fs.pathExists(storagePath))) {
    await fs.writeJson(storagePath, []);
  }
}

export async function listMarketplaceItems(): Promise<MarketplaceItem[]> {
  await ensureStorage();
  return fs.readJson(storagePath);
}

interface UploadPayload {
  sellerId: string;
  title: string;
  description: string;
  priceUsd: number;
  downloadUrl?: string;
  tags?: string[];
}

export async function uploadMarketplaceItem(payload: UploadPayload): Promise<MarketplaceItem> {
  await ensureStorage();
  const items = await listMarketplaceItems();
  const item: MarketplaceItem = {
    id: randomUUID(),
    sellerId: payload.sellerId,
    title: payload.title,
    description: payload.description,
    priceUsd: payload.priceUsd,
    downloadUrl: payload.downloadUrl ?? "https://example.com/download",
    createdAt: new Date().toISOString(),
    tags: payload.tags ?? [],
  };
  items.push(item);
  await fs.writeJson(storagePath, items, { spaces: 2 });
  await appendLedgerEntry({
    userId: payload.sellerId,
    eventType: "marketplace.upload",
    amountUsd: 0,
    metadata: { item },
  });
  return item;
}

export async function purchaseMarketplaceItem(userId: string, itemId: string): Promise<MarketplaceItem | null> {
  const items = await listMarketplaceItems();
  const item = items.find((entry) => entry.id === itemId) ?? null;
  if (!item) return null;
  await appendLedgerEntry({
    userId,
    eventType: "marketplace.purchase",
    amountUsd: item.priceUsd,
    metadata: { itemId },
  });
  return item;
}
