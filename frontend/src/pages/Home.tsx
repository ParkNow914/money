import { useEffect, useState } from "react";

const API_BASE = import.meta.env.VITE_API_BASE || "";

interface AdSlot {
  id: string;
  title: string;
  cta: string;
  url: string;
}

function Home() {
  const [ad, setAd] = useState<AdSlot | null>(null);

  useEffect(() => {
    async function fetchAd() {
      const response = await fetch(`${API_BASE}/api/v1/marketplace/ads/slot`);
      const data = await response.json();
      if (data && data.id) setAd(data);
    }
    if (import.meta.env.VITE_ENABLE_ADS !== "false") {
      fetchAd();
    }
  }, []);

  return (
    <section className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold mb-4">Plataforma always free, pronta para vender</h1>
        <p className="text-lg text-slate-600">
          Comece com zero investimento: IA, marketplace, afiliados e dados em uma stack modular e
          segura. Monetização é automática e o usuário final continua gratuito.
        </p>
      </div>
      <div className="grid gap-6 md:grid-cols-3">
        <div className="p-4 bg-white rounded shadow">
          <h2 className="text-xl font-semibold">IA com cache inteligente</h2>
          <p className="text-sm text-slate-600">Inferência HuggingFace opcional + fallback determinístico.</p>
        </div>
        <div className="p-4 bg-white rounded shadow">
          <h2 className="text-xl font-semibold">Marketplace integrado</h2>
          <p className="text-sm text-slate-600">Envie produtos digitais, registre ledger e payouts simulados.</p>
        </div>
        <div className="p-4 bg-white rounded shadow">
          <h2 className="text-xl font-semibold">Dados e anúncios</h2>
          <p className="text-sm text-slate-600">Slots de ads e dataset diário alimentam novas receitas.</p>
        </div>
      </div>
      {ad && (
        <aside className="border border-dashed border-amber-400 rounded p-4 bg-amber-50">
          <p className="text-xs uppercase text-amber-600">Patrocinado</p>
          <h3 className="text-lg font-semibold">{ad.title}</h3>
          <a href={ad.url} target="_blank" rel="noreferrer" className="text-blue-600">
            {ad.cta}
          </a>
        </aside>
      )}
    </section>
  );
}

export default Home;
