"use client";

import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { api } from "@/lib/api";

type Candidate = {
  id: number;
  full_name: string;
  email: string;
};

export default function Home() {
  const { data, isLoading, isError } = useQuery<Candidate[]>({
    queryKey: ["candidates"],
    queryFn: async () => (await api.get("/candidates/")).data,
  });

  const [filter, setFilter] = useState("");
  const filtered = (data ?? []).filter((c) =>
    c.full_name.toLowerCase().includes(filter.toLowerCase())
  );

  if (isLoading) return <p className="p-8">Loading…</p>;
  if (isError || !data) return <p className="p-8 text-red-500">Error!</p>;

  return (
    <main className="p-8 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Candidate List</h1>

      {/* ❶ フィルタ入力 */}
      <input
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
        placeholder="Search by name…"
        className="mb-4 w-full max-w-sm rounded border px-3 py-1"
      />

      {/* ❷ 件数ゼロのとき */}
      {filtered.length === 0 && (
        <p className="text-gray-500">No candidates yet.</p>
      )}

      {/* ❸ テーブル */}
      {filtered.length > 0 && (
        <table className="w-full border-collapse text-sm">
          <thead className="bg-gray-100">
            <tr>
              <th className="px-3 py-2 text-left">ID</th>
              <th className="px-3 py-2 text-left">Name</th>
              <th className="px-3 py-2 text-left">Email</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((c) => (
              <tr
                key={c.id}
                className="border-b hover:bg-gray-50 transition-colors"
              >
                <td className="px-3 py-2">{c.id}</td>
                <td className="px-3 py-2">{c.full_name}</td>
                <td className="px-3 py-2">{c.email}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </main>
  );
}
