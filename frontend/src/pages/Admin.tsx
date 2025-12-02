import { useState } from "react";

const API_BASE = import.meta.env.VITE_API_BASE || "";

type Metrics = {
  revenueUsd: number;
  quotaViolations: number;
  circuitBreaker: { spentToday: number; downgraded: boolean; budget: number };
  cacheHitRate: number;
};

type Catalog = {
  file: string;
  generatedAt: string;
};

function Admin() {
  const [adminKey, setAdminKey] = useState("changeme-admin");
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [catalog, setCatalog] = useState<Catalog | null>(null);
  const [status, setStatus] = useState<string | null>(null);

  async function fetchMetrics() {
    setStatus("Consultando métricas...");
    const response = await fetch(`${API_BASE}/api/v1/admin/metrics`, {
      headers: { "x-admin-key": adminKey },
    });
    if (!response.ok) {
      const data = await response.json();
      setStatus(data.message || "Erro");
      return;
    }
    setMetrics(await response.json());
    setStatus(null);
  }

  async function fetchCatalog() {
    const response = await fetch(`${API_BASE}/api/v1/admin/data/catalog`, {
      headers: { "x-admin-key": adminKey },
    });
    if (!response.ok) {
      const data = await response.json();
      setStatus(data.message || "Erro");
      return;
    }
    setCatalog(await response.json());
  }

  return (
    <section className="space-y-4">
      <h1 className="text-3xl font-semibold">Painel Admin</h1>
      <label className="flex flex-col gap-1">
        <span>API Key admin</span>
        <input value={adminKey} onChange={(e) => setAdminKey(e.target.value)} />
      </label>
      <div className="flex gap-2">
        <button className="bg-blue-600 text-white px-4 py-2 rounded" onClick={fetchMetrics}>
          Atualizar métricas
        </button>
        <button className="bg-slate-900 text-white px-4 py-2 rounded" onClick={fetchCatalog}>
          Ver dataset
        </button>
      </div>
      {status && <p className="text-sm text-rose-600">{status}</p>}
      {metrics && (
        <div className="grid gap-3 md:grid-cols-2">
          <div className="bg-white rounded shadow p-4">
            <p className="text-xs uppercase text-slate-500">Receita total</p>
            <p className="text-2xl font-bold">US$ {metrics.revenueUsd.toFixed(2)}</p>
          </div>
          <div className="bg-white rounded shadow p-4">
            <p className="text-xs uppercase text-slate-500">Quota breaches</p>
            <p className="text-2xl font-bold">{metrics.quotaViolations}</p>
          </div>
          <div className="bg-white rounded shadow p-4">
            <p className="text-xs uppercase text-slate-500">Circuit breaker</p>
            <p>Gasto: US$ {metrics.circuitBreaker.spentToday.toFixed(2)} / {metrics.circuitBreaker.budget}</p>
            <p>Status: {metrics.circuitBreaker.downgraded ? "Downgrade ativo" : "Normal"}</p>
          </div>
          <div className="bg-white rounded shadow p-4">
            <p className="text-xs uppercase text-slate-500">Cache hit rate</p>
            <p>{(metrics.cacheHitRate * 100).toFixed(1)}%</p>
          </div>
        </div>
      )}
      {catalog && (
        <div className="bg-emerald-50 border border-emerald-200 rounded p-4 text-sm">
          <p>Dataset localizado em: {catalog.file}</p>
          <p>Gerado em: {catalog.generatedAt}</p>
        </div>
      )}
    </section>
  );
}

export default Admin;
