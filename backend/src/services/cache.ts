import Redis from "ioredis";

const DAY_IN_SECONDS = 60 * 60 * 24;

export interface CacheStats {
  hits: number;
  misses: number;
}

class CacheService {
  private redis: Redis | null;
  private memoryStore = new Map<string, { value: string; expiresAt: number }>();
  private stats: CacheStats = { hits: 0, misses: 0 };

  constructor() {
    const redisUrl = process.env.REDIS_URL;
    if (redisUrl) {
      this.redis = new Redis(redisUrl, {
        maxRetriesPerRequest: 2,
        enableReadyCheck: false,
      });
      this.redis.on("error", (err: Error) => {
        console.warn("[cache] Redis error, falling back to memory", err.message);
      });
    } else {
      this.redis = null;
      console.warn("[cache] REDIS_URL not provided. Using in-memory cache only.");
    }
  }

  public async get(key: string): Promise<string | null> {
    if (this.redis) {
      const value = await this.redis.get(key);
      if (value) {
        this.stats.hits += 1;
        return value;
      }
      this.stats.misses += 1;
      return null;
    }

    const record = this.memoryStore.get(key);
    if (record && record.expiresAt > Date.now()) {
      this.stats.hits += 1;
      return record.value;
    }
    if (record) {
      this.memoryStore.delete(key);
    }
    this.stats.misses += 1;
    return null;
  }

  public async set(key: string, value: string, ttlSeconds = DAY_IN_SECONDS): Promise<void> {
    if (this.redis) {
      await this.redis.set(key, value, "EX", ttlSeconds);
      return;
    }
    this.memoryStore.set(key, { value, expiresAt: Date.now() + ttlSeconds * 1000 });
  }

  public getStats(): CacheStats {
    return this.stats;
  }
}

export const cacheService = new CacheService();
