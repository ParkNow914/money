import { NextFunction, Request, Response } from "express";

import { recordMonetizableEvent } from "../services/ledger";
import { getQuotaLimit, getUsage, incrementUsage } from "../services/quotas";

const SOFT_BLOCK_WINDOW = 5 * 60 * 1000;
const lastBlocked = new Map<string, number>();
const SKIP_PATHS = [/^\/health/, /^\/webhooks/, /^\/api\/v1\/admin/];

export async function meteringMiddleware(req: Request, res: Response, next: NextFunction): Promise<void> {
  if (SKIP_PATHS.some((pattern) => pattern.test(req.path))) {
    return next();
  }

  const userId = req.user?.id ?? "anon";
  const isPartner = req.user?.role === "partner";
  const limit = getQuotaLimit(userId, isPartner);
  const used = await getUsage(userId);

  if (used >= limit) {
    const last = lastBlocked.get(userId) ?? 0;
    if (Date.now() - last < SOFT_BLOCK_WINDOW) {
      await recordMonetizableEvent("quota.exceeded", userId, 0, { used, limit });
      res.status(429).json({
        message: "Limite diário atingido",
        upgrade_suggestion: "Ative um plano parceiro ou configure sua chave ADMIN_API_KEY",
        used,
        limit,
      });
      return;
    }
    lastBlocked.set(userId, Date.now());
  }

  const newUsage = await incrementUsage(userId);
  res.setHeader("x-quota-limit", String(limit));
  res.setHeader("x-quota-used", String(newUsage));

  next();
}
