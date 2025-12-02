export interface FraudContext {
  userId: string;
  ip?: string;
  userAgent?: string;
  locale?: string;
  recentRequests: number;
}

export interface FraudAssessment {
  riskScore: number;
  reasons: string[];
  escalateToKyc: boolean;
}

export function assessFraudRisk(ctx: FraudContext): FraudAssessment {
  let riskScore = 0;
  const reasons: string[] = [];

  if (ctx.recentRequests > 50) {
    riskScore += 30;
    reasons.push("usage spike");
  }

  if (ctx.ip && ctx.ip.startsWith("10.")) {
    riskScore += 10;
    reasons.push("suspicious private ip");
  }

  if (ctx.userAgent?.includes("curl")) {
    riskScore += 10;
    reasons.push("curl user agent");
  }

  const escalateToKyc = riskScore >= 40;
  return { riskScore, reasons, escalateToKyc };
}
