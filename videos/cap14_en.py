"""Chapter 14 · Tests and evaluation (English, voice: Zira by default).

Usage:   python cap14_en.py preview
         python cap14_en.py                      # saida\\cap14_en_zira.mp4
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
    (r'fakeModel', 'fake model'), (r'hit@k', 'hit at k'), (r'hit@4', 'hit at 4'), (r'\bMRR\b', 'M R R'), (r'maxSteps', 'max steps'),
    (r'LangChain', 'Lang Chain'), (r'LangGraph', 'Lang Graph'), (r'\bAPI\b', 'A P I'), (r'\bnpm\b', 'N P M'),
    (r'node --test', 'node dash dash test'), (r'\bLLM\b', 'L L M'),
]
TAG = 'Chapter 14 · Tests and evaluation'
NOTE = (130, 225, 215)
WARN_L = (255, 200, 120)


def cv():
    return canvas(TAG)


# ---------- 1 opening ----------
B1 = ['Hello!',
      'In the last chapter, we saw a second engine for the agent.',
      'Now: how do we know that everything works, and keeps working after each change?',
      'There are two answers: tests, and evaluation.']


def s1(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 200), 'Tests and evaluation', font(70, True))
    if k >= 3:
        text_c(d, (640, 285), 'how do we know it works?', font(36), C['acc'])
    if k >= 4:
        box(d, 150, 390, 420, 100, 'Tests', 'does the code do what it should?', 'acc', hi=True, tsize=30, ssize=19)
        box(d, 710, 390, 420, 100, 'Evaluation', 'is the answer good?', 'blue', hi=True, tsize=30, ssize=19)
    return img, d


# ---------- 2 why it is hard ----------
B2 = ['Why is this hard with AI?',
      'A language model answers differently each time, costs money, and needs an internet connection.',
      'A test that calls a real model would be slow, expensive, and flaky.',
      'So the trick is: test everything around the model, with fake pieces, and measure the retrieval separately.']


def s2(k):
    img, d = cv()
    text_c(d, (640, 80), 'Why is it hard with AI?', font(46, True))
    if k >= 2:
        for i, (t, st) in enumerate([('different each time', 'warn'), ('costs money', 'warn'), ('needs internet', 'warn')]):
            box(d, 70 + i * 395, 150, 360, 80, t, '', st, hi=(k == 2), tsize=26)
    if k >= 3:
        rbox(d, (200, 280, 1080, 360), 'warn', hi=(k == 3))
        text_c(d, (640, 320), 'a real model in a test  =  slow · expensive · flaky', font(28, True), C['warn'])
    if k >= 4:
        box(d, 70, 410, 560, 120, 'Tests', 'fake pieces around the model', 'acc', hi=True, tsize=30, ssize=21)
        box(d, 650, 410, 560, 120, 'Evaluation', 'measure the retrieval on its own', 'blue', hi=True, tsize=30, ssize=21)
    return img, d


# ---------- 3 node test ----------
B3 = ['The tests use the test runner that comes with Node, so there is nothing extra to install.',
      'The command is npm test, which runs node dash dash test.',
      'Real result of the project: twenty six tests, all passing, in about seven seconds.',
      'Seven files, each one for a part of the system.']
FILES = [('agent', 4, 'agent loop and registry'), ('cep', 4, 'external API tool'), ('gemini', 4, 'format adapter'), ('guardrails', 4, 'input and output checks'),
         ('hooks', 5, 'middleware hooks'), ('langgraph', 3, 'second engine'), ('rag', 2, 'retrieval')]


def s3(k):
    img, d = cv()
    text_c(d, (640, 80), 'npm test', font(50, True, True))
    text_c(d, (640, 130), 'the test runner built into Node', font(24), C['muted'])
    if k >= 3:
        rbox(d, (60, 165, 1220, 250), 'acc', hi=(k == 3))
        text_c(d, (640, 207), 'tests 26   ·   pass 26   ·   fail 0   ·   ~7 s', font(34, True, True), C['acc'])
    if k >= 4:
        for i, (f, n, desc) in enumerate(FILES):
            col, row = i % 2, i // 2
            x = 60 + col * 580
            y = 285 + row * 80
            rbox(d, (x, y, x + 560, y + 66), 'box', r=10)
            text_l(d, (x + 20, y + 33), f'{f}.test.js', font(21, True, True))
            text_l(d, (x + 255, y + 33), f'{n} tests', font(21, True), C['blue'])
            text_l(d, (x + 360, y + 33), desc, font(17), C['muted'])
    return img, d


# ---------- 4 fake model ----------
B4 = ['How do we test an agent without a real model? With a fake one.',
      'In the native engine, the model is just a function, so the test passes a function that follows a script.',
      'First call: ask for a tool. Second call: give the final text.',
      'In the LangGraph engine, LangChain itself offers a fake model, with the same idea.',
      'The agent, the tools, the guardrails, and the loop run for real. Only the model is fake.']
FM = ['const model = fakeModel()', '  .respondWithTools([{', "    name: 'create_ticket',", "    args: { title: 'VPN', priority: 'alta' },",
      '  }])', "  .respond(new AIMessage('Chamado aberto.'));", '', "const r = await runAgentLangGraph(getAgent('triage'),",
      "  'A VPN caiu para todos', { model, tools });", '', "assert.equal(r.answer, 'Chamado aberto.');", 'assert.equal(r.steps, 2);']


def s4(k):
    img, d = cv()
    bands = {3: [(1, 4, BAND_TEAL), (5, 5, BAND_BLUE)], 4: [(0, 5, BAND_AMBER)], 5: [(7, 11, BAND_TEAL)]}.get(k, [])
    ys = code_panel(d, 'test/langgraph.test.js  (excerpt)', FM, bands, size=20, line_h=30, y0=205)
    if k == 2:
        text_c(d, (640, 590), 'native:  the model is a function  →  the test passes a scripted one', font(24, True), NOTE)
    if k == 3:
        text_l(d, (700, ys[1]), '←  1st call: asks for a tool', font(20, True), NOTE)
        text_l(d, (700, ys[5]), '←  2nd call: final text', font(20, True), NOTE)
    if k == 4:
        text_l(d, (700, ys[0]), "←  LangChain's fake model", font(20, True), WARN_L)
    if k == 5:
        text_c(d, (640, 590), 'real:  agent · tools · guardrails · loop        fake:  the model only', font(22, True), NOTE)
    return img, d


# ---------- 5 what tests check ----------
B5 = ['What do these tests check?',
      'That the loop runs the tool and returns the final answer, in two steps.',
      'That the step limit stops an agent stuck in a loop.',
      'That an injection attempt is blocked before reaching the model.',
      "That a tool outside the agent's list is refused, and that a tool error becomes a result, not a crash.",
      'And that the external API tool does not call the network in tests: the fetch function is injected.']
CHK = [('acc', 'loop runs the tool, then answers', '2 steps'), ('blue', 'step limit stops a stuck agent', 'maxSteps'),
       ('warn', 'injection blocked before the model', 'steps = 0'), ('acc', 'tool outside the list is refused', 'error → result'),
       ('blue', 'external API: no real network in tests', 'fetchImpl injected')]


def s5(k):
    img, d = cv()
    text_c(d, (640, 70), 'What the tests check', font(46, True))
    for i, (st, t, tag) in enumerate(CHK):
        if k >= i + 2:
            y = 130 + i * 90
            rbox(d, (80, y, 1200, y + 74), st, hi=(k == i + 2))
            text_l(d, (110, y + 37), t, font(26, True))
            text_l(d, (800, y + 37), tag, font(22, False, True), C['muted'])
    return img, d


# ---------- 6 evaluation concept ----------
B6 = ['Tests tell us if the code works. They do not tell us if the search finds the right document.',
      'For that, there is the evaluation, with a golden set.',
      'A golden set is a list of questions, each with the document that must appear in the results.',
      'The project has eleven questions, across four documents.']
GOLD = [('Quantos dias de férias eu tenho direito?', 'ferias'), ('Posso trabalhar de outro país?', 'home-office'),
        ('Qual o limite de reembolso para refeições?', 'reembolso'), ('Como configuro a VPN?', 'ti-suporte'), ('...  (11 in total)', '')]


def s6(k):
    img, d = cv()
    text_c(d, (640, 70), 'The golden set', font(46, True))
    if k >= 1:
        text_c(d, (640, 135), 'tests: does the code work?    evaluation: does the search find the right thing?', font(23), C['muted'])
    if k >= 3:
        text_l(d, (110, 190), 'question', font(24, True), C['blue'])
        text_l(d, (870, 190), 'must find', font(24, True), C['acc'])
        d.line((90, 218, 1190, 218), fill=C['line'], width=2)
        for i, (q, doc) in enumerate(GOLD):
            y = 240 + i * 62
            rbox(d, (90, y, 1190, y + 52), 'box', r=10)
            text_l(d, (110, y + 26), q, font(22, False, True))
            text_l(d, (870, y + 26), doc, font(22, True, True), C['acc'])
    if k >= 4:
        text_c(d, (640, 590), 'src/eval/golden.js  ·  11 questions  ·  4 documents', font(22, True), NOTE)
    return img, d


# ---------- 7 metrics ----------
B7 = ['Two numbers summarize the evaluation.',
      'Hit at k: in what share of the questions did the right document appear in the top k results? Here k is four.',
      'M R R, the mean reciprocal rank, rewards a better position: first place counts one, second place counts one half, third counts one third.',
      'The script also fails with an exit code if hit at k falls below eighty percent, so it can guard a pipeline.']


def s7(k):
    img, d = cv()
    text_c(d, (640, 70), 'Two numbers', font(46, True))
    if k >= 2:
        rbox(d, (60, 130, 620, 400), 'acc', hi=(k == 2))
        text_c(d, (340, 175), 'hit@k', font(40, True, True), C['acc'])
        text_c(d, (340, 240), 'did the right document', font(23))
        text_c(d, (340, 272), 'appear in the top k?', font(23))
        text_c(d, (340, 345), 'here  k = 4', font(26, True, True), C['muted'])
    if k >= 3:
        rbox(d, (660, 130, 1220, 400), 'blue', hi=(k == 3))
        text_c(d, (940, 175), 'MRR', font(40, True, True), C['blue'])
        text_c(d, (940, 235), 'rewards a better position', font(23))
        text_c(d, (940, 300), '1st → 1     2nd → 1/2     3rd → 1/3', font(25, True, True))
    if k >= 4:
        rbox(d, (160, 440, 1120, 540), 'warn', hi=(k == 4))
        text_c(d, (640, 475), 'hit@k below 80%  →  exit code 1', font(30, True), C['warn'])
        text_c(d, (640, 513), 'ready to guard a pipeline', font(21), C['muted'])
    return img, d


# ---------- 8 real result ----------
B8 = ['Now, the real result.',
      'The command is npm run eval.',
      'All eleven questions found the right document in first place.',
      'So hit at four is one hundred percent, and M R R is one.',
      'An honest note: this is a small set with a small knowledge base, so a perfect score here does not prove the system is perfect.',
      'The value is the guard: if a future change breaks the search, this number drops.']
EV = ['OK  rank=1  Quantos dias de férias eu tenho direito?', 'OK  rank=1  Posso vender dias de férias?', 'OK  rank=1  Com quanto tempo de antecedência peço férias?',
      'OK  rank=1  Quantos dias por semana posso trabalhar de casa?', 'OK  rank=1  Existe auxílio para internet no home office?',
      'OK  rank=1  Posso trabalhar de outro país?', 'OK  rank=1  Qual o prazo para pedir reembolso de despesas?',
      'OK  rank=1  Qual o limite de reembolso para refeições?', 'OK  rank=1  Como resetar minha senha?', 'OK  rank=1  Como configuro a VPN?',
      'OK  rank=1  Qual o SLA de um chamado de TI?']


def s8(k):
    img, d = cv()
    text_c(d, (640, 62), 'npm run eval', font(42, True, True))
    if k >= 3:
        d.rounded_rectangle((60, 105, 1220, 520), 18, fill=C['code_bg'])
        for i, ln in enumerate(EV):
            text_l(d, (85, 128 + i * 33), ln, font(19, False, True), (150, 235, 180))
    if k >= 4:
        rbox(d, (260, 535, 1020, 595), 'acc', hi=(k == 4))
        text_c(d, (640, 565), 'hit@4: 100%     MRR: 1.00', font(32, True, True), C['acc'])
    return img, d


# ---------- 9 limits ----------
B9 = ['Two honest limits.',
      'First, the evaluation measures only the retrieval, not the quality of the final answer written by the model.',
      'Second, the model is never tested for real: the tests use fake models, so a real key is still needed to check the full path.',
      'A next step could be an automated judge for answers, but that is outside this project.']


def s9(k):
    img, d = cv()
    text_c(d, (640, 85), 'Honest limits', font(50, True), C['warn'])
    if k >= 2:
        rbox(d, (60, 150, 1220, 290), 'warn', hi=(k == 2))
        text_l(d, (90, 195), 'Evaluation = retrieval only', font(30, True), C['warn'])
        text_l(d, (90, 248), "the quality of the model's written answer is not measured", font(23))
    if k >= 3:
        rbox(d, (60, 315, 1220, 455), 'warn', hi=(k == 3))
        text_l(d, (90, 360), 'Tests use fake models', font(30, True), C['warn'])
        text_l(d, (90, 413), 'the full path with a real key still needs to be checked', font(23))
    if k >= 4:
        rbox(d, (60, 480, 1220, 560), 'box', hi=(k == 4))
        text_l(d, (90, 520), 'Next step (out of scope):  an automated judge for answers', font(25, True))
    return img, d


# ---------- 10 wrap-up ----------
B10 = ['To sum up: npm test checks the code, with fake models.',
       'npm run eval checks the search, with a golden set, hit at k, and M R R.',
       'Both are guards that warn us when a change breaks something.',
       'In the next chapter, we will see who calls whom, in the whole system.',
       'See you there!']


def s10(k):
    img, d = cv()
    text_c(d, (640, 90), 'See you there!' if k >= 5 else 'Summing up', font(52, True), C['acc'] if k >= 5 else C['ink'])
    rows = [(1, 'acc', '1   npm test:  the code, with fake models'), (2, 'blue', '2   npm run eval:  the search, with a golden set'),
            (3, 'warn', '3   Both warn us when a change breaks something'), (4, 'box', 'Next chapter:  who calls whom')]
    for i, (kk, st, t) in enumerate(rows):
        if k >= kk:
            y = 160 + i * 105
            rbox(d, (130, y, 1150, y + 82), st, hi=(k == kk))
            text_l(d, (170, y + 41), t, font(27, True))
    return img, d


SCENES = [(B1, s1), (B2, s2), (B3, s3), (B4, s4), (B5, s5), (B6, s6), (B7, s7), (B8, s8), (B9, s9), (B10, s10)]

if __name__ == '__main__':
    work = os.environ.get('VIDEO_WORKDIR', os.path.join(HERE, '_work', f'cap14_en_{VOICE}'))
    if len(sys.argv) > 1 and sys.argv[1] == 'preview':
        preview(SCENES, os.path.join(work, 'preview'))
        print('preview saved in', os.path.join(work, 'preview'))
    else:
        build(SCENES, os.path.join(HERE, 'saida', f'cap14_en_{VOICE}.mp4'), work, TAG)
