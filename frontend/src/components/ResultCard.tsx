interface ResultCardProps {
  result: string;
  cached: boolean;
  links?: string[];
  modelTier?: string;
}

function ResultCard({ result, cached, links = [], modelTier }: ResultCardProps) {
  return (
    <article className="border rounded-lg p-4 bg-white shadow-sm">
      <header className="flex items-center justify-between text-xs text-slate-500 mb-3">
        <span>{cached ? "Servido do cache (economia 90%)" : "Processado em tempo real"}</span>
        {modelTier && <span>Tier: {modelTier}</span>}
      </header>
      <p className="whitespace-pre-wrap text-sm leading-relaxed">{result}</p>
      {links.length > 0 && (
        <div className="mt-3 text-sm">
          <p className="font-semibold">Ofertas recomendadas:</p>
          <ul>
            {links.map((link) => (
              <li key={link}>
                <a href={link} target="_blank" rel="noreferrer" className="text-blue-600">
                  {link}
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}
    </article>
  );
}

export default ResultCard;
