import { createMiddleware, ToolMessage } from 'langchain';
import { sanitizeContext } from '../../guardrails/index.js';

// HOOKS do agente LangGraph, escritos como "middleware" do LangChain.
// Um hook é uma função que o framework chama num ponto fixo do fluxo. Aqui usamos `wrapToolCall`, que
// envolve CADA execução de ferramenta: o hook decide se chama `handler(request)` (executa a ferramenta),
// pode mexer no pedido antes e no resultado depois, ou nem chamar (bloqueio).
// Quem ensina o runner a usá-los é o `middleware: [...]` do createAgent (veja runner.js).

// Recusa uma chamada sem executar a ferramenta. O LLM lê esta mensagem como se fosse o resultado
// (status 'error' avisa o framework de que a ferramenta não rodou).
const refuse = (request, text) =>
  new ToolMessage({ content: text, tool_call_id: request.toolCall.id, name: request.toolCall.name, status: 'error' });

// 1) VALIDAÇÃO ANTES da ferramenta: no máximo `max` chamados por pedido.
// O prompt do agente de triagem já diz "nunca abra mais de um chamado", mas um prompt é só um pedido educado
// ao modelo. Este hook transforma a regra em CÓDIGO: mesmo que o LLM insista, o segundo chamado não é aberto.
// Cria um estado novo por execução (o contador vive na closure), então cada pedido começa do zero.
export const limitTicketsPerRun = (max = 1) => {
  let opened = 0;
  return createMiddleware({
    name: 'limitTicketsPerRun',
    wrapToolCall: async (request, handler) => {
      if (request.toolCall.name !== 'create_ticket') return handler(request);
      // Conta ANTES de executar: o LLM pode pedir duas ferramentas no mesmo turno, e elas rodam em paralelo.
      if (opened >= max) return refuse(request, `Bloqueado: já foi aberto ${max} chamado(s) neste pedido. Não abra outro.`);
      opened++;
      return handler(request);
    },
  });
};

// 2) SANITIZAÇÃO DEPOIS da ferramenta: o texto que a ferramenta devolveu também é "não confiável"
// (um documento ou uma API podem trazer uma ordem escondida). Reaproveita o guardrail do Capítulo 8.
export const sanitizeToolResults = () =>
  createMiddleware({
    name: 'sanitizeToolResults',
    wrapToolCall: async (request, handler) => {
      const result = await handler(request); // executa a ferramenta (ou a próxima camada de hooks)
      if (typeof result?.content !== 'string') return result; // Command ou conteúdo não textual: deixa passar
      const clean = sanitizeContext(result.content);
      if (clean === result.content) return result;
      return new ToolMessage({ content: clean, tool_call_id: result.tool_call_id, name: result.name, status: result.status });
    },
  });

// 3) AUDITORIA: registra toda chamada de ferramenta (quem, com quais argumentos, resultado, duração).
// Não altera nada; só observa. Fica na camada mais externa para ver também as chamadas bloqueadas.
export const auditToolCalls = (log) =>
  createMiddleware({
    name: 'auditToolCalls',
    wrapToolCall: async (request, handler) => {
      const t0 = performance.now();
      const result = await handler(request);
      log.push({
        tool: request.toolCall.name,
        args: request.toolCall.args,
        status: result?.status === 'error' ? 'erro' : 'ok', // 'erro' inclui as recusas dos outros hooks
        ms: Math.round(performance.now() - t0),
      });
      return result;
    },
  });

// A ordem importa: o primeiro da lista é o mais externo. A auditoria vem primeiro para enxergar o resultado final.
export const createDefaultHooks = ({ audit = [] } = {}) => [auditToolCalls(audit), limitTicketsPerRun(1), sanitizeToolResults()];
