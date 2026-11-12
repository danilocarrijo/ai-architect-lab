// Utilidades de texto compartilhadas por BM25 e embeddings.
const STOP = new Set(
  'a o as os de do da dos das e em no na nos nas um uma para por com que se ao ou é são ser foi como mais mas sua seu quais qual quando quanto posso pode preciso tem há já até'.split(' '),
);

export const normalize = (s) => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');

// Stemming ingênuo: truncar em 5 letras aproxima plural/singular e flexões em PT.
export function tokenize(text) {
  return normalize(text)
    .split(/[^a-z0-9]+/)
    .filter((t) => t && !STOP.has(t))
    .map((t) => (t.length > 5 ? t.slice(0, 5) : t));
}
