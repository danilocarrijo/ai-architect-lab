import { z } from 'zod';

// Chamado simulado: guardado no array injetado (em produção, a API do sistema de chamados).
export const createCreateTicketTool = ({ tickets = [] } = {}) => ({
  name: 'create_ticket',
  description: 'Abre um chamado no helpdesk (simulado). Use só quando o usuário pedir ou a política exigir.',
  schema: {
    title: z.string(),
    description: z.string(),
    priority: z.enum(['baixa', 'media', 'alta']).optional().describe('Padrão: media'),
  },
  async run({ title, description, priority = 'media' }) {
    const id = `TCK-${1000 + tickets.length + 1}`;
    tickets.push({ id, title, description, priority });
    return `Chamado ${id} criado (prioridade ${priority}): ${title}`;
  },
});
