import { FormEvent, useMemo, useState } from "react";

const modelTiers = [
  { value: "lite", label: "Lite (sempre grátis)", base: 0.0005 },
  { value: "standard", label: "Standard (cluster otimizado)", base: 0.002 },
  { value: "premium", label: "Premium (quando orçamento permitir)", base: 0.02 },
];

const API_BASE = import.meta.env.VITE_API_BASE || "";

interface ResultPayload {
  result: string;
  cached: boolean;
  costEstimate: number;
  jobId: string;
  modelTier: string;
}

interface Props {
  onResult: (payload: ResultPayload) => void;
}

function estimateCost(prompt: string, tier: string): number {
  const tierBase = modelTiers.find((t) => t.value === tier)?.base ?? 0.0005;
  const tokens = Math.max(prompt.length / 4, 1);
  return Number((tierBase * (tokens / 100)).toFixed(4));
}

function IAForm({ onResult }: Props) {
  const [prompt, setPrompt] = useState("Quero um plano viral para monetizar o free tier.");
  const [tier, setTier] = useState("lite");
  const [userId, setUserId] = useState("demo-user");
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<string | null>(null);

  const estimatedCost = useMemo(() => estimateCost(prompt, tier), [prompt, tier]);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setLoading(true);
    setStatus("Enviando...");
    try {
      const response = await fetch(`${API_BASE}/api/v1/ia/generate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-user-id": userId,
        },
        body: JSON.stringify({ prompt, modelTier: tier }),
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.message || "Erro ao gerar texto");
      }
      setStatus(data.cached ? "Cache hit: custo reduzido" : "Processamento completo");
      onResult(data);
    } catch (error) {
      setStatus((error as Error).message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <form className="flex flex-col gap-4" onSubmit={handleSubmit}>
      <label className="flex flex-col gap-2">
        <span>Prompt</span>
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          rows={4}
          required
          placeholder="Descreva o que deseja gerar"
        />
      </label>
      <label className="flex flex-col gap-2">
        <span>Modelo</span>
        <select value={tier} onChange={(e) => setTier(e.target.value)}>
          {modelTiers.map((model) => (
            <option key={model.value} value={model.value}>
              {model.label}
            </option>
          ))}
        </select>
      </label>
      <label className="flex flex-col gap-2">
        <span>User ID (x-user-id header)</span>
        <input value={userId} onChange={(e) => setUserId(e.target.value)} />
      </label>
      <div className="text-sm text-slate-600">
        Estimativa de custo: US$ {estimatedCost.toFixed(5)} (mostrado apenas para admin)
      </div>
      {status && <div className="text-sm text-blue-600">{status}</div>}
      <button type="submit" disabled={loading} className="bg-blue-600 text-white py-2 rounded">
        {loading ? "Processando..." : "Gerar"}
      </button>
    </form>
  );
}

export default IAForm;
