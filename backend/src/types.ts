export type ModelTier = "lite" | "standard" | "premium";

export interface IAGenerateRequest {
  prompt: string;
  modelTier?: ModelTier;
  metadata?: Record<string, unknown>;
  userId: string;
  ip?: string;
}

export interface IAGenerateResponse {
  jobId: string;
  result: string;
  cached: boolean;
  costEstimate: number;
  modelTier: ModelTier;
  affiliateLinks?: string[];
}

export interface LedgerEntry {
  id: string;
  userId: string;
  eventType:
    | "ia.generate"
    | "marketplace.upload"
    | "marketplace.purchase"
    | "checkout"
    | "ads.impression"
    | "ads.revenue"
    | "affiliate.click"
    | "stripe.charge"
    | "stripe.webhook"
    | "dataset.publish"
    | "quota.exceeded";
  amountUsd: number;
  metadata: Record<string, unknown>;
  createdAt: string;
}

export interface MarketplaceItem {
  id: string;
  sellerId: string;
  title: string;
  description: string;
  priceUsd: number;
  downloadUrl: string;
  createdAt: string;
  tags: string[];
}

export interface JobRecord {
  id: string;
  status: "pending" | "completed" | "failed";
  result?: string;
  error?: string;
  createdAt: string;
  updatedAt: string;
  userId: string;
}

export interface CacheRecord {
  key: string;
  value: string;
  expiresAt: number;
}

export interface KycRequest {
  id: string;
  userId: string;
  status: "pending" | "approved" | "rejected";
  submittedAt: string;
  notes?: string;
  payload: Record<string, unknown>;
}

export interface MetricSnapshot {
  revenueUsd: number;
  quotaViolations: number;
  circuitBreakerDowngrades: number;
  cacheHitRate: number;
}
