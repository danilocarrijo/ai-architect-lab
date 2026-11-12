import Anthropic from '@anthropic-ai/sdk';
import { config } from '../config.js';
import { completeGemini } from './gemini.js';

// Escolha do provedor pela variável de ambiente (Gemini tem prioridade).
// Sem nenhuma chave o projeto roda em modo offline (resposta extrativa, sem LLM).
const geminiKey = () => process.env.GEMINI_API_KEY || process.env.GOOGLE_API_KEY;
export const llmProvider = () => (geminiKey() ? 'gemini' : process.env.ANTHROPIC_API_KEY ? 'anthropic' : null);
export const hasLLM = () => llmProvider() !== null;

let client;
export function complete({ system, messages, tools }) {
  if (llmProvider() === 'gemini') return completeGemini({ system, messages, tools }, { apiKey: geminiKey() });
  client ??= new Anthropic();
  return client.messages.create({
    model: config.llm.model,
    max_tokens: config.llm.maxTokens,
    // cache_control no system prompt: reaproveita o prefixo estável entre chamadas (FinOps)
    system: [{ type: 'text', text: system, cache_control: { type: 'ephemeral' } }],
    messages,
    ...(tools ? { tools } : {}),
  });
}
