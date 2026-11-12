"""Chapter 10 · The tracer: time, tokens and cost (English, voice: Zira by default).

Usage:   python cap10_en.py preview
         python cap10_en.py                      # saida\\cap10_en_zira.mp4
         set VOICE=david && python cap10_en.py   # male voice
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
    (r'FinOps', 'Fin Ops'), (r'LangSmith', 'Lang Smith'), (r'Langfuse', 'Lang fuse'), (r'OpenTelemetry', 'Open Telemetry'),
    (r'LangGraph', 'Lang Graph'), (r'addUsage', 'add usage'), (r'costUSD', 'cost U S D'), (r'\bllm\b', 'L L M'),
    (r'\bnpm\b', 'N P M'),
]
TAG = 'Chapter 10 · The tracer: time, tokens and cost'
NOTE = (130, 225, 215)
WARN_L = (255, 200, 120)


def cv():
    return canvas(TAG)


# ---------- scene 1 · opening ----------
B1 = ['Hello!',
      'In the previous chapter, we saw the semantic cache.',
      'Now, the last piece of observability: the tracer.',
      'It measures the time of each step, the tokens, and the cost.']


def s1(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 200), 'The tracer', font(76, True))
    if k >= 4:
        text_c(d, (640, 282), 'time  ·  tokens  ·  cost', font(38), C['acc'])
    if k >= 2:
        box(d, 150, 355, 400, 90, 'Chapter 9', 'the cache', 'box', hi=(k == 2), tsize=27, ssize=20)
    if k >= 3:
        arrow(d, [(565, 400), (715, 400)], C['ink'], 5)
        box(d, 730, 355, 400, 90, 'Chapter 10', 'the tracer', 'acc', hi=(k == 3), tsize=27, ssize=20)
    if k >= 4:
        text_c(d, (640, 540), 'observability of every run', font(32, True), C['muted'])
    return img, d


# ---------- scene 2 · why measure ----------
B2 = ['Think of the stopwatch and the odometer of a car.',
      'Without them, you only find out that the system is slow or expensive when someone complains.',
      'Calls to language models cost money per token, so measuring is part of the architecture.',
      'This is sometimes called FinOps for AI.']


def s2(k):
    img, d = cv()
    text_c(d, (640, 85), 'Why measure?', font(50, True))
    if k >= 1:
        for i, (t, sub, st) in enumerate([('stopwatch', 'how long each step takes', 'blue'), ('odometer', 'how many tokens were used', 'acc')]):
            x = 90 + i * 560
            rbox(d, (x, 150, x + 500, 330), st, hi=(k == 1))
            text_c(d, (x + 250, 215), t, font(40, True), C['blue'] if st == 'blue' else C['acc'])
            text_c(d, (x + 250, 275), sub, font(26))
    if k >= 2:
        rbox(d, (150, 370, 1130, 450), 'warn', hi=(k == 2))
        text_c(d, (640, 410), 'no measuring  →  you find out when someone complains', font(30, True), C['warn'])
    if k >= 3:
        rbox(d, (150, 475, 1130, 555), 'box', hi=(k == 3))
        text_c(d, (640, 515), 'language models charge per token  →  money', font(30, True))
    if k >= 4:
        text_c(d, (640, 595), 'FinOps for AI', font(36, True), C['acc'])
    return img, d


# ---------- scene 3 · the span ----------
B3 = ['The tracer records each step as a span: a timed step.',
      'The span method receives a name and a function.',
      'It marks the start time, runs the function, and returns its result.',
      'The finally block always runs, even if there is an error: it writes down the name and the duration, in milliseconds.']
SPAN = ['async span(name, fn, attrs = {}) {', '  const t0 = performance.now();', '  try {', '    return await fn();',
        '  } finally {', '    this.spans.push({ name, ms: Math.round(performance.now() - t0), ...attrs });', '  }', '}']


def s3(k):
    img, d = cv()
    bands = {2: [(0, 0, BAND_TEAL)], 3: [(1, 3, BAND_BLUE)], 4: [(4, 6, BAND_AMBER)]}.get(k, [])
    ys = code_panel(d, 'src/observability/trace.js  (span)', SPAN, bands, size=20)
    notes = {2: (0, '←  a name + the step to run'), 3: (3, '←  runs the step')}
    if k in notes:
        i, t = notes[k]
        text_l(d, (700, ys[i]), t, font(22, True), NOTE)
    if k == 4:
        text_c(d, (640, 510), 'always runs, even on error:   name  +  duration (ms)', font(28, True), WARN_L)
    return img, d


# ---------- scene 4 · using spans in ask() ----------
B4 = ['In the ask function, the use is simple.',
      'You wrap the step in a span.',
      'For example, the search: the span runs it, and also records how long it took.',
      'The same goes for the cache.']
USE = ["const cached = await tracer.span('cache', () => cache.get(input.clean, scope));",
       "const hits = await tracer.span('retrieve', () => retriever.retrieve(input.clean, { filter }));"]


def s4(k):
    img, d = cv()
    text_c(d, (640, 85), 'Using it in ask()', font(48, True))
    if k >= 1:
        d.rounded_rectangle((60, 140, 1220, 260), 18, fill=C['code_bg'])
        f = font(21, False, True)
        # a linha do cache fica em cima, a da busca embaixo
        d.text((85, 178), USE[0], font=f, fill=C['code_ink'], anchor='lm')
        d.text((85, 228), USE[1], font=f, fill=C['code_ink'], anchor='lm')
        if k == 3:
            xa = 85 + f.getlength(USE[1][:USE[1].index('tracer.span')])
            d.rectangle((xa - 4, 211, xa + f.getlength("tracer.span('retrieve',") + 4, 245), fill=BAND_AMBER)
            d.text((85, 228), USE[1], font=f, fill=C['code_ink'], anchor='lm')
        if k == 4:
            xa = 85 + f.getlength(USE[0][:USE[0].index('tracer.span')])
            d.rectangle((xa - 4, 161, xa + f.getlength("tracer.span('cache',") + 4, 195), fill=BAND_TEAL)
            d.text((85, 178), USE[0], font=f, fill=C['code_ink'], anchor='lm')
        text_l(d, (60, 280), 'src/llm/ask.js:32  and  :35', font(20, False, True), C['muted'])
    if k >= 2:
        rbox(d, (180, 330, 1100, 540), 'blue', hi=(k == 2))
        text_c(d, (640, 365), 'span', font(30, True), C['blue'])
        box(d, 280, 400, 720, 100, 'the step', 'runs normally  ·  the span times it', 'acc', tsize=28, ssize=20)
    if k >= 3:
        text_c(d, (640, 575), 'retrieve:  measured', font(30, True), C['acc'])
    if k >= 4:
        text_c(d, (640, 575), 'retrieve  ·  cache:  both measured', font(30, True), C['acc'])
    return img, d


# ---------- scene 5 · tokens and cost ----------
B5 = ['Now, the tokens and the cost.',
      'The addUsage method adds the tokens reported by the model: input and output.',
      'The cost is a calculation: input tokens times the input price, plus output tokens times the output price, divided by one million.',
      'The prices are in the configuration file, and they are illustrative.',
      'An example: 1200 input tokens and 300 output tokens cost 0.0081 dollars.']
COST = ['addUsage(u = {}) {', '  this.usage.input += u.input_tokens ?? 0;', '  this.usage.output += u.output_tokens ?? 0;', '}',
        'get costUSD() {', '  const { inPerM, outPerM } = config.pricing;',
        '  return (this.usage.input * inPerM + this.usage.output * outPerM) / 1e6;', '}']


def s5(k):
    img, d = cv()
    bands = {2: [(1, 2, BAND_TEAL)], 3: [(5, 6, BAND_BLUE)]}.get(k, [])
    code_panel(d, 'src/observability/trace.js', COST, bands, size=20, line_h=30, y0=205)
    if k >= 4:
        text_l(d, (125, 470), 'src/config.js:   pricing: { inPerM: 3, outPerM: 15 },', font(22, False, True), WARN_L)
        text_l(d, (125, 500), '(USD per million tokens, illustrative)', font(18), (150, 170, 185))
    if k >= 5:
        text_c(d, (640, 560), '1200 × 3  +  300 × 15  =  8100   ÷   1,000,000   =   US$ 0.0081', font(27, True, True), NOTE)
    return img, d


# ---------- scene 6 · real reports ----------
B6 = ['Here are two real reports.',
      'The first comes from a small test with made-up tokens: one step, 1200 tokens in, 300 out, and the calculated cost.',
      'The second is a real question, offline: the cache step and the search step, and zero tokens, because there is no model.',
      'With an API key, an llm line would also appear, with the time of the call and the tokens spent.']
REP1 = ['[trace:demo]', '  • etapa-a             21 ms', '  tokens in/out: 1200/300 · custo ≈ US$ 0.00810']
REP2 = ['[trace:ask]', '  • cache                0 ms', '  • retrieve             1 ms', '  tokens in/out: 0/0 · custo ≈ US$ 0.00000']


def s6(k):
    img, d = cv()
    text_c(d, (640, 80), 'Two real reports', font(46, True))
    if k >= 2:
        d.rounded_rectangle((40, 130, 1240, 275), 18, fill=C['code_bg'])
        text_l(d, (65, 150), 'test with made-up tokens', font(19, False, True), (150, 170, 185))
        for i, ln in enumerate(REP1):
            text_l(d, (65, 190 + i * 32), ln, font(24, False, True), NOTE if i == 2 else C['code_ink'])
    if k >= 3:
        d.rounded_rectangle((40, 300, 1240, 475), 18, fill=C['code_bg'])
        text_l(d, (65, 320), 'a real question, offline', font(19, False, True), (150, 170, 185))
        for i, ln in enumerate(REP2):
            text_l(d, (65, 360 + i * 32), ln, font(24, False, True), NOTE if i == 3 else C['code_ink'])
    if k >= 4:
        rbox(d, (150, 500, 1130, 595), 'acc', hi=True)
        text_c(d, (640, 535), 'with an API key:  an  llm  line appears', font(30, True), C['acc'])
        text_c(d, (640, 572), '(time of the call + tokens spent)', font(22), C['muted'])
    return img, d


# ---------- scene 7 · notes ----------
B7 = ['A few notes.',
      'The prices are illustrative, only to demonstrate the idea.',
      'In production, this kind of record goes to tools like LangSmith, Langfuse, or OpenTelemetry.',
      'And in the LangGraph engine, a callback feeds this same tracer, so the report looks the same.']


def s7(k):
    img, d = cv()
    text_c(d, (640, 85), 'A few notes', font(50, True))
    if k >= 2:
        rbox(d, (60, 150, 1220, 270), 'warn', hi=(k == 2))
        text_l(d, (90, 190), '1   The prices are illustrative', font(30, True), C['warn'])
        text_l(d, (90, 238), 'only to demonstrate the idea:  set your provider\'s real prices in config.js', font(23))
    if k >= 3:
        rbox(d, (60, 295, 1220, 415), 'blue', hi=(k == 3))
        text_l(d, (90, 335), '2   In production, send it to a dedicated tool', font(30, True), C['blue'])
        text_l(d, (90, 383), 'LangSmith  ·  Langfuse  ·  OpenTelemetry', font(24, True, True))
    if k >= 4:
        rbox(d, (60, 440, 1220, 560), 'acc', hi=(k == 4))
        text_l(d, (90, 480), '3   The LangGraph engine feeds the same tracer', font(30, True), C['acc'])
        text_l(d, (90, 528), 'a callback (TracerHandler)  →  the report looks the same', font(23))
    return img, d


# ---------- scene 8 · wrap-up ----------
B8 = ['To sum up: the tracer measures time, tokens, and cost of every run.',
      'A span times a step, and addUsage counts the tokens.',
      'The cost is a simple calculation, with prices from the configuration.',
      'In the next chapter, we will see agents: where the model decides what to do.',
      'See you there!']


def s8(k):
    img, d = cv()
    text_c(d, (640, 95), 'See you there!' if k >= 5 else 'Summing up', font(54, True), C['acc'] if k >= 5 else C['ink'])
    rows = [(1, 'acc', '1   Tracer:  time · tokens · cost of every run'), (2, 'blue', '2   span() times a step  ·  addUsage() counts tokens'),
            (3, 'warn', '3   Cost = tokens × price (from the configuration)'), (4, 'box', 'Next chapter:  agents, the model decides what to do')]
    for i, (kk, st, t) in enumerate(rows):
        if k >= kk:
            y = 165 + i * 105
            rbox(d, (130, y, 1150, y + 82), st, hi=(k == kk))
            text_l(d, (170, y + 41), t, font(28, True))
    return img, d


SCENES = [(B1, s1), (B2, s2), (B3, s3), (B4, s4), (B5, s5), (B6, s6), (B7, s7), (B8, s8)]

if __name__ == '__main__':
    work = os.environ.get('VIDEO_WORKDIR', os.path.join(HERE, '_work', f'cap10_en_{VOICE}'))
    if len(sys.argv) > 1 and sys.argv[1] == 'preview':
        preview(SCENES, os.path.join(work, 'preview'))
        print('preview saved in', os.path.join(work, 'preview'))
    else:
        build(SCENES, os.path.join(HERE, 'saida', f'cap10_en_{VOICE}.mp4'), work, TAG)
