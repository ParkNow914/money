import { afterEach, beforeAll, describe, expect, it } from "vitest";

process.env.REDIS_URL = "";

let cacheService: typeof import("../backend/src/services/cache").cacheService;

beforeAll(async () => {
  ({ cacheService } = await import("../backend/src/services/cache"));
});

afterEach(() => {
  // Clean stats between tests by reading them (not resetting to keep implementation simple)
});

describe("cache service", () => {
  it("stores and retrieves values with TTL", async () => {
    const key = `test-${Date.now()}`;
    await cacheService.set(key, "value", 1);
    expect(await cacheService.get(key)).toBe("value");
    await new Promise((resolve) => setTimeout(resolve, 1100));
    expect(await cacheService.get(key)).toBeNull();
  });

  it("tracks hits and misses", async () => {
    const key = `stats-${Date.now()}`;
    await cacheService.get(key);
    await cacheService.set(key, "ok");
    await cacheService.get(key);
    const stats = cacheService.getStats();
    expect(stats.hits).toBeGreaterThan(0);
    expect(stats.misses).toBeGreaterThan(0);
  });
});
