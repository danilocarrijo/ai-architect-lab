import { test } from 'node:test';
import assert from 'node:assert/strict';
import { config } from '../src/config.js';
import { loadDocuments } from '../src/rag/loader.js';
import { chunkDocument } from '../src/rag/chunker.js';
import { LocalHashEmbedder } from '../src/rag/embeddings.js';
import { VectorStore } from '../src/rag/vectorstore.js';
import { BM25 } from '../src/rag/bm25.js';
import { HybridRetriever, rrf } from '../src/rag/retriever.js';

test('rrf favorece itens bem ranqueados nas duas listas', () => {
  const r = rrf([[{ id: 'a' }, { id: 'b' }], [{ id: 'b' }, { id: 'c' }]]);
  assert.equal(r[0].id, 'b');
});

test('retriever híbrido acha o documento certo e respeita filtro', async () => {
  const embedder = new LocalHashEmbedder();
  const docs = await loadDocuments(config.dataDir);
  const chunks = docs.flatMap((d) => chunkDocument(d, config.chunk));
  const store = new VectorStore();
  store.add(chunks, await embedder.embed(chunks.map((c) => c.text)));
  const retriever = new HybridRetriever({ store, bm25: new BM25(store.items), embedder, cfg: config.retrieval });

  const res = await retriever.retrieve('Como resetar minha senha?');
  assert.equal(res[0].docId, 'ti-suporte');

  const filtered = await retriever.retrieve('prazo', { filter: { dept: 'rh' } });
  assert.ok(filtered.every((r) => r.meta.dept === 'rh'));
});
