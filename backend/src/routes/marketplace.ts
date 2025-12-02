import { Router, Request, Response } from "express";

import { chooseAd } from "../services/ads";
import { appendLedgerEntry } from "../services/ledger";
import { listMarketplaceItems, uploadMarketplaceItem } from "../services/marketplace";

const router = Router();

router.get("/items", async (_req: Request, res: Response) => {
  const items = await listMarketplaceItems();
  res.json(items);
});

router.post("/upload", async (req: Request, res: Response) => {
  if (!req.user) {
    return res.status(401).json({ message: "Usuário não identificado" });
  }
  const { title, description, priceUsd, downloadUrl, tags } = req.body;
  if (!title || !description || !priceUsd) {
    return res.status(400).json({ message: "Campos obrigatórios ausentes" });
  }
  const item = await uploadMarketplaceItem({
    sellerId: req.user.id,
    title,
    description,
    priceUsd,
    downloadUrl,
    tags,
  });
  res.status(201).json(item);
});

router.get("/ads/slot", async (_req: Request, res: Response) => {
  const ad = await chooseAd();
  if (!ad) return res.json({ message: "Sem anúncios" });
  await appendLedgerEntry({
    userId: "system",
    eventType: "ads.impression",
    amountUsd: 0.0001,
    metadata: { adId: ad.id },
  });
  res.json(ad);
});

export default router;
