import { Router, Request, Response, NextFunction } from "express";

import { cacheService } from "../services/cache";
import { getDatasetCatalog } from "../services/etl";
import { getCircuitBreakerState } from "../services/circuitBreaker";
import { readLedgerEntries } from "../services/ledger";

const router = Router();
const ADMIN_KEY = process.env.ADMIN_API_KEY || "admin";

function requireAdmin(req: Request, res: Response, next: NextFunction): void {
  if (req.header("x-admin-key") !== ADMIN_KEY) {
    res.status(401).json({ message: "Chave admin inválida" });
    return;
  }
  next();
}

router.get("/metrics", requireAdmin, async (_req: Request, res: Response) => {
  const ledger = await readLedgerEntries(500);
  const revenue = ledger.reduce((acc, entry) => acc + entry.amountUsd, 0);
  const quotaViolations = ledger.filter((entry) => entry.eventType === "quota.exceeded").length;
  const breaker = getCircuitBreakerState();
  const cacheStats = cacheService.getStats();
  res.json({
    revenueUsd: revenue,
    quotaViolations,
    circuitBreaker: breaker,
    cacheHitRate: cacheStats.hits + cacheStats.misses === 0 ? 0 : cacheStats.hits / (cacheStats.hits + cacheStats.misses),
  });
});

router.get("/data/catalog", requireAdmin, async (_req: Request, res: Response) => {
  const catalog = await getDatasetCatalog();
  res.json(catalog);
});

export default router;
