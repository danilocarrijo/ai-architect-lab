import { tokenize, normalize } from './text.js';

const DIM = 512;
const hash = (s) => {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) h = Math.imul(h ^ s.charCodeAt(i), 16777619);
  return h >>> 0;
};

function unit(v) {
  let n = 0;
  for (const x of v) n += x * x;
  n = Math.sqrt(n) || 1;
  return v.map((x) => x / n);
}

// Embedder local (hashing trick: tokens + trigramas de caracteres). Determinístico, offline,
// sem dependências. NÃO é semântico como um modelo neural, mas mantém a mesma INTERFACE.
export class LocalHashEmbedder {
  name = 'local-hash-512';
  async embed(texts) {
    return texts.map((t) => {
      const v = new Float32Array(DIM);
      for (const tok of tokenize(t)) v[hash(tok) % DIM] += 1;
      const n = normalize(t).replace(/[^a-z0-9]/g, '');
      for (let i = 0; i < n.length - 2; i++) v[hash(n.slice(i, i + 3)) % DIM] += 0.15;
      return unit(v);
    });
  }
}

// Embedder remoto (ex.: Voyage AI, recomendado pela Anthropic). Ative com VOYAGE_API_KEY.
export class VoyageEmbedder {
  name = 'voyage-3';
  constructor(key) {
    this.key = key;
  }
  async embed(texts) {
    const res = await fetch('https://api.voyageai.com/v1/embeddings', {
      method: 'POST',
      headers: { 'content-type': 'application/json', authorization: `Bearer ${this.key}` },
      body: JSON.stringify({ model: 'voyage-3', input: texts }),
    });
    if (!res.ok) throw new Error(`Voyage ${res.status}`);
    const { data } = await res.json();
    return data.map((d) => unit(Float32Array.from(d.embedding)));
  }
}

export const createEmbedder = () =>
  process.env.VOYAGE_API_KEY ? new VoyageEmbedder(process.env.VOYAGE_API_KEY) : new LocalHashEmbedder();

export const cosine = (a, b) => {
  let s = 0;
  for (let i = 0; i < a.length; i++) s += a[i] * b[i];
  return s;
};
