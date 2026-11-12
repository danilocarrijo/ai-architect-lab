"""Chapter 15 · Who calls whom (English, voice: Zira by default).

Usage:   python cap15_en.py preview
         python cap15_en.py                      # saida\\cap15_en_zira.mp4
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
engine.SPEECH = [
    (r'cli\.js', 'C L I dot J S'), (r'\bCLI\b', 'C L I'), (r'ask\.js', 'ask dot J S'), (r'buildIndex', 'build index'),
    (r'loadRetriever', 'load retriever'), (r'createAssistant', 'create assistant'), (r'createTools', 'create tools'),
    (r'runAgent', 'run agent'), (r'checkInput', 'check input'), (r'checkOutput', 'check output'), (r'sanitizeContext', 'sanitize context'),
    (r'search_policies', 'search policies'), (r'HybridRetriever', 'Hybrid Retriever'), (r'\bMCP\b', 'M C P'),
    (r'\bAPI\b', 'A P I'), (r'\bLLM\b', 'L L M'), (r'\bnpm\b', 'N P M'), (r'LangGraph', 'Lang Graph'),
]
TAG = 'Chapter 15 · Who calls whom'
NOTE = (130, 225, 215)
WARN_L = (255, 200, 120)


def cv():
    return canvas(TAG)


def chain(d, y, items, k0, k, x0=40, w=215, gap=36, h=84, styles=None, tsize=21):
    """Horizontal chain of boxes; item i appears when k >= k0 + i; the item of the current beat is highlighted."""
    for i, (t, sub) in enumerate(items):
        if k >= k0 + i:
            x = x0 + i * (w + gap)
            box(d, x, y, w, h, t, sub, (styles[i] if styles else 'box'), hi=(k == k0 + i), tsize=tsize, ssize=15)
            if i < len(items) - 1 and k >= k0 + i + 1:
                arrow(d, [(x + w + 3, y + h // 2), (x + w + gap - 3, y + h // 2)], C['ink'], 3, head=9)


# ---------- 1 opening ----------
B1 = ['Hello!',
      'Until now, we studied each piece alone.',
      'In this chapter, we put everything together, and answer one question: who calls whom, and when?',
      'We will follow the real code, file by file, in three flows.']


def s1(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 195), 'Who calls whom?', font(72, True))
    if k >= 3:
        text_c(d, (640, 285), 'the whole system, following the real code', font(34), C['acc'])
    if k >= 4:
        for i, (t, st) in enumerate([('1  Ingest', 'acc'), ('2  Ask', 'blue'), ('3  Agent', 'warn')]):
            box(d, 130 + i * 360, 390, 300, 90, t, '', st, hi=True, tsize=32)
    return img, d


# ---------- 2 entry point ----------
B2 = ['Everything starts in one file: cli.js.',
      'It reads the first word of the command, and chooses the path.',
      'The word ingest builds the index.',
      'The word agent runs an agent.',
      'Anything else is a question for the assistant.']
CLI = ["const [cmd, ...rest] = process.argv.slice(2);", '', "if (cmd === 'ingest') {", '  await buildIndex({ log: console.log });',
       "} else if (cmd === 'agent') {", '  const { retriever } = await loadRetriever();', '  const r = await run(getAgent(name), rest.join(\' \'), { retriever });',
       '} else {', '  const { ask } = await createAssistant();', '  print(await ask(q));', '}']


def s2(k):
    img, d = cv()
    bands = {2: [(0, 1, BAND_AMBER)], 3: [(2, 3, BAND_TEAL)], 4: [(4, 6, BAND_BLUE)], 5: [(7, 9, BAND_AMBER)]}.get(k, [])
    ys = code_panel(d, 'src/cli.js  (condensed)', CLI, bands, size=19, line_h=31, y0=205)
    if k == 3:
        text_l(d, (700, ys[3]), '←  flow 1: ingest', font(21, True), NOTE)
    if k == 4:
        text_l(d, (800, ys[5]), '←  flow 3: agent', font(21, True), (150, 190, 255))
    if k == 5:
        text_l(d, (700, ys[8]), '←  flow 2: ask', font(21, True), WARN_L)
    return img, d


# ---------- 3 flow 1 ingest ----------
B3 = ['Flow one: ingest. It runs before any question.',
      'The function buildIndex loads the documents, cuts each one into chunks, and turns each chunk into a vector.',
      'Then it stores everything in the vector store, and saves the index to a file.',
      'Real result: four documents become sixteen chunks.',
      'Later, loadRetriever reads this file, builds the keyword index, and assembles the hybrid retriever.']
ING = [('loadDocuments', 'loader.js'), ('chunkDocument', 'chunker.js'), ('embedder.embed', 'embeddings.js'), ('store.add + save', 'vectorstore.js')]


def s3(k):
    img, d = cv()
    text_c(d, (640, 70), 'Flow 1 · ingest', font(46, True))
    if k >= 1:
        box(d, 440, 120, 400, 66, 'buildIndex()', 'src/rag/index.js', 'acc', hi=(k == 1), tsize=27, ssize=17)
    if k >= 2:
        chain(d, 230, ING, 2, k, x0=40, w=265, gap=40, h=92, styles=['box'] * 4, tsize=21)
        arrow(d, [(640, 188), (640, 212), (172, 212), (172, 228)], C['muted'], 2, head=8)
    if k >= 3:
        rbox(d, (240, 370, 1040, 440), 'acc', hi=(k == 4))
        text_c(d, (640, 405), '4 documents  →  16 chunks', font(32, True), C['acc'])
    if k >= 5:
        rbox(d, (60, 470, 1220, 590), 'blue', hi=True)
        text_c(d, (640, 505), 'later:  loadRetriever()', font(26, True), C['blue'])
        text_c(d, (640, 548), 'reads the file  →  builds BM25  →  HybridRetriever({ store, bm25, embedder })', font(21, False, True))
    return img, d


# ---------- 4 flow 2 ask ----------
B4 = ['Flow two: ask. This is the main path of a question.',
      'First, the input guardrail checks the question. If it is unsafe, the flow stops here.',
      'Second, the semantic cache is consulted. If there is a match, we return right away.',
      'Third, the retriever fetches the best chunks.',
      'Fourth, the model writes the answer from those chunks, if a key exists. Without a key, the project returns the best chunk.',
      'Fifth, the output guardrail checks the citations. And only a grounded answer is saved in the cache.']
ASK = ['const input = checkInput(question);', 'if (!input.ok) return { ..., blocked: true };', '',
       'const cached = await tracer.span(\'cache\', () => cache.get(...));', 'if (cached) return { ...cached, cached: true };', '',
       'const hits = await tracer.span(\'retrieve\', () => retriever.retrieve(...));', '',
       'answer = hasLLM() ? await complete({ system, messages }) : extractive(hits);', '',
       'const out = checkOutput(answer, hits.length);', 'if (out.grounded) await cache.set(input.clean, result);']


def s4(k):
    img, d = cv()
    bands = {2: [(0, 1, BAND_AMBER)], 3: [(3, 4, BAND_BLUE)], 4: [(6, 6, BAND_TEAL)], 5: [(8, 8, BAND_BLUE)], 6: [(10, 11, BAND_AMBER)]}.get(k, [])
    ys = code_panel(d, 'src/llm/ask.js  ·  ask()  (condensed)', ASK, bands, size=18, line_h=31, y0=205)
    marks = {2: (0, '1'), 3: (3, '2'), 4: (6, '3'), 5: (8, '4'), 6: (10, '5')}
    if k in marks:
        i, n = marks[k]
        d.ellipse((1100, ys[i] - 16, 1140, ys[i] + 16), fill=C['acc'])
        text_c(d, (1120, ys[i]), n, font(22, True), (255, 255, 255))
    return img, d


# ---------- 5 ask real trace ----------
B5 = ['Here is the same flow, running for real, in offline mode.',
      'The question: how many vacation days do I have?',
      'The answer is the best chunk, with the citation number one.',
      'The four sources come from the vacation document, ranked by score.',
      'And the trace shows the two steps that ran: the cache, then the retrieval.',
      'There is no model step, because there is no key. With a key, an L L M step would appear here.']
OUT = ['Todo colaborador CLT tem direito a 30 dias de férias', 'após 12 meses de trabalho (período aquisitivo). ... [1]', '',
       '[1] ferias.md > Direito a férias (0.292)', '[2] ferias.md > Como solicitar (0.278)', '[3] ferias.md > Abono pecuniário (0.258)',
       '[4] ferias.md > Pagamento (0.255)', '', '[trace:ask]', '  • cache      1 ms', '  • retrieve   2 ms']


def s5(k):
    img, d = cv()
    text_c(d, (640, 62), 'Flow 2, running for real', font(40, True))
    if k >= 2:
        rbox(d, (200, 98, 1080, 142), 'warn')
        text_c(d, (640, 120), 'Quantos dias de férias eu tenho?', font(22, True, True), C['warn'])
    if k >= 3:
        d.rounded_rectangle((60, 160, 1220, 600), 18, fill=C['code_bg'])
        for i, ln in enumerate(OUT[:2]):
            text_l(d, (85, 190 + i * 32), ln, font(20, False, True), C['code_ink'])
    if k >= 4:
        for i, ln in enumerate(OUT[3:7]):
            y = 290 + i * 32
            if k == 4:
                d.rectangle((72, y - 16, 1208, y + 16), fill=BAND_TEAL)
            text_l(d, (85, y), ln, font(20, False, True), (150, 235, 180))
    if k >= 5:
        for i, ln in enumerate(OUT[8:]):
            y = 450 + i * 32
            if k == 5 and i > 0:
                d.rectangle((72, y - 16, 1208, y + 16), fill=BAND_BLUE)
            text_l(d, (85, y), ln, font(20, False, True), C['code_ink'])
    if k >= 6:
        text_l(d, (400, 546), '←  no "llm" step: no API key', font(20, True), WARN_L)
    return img, d


# ---------- 6 flow 3 agent ----------
B6 = ['Flow three: the agent. The difference is who decides.',
      'In the ask flow, our code always runs the same order. In the agent flow, the model decides.',
      'The runner checks the input, then repeats: call the model, and if it asks for a tool, run the tool and give the result back.',
      'When the model answers with text, the loop ends.',
      'The step limit stops a model that never finishes.']
AGL = ['checkInput(question)', 'for (step = 1; step <= agent.maxSteps; step++) {', '  const res = await llm({ system, messages, tools });',
       "  if (res.stop_reason !== 'tool_use') return { answer, steps: step };", '  const tool = tools.find((t) => t.name === b.name);',
       '  content = await tool.run(b.input);', '  messages.push({ role: \'user\', content: results });', '}',
       "return { answer: 'Limite de passos atingido...' };"]


def s6(k):
    img, d = cv()
    bands = {3: [(0, 0, BAND_AMBER), (1, 2, BAND_BLUE), (4, 6, BAND_TEAL)], 4: [(3, 3, BAND_AMBER)], 5: [(1, 1, BAND_BLUE), (8, 8, BAND_BLUE)]}.get(k, [])
    ys = code_panel(d, 'src/agent/runner.js  ·  runAgent()  (condensed)', AGL, bands, size=18, line_h=31, y0=205)
    if k == 2:
        text_c(d, (640, 520), 'ask:  fixed order in our code        agent:  the model decides', font(25, True), NOTE)
    return img, d


# ---------- 7 who passes retriever ----------
B7 = ['Now, the question from before: how does the tool know the retriever?',
      'It is created once, in loadRetriever.',
      'The command line receives it, and passes it to the runner.',
      'The runner passes it to createTools, which builds each tool.',
      'And search policies keeps it, because it was built inside a function that received the retriever.',
      'This is a closure. Nobody imports a global; each piece receives what it needs.']
RJ = [('loadRetriever()', 'creates it', 'acc'), ('cli.js', 'passes it on', 'box'), ('runAgent()', 'passes it on', 'box'),
      ('createTools()', 'builds the tools', 'blue'), ('search_policies', 'keeps it (closure)', 'warn')]


def s7(k):
    img, d = cv()
    text_c(d, (640, 62), 'The journey of the retriever', font(42, True))
    for i, (t, sub, st) in enumerate(RJ):
        if k >= i + 2:
            x = 40 + i * 248
            box(d, x, 150, 215, 100, t, sub, st, hi=(k == i + 2), tsize=21, ssize=16)
            if i > 0:
                arrow(d, [(x - 30, 200), (x - 4, 200)], C['ink'], 3, head=9)
    if k >= 5:
        rbox(d, (40, 300, 1240, 440), 'warn')
        text_l(d, (70, 335), 'export const createSearchPoliciesTool = ({ retriever }) => ({', font(22, False, True))
        text_l(d, (70, 372), '  async run({ query, dept }) {', font(22, False, True))
        text_l(d, (70, 409), '    const hits = await retriever.retrieve(query, ...);', font(22, False, True), C['warn'])
    if k >= 6:
        text_c(d, (640, 500), 'closure:  an inner function remembers what the outer one received', font(26, True), NOTE)
        text_c(d, (640, 545), 'no globals · each piece receives what it needs · easy to fake in tests', font(22), C['muted'])
    return img, d


# ---------- 8 the map ----------
B8 = ['Let us see everything on a single map.',
      'On the left, the three entry points. The command line, the M C P server, and the tests.',
      'In the middle, the two paths: the assistant and the agent.',
      'Both use the retriever and the guardrails.',
      'And the M C P server reuses the same tools as the agent.',
      'But note: M C P calls skip the agent guardrails and hooks, since only the tools are exposed.']


def s8(k):
    img, d = cv()
    text_c(d, (640, 62), 'The map', font(44, True))
    if k >= 2:
        box(d, 40, 130, 230, 80, 'tests', 'fake model + fake retriever', 'box', hi=(k == 2), tsize=24, ssize=14)
        box(d, 40, 270, 230, 80, 'cli.js', 'ingest · ask · agent', 'box', hi=(k == 2), tsize=24, ssize=16)
        box(d, 40, 410, 230, 80, 'mcp/server.js', 'stdio', 'box', hi=(k == 2), tsize=22, ssize=16)
    if k >= 3:
        box(d, 400, 130, 270, 90, 'ask()', 'assistant', 'blue', hi=(k == 3), tsize=26, ssize=17)
        box(d, 400, 410, 270, 90, 'runAgent()', 'agent', 'warn', hi=(k == 3), tsize=26, ssize=17)
        arrow(d, [(272, 170), (398, 170)], C['ink'], 3, head=9)
        arrow(d, [(272, 310), (335, 310), (335, 175), (398, 175)], C['ink'], 3, head=9)
        arrow(d, [(335, 310), (335, 450), (398, 450)], C['ink'], 3, head=9)
    if k >= 4:
        box(d, 800, 130, 420, 90, 'retriever + guardrails', 'shared', 'acc', hi=(k == 4), tsize=25, ssize=17)
        arrow(d, [(672, 175), (798, 175)], C['ink'], 3, head=9)
        arrow(d, [(672, 440), (760, 440), (760, 200), (798, 200)], C['ink'], 3, head=9)
    if k >= 5:
        box(d, 800, 410, 420, 90, 'tools', 'search · ticket · cep', 'box', hi=(k == 5), tsize=25, ssize=17)
        arrow(d, [(672, 455), (798, 455)], C['ink'], 3, head=9)
        arrow(d, [(272, 480), (300, 480), (300, 524), (900, 524), (900, 502)], C['ink'], 3, head=9)
        arrow(d, [(1010, 408), (1010, 224)], C['muted'], 2, head=8)
    if k >= 6:
        rbox(d, (300, 548, 980, 606), 'warn', hi=True)
        text_c(d, (640, 577), 'M C P calls skip the agent guardrails and hooks'.replace('M C P', 'MCP'), font(24, True), C['warn'])
    return img, d


# ---------- 9 wrap-up ----------
B9 = ['To sum up: three flows, one entry point.',
      'Ingest prepares the index. Ask runs a fixed order. The agent lets the model decide.',
      'The retriever is created once, and passed down piece by piece.',
      'In the next chapter, we will see how to run everything, command by command.',
      'See you there!']


def s9(k):
    img, d = cv()
    text_c(d, (640, 90), 'See you there!' if k >= 5 else 'Summing up', font(52, True), C['acc'] if k >= 5 else C['ink'])
    rows = [(1, 'acc', '1   Three flows, one entry point:  cli.js'), (2, 'blue', '2   Ingest prepares  ·  ask is fixed  ·  agent decides'),
            (3, 'warn', '3   The retriever is created once and passed down'), (4, 'box', 'Next chapter:  running everything')]
    for i, (kk, st, t) in enumerate(rows):
        if k >= kk:
            y = 160 + i * 105
            rbox(d, (130, y, 1150, y + 82), st, hi=(k == kk))
            text_l(d, (170, y + 41), t, font(27, True))
    return img, d


SCENES = [(B1, s1), (B2, s2), (B3, s3), (B4, s4), (B5, s5), (B6, s6), (B7, s7), (B8, s8), (B9, s9)]

if __name__ == '__main__':
    work = os.environ.get('VIDEO_WORKDIR', os.path.join(HERE, '_work', f'cap15_en_{VOICE}'))
    if len(sys.argv) > 1 and sys.argv[1] == 'preview':
        preview(SCENES, os.path.join(work, 'preview'))
        print('preview saved in', os.path.join(work, 'preview'))
    else:
        build(SCENES, os.path.join(HERE, 'saida', f'cap15_en_{VOICE}.mp4'), work, TAG)
