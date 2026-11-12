import { z } from 'zod';

// Ferramenta que chama uma API EXTERNA (ViaCEP, pública e sem chave) em vez de buscar no índice vetorial.
// O fetch é injetável: em produção usa o global; nos testes passamos um falso (nada de internet).
export const createLookupCepTool = ({ fetchImpl = fetch } = {}) => ({
  name: 'lookup_cep',
  description: 'Consulta o endereço de um CEP brasileiro. Use quando o usuário informar um CEP.',
  schema: { cep: z.string().describe('CEP com 8 dígitos, com ou sem hífen') },
  async run({ cep }) {
    const digits = cep.replace(/\D/g, '');
    if (digits.length !== 8) return 'CEP inválido: informe 8 dígitos.';
    // Sem timeout, uma API lenta travaria o agente. Erros viram texto: o LLM lê e explica ao usuário.
    let res;
    try {
      res = await fetchImpl(`https://viacep.com.br/ws/${digits}/json/`, { signal: AbortSignal.timeout(8000) });
    } catch {
      return 'Não foi possível consultar a API de CEP agora (rede ou tempo esgotado).';
    }
    if (!res.ok) return `A API de CEP respondeu com erro ${res.status}.`;
    const d = await res.json();
    if (d.erro) return 'CEP não encontrado.'; // o ViaCEP responde 200 com { "erro": "true" } para CEP inexistente
    return `${d.logradouro}, ${d.bairro}, ${d.localidade}/${d.uf}`; // só os campos úteis (poupa tokens)
  },
});
