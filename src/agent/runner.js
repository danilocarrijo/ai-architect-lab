import { complete } from '../llm/client.js';
import { Tracer } from '../observability/trace.js';
import { checkInput } from '../guardrails/index.js';
import { createTools, pickTools, toAnthropicTools } from './tools/index.js';

// Executor genérico: roda QUALQUER definição de agente. O `llm` é injetável (facilita testes).
export async function runAgent(agent, question, { retriever, llm = complete, tools: allTools } = {}) {
  const input = checkInput(question);
  if (!input.ok) return { answer: input.reason, steps: 0 };

  const tracer = new Tracer(`agent:${agent.name}`);
  const tools = pickTools(allTools ?? createTools({ retriever }), agent.tools); // menor privilégio: só as ferramentas do agente
  const defs = toAnthropicTools(tools);
  const messages = [{ role: 'user', content: input.clean }];

  for (let step = 1; step <= agent.maxSteps; step++) {
    const res = await tracer.span(`llm#${step}`, () => llm({ system: agent.system, messages, tools: defs }));
    tracer.addUsage(res.usage);
    messages.push({ role: 'assistant', content: res.content });
    if (res.stop_reason !== 'tool_use') {
      return { answer: res.content.filter((b) => b.type === 'text').map((b) => b.text).join(''), steps: step, tracer };
    }
    const results = [];
    for (const b of res.content.filter((c) => c.type === 'tool_use')) {
      const tool = tools.find((t) => t.name === b.name);
      let content;
      try {
        if (!tool) throw new Error(`ferramenta não permitida: ${b.name}`);
        content = await tracer.span(`tool:${b.name}`, () => tool.run(b.input));
      } catch (e) {
        content = `Erro: ${e.message}`;
      }
      results.push({ type: 'tool_result', tool_use_id: b.id, content: String(content) });
    }
    messages.push({ role: 'user', content: results });
  }
  return { answer: 'Limite de passos atingido sem resposta final.', steps: agent.maxSteps, tracer };
}
