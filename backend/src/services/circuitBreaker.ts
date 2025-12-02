import pino from "pino";

import { ModelTier } from "../types";

const logger = pino({ name: "circuit-breaker" });

const DEFAULT_BUDGET = Number(process.env.CIRCUIT_BREAKER_DAILY_BUDGET ?? 5);
const state = {
  spentToday: 0,
  downgraded: false,
  downgradedTier: "lite" as ModelTier,
  lastReset: Date.now(),
};

function maybeReset(): void {
  const DAY_MS = 24 * 60 * 60 * 1000;
  if (Date.now() - state.lastReset > DAY_MS) {
    state.spentToday = 0;
    state.downgraded = false;
    state.lastReset = Date.now();
  }
}

export function registerSpend(cost: number): void {
  maybeReset();
  state.spentToday += cost;
  if (!state.downgraded && state.spentToday >= DEFAULT_BUDGET) {
    state.downgraded = true;
    logger.warn({ spend: state.spentToday }, "Daily budget exceeded. Downgrading to lite tier");
  }
}

export function resolveTier(requestedTier: ModelTier): ModelTier {
  maybeReset();
  if (state.downgraded && requestedTier !== "lite") {
    return "lite";
  }
  return requestedTier;
}

export function getCircuitBreakerState() {
  maybeReset();
  return { ...state, budget: DEFAULT_BUDGET };
}
