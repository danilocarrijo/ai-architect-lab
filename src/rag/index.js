import fs from 'node:fs/promises';
import { config } from '../config.js';
import { loadDocuments } from './loader.js';
import { chunkDocument } from './chunker.js';
import { createEmbedder } from './embeddings.js';
import { VectorStore } from './vectorstore.js';
import { BM25 } from './bm25.js';
import { HybridRetriever } from './retriever.js';

// Pipeline de INGESTÃO: carregar -> chunk -> embed -> indexar (vetorial + lexical) -> persistir.
export async function buildIndex({ log = () => {} } = {}) {
  const embedder = createEmbedder();
  const docs = await loadDocuments(config.dataDir);
  const chunks = docs.flatMap((d) => chunkDocument(d, config.chunk));
  const vectors = await embedder.embed(chunks.map((c) => c.text));
  const store = new VectorStore();
  store.add(chunks, vectors);
  await store.save(config.indexFile, embedder.name);
  log(`${docs.length} documentos -> ${chunks.length} chunks (embedder: ${embedder.name})`);
  return { store, embedder };
}

// Carrega o índice persistido (ou reconstrói se faltar/estiver incompatível) e monta o retriever.
export async function loadRetriever() {
  const embedder = createEmbedder();
  let store;
  try {
    store = await VectorStore.load(config.indexFile, embedder.name);
  } catch {
    await fs.rm(config.indexFile, { force: true });
    ({ store } = await buildIndex());
  }
  const bm25 = new BM25(store.items);
  return { retriever: new HybridRetriever({ store, bm25, embedder, cfg: config.retrieval }), store, embedder };
}
