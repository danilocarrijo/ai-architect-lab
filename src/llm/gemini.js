import { randomUUID } from 'node:crypto';
import { config } from '../config.js';

// Adaptador Gemini: recebe/devolve o MESMO formato do SDK da Anthropic (blocos text/tool_use/tool_result,
// stop_reason, usage), então runner.js e ask.js não precisam saber qual provedor está por trás.
const BASE = 'https://generativelanguage.googleapis.com/v1beta/models';
const DROP = new Set(['$schema', 'additionalProperties']); // o Gemini só aceita um subconjunto do JSON Schema

export function cleanSchema(s) {
  if (Array.isArray(s)) return s.map(cleanSchema);
  if (s && typeof s === 'object') {
    return Object.fromEntries(Object.entries(s).filter(([k]) => !DROP.has(k)).map(([k, v]) => [k, cleanSchema(v)]));
  }
  return s;
}

export function toGeminiRequest({ system, messages, tools }) {
  const names = new Map(); // tool_use_id -> nome (o Gemini exige o nome na resposta da ferramenta)
  for (const m of messages) {
    if (Array.isArray(m.content)) for (const b of m.content) if (b.type === 'tool_use') names.set(b.id, b.name);
  }
  const contents = messages.map((m) => {
    const role = m.role === 'assistant' ? 'model' : 'user';
    if (typeof m.content === 'string') return { role, parts: [{ text: m.content }] };
    const parts = m.content
      .map((b) => {
        if (b.type === 'text') return b.text ? { text: b.text } : null;
        if (b.type === 'tool_use') return b._part ?? { functionCall: { name: b.name, args: b.input } };
        if (b.type === 'tool_result') {
          return { functionResponse: { name: names.get(b.tool_use_id) ?? 'unknown', response: { result: b.content } } };
        }
        return null;
      })
      .filter(Boolean);
    return { role, parts };
  });
  return {
    systemInstruction: { parts: [{ text: system }] },
    contents,
    generationConfig: { maxOutputTokens: config.gemini.maxTokens },
    ...(tools?.length
      ? { tools: [{ functionDeclarations: tools.map((t) => ({ name: t.name, description: t.description, parameters: cleanSchema(t.input_schema) })) }] }
      : {}),
  };
}

export function fromGeminiResponse(data) {
  const cand = data.candidates?.[0];
  const content = [];
  for (const p of cand?.content?.parts ?? []) {
    if (p.functionCall) {
      // _part guarda o trecho original (o Gemini pode exigir de volta campos como thoughtSignature)
      content.push({ type: 'tool_use', id: `call_${randomUUID()}`, name: p.functionCall.name, input: p.functionCall.args ?? {}, _part: p });
    } else if (p.text && !p.thought) content.push({ type: 'text', text: p.text });
  }
  if (!content.length) {
    const why = cand?.finishReason ?? data.promptFeedback?.blockReason ?? 'sem motivo informado';
    content.push({ type: 'text', text: `O Gemini devolveu uma resposta vazia (${why}).` });
  }
  const u = data.usageMetadata ?? {};
  return {
    stop_reason: content.some((b) => b.type === 'tool_use') ? 'tool_use' : 'end_turn',
    content,
    usage: { input_tokens: u.promptTokenCount ?? 0, output_tokens: u.candidatesTokenCount ?? 0 },
  };
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

export async function completeGemini(req, { apiKey, fetchImpl = fetch, retryMs = 2000, timeoutMs = Number(process.env.GEMINI_TIMEOUT_MS) || 180_000 } = {}) {
  const url = `${BASE}/${config.gemini.model}:generateContent`;
  const body = JSON.stringify(toGeminiRequest(req));
  for (let attempt = 1; ; attempt++) {
    console.error(`[gemini] ${config.gemini.model}, tentativa ${attempt}...`);
    let res;
    try {
      res = await fetchImpl(url, {
        method: 'POST',
        headers: { 'content-type': 'application/json', 'x-goog-api-key': apiKey },
        body,
        signal: AbortSignal.timeout(timeoutMs), // sem isso, uma conexão pendurada trava a CLI para sempre
      });
    } catch (e) {
      if (e.name === 'TimeoutError') throw new Error(`Gemini não respondeu em ${timeoutMs / 1000}s (rede, firewall ou modelo lento).`);
      throw new Error(`Falha de rede ao chamar o Gemini: ${e.cause?.code ?? e.message}`);
    }
    if (res.ok) return fromGeminiResponse(await res.json());
    // plano gratuito: 429 (limite) e 503 (sobrecarga) costumam passar com uma nova tentativa
    if ((res.status === 429 || res.status === 503) && attempt < 3) {
      console.error(`[gemini] HTTP ${res.status}, aguardando ${(retryMs * attempt) / 1000}s para tentar de novo`);
      await sleep(retryMs * attempt);
      continue;
    }
    throw new Error(`Gemini ${res.status}: ${(await res.text()).slice(0, 300)}`);
  }
}
