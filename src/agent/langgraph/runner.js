import { createAgent } from 'langchain';
import { GraphRecursionError } from '@langchain/langgraph';
import { BaseCallbackHandler } from '@langchain/core/callbacks/base';
import { Tracer } from '../../observability/trace.js';
import { checkInput } from '../../guardrails/index.js';
import { createTools, pickTools } from '../tools/index.js';
import { toLangChainTools } from './tools.js';
import { createChatModel } from './model.js';
import { createDefaultHooks } from './hooks.js';

// Ponte LangChain -> Tracer próprio: cada chamada de modelo/ferramenta vira um span.
class TracerHandler extends BaseCallbackHandler {
  name = 'tracer-handler';
  #starts = new Map();
  #llmCalls = 0;
  constructor(tracer) {
    super();
    this.tracer = tracer;
  }
  #start(runId, label) {
    this.#starts.set(runId, { label, t0: performance.now() });
  }
  #end(runId) {
    const s = this.#starts.get(runId);
    if (!s) return;
    this.#starts.delete(runId);
    this.tracer.spans.push({ name: s.label, ms: Math.round(performance.now() - s.t0) });
  }
  handleChatModelStart(_llm, _msgs, runId) {
    this.#start(runId, `llm#${++this.#llmCalls}`);
  }
  handleLLMEnd(output, runId) {
    this.#end(runId);
    const u = output.generations?.[0]?.[0]?.message?.usage_metadata;
    if (u) this.tracer.addUsage({ input_tokens: u.input_tokens, output_tokens: u.output_tokens });
  }
  handleLLMError(_err, runId) {
    this.#end(runId);
  }
  handleToolStart(tool, _input, runId, _parent, _tags, _meta, name) {
    this.#start(runId, `tool:${name ?? tool?.name ?? '?'}`);
  }
  handleToolEnd(_out, runId) {
    this.#end(runId);
  }
  handleToolError(_err, runId) {
    this.#end(runId);
  }
}

const textOf = (content) =>
  typeof content === 'string' ? content : content.filter((b) => b.type === 'text').map((b) => b.text).join('');

// Equivalente LangGraph do src/agent/runner.js: mesmos agentes, mesmas ferramentas, mesmos guardrails.
// `model` é injetável (testes passam um fakeModel; em produção sai de createChatModel()).
// `hooks` é a lista de middleware do LangChain (hooks.js); sem ela valem os padrões. Passe [] para rodar sem hooks.
export async function runAgentLangGraph(agent, question, { retriever, model, tools: allTools, hooks } = {}) {
  const input = checkInput(question);
  if (!input.ok) return { answer: input.reason, steps: 0 };

  const tracer = new Tracer(`langgraph:${agent.name}`);
  const audit = []; // registro de auditoria das chamadas de ferramenta, preenchido pelos hooks padrão
  const tools = pickTools(allTools ?? createTools({ retriever }), agent.tools); // menor privilégio, como no runner
  const graph = createAgent({
    model: model ?? createChatModel(),
    tools: toLangChainTools(tools),
    systemPrompt: agent.system,
    middleware: hooks ?? createDefaultHooks({ audit }),
  });

  const run = (limit) =>
    graph.invoke(
      { messages: [{ role: 'user', content: input.clean }] },
      { recursionLimit: limit, callbacks: [new TracerHandler(tracer)] },
    );

  try {
    // cada "passo" do runner próprio = 1 chamada de modelo (+ ferramentas) => ~2 super-passos no grafo
    const { messages } = await run(agent.maxSteps * 2 + 1);
    const steps = messages.filter((m) => m.type === 'ai').length;
    return { answer: textOf(messages.at(-1).content), steps, tracer, audit };
  } catch (e) {
    if (e instanceof GraphRecursionError || e?.name === 'GraphRecursionError') {
      return { answer: 'Limite de passos atingido sem resposta final.', steps: agent.maxSteps, tracer, audit };
    }
    throw e;
  }
}
