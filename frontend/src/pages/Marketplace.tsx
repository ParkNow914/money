import { FormEvent, useCallback, useEffect, useState } from "react";

const API_BASE = import.meta.env.VITE_API_BASE || "";

type Item = {
  id: string;
  title: string;
  description: string;
  priceUsd: number;
  sellerId: string;
  downloadUrl: string;
  tags: string[];
};

function Marketplace() {
  const [items, setItems] = useState<Item[]>([]);
  const [form, setForm] = useState({ title: "", description: "", priceUsd: "5", tags: "" });
  const [userId, setUserId] = useState("seller-demo");
  const [status, setStatus] = useState<string | null>(null);

  const loadItems = useCallback(async () => {
    const response = await fetch(`${API_BASE}/api/v1/marketplace/items`);
    const data = await response.json();
    setItems(data);
  }, []);

  useEffect(() => {
    loadItems();
  }, [loadItems]);

  async function handleUpload(event: FormEvent) {
    event.preventDefault();
    setStatus("Enviando...");
    const response = await fetch(`${API_BASE}/api/v1/marketplace/upload`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-user-id": userId,
      },
      body: JSON.stringify({
        ...form,
        priceUsd: Number(form.priceUsd),
        tags: form.tags.split(",").map((tag) => tag.trim()).filter(Boolean),
      }),
    });
    if (response.ok) {
      setStatus("Produto publicado");
      setForm({ title: "", description: "", priceUsd: "5", tags: "" });
      loadItems();
    } else {
      const data = await response.json();
      setStatus(data.message || "Erro");
    }
  }

  async function handleCheckout(itemId: string) {
    const response = await fetch(`${API_BASE}/api/v1/checkout`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-user-id": userId,
      },
      body: JSON.stringify({ itemId }),
    });
    const data = await response.json();
    setStatus(data.message || "Compra efetuada");
  }

  return (
    <section className="space-y-6">
      <h1 className="text-3xl font-semibold">Marketplace sempre grátis</h1>
      <p className="text-sm text-slate-500">
        Upload gratuito, ledger automático e checkout manual caso Stripe não esteja configurado.
      </p>
      <form className="grid gap-3" onSubmit={handleUpload}>
        <h2 className="text-xl font-semibold">Enviar produto</h2>
        <label className="flex flex-col gap-1">
          <span>Título</span>
          <input value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} required />
        </label>
        <label className="flex flex-col gap-1">
          <span>Descrição</span>
          <textarea
            rows={3}
            value={form.description}
            onChange={(e) => setForm({ ...form, description: e.target.value })}
            required
          />
        </label>
        <label className="flex flex-col gap-1">
          <span>Preço (USD)</span>
          <input
            type="number"
            value={form.priceUsd}
            onChange={(e) => setForm({ ...form, priceUsd: e.target.value })}
            min="0"
            step="0.5"
            required
          />
        </label>
        <label className="flex flex-col gap-1">
          <span>Tags (separadas por vírgula)</span>
          <input value={form.tags} onChange={(e) => setForm({ ...form, tags: e.target.value })} />
        </label>
        <label className="flex flex-col gap-1">
          <span>User ID</span>
          <input value={userId} onChange={(e) => setUserId(e.target.value)} />
        </label>
        <button className="bg-emerald-600 text-white py-2 rounded" type="submit">
          Publicar no marketplace
        </button>
      </form>
      {status && <p className="text-sm text-blue-600">{status}</p>}
      <div className="grid gap-4 md:grid-cols-2">
        {items.map((item) => (
          <article key={item.id} className="bg-white p-4 rounded shadow">
            <h3 className="text-lg font-semibold">{item.title}</h3>
            <p className="text-sm text-slate-500">{item.description}</p>
            <p className="text-sm mt-2">US$ {item.priceUsd.toFixed(2)}</p>
            <button className="mt-3 bg-slate-900 text-white px-3 py-1 text-sm" onClick={() => handleCheckout(item.id)}>
              Comprar (stub)
            </button>
          </article>
        ))}
      </div>
    </section>
  );
}

export default Marketplace;
