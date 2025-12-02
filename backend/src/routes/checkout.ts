import { Router, Request, Response } from "express";

import { appendLedgerEntry } from "../services/ledger";
import { purchaseMarketplaceItem } from "../services/marketplace";

const router = Router();

router.post("/checkout", async (req: Request, res: Response) => {
  const userId = req.user?.id ?? "anon";
  const { itemId } = req.body;
  if (!itemId) {
    return res.status(400).json({ message: "itemId é obrigatório" });
  }
  const item = await purchaseMarketplaceItem(userId, itemId);
  if (!item) {
    return res.status(404).json({ message: "Item não encontrado" });
  }

  if (process.env.STRIPE_KEY) {
    console.info("[checkout] Stripe disponível. Rodaria Stripe PaymentIntent aqui");
  } else {
    const invoice = {
      userId,
      itemId,
      amountUsd: item.priceUsd,
      createdAt: new Date().toISOString(),
      mode: "manual",
    };
    await appendLedgerEntry({ userId, eventType: "checkout", amountUsd: item.priceUsd, metadata: invoice });
  }

  res.json({ message: "Compra registrada", item });
});

export default router;
