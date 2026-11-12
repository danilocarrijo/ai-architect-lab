import readline from 'node:readline/promises';
import { buildIndex, loadRetriever } from './rag/index.js';
import { createAssistant } from './llm/ask.js';
import { runAgent } from './agent/runner.js';
import { agents, getAgent } from './agent/agents/index.js';
import { hasLLM } from './llm/client.js';

const [cmd, ...rest] = process.argv.slice(2);

function print(r) {
  console.log(`\n${r.answer}\n`);
  r.sources?.forEach((s) => console.log(`  [${s.n}] ${s.source} > ${s.section} (${s.score})`));
  if (r.cached) console.log('  (cache semântico)');
  if (r.grounded === false) console.log('  ! resposta sem citação válida');
  if (r.tracer) console.log(r.tracer.report());
}

if (cmd === 'ingest') {
  await buildIndex({ log: console.log });
} else if (cmd === 'agents') {
  agents.forEach((a) => console.log(`${a.name.padEnd(10)} ${a.description}  [tools: ${a.tools.join(', ')}]`));
} else if (cmd === 'agent') {
  // uso: agent [--name triage] [--engine langgraph] pergunta...
  const opt = (flag, fallback) => {
    const i = rest.indexOf(flag);
    return i >= 0 ? rest.splice(i, 2)[1] : fallback;
  };
  const name = opt('--name', 'helpdesk');
  const engine = opt('--engine', 'native');
  if (!hasLLM()) throw new Error('O agente precisa de GEMINI_API_KEY (ou ANTHROPIC_API_KEY).');
  if (!['native', 'langgraph'].includes(engine)) throw new Error(`Engine desconhecida: ${engine}. Use native ou langgraph.`);
  const { retriever } = await loadRetriever();
  const run = engine === 'langgraph' ? (await import('./agent/langgraph/runner.js')).runAgentLangGraph : runAgent;
  const r = await run(getAgent(name), rest.join(' '), { retriever });
  console.log(`\n${r.answer}\n(passos: ${r.steps})`);
  if (r.tracer) console.log(r.tracer.report());
  if (r.audit?.length) console.log(`[hooks: auditoria]\n${r.audit.map((a) => `  • ${a.tool} → ${a.status}`).join('\n')}`);
} else {
  const { ask } = await createAssistant();
  if (!hasLLM()) console.log('Modo offline (sem GEMINI_API_KEY nem ANTHROPIC_API_KEY): resposta extrativa.');
  const q = [cmd, ...rest].filter(Boolean).join(' ');
  if (q) print(await ask(q));
  else {
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    for (;;) {
      const line = await rl.question('pergunta> ');
      if (!line || line === 'sair') break;
      print(await ask(line));
    }
    rl.close();
  }
}
