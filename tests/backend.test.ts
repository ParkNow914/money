import path from "node:path";

import fs from "fs-extra";
import request from "supertest";
import { beforeAll, describe, expect, it } from "vitest";

process.env.NODE_ENV = "test";
process.env.PORT = "0";
process.env.HF_API_KEY = "";
process.env.REDIS_URL = "";

const dataDir = path.resolve(process.cwd(), "data");

beforeAll(async () => {
  await fs.ensureDir(dataDir);
  await fs.emptyDir(dataDir);
});

const { app } = await import("../backend/src/index");
const { getLedgerFilePath } = await import("../backend/src/services/ledger");

describe("backend API", () => {
  it("responds to /health", async () => {
    const response = await request(app).get("/health");
    expect(response.status).toBe(200);
    expect(response.body.status).toBe("ok");
  });

  it("handles IA generation and logs ledger", async () => {
    const response = await request(app)
      .post("/api/v1/ia/generate")
      .set("x-user-id", "test-user")
      .send({ prompt: "Teste de resposta" });

    expect(response.status).toBe(200);
    expect(response.body.result).toBeTruthy();

    const ledgerPath = getLedgerFilePath();
    const exists = await fs.pathExists(ledgerPath);
    expect(exists).toBe(true);
    const ledgerLines = (await fs.readFile(ledgerPath, "utf8")).trim().split("\n");
    expect(ledgerLines.pop()).toContain("ia.generate");
  });
});
