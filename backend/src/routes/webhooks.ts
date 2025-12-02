import { Router, Request, Response } from "express";

import { appendLedgerEntry } from "../services/ledger";

const router = Router();

router.post("/stripe", async (req: Request, res: Response) => {
  if (!process.env.STRIPE_WEBHOOK_SECRET) {
    return res.json({ message: "Stripe não configurado. noop." });
  }
  await appendLedgerEntry({
    userId: req.body?.data?.object?.customer || "stripe",
    eventType: "stripe.webhook",
    amountUsd: req.body?.data?.object?.amount_paid / 100 || 0,
    metadata: { type: req.body.type },
  });
  res.json({ received: true });
});

router.post("/ads/revenue", async (req: Request, res: Response) => {
  await appendLedgerEntry({
    userId: "ads",
    eventType: "ads.revenue",
    amountUsd: Number(req.body.amountUsd || 0),
    metadata: req.body,
  });
  res.json({ ok: true });
});

router.post("/affiliate/notification", async (req: Request, res: Response) => {
  await appendLedgerEntry({
    userId: "affiliate",
    eventType: "affiliate.click",
    amountUsd: Number(req.body.commission || 0),
    metadata: req.body,
  });
  res.json({ ok: true });
});

export default router;
