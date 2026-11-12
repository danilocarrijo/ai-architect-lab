// Guardrails em camadas: entrada (PII, injection), contexto recuperado (não confiável) e saída.
const PII = [
  [/\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b/g, '[CPF]'],
  [/[\w.+-]+@[\w-]+\.[\w.]+/g, '[EMAIL]'],
  [/\(?\b\d{2}\)?\s?9?\d{4}-?\d{4}\b/g, '[TELEFONE]'],
];

const INJECTION = [
  /ignore (todas )?(as )?(instru|regras|anteriores)/i,
  /ignore (all )?(the )?(previous|prior|above) (instructions|rules)/i,
  /desconsidere .{0,30}instru/i,
  /revele .{0,30}(prompt|instru)/i,
  /(system|developer) prompt/i,
  /you are now/i,
  /voc[êe] agora [ée]/i,
];

export const redactPII = (text) => PII.reduce((t, [re, tag]) => t.replace(re, tag), text);
export const looksLikeInjection = (text) => INJECTION.some((re) => re.test(text));

// Conteúdo recuperado é DADO, nunca instrução (injeção indireta): remove linhas suspeitas.
export function sanitizeContext(text) {
  return text.split('\n').filter((l) => !looksLikeInjection(l)).join('\n');
}

export function checkInput(question) {
  if (!question?.trim()) return { ok: false, reason: 'Pergunta vazia.' };
  if (question.length > 2000) return { ok: false, reason: 'Pergunta longa demais.' };
  if (looksLikeInjection(question)) return { ok: false, reason: 'Possível prompt injection bloqueado.' };
  return { ok: true, clean: redactPII(question) };
}

// Checagem de saída barata: toda resposta factual deve citar uma fonte [n] existente.
export function checkOutput(answer, nSources) {
  const cited = [...answer.matchAll(/\[(\d+)\]/g)].map((m) => Number(m[1]));
  const valid = cited.length > 0 && cited.every((n) => n >= 1 && n <= nSources);
  return { grounded: valid, text: redactPII(answer) };
}
