import { z } from 'zod';

// Contrato de uma ferramenta: { name, description, schema (shape Zod), run(args) }.
// Cada ferramenta recebe suas dependências por fábrica (inversão de dependência).
export const createSearchPoliciesTool = ({ retriever }) => ({
  name: 'search_policies',
  description: 'Busca trechos nas políticas internas (férias, home-office, reembolso, TI). Use sempre antes de responder.',
  schema: { query: z.string().describe('Texto da busca'), dept: z.enum(['rh', 'ti', 'financeiro']).optional() },
  async run({ query, dept }) {
    const hits = await retriever.retrieve(query, { filter: dept ? { dept } : undefined });
    return hits.length
      ? hits.map((h) => `(${h.source} > ${h.section}) ${h.text.split('\n').slice(1).join(' ')}`).join('\n---\n')
      : 'Nenhum resultado.';
  },
});
