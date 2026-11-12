import { test } from 'node:test';
import assert from 'node:assert/strict';
import { fakeModel } from '@langchain/core/testing';
import { AIMessage } from '@langchain/core/messages';
import { createLookupCepTool } from '../src/agent/tools/lookup-cep.js';
import { createTools } from '../src/agent/tools/index.js';
import { getAgent } from '../src/agent/agents/index.js';
import { runAgent } from '../src/agent/runner.js';
import { runAgentLangGraph } from '../src/agent/langgraph/runner.js';

// fetch falso: devolve o que o teste mandar e guarda as URLs chamadas (nenhuma chamada vai à internet).
const fakeFetch = (reply) => {
  const calls = [];
  const fn = async (url) => {
    calls.push(url);
    if (reply instanceof Error) throw reply;
    return reply;
  };
  fn.calls = calls;
  return fn;
};
const json = (body, status = 200) => ({ ok: status < 400, status, json: async () => body });
const paulista = { logradouro: 'Avenida Paulista', bairro: 'Bela Vista', localidade: 'São Paulo', uf: 'SP' };

test('lookup_cep: formata o endereço e chama a URL só com os dígitos', async () => {
  const f = fakeFetch(json(paulista));
  const tool = createLookupCepTool({ fetchImpl: f });
  assert.equal(await tool.run({ cep: '01310-100' }), 'Avenida Paulista, Bela Vista, São Paulo/SP');
  assert.equal(f.calls[0], 'https://viacep.com.br/ws/01310100/json/');
});

test('lookup_cep: CEP inválido nem chama a API; falhas viram texto, não exceção', async () => {
  const f = fakeFetch(json(paulista));
  assert.match(await createLookupCepTool({ fetchImpl: f }).run({ cep: '123' }), /inválido/);
  assert.equal(f.calls.length, 0);

  assert.match(await createLookupCepTool({ fetchImpl: fakeFetch(json({ erro: 'true' })) }).run({ cep: '99999999' }), /não encontrado/);
  assert.match(await createLookupCepTool({ fetchImpl: fakeFetch(json({}, 500)) }).run({ cep: '01310100' }), /erro 500/);
  assert.match(await createLookupCepTool({ fetchImpl: fakeFetch(new Error('rede')) }).run({ cep: '01310100' }), /Não foi possível/);
});

test('agente cep: só enxerga lookup_cep e o loop usa a ferramenta (motor próprio)', async () => {
  const agent = getAgent('cep');
  assert.deepEqual(agent.tools, ['lookup_cep']);
  const f = fakeFetch(json(paulista));
  const turns = [
    { stop_reason: 'tool_use', content: [{ type: 'tool_use', id: 't1', name: 'lookup_cep', input: { cep: '01310-100' } }] },
    { stop_reason: 'end_turn', content: [{ type: 'text', text: 'Fica na Avenida Paulista.' }] },
  ];
  let i = 0;
  const r = await runAgent(agent, 'Qual o endereço do CEP 01310-100?', { llm: async () => turns[i++], tools: createTools({ fetchImpl: f }) });
  assert.equal(r.answer, 'Fica na Avenida Paulista.');
  assert.equal(r.steps, 2);
  assert.equal(f.calls.length, 1);
});

test('agente cep: a mesma ferramenta funciona na engine LangGraph', async () => {
  const f = fakeFetch(json(paulista));
  const model = fakeModel()
    .respondWithTools([{ name: 'lookup_cep', args: { cep: '01310-100' } }])
    .respond(new AIMessage('Fica na Avenida Paulista.'));
  const r = await runAgentLangGraph(getAgent('cep'), 'Qual o endereço do CEP 01310-100?', { model, tools: createTools({ fetchImpl: f }) });
  assert.equal(r.answer, 'Fica na Avenida Paulista.');
  assert.equal(f.calls.length, 1);
});
