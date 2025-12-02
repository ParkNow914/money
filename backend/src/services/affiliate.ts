import fs from "fs-extra";
import path from "node:path";

interface AffiliateRule {
  keyword: string;
  url: string;
}

interface AffiliateConfig {
  defaultTracker?: string;
  rules: AffiliateRule[];
}

const configPath = path.resolve(process.cwd(), "affiliates.json");
let configCache: AffiliateConfig | null = null;

async function loadConfig(): Promise<AffiliateConfig> {
  if (configCache) {
    return configCache;
  }

  try {
    const raw = await fs.readFile(configPath, "utf8");
    configCache = JSON.parse(raw) as AffiliateConfig;
    return configCache;
  } catch (error) {
    console.warn("[affiliate] Unable to read affiliates.json, using default config", error);
    configCache = { rules: [] };
    return configCache;
  }
}

export async function injectAffiliateLinks(text: string): Promise<{ enriched: string; links: string[] }> {
  const config = await loadConfig();
  const links: string[] = [];
  let enriched = text;

  for (const rule of config.rules) {
    if (text.toLowerCase().includes(rule.keyword.toLowerCase())) {
      links.push(rule.url);
      enriched += `\nOferta recomendada: ${rule.url}`;
    }
  }

  const tracker = config.defaultTracker || process.env.AFFILIATE_DEFAULT_TRACKER;
  if (!links.length && tracker) {
    const defaultLink = `https://example.com?trk=${tracker}`;
    enriched += `\nOferta padrão: ${defaultLink}`;
    links.push(defaultLink);
  }

  return { enriched, links };
}
