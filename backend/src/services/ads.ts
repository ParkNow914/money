import fs from "fs-extra";
import path from "node:path";

const adsFile = path.resolve(process.cwd(), process.env.ADS_SOURCE_FILE || "adsdb.json");

export interface AdSlot {
  id: string;
  title: string;
  cta: string;
  url: string;
}

export async function chooseAd(): Promise<AdSlot | null> {
  try {
    const ads = (await fs.readJson(adsFile)) as AdSlot[];
    if (!ads.length) return null;
    return ads[Math.floor(Math.random() * ads.length)];
  } catch {
    return null;
  }
}
