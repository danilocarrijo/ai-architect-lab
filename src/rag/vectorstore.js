import fs from 'node:fs/promises';
import path from 'node:path';
import { cosine } from './embeddings.js';

// Vector store em memória com persistência em JSON. Em produção: pgvector, Qdrant, etc.
// A busca é força-bruta O(n); índices ANN (HNSW/IVF) trocam precisão por velocidade.
export class VectorStore {
  constructor() {
    this.items = [];
  }
  add(chunks, vectors) {
    chunks.forEach((c, i) => this.items.push({ ...c, vector: Array.from(vectors[i]) }));
  }
  get(id) {
    return this.items.find((i) => i.id === id);
  }
  // filtro por metadados (pre-filter) — essencial para multi-tenant e controle de acesso
  filterIds(filter = {}) {
    return new Set(
      this.items.filter((i) => Object.entries(filter).every(([k, v]) => i.meta[k] === v)).map((i) => i.id),
    );
  }
  search(qVec, k, allow) {
    return this.items
      .filter((i) => !allow || allow.has(i.id))
      .map((i) => ({ id: i.id, score: cosine(qVec, i.vector) }))
      .sort((a, b) => b.score - a.score)
      .slice(0, k);
  }
  async save(file, embedderName) {
    await fs.mkdir(path.dirname(file), { recursive: true });
    await fs.writeFile(file, JSON.stringify({ embedder: embedderName, items: this.items }));
  }
  static async load(file, embedderName) {
    const raw = JSON.parse(await fs.readFile(file, 'utf8'));
    if (raw.embedder !== embedderName) throw new Error('Índice criado com outro embedder: reindexe.');
    const s = new VectorStore();
    s.items = raw.items;
    return s;
  }
}
