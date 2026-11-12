"""Chapter 19 · An agent that calls an external API (English, voice: Zira by default)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine  # noqa: E402
from engine import BAND_AMBER, BAND_BLUE, BAND_TEAL, C, arrow, box, build, canvas, code_panel, font, preview, rbox, text_c, text_l  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
VOICES = {'zira': 'Microsoft Zira Desktop', 'david': 'Microsoft David Desktop'}
VOICE = os.environ.get('VOICE', 'zira').lower()
engine.SINGLE_VOICE = VOICES[VOICE]
engine.SPEECH = [
    (r'ViaCEP', 'Via C E P'), (r'\bCEP\b', 'C E P'), (r'lookup_cep', 'lookup C E P'), (r'fetchImpl', 'fetch impl'), (r'\bAPI\b', 'A P I'),
    (r'\bLLM\b', 'L L M'), (r'\bMCP\b', 'M C P'), (r'LangGraph', 'Lang Graph'), (r'search_policies', 'search policies'),
    (r'create_ticket', 'create ticket'), (r'AbortSignal\.timeout', 'abort signal timeout'), (r'\bnpm\b', 'N P M'),
    (r'runAgent', 'run agent'), (r'maxSteps', 'max steps'),
]
TAG = 'Chapter 19 · An agent with an external API'
NOTE = (130, 225, 215)
WARN_L = (255, 200, 120)


def cv():
    return canvas(TAG)


B1 = ['Hello!',
      'Until now, the only smart tool of the agent was a search in the vector index.',
      'This chapter answers a natural question: what if I want the agent to call an A P I on the internet?',
      'The short answer: you write one new tool, and one new agent. The rest of the project does not change.']


def s1(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 195), 'An agent with an external API', font(60, True))
    if k >= 2:
        box(d, 150, 320, 400, 100, 'Until now', 'search in the index', 'acc', hi=(k == 2), tsize=28, ssize=21)
    if k >= 3:
        arrow(d, [(565, 370), (715, 370)], C['ink'], 5)
        box(d, 730, 320, 400, 100, 'Now', 'an API on the internet', 'blue', hi=(k == 3), tsize=28, ssize=21)
    if k >= 4:
        text_c(d, (640, 520), 'one new tool  +  one new agent', font(34, True), C['warn'])
    return img, d


B2 = ['Think of it like this: the agent is an employee, and the tools are the systems the employee can open.',
      'So far, one employee had the internal library and the ticket system.',
      'Now, a second employee gets access to a third system: a postal code lookup.',
      'The employee, which is the loop from chapter eleven, is the same. Only what it can open changes.',
      'The example A P I is Via C E P, a public, free service for Brazilian postal codes, with no key needed.']


def s2(k):
    img, d = cv()
    text_c(d, (640, 70), 'The employee and the systems', font(44, True))
    if k >= 2:
        box(d, 60, 140, 330, 100, 'Employee 1', 'helpdesk agent', 'acc', hi=(k == 2), tsize=26, ssize=20)
        box(d, 520, 125, 300, 60, 'library', '', 'box', tsize=22)
        box(d, 520, 200, 300, 60, 'ticket system', '', 'box', tsize=22)
        arrow(d, [(392, 175), (518, 155)], C['ink'], 3, head=9)
        arrow(d, [(392, 205), (518, 230)], C['ink'], 3, head=9)
    if k >= 3:
        box(d, 60, 340, 330, 100, 'Employee 2', 'cep agent', 'blue', hi=(k == 3), tsize=26, ssize=20)
        box(d, 520, 355, 300, 70, 'postal code lookup', 'external', 'warn', hi=(k == 3), tsize=21, ssize=18)
        arrow(d, [(392, 390), (518, 390)], C['ink'], 3, head=9)
    if k >= 4:
        rbox(d, (870, 125, 1230, 440), 'acc', hi=(k == 4))
        text_c(d, (1050, 170), 'same', font(30, True), C['acc'])
        text_c(d, (1050, 215), 'employee', font(30, True), C['acc'])
        text_c(d, (1050, 275), '(the loop of', font(21))
        text_c(d, (1050, 305), 'chapter 11)', font(21))
        text_c(d, (1050, 375), 'only what it can open', font(21, True), C['muted'])
        text_c(d, (1050, 405), 'changes', font(21, True), C['muted'])
    if k >= 5:
        rbox(d, (160, 490, 1120, 570), 'warn', hi=(k == 5))
        text_c(d, (640, 520), 'ViaCEP: public · free · no key', font(28, True), C['warn'])
        text_c(d, (640, 553), 'chosen only as an example: the same mold fits any API', font(19), C['muted'])
    return img, d


FILES = [('src/agent/tools/lookup-cep.js', 'NEW', 'the tool that calls the API', 'acc'), ('src/agent/agents/cep-agent.js', 'NEW', 'the agent that uses only it', 'acc'),
         ('test/cep.test.js', 'NEW', '4 tests, no internet', 'acc'), ('tools/index.js', '2 lines', 'an import and the factory in the list', 'blue'),
         ('agents/index.js', '2 lines', 'an import and the agent in the list', 'blue'),
         ('runner · langgraph · mcp · cli · guardrails', 'no change', 'they read the same lists', 'warn')]
B3 = ['What changed in the project? Very little.',
      'Three new files: the tool, the agent, and the tests.',
      'Two existing files got two lines each: one import, and one entry in a list.',
      'And the runner, the Lang Graph engine, the M C P server, the command line, and the guardrails had no change at all.',
      'That is the most important point: the project is open for extension.',
      'The M C P server and the Lang Graph engine offered the new tool without anyone editing them, because both read the same list.']


def s3(k):
    img, d = cv()
    text_c(d, (640, 60), 'What changed?', font(44, True))
    ranges = {2: (0, 3), 3: (3, 5), 4: (5, 6), 5: (5, 6), 6: (5, 6)}
    for i, (f, tag, desc, st) in enumerate(FILES):
        show = (k >= 2 and i < 3) or (k >= 3 and i < 5) or (k >= 4)
        if show:
            y = 110 + i * 78
            lo, hi_ = ranges.get(k, (0, 0))
            rbox(d, (40, y, 1240, y + 66), st, hi=(lo <= i < hi_), r=10)
            text_l(d, (65, y + 33), f, font(21, False, True))
            text_l(d, (680, y + 33), tag, font(21, True), C[st])
            text_l(d, (830, y + 33), desc, font(17), C['muted'])
    if k >= 5:
        text_c(d, (640, 600), 'open for extension', font(26, True), NOTE)
    return img, d


REG = ["import { createLookupCepTool } from './lookup-cep.js';", '',
       'const factories = [createSearchPoliciesTool, createCreateTicketTool, createLookupCepTool];', '',
       "import { cepAgent } from './cep-agent.js';", '',
       'export const agents = [helpdeskAgent, triageAgent, cepAgent];']
B4 = ['These are the only edited lines.',
      'In the tools registry: one import, and the factory added to the list.',
      'In the agents registry: one import, and the agent added to the list.',
      'From then on, create tools includes lookup C E P, and get agent with the name cep works.']


def s4(k):
    img, d = cv()
    bands = {2: [(0, 2, BAND_TEAL)], 3: [(4, 6, BAND_BLUE)], 4: [(2, 2, BAND_AMBER), (6, 6, BAND_AMBER)]}.get(k, [])
    ys = code_panel(d, 'the only edited lines', REG, bands, size=18, line_h=34, y0=210)
    if k >= 2:
        text_l(d, (110, 575), 'tools/index.js  (top)   ·   agents/index.js  (bottom)', font(19, True), NOTE)
    return img, d


TOOL = ['async run({ cep }) {', "  const digits = cep.replace(/\\D/g, '');", "  if (digits.length !== 8) return 'CEP inválido: informe 8 dígitos.';",
        '  let res;', '  try {', '    res = await fetchImpl(url, { signal: AbortSignal.timeout(8000) });', '  } catch {',
        "    return 'Não foi possível consultar a API de CEP agora ...';", '  }', '  if (!res.ok) return `A API de CEP respondeu com erro ${res.status}.`;',
        '  const d = await res.json();', "  if (d.erro) return 'CEP não encontrado.';",
        '  return `${d.logradouro}, ${d.bairro}, ${d.localidade}/${d.uf}`;', '}']
B5 = ['Now, the tool itself. The structure is the same as any tool. What changes is the body of run, and it holds the decisions that apply to any external A P I.',
      'First, validate before calling. An invalid input does not spend a network call.',
      'Second, a timeout. A slow A P I must not freeze the agent forever.',
      'Third, errors become text. The model reads the sentence and explains it to the user. An exception would break the conversation.',
      'Fourth, know the A P I. Via C E P answers 200 even for a postal code that does not exist, with an error field. Reading the documentation avoids a silent bug.',
      'And fifth, a lean answer: four fields, out of about twelve, to save tokens.']


def s5(k):
    img, d = cv()
    bands = {2: [(1, 2, BAND_TEAL)], 3: [(5, 5, BAND_BLUE)], 4: [(6, 9, BAND_AMBER)], 5: [(10, 11, BAND_TEAL)], 6: [(12, 12, BAND_BLUE)]}.get(k, [])
    ys = code_panel(d, 'src/agent/tools/lookup-cep.js  (condensed)', TOOL, bands, size=16, line_h=26, y0=198)
    notes = {2: (1, '←  1 · validate first'), 3: (5, '←  2 · timeout: 8 s'), 4: (7, '←  3 · errors become text'), 5: (11, '←  4 · the API answers 200 for a missing CEP'), 6: (12, '←  5 · only 4 fields (of ~12)')}
    if k in notes:
        i, t = notes[k]
        text_l(d, (700 if k != 5 else 560, ys[i]), t, font(19, True), NOTE)
    return img, d


B6 = ['Here is the real result, running this tool against the real Via C E P service.',
      'A valid code, with a hyphen: the address comes back.',
      'An invalid code, with three digits: it is refused right away, without calling the network.',
      'A code that does not exist: the tool says it was not found.',
      'Three different outcomes, and in none of them an exception.']
RES = [('cep: "01310-100"', 'Avenida Paulista, Bela Vista, São Paulo/SP', 'acc'), ('cep: "123"', 'CEP inválido: informe 8 dígitos.', 'warn'),
       ('cep: "00000-000"', 'CEP não encontrado.', 'blue')]


def s6(k):
    img, d = cv()
    text_c(d, (640, 62), 'Real result · tool run against ViaCEP', font(36, True))
    for i, (q, a, st) in enumerate(RES):
        if k >= i + 2:
            y = 130 + i * 130
            rbox(d, (60, y, 1220, y + 110), st, hi=(k == i + 2))
            text_l(d, (90, y + 33), 'run(' + q + ')', font(24, True, True))
            text_l(d, (90, y + 76), '→  ' + a, font(26, False, True), C[st])
    if k >= 5:
        text_c(d, (640, 560), 'valid · invalid · not found:  no exception in any of them', font(26, True), NOTE)
    return img, d


AGENT = ['export const cepAgent = {', "  name: 'cep',", "  description: 'Consulta endereços por CEP em uma API externa (ViaCEP).',",
         '  system: `Você ajuda a consultar endereços brasileiros pelo CEP. ...`,', "  tools: ['lookup_cep'],", '  maxSteps: 3,', '};']
B7 = ['Now, the agent. It is only data: a name, a description, instructions, a list of tools, and a step limit.',
      'The list has only one tool: lookup C E P.',
      'That is least privilege. This agent cannot even see the policy search, or the ticket tool.',
      'And three steps is enough: ask for the tool, read the result, answer.']


def s7(k):
    img, d = cv()
    bands = {2: [(4, 4, BAND_TEAL)], 3: [(4, 4, BAND_AMBER)], 4: [(5, 5, BAND_BLUE)]}.get(k, [])
    ys = code_panel(d, 'src/agent/agents/cep-agent.js', AGENT, bands, size=19, line_h=36, y0=215)
    if k == 3:
        text_c(d, (640, 540), 'least privilege:  it cannot see search_policies or create_ticket', font(26, True), WARN_L)
    if k == 4:
        text_c(d, (640, 540), 'ask for the tool  →  read the result  →  answer', font(26, True), NOTE)
    return img, d


FETCH = ['const fakeFetch = (reply) => {', '  const calls = [];', '  const fn = async (url) => { calls.push(url); return reply; };', '  fn.calls = calls;',
         '  return fn;', '};', '', 'const tool = createLookupCepTool({ fetchImpl: f });',
         "assert.equal(await tool.run({ cep: '01310-100' }), 'Avenida Paulista, Bela Vista, São Paulo/SP');",
         "assert.equal(f.calls[0], 'https://viacep.com.br/ws/01310100/json/');"]
B8 = ['How do we test it without internet? The fetch function is injected.',
      'In production, the tool uses the global fetch. In the tests, we pass a fake one, that returns what the test wants, and records the called addresses.',
      'So the test checks the formatted address, and also that the address called contains only the digits.',
      'There are four tests: the tool, its failures, the agent in the own engine, and the same tool in Lang Graph.',
      'An honest limit: the real service was called in this chapter, by the tool alone. The full agent, with a real model, was never run.']


def s8(k):
    img, d = cv()
    bands = {2: [(0, 5, BAND_TEAL), (7, 7, BAND_BLUE)], 3: [(8, 9, BAND_AMBER)]}.get(k, [])
    ys = code_panel(d, 'test/cep.test.js  (excerpt)', FETCH, bands, size=15, line_h=30, y0=205)
    if k == 2:
        text_c(d, (640, 560), 'production: global fetch     tests: a fake fetch  (no internet)', font(22, True), NOTE)
    if k == 4:
        rbox(d, (240, 540, 1040, 600), 'box', hi=True)
        text_c(d, (640, 570), '4 tests:  tool · failures · own engine · LangGraph', font(24, True))
    if k == 5:
        rbox(d, (160, 535, 1120, 605), 'warn', hi=True)
        text_c(d, (640, 570), 'real API: tool only   ·   full agent with a real model: never run', font(22, True), C['warn'])
    return img, d


B9 = ['To sum up: a new data source is a new tool, and a new agent.',
      'Validate, set a timeout, turn errors into text, know the A P I, and keep the answer lean.',
      'Inject the network call, so the tests need no internet.',
      'In the next chapter, the last one: hooks, to validate and control the agent. See you there!']


def s9(k):
    img, d = cv()
    text_c(d, (640, 90), 'See you there!' if k >= 4 else 'Summing up', font(52, True), C['acc'] if k >= 4 else C['ink'])
    rows = [(1, 'acc', '1   New data source = new tool + new agent'), (2, 'blue', '2   Validate · timeout · errors as text · lean answer'),
            (3, 'warn', '3   Inject the network call: tests without internet'), (4, 'box', 'Next chapter:  hooks')]
    for i, (kk, st, t) in enumerate(rows):
        if k >= kk:
            y = 160 + i * 105
            rbox(d, (130, y, 1150, y + 82), st, hi=(k == kk))
            text_l(d, (170, y + 41), t, font(27, True))
    return img, d


SCENES = [(B1, s1), (B2, s2), (B3, s3), (B4, s4), (B5, s5), (B6, s6), (B7, s7), (B8, s8), (B9, s9)]

if __name__ == '__main__':
    work = os.environ.get('VIDEO_WORKDIR', os.path.join(HERE, '_work', f'cap19_en_{VOICE}'))
    if len(sys.argv) > 1 and sys.argv[1] == 'preview':
        preview(SCENES, os.path.join(work, 'preview'))
        print('preview saved in', os.path.join(work, 'preview'))
    else:
        build(SCENES, os.path.join(HERE, 'saida', f'cap19_en_{VOICE}.mp4'), work, TAG)
