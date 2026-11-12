import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { loadRetriever } from '../rag/index.js';
import { createTools } from '../agent/tools/index.js';

// Servidor MCP (stdio): expõe as mesmas ferramentas do agente a qualquer cliente MCP (Claude Desktop, Claude Code...).
// Não escreva em stdout além do protocolo: use stderr para logs.
const { retriever } = await loadRetriever();
const server = new McpServer({ name: 'helpdesk', version: '1.0.0' });

for (const t of createTools({ retriever })) {
  server.registerTool(t.name, { description: t.description, inputSchema: t.schema }, async (args) => ({
    content: [{ type: 'text', text: await t.run(args) }],
  }));
}

await server.connect(new StdioServerTransport());
console.error('MCP helpdesk pronto (stdio)');
