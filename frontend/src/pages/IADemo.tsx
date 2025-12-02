import { useState } from "react";

import IAForm from "../components/IAForm";
import ResultCard from "../components/ResultCard";

interface ResultPayload {
  result: string;
  cached: boolean;
  costEstimate: number;
  jobId: string;
  modelTier: string;
  affiliateLinks?: string[];
}

function IADemo() {
  const [output, setOutput] = useState<ResultPayload | null>(null);

  return (
    <section className="grid gap-8 md:grid-cols-2">
      <div>
        <h1 className="text-2xl font-semibold mb-4">Demo de IA</h1>
        <IAForm onResult={setOutput} />
      </div>
      <div className="space-y-4">
        <h2 className="font-semibold">Resultado</h2>
        {output ? (
          <ResultCard
            result={output.result}
            cached={output.cached}
            links={output.affiliateLinks}
            modelTier={output.modelTier}
          />
        ) : (
          <p className="text-sm text-slate-500">Envie um prompt para ver a mágica.</p>
        )}
      </div>
    </section>
  );
}

export default IADemo;
