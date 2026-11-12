import { cosine } from './embeddings.js';

// Cache semântico: perguntas parecidas reaproveitam a resposta (menos custo e latência).
// Cuidado: limiar alto demais = sem ganho; baixo demais = respostas erradas. Invalide ao reindexar.
export class SemanticCache {
  constructor(embedder, { threshold, ttlMs }) {
    Object.assign(this, { embedder, threshold, ttlMs, entries: [] });
  }
  async get(question, scope = '') {
    const [v] = await this.embedder.embed([question]);
    const now = Date.now();
    const hit = this.entries.find((e) => e.scope === scope && now - e.at < this.ttlMs && cosine(v, e.vector) >= this.threshold);
    return hit?.value ?? null;
  }
  async set(question, value, scope = '') {
    const [vector] = await this.embedder.embed([question]);
    this.entries.push({ vector, value, scope, at: Date.now() });
  }
}
