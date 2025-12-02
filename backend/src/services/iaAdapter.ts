import fetch, { Response } from "node-fetch";

import { IAGenerateRequest, ModelTier } from "../types";
import { injectAffiliateLinks } from "./affiliate";
import { registerSpend, resolveTier } from "./circuitBreaker";

const tierModelMap: Record<ModelTier, string> = {
  lite: process.env.HF_MODEL_LITE || "tiiuae/falcon-7b-instruct",
  standard: process.env.HF_MODEL_STANDARD || "mistralai/Mistral-7B-Instruct-v0.2",
  premium: process.env.HF_MODEL_PREMIUM || "meta-llama/Llama-2-13b-chat-hf",
};

export function estimateCost(prompt: string, tier: ModelTier): number {
  const baseCost = {
    lite: 0.0005,
    standard: 0.002,
    premium: 0.02,
  }[tier];
  const tokens = Math.max(prompt.length / 4, 1);
  return Number((baseCost * (tokens / 100)).toFixed(4));
}

async function callHuggingFace(prompt: string, modelId: string): Promise<string> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 10_000);
  try {
    const response: Response = await fetch(`https://api-inference.huggingface.co/models/${modelId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${process.env.HF_API_KEY}`,
      },
      body: JSON.stringify({ inputs: prompt }),
      signal: controller.signal,
    });
    if (!response.ok) {
      throw new Error(`HF inference failed with status ${response.status}`);
    }
    const data = (await response.json()) as Array<{ generated_text?: string }>;
    return data?.[0]?.generated_text ?? "Sem resposta";
  } finally {
    clearTimeout(timeout);
  }
}

function fallbackGenerator(prompt: string): string {
  const reversed = prompt.split("").reverse().join("");
  return `Resposta determinística para: ${prompt.substring(0, 40)}... | Hash: ${Buffer.from(reversed).toString("base64").slice(0, 24)}`;
}

export async function generateIAResponse(request: IAGenerateRequest): Promise<{
  text: string;
  tier: ModelTier;
  costUsd: number;
  affiliateLinks: string[];
}> {
  const tier = resolveTier(request.modelTier ?? "lite");
  const costUsd = estimateCost(request.prompt, tier);
  let text: string;
  if (process.env.HF_API_KEY) {
    try {
      text = await callHuggingFace(request.prompt, tierModelMap[tier]);
    } catch (error) {
      console.warn("[iaAdapter] HF call failed, using fallback", error);
      text = fallbackGenerator(request.prompt);
    }
  } else {
    text = fallbackGenerator(request.prompt);
  }

  registerSpend(costUsd);
  const affiliate = await injectAffiliateLinks(text);
  return { text: affiliate.enriched, tier, costUsd, affiliateLinks: affiliate.links };
}
