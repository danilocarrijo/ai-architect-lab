import { ChatAnthropic } from '@langchain/anthropic';
import { ChatGoogleGenerativeAI } from '@langchain/google-genai';
import { config } from '../../config.js';
import { llmProvider } from '../../llm/client.js';

// Mesma regra de escolha do client.js (Gemini tem prioridade), mas devolvendo um chat model do LangChain.
// Trocar de provedor aqui não exige mudar o agente: ambos expõem a mesma interface.
export function createChatModel() {
  const provider = llmProvider();
  if (provider === 'gemini') {
    return new ChatGoogleGenerativeAI({
      model: config.gemini.model,
      apiKey: process.env.GEMINI_API_KEY || process.env.GOOGLE_API_KEY,
      maxOutputTokens: config.gemini.maxTokens,
    });
  }
  if (provider === 'anthropic') {
    return new ChatAnthropic({ model: config.llm.model, maxTokens: config.llm.maxTokens });
  }
  throw new Error('O agente precisa de GEMINI_API_KEY (ou ANTHROPIC_API_KEY).');
}
