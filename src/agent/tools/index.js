import { z } from 'zod';
import { createSearchPoliciesTool } from './search-policies.js';
import { createCreateTicketTool } from './create-ticket.js';
import { createLookupCepTool } from './lookup-cep.js';

// Registro de ferramentas. Para adicionar uma: crie o arquivo e acrescente a fábrica aqui
// (nem o agente nem o servidor MCP precisam mudar — aberto para extensão).
const factories = [createSearchPoliciesTool, createCreateTicketTool, createLookupCepTool];

export const createTools = (deps) => factories.map((make) => make(deps));

export function pickTools(tools, names) {
  return names.map((n) => {
    const tool = tools.find((t) => t.name === n);
    if (!tool) throw new Error(`Ferramenta desconhecida: ${n}`);
    return tool;
  });
}

export const toAnthropicTools = (tools) =>
  tools.map((t) => ({ name: t.name, description: t.description, input_schema: z.toJSONSchema(z.object(t.schema)) }));
