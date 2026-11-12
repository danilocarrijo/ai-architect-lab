import { test } from 'node:test';
import assert from 'node:assert/strict';
import { cleanSchema, toGeminiRequest, fromGeminiResponse, completeGemini } from '../src/llm/gemini.js';

test('cleanSchema remove campos que o Gemini rejeita, em qualquer nível', () => {
  const out = cleanSchema({ $schema: 'x', type: 'object', additionalProperties: false, properties: { a: { type: 'string', additionalProperties: false } } });
  assert.deepEqual(out, { type: 'object', properties: { a: { type: 'string' } } });
});

test('toGeminiRequest converte histórico com ferramenta para o formato do Gemini', () => {
  const messages = [
    { role: 'user', content: 'A VPN caiu' },
    { role: 'assistant', content: [{ type: 'tool_use', id: 'c1', name: 'search_policies', input: { query: 'vpn' } }] },
    { role: 'user', content: [{ type: 'tool_result', tool_use_id: 'c1', content: 'P3 para falhas pontuais' }] },
  ];
  const tools = [{ name: 'search_policies', description: 'busca', input_schema: { $schema: 'x', type: 'object', properties: {} } }];
  const req = toGeminiRequest({ system: 'sys', messages, tools });
  assert.equal(req.systemInstruction.parts[0].text, 'sys');
  assert.deepEqual(req.contents.map((c) => c.role), ['user', 'model', 'user']);
  assert.deepEqual(req.contents[1].parts[0], { functionCall: { name: 'search_policies', args: { query: 'vpn' } } });
  assert.deepEqual(req.contents[2].parts[0].functionResponse, { name: 'search_policies', response: { result: 'P3 para falhas pontuais' } });
  assert.equal(req.tools[0].functionDeclarations[0].parameters.$schema, undefined);
});

test('fromGeminiResponse mapeia functionCall para tool_use e texto para end_turn', () => {
  const tool = fromGeminiResponse({ candidates: [{ content: { parts: [{ functionCall: { name: 'create_ticket', args: { title: 't' } } }] } }], usageMetadata: { promptTokenCount: 10, candidatesTokenCount: 5 } });
  assert.equal(tool.stop_reason, 'tool_use');
  assert.equal(tool.content[0].name, 'create_ticket');
  assert.deepEqual(tool.usage, { input_tokens: 10, output_tokens: 5 });
  const text = fromGeminiResponse({ candidates: [{ content: { parts: [{ text: 'oi' }] } }] });
  assert.equal(text.stop_reason, 'end_turn');
  assert.equal(text.content[0].text, 'oi');
  const empty = fromGeminiResponse({ promptFeedback: { blockReason: 'SAFETY' } });
  assert.match(empty.content[0].text, /SAFETY/);
});

test('completeGemini tenta de novo em 429 e falha com mensagem clara em erro', async () => {
  const ok = { ok: true, json: async () => ({ candidates: [{ content: { parts: [{ text: 'feito' }] } }] }) };
  const seq = [{ ok: false, status: 429, text: async () => 'limite' }, ok];
  const r = await completeGemini({ system: 's', messages: [{ role: 'user', content: 'q' }] }, { apiKey: 'k', retryMs: 0, fetchImpl: async () => seq.shift() });
  assert.equal(r.content[0].text, 'feito');
  await assert.rejects(
    completeGemini({ system: 's', messages: [{ role: 'user', content: 'q' }] }, { apiKey: 'k', fetchImpl: async () => ({ ok: false, status: 400, text: async () => 'ruim' }) }),
    /Gemini 400: ruim/,
  );
});
