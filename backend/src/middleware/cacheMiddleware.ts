import { NextFunction, Request, Response } from "express";
import crypto from "node:crypto";

import { cacheService } from "../services/cache";

const DAY_SECONDS = 24 * 60 * 60;

export async function cacheMiddleware(req: Request, res: Response, next: NextFunction): Promise<void> {
  if (req.method !== "POST" || !req.body?.prompt) {
    return next();
  }

  const hash = crypto.createHash("sha256").update(`${req.body.prompt}-${req.body.modelTier || "lite"}`).digest("hex");
  res.locals.cacheKey = hash;
  const cached = await cacheService.get(hash);
  if (cached) {
    res.locals.cachedResult = JSON.parse(cached);
  }
  res.locals.cacheTtl = DAY_SECONDS;
  next();
}

export async function persistCache(key: string, payload: unknown, ttl = DAY_SECONDS): Promise<void> {
  await cacheService.set(key, JSON.stringify(payload), ttl);
}
