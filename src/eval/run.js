import { loadRetriever } from '../rag/index.js';
import { GOLDEN } from './golden.js';

// Avaliação offline da recuperação: hit@k e MRR contra um conjunto dourado.
const { retriever } = await loadRetriever();
let hits = 0;
let rr = 0;
for (const { q, doc } of GOLDEN) {
  const res = await retriever.retrieve(q);
  const rank = res.findIndex((r) => r.docId === doc) + 1;
  if (rank) {
    hits++;
    rr += 1 / rank;
  }
  console.log(`${rank ? 'OK ' : 'ERR'} rank=${rank || '-'}  ${q}`);
}
console.log(`\nhit@${retriever.cfg.topK}: ${((hits / GOLDEN.length) * 100).toFixed(0)}%  MRR: ${(rr / GOLDEN.length).toFixed(2)}`);
process.exit(hits / GOLDEN.length >= 0.8 ? 0 : 1);
