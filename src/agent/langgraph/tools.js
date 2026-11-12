import { z } from 'zod';
import { tool } from '@langchain/core/tools';

// Adapta o contrato próprio { name, description, schema, run } para `tool()` do LangChain.
// A lógica das ferramentas continua em src/agent/tools (reaproveitada por runner, MCP e LangGraph).
export const toLangChainTools = (tools) =>
  tools.map((t) =>
    tool(
      async (args) => {
        try {
          return String(await t.run(args));
        } catch (e) {
          return `Erro: ${e.message}`; // mesmo comportamento do runner: o erro vira resultado, o loop segue
        }
      },
      { name: t.name, description: t.description, schema: z.object(t.schema) },
    ),
  );
