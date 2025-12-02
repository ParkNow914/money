import { Router, Request, Response } from "express";
import { randomUUID } from "node:crypto";

import { cacheMiddleware, persistCache } from "../middleware/cacheMiddleware";
import { generateIAResponse } from "../services/iaAdapter";
import { appendLedgerEntry } from "../services/ledger";
import { assessFraudRisk } from "../services/fraud";
import { createJob, updateJob } from "../services/jobs";
import { IAGenerateRequest, IAGenerateResponse } from "../types";

const router = Router();

async function finishJob(jobId: string, payload: IAGenerateRequest): Promise<void> {
  try {
    const result = await generateIAResponse(payload);
    await updateJob(jobId, {
      status: "completed",
      result: result.text,
    });
    await appendLedgerEntry({
      userId: payload.userId,
      eventType: "ia.generate",
      amountUsd: result.costUsd,
      metadata: { tier: result.tier, async: true },
    });
  } catch (error) {
    await updateJob(jobId, {
      status: "failed",
      error: (error as Error).message,
    });
  }
}

router.post("/generate", cacheMiddleware, async (req: Request, res: Response) => {
  if (!req.body?.prompt) {
    return res.status(400).json({ message: "prompt é obrigatório" });
  }
  const userId = req.user?.id ?? "anon";
  const payload: IAGenerateRequest = {
    prompt: req.body.prompt,
    modelTier: req.body.modelTier,
    metadata: req.body.metadata,
    userId,
    ip: req.ip,
  };

  if (res.locals.cachedResult) {
    const cached = res.locals.cachedResult as IAGenerateResponse;
    await appendLedgerEntry({
      userId,
      eventType: "ia.generate",
      amountUsd: 0.0001,
      metadata: { cached: true },
    });
    return res.json({ ...cached, cached: true });
  }

  const fraud = assessFraudRisk({
    userId,
    ip: req.ip,
    userAgent: req.header("user-agent") || "",
    recentRequests: Number(res.get("x-quota-used")) || 0,
  });
  if (fraud.escalateToKyc) {
    return res.status(403).json({
      message: "Verificação adicional necessária. Envie seus documentos em /api/v1/kyc/submit",
      reasons: fraud.reasons,
    });
  }

  const shouldAsync = payload.prompt.length > 400 || req.body?.metadata?.async === true;
  if (shouldAsync) {
    const job = await createJob(userId);
    finishJob(job.id, payload);
    return res.status(202).json({ jobId: job.id, status: "pending" });
  }

  const result = await generateIAResponse(payload);
  const response: IAGenerateResponse = {
    jobId: randomUUID(),
    result: result.text,
    cached: false,
    costEstimate: result.costUsd,
    modelTier: result.tier,
    affiliateLinks: result.affiliateLinks,
  };
  if (res.locals.cacheKey) {
    await persistCache(res.locals.cacheKey as string, response, res.locals.cacheTtl);
  }
  await appendLedgerEntry({
    userId,
    eventType: "ia.generate",
    amountUsd: result.costUsd,
    metadata: { tier: result.tier },
  });
  return res.json(response);
});

export default router;
