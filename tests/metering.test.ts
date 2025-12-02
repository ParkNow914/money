import { beforeAll, describe, expect, it, vi } from "vitest";

vi.mock("../backend/src/services/quotas", () => ({
  getQuotaLimit: vi.fn().mockImplementation(() => 1),
  getUsage: vi.fn().mockResolvedValue(1),
  incrementUsage: vi.fn().mockResolvedValue(2),
}));

vi.mock("../backend/src/services/ledger", () => ({
  recordMonetizableEvent: vi.fn().mockResolvedValue(undefined),
}));

let meteringMiddleware: typeof import("../backend/src/middleware/metering") extends { meteringMiddleware: infer T }
  ? T
  : never;

beforeAll(async () => {
  ({ meteringMiddleware } = await import("../backend/src/middleware/metering"));
});

function buildReq() {
  return {
    path: "/api/v1/ia/generate",
    method: "POST",
    user: { id: "tester", role: "user" },
  } as any;
}

function buildRes() {
  const headers: Record<string, string> = {};
  return {
    statusCode: 200,
    body: null as any,
    status(code: number) {
      this.statusCode = code;
      return this;
    },
    json(payload: unknown) {
      this.body = payload;
      return this;
    },
    setHeader(key: string, value: string) {
      headers[key] = value;
    },
    getHeader() {
      return headers["x-quota-used"];
    },
  } as any;
}

describe("meteringMiddleware", () => {
  it("soft-blocks repeated quota violations", async () => {
    const next = vi.fn();
    const req = buildReq();

    await meteringMiddleware(req, buildRes(), next);
    expect(next).toHaveBeenCalled();

    const res2 = buildRes();
    const next2 = vi.fn();
    await meteringMiddleware(req, res2, next2);

    expect(res2.statusCode).toBe(429);
    expect(next2).not.toHaveBeenCalled();
    expect(res2.body.upgrade_suggestion).toBeTruthy();
  });
});
