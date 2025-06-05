"use client";

import CytoscapeComponent from "react-cytoscapejs";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";

export default function GraphPage() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ["graph"],
    queryFn: async () => (await api.get("/graph/")).data,
  });

  if (isLoading) return <p className="p-8">Loading…</p>;
  if (isError) return <p className="p-8 text-red-500">Error!</p>;

  return (
    <main className="p-8 max-w-4xl mx-auto space-y-4">
      <h1 className="text-2xl font-bold">Network Graph</h1>
      <CytoscapeComponent
        elements={CytoscapeComponent.normalizeElements(data)}
        style={{ width: "100%", height: "500px", border: "1px solid #eee" }}
        layout={{ name: "cose" }}
        stylesheet={[
          { selector: "node", style: { label: "data(label)" } },
          { selector: "edge", style: { "target-arrow-shape": "triangle" } },
        ]}
      />
    </main>
  );
}
