import { Router, Request, Response } from "express";

import { getJob } from "../services/jobs";

const router = Router();

router.get("/jobs/:id", async (req: Request, res: Response) => {
  const job = await getJob(req.params.id);
  if (!job) {
    return res.status(404).json({ message: "Job não encontrado" });
  }
  res.json(job);
});

export default router;
