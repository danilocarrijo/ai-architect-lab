// Chunking estruturado: respeita seções (##) e só então divide por tamanho, com overlap.
// Cada chunk recebe um cabeçalho de contexto ("Título > Seção") — "contextual chunking".

function splitLong(text, max, overlap) {
  if (text.length <= max) return [text];
  const sentences = text.match(/[^.!?]+[.!?]+\s*|[^.!?]+$/g) ?? [text];
  const out = [];
  let cur = '';
  for (const s of sentences) {
    if ((cur + s).length > max && cur) {
      out.push(cur.trim());
      cur = cur.slice(-overlap) + s; // overlap preserva contexto na fronteira
    } else cur += s;
  }
  if (cur.trim()) out.push(cur.trim());
  return out;
}

export function chunkDocument(doc, { maxChars, overlapChars }) {
  const title = doc.meta.title ?? doc.id;
  const sections = doc.body.split(/\n(?=## )/).map((s) => s.trim()).filter(Boolean);
  const chunks = [];
  for (const sec of sections) {
    const [head, ...rest] = sec.split('\n');
    const isH2 = head.startsWith('## ');
    const sectionName = isH2 ? head.slice(3) : 'Introdução';
    const body = (isH2 ? rest.join('\n') : sec.replace(/^# .*\n?/, '')).trim();
    if (!body) continue;
    for (const piece of splitLong(body, maxChars, overlapChars)) {
      chunks.push({
        id: `${doc.id}#${chunks.length}`,
        docId: doc.id,
        source: doc.source,
        section: sectionName,
        text: `${title} > ${sectionName}\n${piece}`,
        meta: { dept: doc.meta.dept, updated: doc.meta.updated, title },
      });
    }
  }
  return chunks;
}
