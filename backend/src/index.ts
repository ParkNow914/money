import "dotenv/config";

import express, { Request, Response, NextFunction } from "express";
import cors from "cors";
import pino from "pino";
import crypto from "node:crypto";
import * as Sentry from "@sentry/node";

import iaRouter from "./routes/ia";
import marketplaceRouter from "./routes/marketplace";
import adminRouter from "./routes/admin";
import webhooksRouter from "./routes/webhooks";
import checkoutRouter from "./routes/checkout";
import jobsRouter from "./routes/jobs";
import kycRouter from "./routes/kyc";
import { getDatasetCatalog } from "./services/etl";
import { authMiddleware } from "./middleware/auth";
import { meteringMiddleware } from "./middleware/metering";
import { scheduleEtlWorker } from "./workers/etlWorker";
import { scheduleBillingWorker } from "./workers/billingWorker";

const logger = pino({ name: "api" });
const ADMIN_KEY = process.env.ADMIN_API_KEY || "admin";

if (process.env.SENTRY_DSN) {
  Sentry.init({ dsn: process.env.SENTRY_DSN, tracesSampleRate: 0.1 });
}

export const app = express();

if (process.env.SENTRY_DSN) {
  app.use(Sentry.Handlers.requestHandler());
}

app.use(cors());
app.use(express.json({ limit: "2mb" }));
app.use((req: Request, _res: Response, next: NextFunction) => {
  req.fingerprint = crypto.createHash("sha1").update(`${req.ip}-${req.headers["user-agent"] || ""}`).digest("hex");
  next();
});
app.use(authMiddleware);
app.use(meteringMiddleware);

app.get("/health", (_req: Request, res: Response) => {
  res.json({ status: "ok", now: new Date().toISOString() });
});

app.get("/data/catalog", async (req: Request, res: Response) => {
  if (req.header("x-admin-key") !== ADMIN_KEY) {
    return res.status(401).json({ message: "Chave admin inválida" });
  }
  const catalog = await getDatasetCatalog();
  res.json(catalog);
});

app.use("/api/v1/ia", iaRouter);
app.use("/api/v1/marketplace", marketplaceRouter);
app.use("/api/v1/admin", adminRouter);
app.use("/api/v1", checkoutRouter);
app.use("/api/v1", jobsRouter);
app.use("/api/v1", kycRouter);
app.use("/webhooks", webhooksRouter);

if (process.env.SENTRY_DSN) {
  app.use(Sentry.Handlers.errorHandler());
}

const port = Number(process.env.PORT || 4000);

export function startServer(): void {
  app.listen(port, () => {
    logger.info({ port }, "API pronta");
  });
  scheduleEtlWorker();
  scheduleBillingWorker();
}

if (process.env.NODE_ENV !== "test") {
  startServer();
}
