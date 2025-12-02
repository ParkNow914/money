import { beforeAll, describe, expect, it } from "vitest";

process.env.HF_API_KEY = "";

let generateIAResponse: typeof import("../backend/src/services/iaAdapter") extends { generateIAResponse: infer T }
  ? T
  : never;

beforeAll(async () => {
  ({ generateIAResponse } = await import("../backend/src/services/iaAdapter"));
});

describe("iaAdapter", () => {
  it("usa fallback determinístico quando não há HF_API_KEY", async () => {
    const result = await generateIAResponse({ prompt: "Teste IA", userId: "tester" });
    expect(result.text).toContain("Resposta determinística");
    expect(result.affiliateLinks?.length).toBeGreaterThan(0);
  });
});
