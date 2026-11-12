// Conjunto dourado: pergunta -> documento que deve aparecer no top-k.
export const GOLDEN = [
  { q: 'Quantos dias de férias eu tenho direito?', doc: 'ferias' },
  { q: 'Posso vender dias de férias?', doc: 'ferias' },
  { q: 'Com quanto tempo de antecedência peço férias?', doc: 'ferias' },
  { q: 'Quantos dias por semana posso trabalhar de casa?', doc: 'home-office' },
  { q: 'Existe auxílio para internet no home office?', doc: 'home-office' },
  { q: 'Posso trabalhar de outro país?', doc: 'home-office' },
  { q: 'Qual o prazo para pedir reembolso de despesas?', doc: 'reembolso' },
  { q: 'Qual o limite de reembolso para refeições?', doc: 'reembolso' },
  { q: 'Como resetar minha senha?', doc: 'ti-suporte' },
  { q: 'Como configuro a VPN?', doc: 'ti-suporte' },
  { q: 'Qual o SLA de um chamado de TI?', doc: 'ti-suporte' },
];
