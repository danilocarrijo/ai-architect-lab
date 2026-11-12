import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

export const config = {
  dataDir: path.join(ROOT, 'data'),
  indexFile: path.join(ROOT, '.cache', 'index.json'),
  chunk: { maxChars: 600, overlapChars: 100 },
  retrieval: { topKCandidates: 12, topK: 4, rrfK: 60, minScore: 0.05 },
  llm: { model: process.env.LLM_MODEL || 'claude-sonnet-5-5', maxTokens: 800 },
  // maxTokens maior: modelos Gemini com "thinking" gastam parte do limite pensando antes de responder
  gemini: { model: process.env.GEMINI_MODEL || 'gemini-3.8-flash', maxTokens: 2048 },
  cache: { threshold: 0.92, ttlMs: 10 * 60 * 1000 },
  // preço ilustrativo (USD por 1M tokens) só para demonstrar FinOps
  pricing: { inPerM: 3, outPerM: 15 },
};
