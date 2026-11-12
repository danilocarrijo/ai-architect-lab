"""Chapter 11 · Agents: the model decides what to do (English, voice: Zira by default).

Usage:   python cap11_en.py preview
         python cap11_en.py                      # saida\\cap11_en_zira.mp4
         set VOICE=david && python cap11_en.py   # male voice
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine  # noqa: E402
from engine import (BAND_AMBER, BAND_BLUE, BAND_TEAL, C, arrow, box, build, canvas, code_panel, dashed,  # noqa: E402
                    font, preview, rbox, text_c, text_l)

HERE = os.path.dirname(os.path.abspath(__file__))
VOICES = {'zira': 'Microsoft Zira Desktop', 'david': 'Microsoft David Desktop'}
VOICE = os.environ.get('VOICE', 'zira').lower()
engine.SINGLE_VOICE = VOICES[VOICE]
engine.SPEECH = [   # spoken-only fixes (the subtitles keep the original text)
    (r'\bMCP\b', 'M C P'), (r'pickTools', 'pick tools'), (r'create_ticket', 'create ticket'), (r'search_policies', 'search policies'),
    (r'TCK-1001', 'T C K one thousand one'), (r'maxSteps', 'max steps'), (r'tool_use', 'tool use'), (r'end_turn', 'end turn'),
    (r'\bZod\b', 'zod'), (r'\bnpm\b', 'N P M'),
]
TAG = 'Chapter 11 · Agents: the model decides what to do'
NOTE = (130, 225, 215)
WARN_L = (255, 200, 120)


def cv():
    return canvas(TAG)


# ---------- scene 1 · opening ----------
B1 = ['Hello!',
      'So far, the question followed a fixed path: always search, then answer.',
      'Now, the model will decide what to do.',
      'In this chapter, you will meet agents: tools, definitions, and the loop that runs them.']


def s1(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 200), 'Agents', font(80, True))
    if k >= 3:
        text_c(d, (640, 282), 'the model decides what to do', font(38), C['acc'])
    if k >= 2:
        box(d, 150, 355, 400, 90, 'Until now', 'a fixed path', 'box', hi=(k == 2), tsize=27, ssize=20)
    if k >= 3:
        arrow(d, [(565, 400), (715, 400)], C['ink'], 5)
        box(d, 730, 355, 400, 90, 'Chapter 11', 'the model chooses', 'acc', hi=(k == 3), tsize=27, ssize=20)
    if k >= 4:
        text_c(d, (640, 540), 'Tools   ·   Definitions   ·   The loop', font(32, True), C['muted'])
    return img, d


# ---------- scene 2 · assembly line vs intern ----------
B2 = ['The ask function is an assembly line: the same steps, every time.',
      'An agent is different. Think of an intern with a boss.',
      'At each round, the boss, the language model, decides: do I need to look up a policy? Do I need to open a ticket? Or can I already answer?',
      'And the runner is the messenger that carries notes between the boss and the tools.',
      'One important detail: the language model never runs code.',
      'It only writes text. When it wants a tool, it writes a request, and your code is the one that really runs it.']


def s2(k):
    img, d = cv()
    text_c(d, (640, 80), 'Assembly line  vs  agent', font(44, True))
    if k >= 1:
        rbox(d, (40, 125, 520, 590), 'box', hi=(k == 1))
        text_c(d, (280, 165), 'ask()  ·  assembly line', font(26, True))
        for i, t in enumerate(['check input', 'cache', 'search', 'model', 'check output']):
            box(d, 110, 205 + i * 70, 340, 52, t, '', 'blue' if i in (1,) else ('warn' if i in (0, 4) else 'acc'), tsize=22)
        text_c(d, (280, 570), 'the same steps, every time', font(21, True), C['muted'])
    if k >= 2:
        rbox(d, (560, 125, 1240, 590), 'acc', hi=(k == 2))
        text_c(d, (900, 162), 'agent  ·  an intern with a boss', font(26, True), C['acc'])
        box(d, 640, 195, 520, 62 if k < 3 else 92, 'the boss  =  the language model', '"look up a policy?  open a ticket?  or answer?"' if k >= 3 else '',
            'blue', hi=(k in (2, 3)), tsize=24, ssize=18)
    if k >= 4:
        y = 310 if k >= 3 else 280
        box(d, 640, y, 520, 56, 'the messenger  =  the runner', '', 'box', hi=(k == 4), tsize=23)
        box(d, 640, y + 95, 520, 74, 'the tools', 'search policies · create ticket', 'warn', tsize=23, ssize=17)
        arrow(d, [(900, 290), (900, y - 3)], C['ink'], 3, head=9)
        arrow(d, [(900, y + 58), (900, y + 92)], C['ink'], 3, head=9)
    if k >= 5:
        rbox(d, (600, 490, 1200, 535), 'warn', hi=(k == 5))
        text_c(d, (900, 513), 'the model never runs code', font(26, True), C['warn'])
    if k >= 6:
        text_c(d, (900, 562), 'it writes a request  ·  your code runs it', font(22, True), C['acc'])
    return img, d


# ---------- scene 3 · the tool ----------
B3 = ['First piece: the tool.',
      'A tool is an object with four fields: a name, a description, a schema, and the run function that does the work.',
      'The description is what the model reads to decide when to use it, so write it well.',
      'The schema uses the Zod library to say which arguments exist and what type they are.',
      'The ticket is simulated: it is only saved in a list in memory. In production, run would call the ticketing system.']
TOOL = ['export const createCreateTicketTool = ({ tickets = [] } = {}) => ({', "  name: 'create_ticket',",
        "  description: 'Abre um chamado no helpdesk (simulado)...',", '  schema: {', '    title: z.string(),',
        '    description: z.string(),', "    priority: z.enum(['baixa', 'media', 'alta']).optional(),", '  },',
        "  async run({ title, description, priority = 'media' }) {", '    const id = `TCK-${1000 + tickets.length + 1}`;',
        '    tickets.push({ id, title, description, priority });',
        '    return `Chamado ${id} criado (prioridade ${priority}): ${title}`;', '  },', '});']


def s3(k):
    img, d = cv()
    bands = {2: [(1, 1, BAND_TEAL), (2, 2, BAND_BLUE), (3, 7, BAND_AMBER), (8, 11, BAND_TEAL)], 3: [(2, 2, BAND_BLUE)],
             4: [(3, 7, BAND_AMBER)], 5: [(8, 11, BAND_TEAL)]}.get(k, [])
    ys = code_panel(d, 'src/agent/tools/create-ticket.js  (shortened)', TOOL, bands, size=19, line_h=30, y0=204)
    notes = {2: None, 3: (2, '←  what the model reads'), 4: (5, '←  Zod: which arguments, which types'), 5: (9, '←  simulated: a list in memory')}
    if k == 2:
        for i, t in [(1, '←  name'), (2, '←  description'), (4, '←  schema'), (8, '←  run')]:
            text_l(d, (860, ys[i]), t, font(21, True), NOTE)
    elif notes.get(k):
        i, t = notes[k]
        text_l(d, (860, ys[i]) if k != 3 else (900, ys[i]), t, font(21, True), NOTE)
    return img, d


# ---------- scene 4 · search_policies ----------
B4 = ['The other tool, search_policies, uses the retriever you already know.',
      'Notice what happened: the entire RAG, from chapters 2 to 6, became just one tool, that the agent can use whenever it wants.']
SEARCH = ['export const createSearchPoliciesTool = ({ retriever }) => ({', "  name: 'search_policies',",
          "  schema: { query: z.string(), dept: z.enum(['rh', 'ti', 'financeiro']).optional() },",
          '  async run({ query, dept }) {',
          '    const hits = await retriever.retrieve(query, { filter: dept ? { dept } : undefined });',
          "    return hits.length ? hits.map(/* ... */).join('\\n---\\n') : 'Nenhum resultado.';", '  },', '});']


def s4(k):
    img, d = cv()
    bands = {1: [(4, 4, BAND_TEAL)], 2: [(0, 7, BAND_BLUE)]}.get(k, [])
    ys = code_panel(d, 'src/agent/tools/search-policies.js  (condensed)', SEARCH, bands, size=19, line_h=32, y0=208)
    if k == 1:
        text_l(d, (800, ys[4] + 34), '↑  the retriever of chapter 6', font(22, True), NOTE)
    if k >= 2:
        text_c(d, (640, 520), 'the entire RAG  (chapters 2 to 6)   =   one tool', font(33, True), NOTE)
    return img, d


# ---------- scene 5 · the agent definition ----------
B5 = ['Second piece: the agent definition.',
      'An agent is just data: an object that says who it is and what it can use.',
      'The system field holds its instructions: its job description.',
      'The tools field is the list of tools it is allowed to use. This is the principle of least privilege: it only sees what is on this list.',
      'And max steps is the maximum number of rounds, to avoid an endless loop that burns money.',
      'The project has three agents: helpdesk, triage, and cep, which calls an external API, as we will see later.']
AGENT = ['export const helpdeskAgent = {', "  name: 'helpdesk',", "  description: 'Responde dúvidas sobre políticas internas e abre chamados...',",
         '  system: `Você é um agente de helpdesk da Acme. Use search_policies para fundamentar respostas...`,',
         "  tools: ['search_policies', 'create_ticket'],", '  maxSteps: 6,', '};']


def s5(k):
    img, d = cv()
    bands = {2: [(1, 5, BAND_TEAL)], 3: [(3, 3, BAND_BLUE)], 4: [(4, 4, BAND_AMBER)], 5: [(5, 5, BAND_TEAL)]}.get(k, [])
    ys = code_panel(d, 'src/agent/agents/helpdesk-agent.js  (shortened)', AGENT, bands, size=19, line_h=32, y0=208)
    notes = {3: (3, '↑  the job description'), 4: (4, '←  the only tools it may use'), 5: (5, '←  at most 6 rounds')}
    if k in notes:
        i, t = notes[k]
        text_l(d, (700 if k != 3 else 130, ys[i] + (38 if k == 3 else 0)), t, font(22, True), NOTE)
    if k >= 4:
        text_c(d, (640, 470), 'least privilege:  it only sees what is on the list', font(28, True), WARN_L)
    if k >= 6:
        for i, (t, sub, st) in enumerate([('helpdesk', 'answers + tickets', 'acc'), ('triage', 'IT incidents', 'blue'), ('cep', 'external API (Ch. 19)', 'warn')]):
            box(d, 120 + i * 360, 505, 320, 85, t, sub, st, hi=(k == 6), tsize=25, ssize=18)
    return img, d


# ---------- scene 6 · the runner loop ----------
B6 = ['Third piece: the loop that runs the agent, in the runner.',
      'Before the loop, the input guardrail cleans the question, and pickTools separates only the agent\'s tools.',
      'Each round, the runner sends to the model the instructions, the conversation history, and the menu of tools.',
      'If the model did not ask for a tool, it is done: the runner returns the answer.',
      'If it asked, the runner executes the tool with the arguments the model sent.',
      'It stores the result in the history, and the next round begins.',
      'If the rounds run out, it gives up with a limit message.']
LOOP = ['const tools = pickTools(allTools ?? createTools({ retriever }), agent.tools);',
        "const messages = [{ role: 'user', content: input.clean }];", '',
        'for (let step = 1; step <= agent.maxSteps; step++) {',
        '  const res = await llm({ system: agent.system, messages, tools: defs });',
        "  messages.push({ role: 'assistant', content: res.content });",
        "  if (res.stop_reason !== 'tool_use') return { answer, steps: step };",
        "  for (const b of res.content.filter((c) => c.type === 'tool_use')) {",
        '    content = await tool.run(b.input);',
        "    results.push({ type: 'tool_result', tool_use_id: b.id, content });", '  }',
        "  messages.push({ role: 'user', content: results });", '}',
        "return { answer: 'Limite de passos atingido sem resposta final.', steps: agent.maxSteps };"]


def s6(k):
    img, d = cv()
    bands = {2: [(0, 1, BAND_TEAL)], 3: [(3, 5, BAND_BLUE)], 4: [(6, 6, BAND_AMBER)], 5: [(7, 9, BAND_TEAL)], 6: [(11, 11, BAND_BLUE)],
             7: [(13, 13, BAND_AMBER)]}.get(k, [])
    code_panel(d, 'src/agent/runner.js  (condensed)', LOOP, bands, size=18, line_h=30, y0=205)
    return img, d


# ---------- scene 7 · two safety decisions ----------
B7 = ['Two safety decisions are hidden in this code.',
      'If the model asks for a tool that is not on the agent\'s list, the runner refuses.',
      'And if a tool fails, the runner does not break: it returns the error as the result, so the model can try again or explain the problem.']


def s7(k):
    img, d = cv()
    text_c(d, (640, 85), 'Two safety decisions', font(48, True))
    if k >= 2:
        rbox(d, (60, 150, 620, 520), 'warn', hi=(k == 2))
        text_c(d, (340, 195), 'a tool outside the list', font(30, True), C['warn'])
        text_c(d, (340, 245), 'is refused', font(30, True), C['warn'])
        d.rounded_rectangle((85, 295, 595, 405), 12, fill=C['code_bg'])
        text_l(d, (100, 330), 'if (!tool) throw new Error(', font(19, False, True), C['code_ink'])
        text_l(d, (100, 365), '  `ferramenta não permitida: ${b.name}`', font(19, False, True), C['code_ink'])
        text_c(d, (340, 470), 'least privilege, enforced', font(24, True), C['warn'])
    if k >= 3:
        rbox(d, (660, 150, 1220, 520), 'blue', hi=(k == 3))
        text_c(d, (940, 195), 'a tool that fails', font(30, True), C['blue'])
        text_c(d, (940, 245), 'does not break the loop', font(30, True), C['blue'])
        d.rounded_rectangle((685, 295, 1195, 405), 12, fill=C['code_bg'])
        text_l(d, (700, 330), '} catch (e) {', font(19, False, True), C['code_ink'])
        text_l(d, (700, 365), '  content = `Erro: ${e.message}`;', font(19, False, True), C['code_ink'])
        text_c(d, (940, 470), 'the model reads the error and decides', font(24, True), C['blue'])
    return img, d


# ---------- scene 8 · the VPN example ----------
B8 = ['An example: the VPN is down for everyone.',
      "This is the scenario of the project's automatic test, with the triage agent.",
      'Round one: the model receives the question and the menu of tools.',
      'It answers asking for create_ticket, with the title VPN and priority high.',
      'The runner executes the tool, and gets: ticket TCK-1001 created, high priority.',
      'Round two: the model receives this result, and now answers with text only: ticket opened.',
      'Two steps, and the ticket was really created.']
LANES = [(150, 'User', 'box'), (430, 'runner', 'acc'), (760, 'Model', 'blue'), (1090, 'Tool', 'warn')]
MSGS = [(2, 0, 1, 150, 'A VPN caiu para todos', False), (3, 1, 2, 215, 'instructions + question + tools menu', False),
        (4, 2, 1, 280, 'tool_use: create_ticket(title: "VPN", priority: "alta")', True), (5, 1, 3, 345, 'tool.run(args)', False),
        (5, 3, 1, 400, '"Chamado TCK-1001 criado (prioridade alta): VPN"', True), (6, 1, 2, 460, 'round 2: history + the result', False),
        (6, 2, 1, 515, 'end_turn:  "Chamado aberto."', True), (7, 1, 0, 575, 'answer  +  steps = 2', False)]


def s8(k):
    img, d = cv()
    d.text((1240, 38), 'Example: "the VPN is down"', font=font(30, True), fill=C['ink'], anchor='rm')
    if k >= 1:
        for x, t, st in LANES:
            box(d, x - 70, 70, 140, 40, t, '', st, tsize=21)
            d.line((x, 112, x, 600), fill=C['line'], width=2)
    for kk, a, b, y, label, dash_ in MSGS:
        if k >= kk:
            xa, xb = LANES[a][0], LANES[b][0]
            off = 4 if xb > xa else -4
            arrow(d, [(xa + off, y), (xb - off * 2, y)], C['ink'] if not dash_ else C['muted'], 3, dash=dash_, head=10)
            mid = (xa + xb) / 2
            text_c(d, (mid, y - 16), label, font(17, True, True) if kk in (4, 5) and dash_ else font(18, True), C['ink'])
    if k >= 7:
        text_c(d, (1010, 600), '(scripted model in the test)', font(16), C['muted'])
    return img, d


# ---------- scene 9 · ask vs agent ----------
B9 = ['So, what is the practical difference between ask and an agent?',
      'In ask, the code decides the order of the steps: always search, then generate.',
      'In the agent, the model decides which tools to use, how many times, and when to stop.',
      'That is why the agent needs a step limit and restricted tools: the one deciding is a model, and models make mistakes.']


def s9(k):
    img, d = cv()
    text_c(d, (640, 85), 'ask()  vs  agent', font(50, True))
    if k >= 2:
        rbox(d, (60, 150, 620, 430), 'box', hi=(k == 2))
        text_c(d, (340, 195), 'ask()', font(38, True))
        text_c(d, (340, 275), 'the CODE decides', font(32, True), C['blue'])
        text_c(d, (340, 330), 'the order of the steps', font(26))
        text_c(d, (340, 375), 'always: search, then generate', font(23), C['muted'])
    if k >= 3:
        rbox(d, (660, 150, 1220, 430), 'acc', hi=(k == 3))
        text_c(d, (940, 195), 'agent', font(38, True), C['acc'])
        text_c(d, (940, 275), 'the MODEL decides', font(32, True), C['acc'])
        text_c(d, (940, 325), 'which tools · how many times', font(25))
        text_c(d, (940, 365), 'and when to stop', font(25))
    if k >= 4:
        rbox(d, (150, 470, 1130, 565), 'warn', hi=True)
        text_c(d, (640, 505), 'needs:   a step limit   +   restricted tools', font(33, True), C['warn'])
        text_c(d, (640, 543), 'the one deciding is a model, and models make mistakes', font(23), C['warn'])
    return img, d


# ---------- scene 10 · wrap-up ----------
B10 = ['To sum up: a tool is a function the model can request.',
       'An agent is just data: instructions, allowed tools, and a step limit.',
       'The runner is the loop that carries requests and results, with safety built in.',
       'In the next chapter, we will see how the same tools can be offered to other programs, with MCP.',
       'See you there!']


def s10(k):
    img, d = cv()
    text_c(d, (640, 95), 'See you there!' if k >= 5 else 'Summing up', font(54, True), C['acc'] if k >= 5 else C['ink'])
    rows = [(1, 'acc', '1   A tool:  a function the model can request'), (2, 'blue', '2   An agent:  instructions · allowed tools · step limit'),
            (3, 'warn', '3   The runner:  the loop, with safety built in'), (4, 'box', 'Next chapter:  MCP, the same tools for other programs')]
    for i, (kk, st, t) in enumerate(rows):
        if k >= kk:
            y = 165 + i * 105
            rbox(d, (130, y, 1150, y + 82), st, hi=(k == kk))
            text_l(d, (170, y + 41), t, font(28, True))
    return img, d


SCENES = [(B1, s1), (B2, s2), (B3, s3), (B4, s4), (B5, s5), (B6, s6), (B7, s7), (B8, s8), (B9, s9), (B10, s10)]

if __name__ == '__main__':
    work = os.environ.get('VIDEO_WORKDIR', os.path.join(HERE, '_work', f'cap11_en_{VOICE}'))
    if len(sys.argv) > 1 and sys.argv[1] == 'preview':
        preview(SCENES, os.path.join(work, 'preview'))
        print('preview saved in', os.path.join(work, 'preview'))
    else:
        build(SCENES, os.path.join(HERE, 'saida', f'cap11_en_{VOICE}.mp4'), work, TAG)
