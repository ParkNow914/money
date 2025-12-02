import { Router, Request, Response } from "express";
import fs from "fs-extra";
import path from "node:path";

import { KycRequest } from "../types";

const router = Router();
const kycFile = path.resolve(process.cwd(), "data", "kycRequests.json");

async function ensureKycFile(): Promise<void> {
  await fs.ensureDir(path.dirname(kycFile));
  if (!(await fs.pathExists(kycFile))) {
    await fs.writeJson(kycFile, []);
  }
}

router.post("/kyc/submit", async (req: Request, res: Response) => {
  const userId = req.user?.id ?? "anon";
  await ensureKycFile();
  const requests = (await fs.readJson(kycFile)) as KycRequest[];
  const request: KycRequest = {
    id: `${userId}-${Date.now()}`,
    userId,
    status: "pending",
    submittedAt: new Date().toISOString(),
    payload: req.body || {},
  };
  requests.push(request);
  await fs.writeJson(kycFile, requests, { spaces: 2 });
  res.status(201).json({ message: "KYC recebido", requestId: request.id });
});

export default router;
