import { tokenize } from './text.js';

// BM25 implementado do zero: busca lexical (bom para siglas, códigos, nomes exatos).
export class BM25 {
  constructor(docs, k1 = 1.4, b = 0.75) {
    this.k1 = k1;
    this.b = b;
    this.docs = docs.map((d) => ({ id: d.id, tokens: tokenize(d.text) }));
    this.avgLen = this.docs.reduce((s, d) => s + d.tokens.length, 0) / (this.docs.length || 1);
    this.df = new Map();
    for (const d of this.docs) for (const t of new Set(d.tokens)) this.df.set(t, (this.df.get(t) ?? 0) + 1);
  }
  search(query, k = 10, allow) {
    const q = tokenize(query);
    const N = this.docs.length;
    return this.docs
      .filter((d) => !allow || allow.has(d.id))
      .map((d) => {
        let score = 0;
        for (const t of q) {
          const f = d.tokens.filter((x) => x === t).length;
          if (!f) continue;
          const df = this.df.get(t) ?? 0;
          const idf = Math.log(1 + (N - df + 0.5) / (df + 0.5));
          score += (idf * f * (this.k1 + 1)) / (f + this.k1 * (1 - this.b + (this.b * d.tokens.length) / this.avgLen));
        }
        return { id: d.id, score };
      })
      .filter((r) => r.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, k);
  }
}
