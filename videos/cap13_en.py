"""Chapter 13 · LangChain and LangGraph: the same agent, another engine (English, voice: Zira by default).

Usage:   python cap13_en.py preview
         python cap13_en.py                      # saida\\cap13_en_zira.mp4
         set VOICE=david && python cap13_en.py   # male voice
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine  # noqa: E402
from engine import (BAND_AMBER, BAND_BLUE, BAND_TEAL, C, arrow, box, build, canvas, code_panel, font,  # noqa: E402
                    preview, rbox, text_c, text_l)

HERE = os.path.dirname(os.path.abspath(__file__))
VOICES = {'zira': 'Microsoft Zira Desktop', 'david': 'Microsoft David Desktop'}
VOICE = os.environ.get('VOICE', 'zira').lower()
engine.SINGLE_VOICE = VOICES[VOICE]
engine.SPEECH = [   # spoken-only fixes (the subtitles keep the original text)
    (r'LangChain', 'Lang Chain'), (r'LangGraph', 'Lang Graph'), (r'createAgent', 'create agent'),
    (r'createChatModel', 'create chat model'), (r'toLangChainTools', 'to Lang Chain tools'), (r'TracerHandler', 'Tracer Handler'),
    (r'recursionLimit', 'recursion limit'), (r'maxSteps', 'max steps'), (r'ChatGoogleGenerativeAI', 'Chat Google Generative A I'),
    (r'ChatAnthropic', 'Chat Anthropic'), (r'client\.js', 'client dot J S'), (r'\bAPI\b', 'A P I'), (r'\bMCP\b', 'M C P'),
    (r'\bnpm\b', 'N P M'), (r'\bZod\b', 'zod'),
]
TAG = 'Chapter 13 · LangChain and LangGraph: another engine'
NOTE = (130, 225, 215)
WARN_L = (255, 200, 120)


def cv():
    return canvas(TAG)


# ---------- scene 1 · opening ----------
B1 = ['Hello!',
      'In the previous chapter, we shared the tools with MCP.',
      'Now, the same agent, built with a popular framework: LangChain, and its LangGraph part.',
      'You will see how little changes, and what the framework brings.']


def s1(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 195), 'LangChain + LangGraph', font(70, True))
    if k >= 3:
        text_c(d, (640, 280), 'the same agent, another engine', font(36), C['acc'])
    if k >= 2:
        box(d, 150, 355, 400, 90, 'Chapter 12', 'MCP', 'box', hi=(k == 2), tsize=27, ssize=20)
    if k >= 3:
        arrow(d, [(565, 400), (715, 400)], C['ink'], 5)
        box(d, 730, 355, 400, 90, 'Chapter 13', 'a framework', 'blue', hi=(k == 3), tsize=27, ssize=20)
    if k >= 4:
        text_c(d, (640, 540), 'how little changes   ·   what the framework brings', font(30, True), C['muted'])
    return img, d


# ---------- scene 2 · what they are ----------
B2 = ['LangChain is a library for building applications with language models.',
      'It offers ready-made pieces: models, tools, and agents.',
      'LangGraph is the part that organizes an agent as a graph of steps: model, tools, model, and so on.',
      'Think of it this way: in chapter 11, you built the engine piece by piece. LangGraph is a factory engine.',
      'It does the same job, and comes with extras. But the car stays the same: agents, tools, and guardrails do not change.']


def s2(k):
    img, d = cv()
    text_c(d, (640, 80), 'What are they?', font(46, True))
    if k >= 1:
        rbox(d, (60, 130, 1220, 560), 'blue', hi=(k == 1))
        text_c(d, (640, 170), 'LangChain  ·  a library for LLM applications', font(29, True), C['blue'])
    if k >= 2:
        for i, t in enumerate(['models', 'tools', 'agents']):
            box(d, 130 + i * 270, 215, 240, 60, t, '', 'box', hi=(k == 2), tsize=24)
    if k >= 3:
        rbox(d, (110, 305, 1170, 440), 'acc', hi=(k == 3))
        text_c(d, (640, 337), 'LangGraph  ·  an agent as a graph of steps', font(28, True), C['acc'])
        for i, t in enumerate(['model', 'tools', 'model', '...']):
            box(d, 195 + i * 250, 370, 190, 50, t, '', 'box', tsize=22)
            if i < 3:
                arrow(d, [(387 + i * 250, 395), (443 + i * 250, 395)], C['ink'], 3, head=9)
    if k >= 4:
        text_l(d, (110, 480), 'chapter 11:  engine built piece by piece', font(24, True), C['muted'])
        text_l(d, (110, 520), 'LangGraph:  a factory engine', font(24, True), C['acc'])
    if k >= 5:
        rbox(d, (640, 462, 1190, 545), 'warn', hi=True)
        text_c(d, (915, 503), 'same car:  agents · tools · guardrails', font(23, True), C['warn'])
    return img, d


# ---------- scene 3 · the picture ----------
B3 = ['Here is the picture.',
      'The command line chooses the engine, with the engine flag.',
      'Native is our own loop.',
      'LangGraph uses createAgent.',
      'Both share the agents, the tools, the input guardrail, and the tracer.',
      'And the LangGraph path goes through an adapter that wraps our tools.']


def s3(k):
    img, d = cv()
    if k >= 1:
        box(d, 450, 70, 380, 70, 'CLI  ·  agent', '--engine native | langgraph', 'box', hi=(k <= 2), tsize=26, ssize=18)
    if k >= 2:
        arrow(d, [(520, 142), (520, 165), (330, 165), (330, 188)], C['ink'], 4, head=11)
        arrow(d, [(760, 142), (760, 165), (950, 165), (950, 188)], C['ink'], 4, head=11)
    if k >= 3:
        box(d, 60, 190, 540, 110, 'native  (default)', 'runAgent · src/agent/runner.js', 'acc', hi=(k == 3), tsize=26, ssize=18)
    if k >= 4:
        box(d, 680, 190, 540, 110, 'langgraph', 'runAgentLangGraph · agent/langgraph/', 'blue', hi=(k == 4), tsize=26, ssize=18)
    if k >= 6:
        box(d, 740, 335, 420, 56, 'toLangChainTools()', 'tool() + Zod', 'box', hi=(k == 6), tsize=22, ssize=16)
        arrow(d, [(950, 302), (950, 332)], C['ink'], 3, head=9)
    if k >= 5:
        rbox(d, (60, 430, 1220, 560), 'warn', hi=(k == 5))
        text_c(d, (640, 466), 'Shared by both engines', font(27, True), C['warn'])
        text_c(d, (640, 506), 'agents  ·  tools (createTools + pickTools)  ·  checkInput', font(23))
        text_c(d, (640, 538), 'Tracer  (in langgraph, fed by a LangChain callback)', font(21), C['muted'])
        arrow(d, [(330, 302), (330, 428)], C['ink'], 3, head=9)
        arrow(d, [(950, 393 if k >= 6 else 302), (950, 428)], C['ink'], 3, head=9)
    return img, d


# ---------- scene 4 · piece 1: the tools ----------
B4 = ['First piece: adapting the tools.',
      'LangChain has its own tool format. Instead of rewriting the tools, the project wraps the existing ones.',
      'The real logic stays in run.',
      'The wrapper only hands over the name, the description, and the schema, in the format LangChain expects.',
      'And it keeps the same behavior: an error becomes a result, and the loop does not break.']
ADAPT = ['export const toLangChainTools = (tools) =>', '  tools.map((t) =>', '    tool(', '      async (args) => {', '        try {',
         '          return String(await t.run(args));', '        } catch (e) {', '          return `Erro: ${e.message}`;', '        }',
         '      },', '      { name: t.name, description: t.description, schema: z.object(t.schema) },', '    ),', '  );']


def s4(k):
    img, d = cv()
    bands = {2: [(1, 12, BAND_TEAL)], 3: [(5, 5, BAND_AMBER)], 4: [(10, 10, BAND_BLUE)], 5: [(6, 8, BAND_TEAL)]}.get(k, [])
    ys = code_panel(d, 'src/agent/langgraph/tools.js', ADAPT, bands, size=20, line_h=31, y0=205)
    notes = {3: (5, '←  our logic, untouched'), 4: (10, ''), 5: (7, '←  an error becomes a result')}
    if k == 3:
        text_l(d, (760, ys[5]), '←  our logic, untouched', font(21, True), NOTE)
    if k == 5:
        text_l(d, (700, ys[7]), '←  an error becomes a result', font(21, True), NOTE)
    if k == 4:
        text_c(d, (640, 540), 'name  ·  description  ·  schema:  handed over in LangChain\'s format', font(24, True), NOTE)
    return img, d


# ---------- scene 5 · piece 2: the model ----------
B5 = ['Second piece: choosing the model.',
      'The same rule as client.js: Gemini first, then Claude.',
      'But now it returns LangChain objects.',
      'ChatGoogleGenerativeAI and ChatAnthropic have the same interface, so the rest of the code does not know which one it is using.',
      'And the Gemini adapter we wrote by hand, which translates formats, is not needed here.']
MODEL = ['export function createChatModel() {', '  const provider = llmProvider();', "  if (provider === 'gemini') {",
         '    return new ChatGoogleGenerativeAI({ model: config.gemini.model, /* ... */ });', '  }',
         "  if (provider === 'anthropic') {",
         '    return new ChatAnthropic({ model: config.llm.model, maxTokens: config.llm.maxTokens });', '  }',
         "  throw new Error('O agente precisa de GEMINI_API_KEY (ou ANTHROPIC_API_KEY).');", '}']


def s5(k):
    img, d = cv()
    bands = {2: [(1, 2, BAND_TEAL), (5, 5, BAND_TEAL)], 3: [(3, 3, BAND_BLUE), (6, 6, BAND_BLUE)], 4: [(3, 3, BAND_AMBER), (6, 6, BAND_AMBER)]}.get(k, [])
    code_panel(d, 'src/agent/langgraph/model.js  (condensed)', MODEL, bands, size=19, line_h=31, y0=205)
    if k >= 4:
        text_c(d, (640, 535), 'same interface  →  the rest of the code does not know which one it uses', font(25, True), WARN_L)
    if k >= 5:
        text_c(d, (640, 575), 'gemini.js (the hand-made adapter) is not needed here', font(23, True), NOTE)
    return img, d


# ---------- scene 6 · piece 3: the agent ----------
B6 = ['Third piece: the agent itself.',
      'Compare with chapter 11. The for loop, with about twenty lines, disappeared.',
      'createAgent builds the graph: model, tools, model, and so on, with the model, our wrapped tools, and the agent instructions.',
      'The middleware line is where hooks plug in, which is the topic of a later chapter.',
      'The step limit is called recursion limit, and counts steps of the graph. Each step of our own runner equals about two graph steps, so we use max steps times two, plus one.',
      'And a small listener, the TracerHandler, feeds the same tracer as before.']
AG = ['const graph = createAgent({', '  model: model ?? createChatModel(),', '  tools: toLangChainTools(tools),',
      '  systemPrompt: agent.system,', '  middleware: hooks ?? createDefaultHooks({ audit }),', '});', '',
      'const run = (limit) =>', '  graph.invoke(', "    { messages: [{ role: 'user', content: input.clean }] },",
      '    { recursionLimit: limit, callbacks: [new TracerHandler(tracer)] },', '  );', '',
      'const { messages } = await run(agent.maxSteps * 2 + 1);']


def s6(k):
    img, d = cv()
    bands = {3: [(0, 5, BAND_TEAL)], 4: [(4, 4, BAND_AMBER)], 5: [(10, 10, BAND_BLUE), (13, 13, BAND_BLUE)], 6: [(10, 10, BAND_TEAL)]}.get(k, [])
    ys = code_panel(d, 'src/agent/langgraph/runner.js  (excerpt)', AG, bands, size=19, line_h=28, y0=200)
    if k == 2:
        text_c(d, (640, 300), 'chapter 11:  a for loop of about 20 lines', font(31, True), WARN_L)
        text_c(d, (640, 355), '→   createAgent', font(38, True), NOTE)
    if k == 3:
        text_l(d, (780, ys[2]), '←  the graph: model → tools → model', font(20, True), NOTE)
    if k == 4:
        text_l(d, (780, ys[4]), '←  hooks plug in here', font(21, True), WARN_L)
    if k == 5:
        text_l(d, (700, ys[13]), '←  max steps × 2 + 1', font(21, True), NOTE)
    if k == 6:
        text_l(d, (940, ys[10]), '←  feeds the Tracer', font(20, True), NOTE)
    return img, d


# ---------- scene 7 · real comparison ----------
B7 = ['Now, a real comparison.',
      'The same scenario: the VPN is down, with the triage agent, and a scripted model.',
      'Both engines produce the same answer, in two steps, and create the same ticket.',
      'The differences are small: the trace name says which engine ran, and the LangGraph engine also returns the audit from the hooks.']
NAT = ['answer:  Chamado aberto.', 'steps:   2', 'ticket:  TCK-1001', '', '[trace:agent:triage]', '  • llm#1', '  • tool:create_ticket', '  • llm#2', '', 'audit:   (none)']
LGR = ['answer:  Chamado aberto.', 'steps:   2', 'ticket:  TCK-1001', '', '[trace:langgraph:triage]', '  • llm#1', '  • tool:create_ticket', '  • llm#2', '', 'audit:   create_ticket → ok']


def s7(k):
    img, d = cv()
    text_c(d, (640, 70), 'A real comparison', font(44, True))
    if k >= 2:
        rbox(d, (330, 105, 950, 150), 'warn')
        text_c(d, (640, 128), 'scenario:  "A VPN caiu para todos"  (triage agent)', font(22, True, True), C['warn'])
    if k >= 3:
        for x, title, lines, st in [(40, 'native', NAT, 'acc'), (660, 'langgraph', LGR, 'blue')]:
            d.rounded_rectangle((x, 170, x + 580, 600), 18, fill=C['code_bg'])
            text_l(d, (x + 25, 195), title, font(24, True, True), NOTE if st == 'acc' else (150, 190, 255))
            for i, ln in enumerate(lines):
                diff = (k >= 4 and i in (4, 9))
                if diff:
                    d.rectangle((x + 12, 232 + i * 36 - 17, x + 568, 232 + i * 36 + 17), fill=BAND_AMBER)
                text_l(d, (x + 25, 232 + i * 36), ln, font(22, False, True), C['code_ink'])
    if k >= 4:
        text_c(d, (640, 615), 'highlighted:  the only differences', font(18, True), WARN_L)
    return img, d


# ---------- scene 8 · the comparison table ----------
B8 = ['Piece by piece, here is what each engine uses.',
      'The loop: a for in our runner, or a graph built by createAgent.',
      'The model: our complete function, or the LangChain chat models.',
      'The tools: our objects, or the same objects wrapped.',
      'The step limit: max steps, or recursion limit.',
      'The tests: a fake function, or the fake model of LangChain.',
      'And hooks only exist in the LangGraph engine.']
TABLE = [('loop', 'a for loop · runner.js', 'a graph built by createAgent'), ('model', 'complete()  (client.js)', 'ChatGoogleGenerativeAI · ChatAnthropic'),
         ('tools', '{ name, description, schema, run }', 'the same, wrapped by tool()'),
         ('step limit', 'maxSteps', 'recursionLimit = maxSteps × 2 + 1'), ('tests', 'a fake llm function', 'fakeModel() from LangChain'),
         ('hooks', 'none', 'middleware')]


def s8(k):
    img, d = cv()
    text_c(d, (640, 70), 'Engine by engine', font(46, True))
    if k >= 1:
        for x, t, col in [(60, '', C['muted']), (310, 'native', C['acc']), (790, 'langgraph', C['blue'])]:
            text_l(d, (x, 135), t, font(26, True), col)
        d.line((50, 155, 1230, 155), fill=C['line'], width=2)
    for i, (c, a, b) in enumerate(TABLE):
        if k >= i + 2:
            y = 185 + i * 66
            hi = (k == i + 2)
            rbox(d, (40, y, 1240, y + 54), 'acc' if hi else 'box', r=10)
            text_l(d, (60, y + 27), c, font(24, True), C['muted'])
            text_l(d, (310, y + 27), a, font(22, False, True))
            text_l(d, (790, y + 27), b, font(20, False, True), C['blue'])
    return img, d


# ---------- scene 9 · honest limit ----------
B9 = ['An honest limit.',
      'The LangGraph engine was tested only with a fake model.',
      'It has not run against a real API yet.',
      'So the real Gemini and Claude paths, and the real token counts in the trace, still need to be checked with a key.']


def s9(k):
    img, d = cv()
    text_c(d, (640, 85), 'An honest limit', font(50, True), C['warn'])
    if k >= 2:
        rbox(d, (60, 150, 1220, 270), 'acc', hi=(k == 2))
        text_l(d, (90, 190), 'Verified:', font(30, True), C['acc'])
        text_l(d, (90, 238), 'the agent loop, tools, guardrails and hooks, with a fake model (fakeModel)', font(24))
    if k >= 3:
        rbox(d, (60, 295, 1220, 415), 'warn', hi=(k == 3))
        text_l(d, (90, 335), 'Not verified:', font(30, True), C['warn'])
        text_l(d, (90, 383), 'a run against a real API', font(24))
    if k >= 4:
        rbox(d, (60, 440, 1220, 570), 'box', hi=(k == 4))
        text_l(d, (90, 478), 'To check with a key:', font(28, True))
        text_l(d, (90, 523), 'the real Gemini and Claude paths  ·  the real token counts in the trace', font(23))
    return img, d


# ---------- scene 10 · wrap-up ----------
B10 = ['To sum up: LangGraph runs the same agent as our own runner.',
       'The tools are wrapped, not rewritten.',
       'The model comes from LangChain chat models.',
       'And createAgent replaces the loop.',
       'In the next chapter, we will see how the project is tested.',
       'See you there!']


def s10(k):
    img, d = cv()
    text_c(d, (640, 90), 'See you there!' if k >= 6 else 'Summing up', font(52, True), C['acc'] if k >= 6 else C['ink'])
    rows = [(1, 'acc', '1   The same agent runs on LangGraph'), (2, 'blue', '2   Tools:  wrapped, not rewritten'),
            (3, 'warn', '3   Model:  LangChain chat models  ·  Loop:  createAgent'), (5, 'box', 'Next chapter:  tests and evaluation')]
    pos = {1: 0, 2: 1, 3: 2, 5: 3}
    for kk, st, t in rows:
        if k >= kk:
            y = 160 + pos[kk] * 105
            rbox(d, (130, y, 1150, y + 82), st, hi=(k == kk or (kk == 3 and k == 4)))
            text_l(d, (170, y + 41), t, font(27, True))
    return img, d


SCENES = [(B1, s1), (B2, s2), (B3, s3), (B4, s4), (B5, s5), (B6, s6), (B7, s7), (B8, s8), (B9, s9), (B10, s10)]

if __name__ == '__main__':
    work = os.environ.get('VIDEO_WORKDIR', os.path.join(HERE, '_work', f'cap13_en_{VOICE}'))
    if len(sys.argv) > 1 and sys.argv[1] == 'preview':
        preview(SCENES, os.path.join(work, 'preview'))
        print('preview saved in', os.path.join(work, 'preview'))
    else:
        build(SCENES, os.path.join(HERE, 'saida', f'cap13_en_{VOICE}.mp4'), work, TAG)
