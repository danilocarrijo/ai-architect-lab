import { tokenize } from './text.js';

// Reciprocal Rank Fusion: combina rankings de escalas diferentes (cosseno x BM25) usando só a posição.
export function rrf(lists, k = 60) {
  const scores = new Map();
  for (const list of lists) list.forEach((r, i) => scores.set(r.id, (scores.get(r.id) ?? 0) + 1 / (k + i + 1)));
  return [...scores].map(([id, score]) => ({ id, score })).sort((a, b) => b.score - a.score);
}

// Retriever híbrido: vetorial (semântico) + BM25 (lexical) -> RRF -> rerank -> corte por relevância.
export class HybridRetriever {
  constructor({ store, bm25, embedder, cfg }) {
    Object.assign(this, { store, bm25, embedder, cfg });
  }

  // Reranker leve: cobertura ponderada por IDF dos termos da pergunta no chunk.
  // Em produção: cross-encoder (Cohere Rerank, bge-reranker) ou LLM-as-reranker.
  rerank(query, candidates) {
    const N = this.bm25.docs.length;
    const q = [...new Set(tokenize(query))];
    const w = (t) => Math.log(1 + N / (this.bm25.df.get(t) ?? 1));
    const total = q.reduce((s, t) => s + w(t), 0) || 1;
    return candidates
      .map((c) => {
        const toks = new Set(tokenize(c.text));
        const coverage = q.reduce((s, t) => s + (toks.has(t) ? w(t) : 0), 0) / total;
        return { ...c, coverage, score: 0.7 * coverage + 0.3 * Math.max(c.cos, 0) };
      })
      .sort((a, b) => b.score - a.score);
  }

  async retrieve(query, { filter, k = this.cfg.topK } = {}) {
    const allow = filter && Object.keys(filter).length ? this.store.filterIds(filter) : undefined;
    const n = this.cfg.topKCandidates;
    const [qv] = await this.embedder.embed([query]);
    const vec = this.store.search(qv, n, allow);
    const lex = this.bm25.search(query, n, allow);
    const cosById = new Map(vec.map((r) => [r.id, r.score]));
    const candidates = rrf([vec, lex], this.cfg.rrfK)
      .slice(0, n)
      .map((r) => ({ ...this.store.get(r.id), vector: undefined, cos: cosById.get(r.id) ?? 0, rrf: r.score }));
    return this.rerank(query, candidates)
      .filter((c) => c.score >= this.cfg.minScore)
      .slice(0, k);
  }
}
