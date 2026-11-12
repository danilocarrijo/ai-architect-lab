"""Chapter 9 · The semantic cache (English, voice: Zira by default).

Usage:   python cap09_en.py preview
         python cap09_en.py                      # saida\\cap09_en_zira.mp4
         set VOICE=david && python cap09_en.py   # male voice
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
engine.SPEECH = [(r'\bnpm\b', 'N P M')]   # spoken-only fixes (the subtitles keep the original text)
TAG = 'Chapter 9 · The semantic cache'
NOTE = (130, 225, 215)
WARN_L = (255, 200, 120)
Q = 'Quantos dias de férias eu tenho?'


def cv():
    return canvas(TAG)


# ---------- scene 1 · opening ----------
B1 = ['Hello!',
      'In the previous chapter, we saw the three guardrails.',
      'Now, a piece that saves time and money: the semantic cache.',
      'You will see how it works, and a real demonstration.']


def s1(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 200), 'Semantic cache', font(76, True))
    if k >= 3:
        text_c(d, (640, 282), "don't pay twice for the same question", font(36), C['acc'])
    if k >= 2:
        box(d, 150, 355, 400, 90, 'Chapter 8', 'the guardrails', 'box', hi=(k == 2), tsize=27, ssize=20)
    if k >= 3:
        arrow(d, [(565, 400), (715, 400)], C['ink'], 5)
        box(d, 730, 355, 400, 90, 'Chapter 9', 'the cache', 'blue', hi=(k == 3), tsize=27, ssize=20)
    if k >= 4:
        text_c(d, (640, 540), 'How it works   ·   A real demonstration', font(32, True), C['muted'])
    return img, d


# ---------- scene 2 · the attendant analogy ----------
B2 = ['Imagine an attendant who answered a question ten minutes ago.',
      'If someone asks a very similar question, he reuses the answer, instead of going back to the library.',
      'That saves time, and money, because it avoids another call to the language model.']


def s2(k):
    img, d = cv()
    text_c(d, (640, 85), 'The attendant who remembers', font(46, True))
    if k >= 1:
        box(d, 60, 190, 280, 100, 'Question #1', '10 minutes ago', 'box', hi=(k == 1), tsize=26, ssize=20)
        arrow(d, [(345, 240), (425, 240)], C['ink'], 4)
        box(d, 430, 190, 330, 100, 'full answer', 'saved by the attendant', 'blue', tsize=26, ssize=20)
    if k >= 2:
        box(d, 60, 370, 280, 100, 'Question #2', 'very similar', 'warn', hi=(k == 2), tsize=26, ssize=20)
        arrow(d, [(345, 420), (425, 420)], C['ink'], 4)
        box(d, 430, 370, 330, 100, 'seen it?  yes', 'reuse the saved answer', 'acc', hi=(k == 2), tsize=26, ssize=20)
        arrow(d, [(595, 368), (595, 294)], C['blue'], 4, dash=True)
        text_c(d, (1010, 350), 'no trip to the library', font(28, True), C['acc'])
        text_c(d, (1010, 395), '(no search)', font(24), C['muted'])
    if k >= 3:
        rbox(d, (800, 180, 1230, 300), 'acc', hi=True)
        text_c(d, (1015, 215), 'saves time', font(32, True), C['acc'])
        text_c(d, (1015, 262), 'and money', font(32, True), C['acc'])
        text_c(d, (640, 560), 'no extra call to the language model', font(32, True), C['blue'])
    return img, d


# ---------- scene 3 · the cache in code ----------
B3 = ['Here is the cache, in code.',
      'The get method turns the question into a vector.',
      'Then it looks for a saved entry that is in the same scope, still fresh, and similar enough.',
      'If it finds one, it returns the saved answer. Otherwise, nothing.',
      'The set method saves the question vector, the answer, the scope, and the time.']
CACHE = ["async get(question, scope = '') {", '  const [v] = await this.embedder.embed([question]);', '  const now = Date.now();',
         '  const hit = this.entries.find((e) =>',
         '    e.scope === scope && now - e.at < this.ttlMs && cosine(v, e.vector) >= this.threshold);',
         '  return hit?.value ?? null;', '}', "async set(question, value, scope = '') {",
         '  const [vector] = await this.embedder.embed([question]);',
         '  this.entries.push({ vector, value, scope, at: Date.now() });', '}']


def s3(k):
    img, d = cv()
    bands = {2: [(1, 1, BAND_TEAL)], 3: [(3, 4, BAND_BLUE)], 4: [(5, 5, BAND_AMBER)], 5: [(7, 10, BAND_TEAL)]}.get(k, [])
    code_panel(d, 'src/rag/cache.js  (formatted)', CACHE, bands, size=20, line_h=31, y0=206)
    return img, d


# ---------- scene 4 · three tests ----------
B4 = ['The entry must pass three tests.',
      'Same scope: the cache is kept apart when the department filter is different.',
      'Still fresh: less than 10 minutes old.',
      'And similar enough: a cosine of at least 0.92.',
      'These numbers live in the configuration file.']


def s4(k):
    img, d = cv()
    text_c(d, (640, 85), 'Three tests', font(48, True))
    cards = [(2, 'acc', '1   Same scope', 'different filter (dept)  →  different cache'),
             (3, 'blue', '2   Still fresh', 'less than 10 minutes old'),
             (4, 'warn', '3   Similar enough', 'cosine  ≥  0.92')]
    for i, (kk, st, t, sub) in enumerate(cards):
        if k >= kk:
            y = 140 + i * 120
            rbox(d, (110, y, 1170, y + 98), st, hi=(k == kk))
            text_l(d, (150, y + 32), t, font(32, True))
            text_l(d, (150, y + 70), sub, font(24), C['muted'])
    if k >= 5:
        d.rounded_rectangle((90, 505, 1190, 595), 18, fill=C['code_bg'])
        text_l(d, (115, 528), 'src/config.js', font(20, False, True), (150, 170, 185))
        f, x0, y = font(28, False, True), 115, 566
        txt = 'cache: { threshold: 0.92, ttlMs: 10 * 60 * 1000 },'
        for sub, col in [('threshold: 0.92', BAND_BLUE), ('ttlMs: 10 * 60 * 1000', BAND_AMBER)]:
            i = txt.index(sub)
            xa = x0 + d.textlength(txt[:i], font=f)
            d.rectangle((xa - 5, y - 20, xa + d.textlength(sub, font=f) + 5, y + 20), fill=col)
        d.text((x0, y), txt, font=f, fill=C['code_ink'], anchor='lm')
    return img, d


# ---------- scene 5 · what gets cached ----------
B5 = ['Which answers go into the cache?',
      'Only the ones with a valid citation.',
      'This is a single line in the ask function.',
      'A doubtful answer, if it were saved, would be repeated for everyone, for ten minutes.']


def s5(k):
    img, d = cv()
    text_c(d, (640, 85), 'What goes into the cache?', font(46, True))
    if k >= 2:
        rbox(d, (60, 150, 620, 330), 'acc', hi=(k == 2))
        text_c(d, (340, 195), 'grounded:  true', font(32, True, True), C['acc'])
        text_c(d, (340, 255), 'valid citation', font(26))
        text_c(d, (340, 295), '→  saved', font(30, True), C['acc'])
        rbox(d, (660, 150, 1220, 330), 'warn')
        text_c(d, (940, 195), 'grounded:  false', font(32, True, True), C['warn'])
        text_c(d, (940, 255), 'no valid citation', font(26))
        text_c(d, (940, 295), '→  not saved', font(30, True), C['warn'])
    if k >= 3:
        d.rounded_rectangle((90, 370, 1190, 450), 18, fill=C['code_bg'])
        f = font(25, False, True)
        txt = 'if (out.grounded) await cache.set(input.clean, result, scope);'
        d.rectangle((105, 392, 105 + d.textlength('if (out.grounded)', font=f) + 8, 428), fill=BAND_TEAL)
        d.text((115, 410), txt, font=f, fill=C['code_ink'], anchor='lm')
        text_l(d, (115, 465), 'src/llm/ask.js:53', font(20, False, True), C['muted'])
    if k >= 4:
        rbox(d, (150, 505, 1130, 590), 'warn', hi=True)
        text_c(d, (640, 548), 'a doubtful answer would be repeated for everyone, for 10 minutes', font(27, True), C['warn'])
    return img, d


# ---------- scene 6 · real demo A ----------
B6 = ['Now, a real demonstration.',
      'We ask the same question twice.',
      'The first time, the full process runs: the cache looks, finds nothing, and the search runs.',
      'The second time, the cache already has the answer, and the search does not even run.',
      'No search, no model, no cost.']


def s6(k):
    img, d = cv()
    text_c(d, (640, 80), 'Real demonstration', font(46, True))
    if k >= 2:
        rbox(d, (240, 120, 1040, 175), 'warn')
        text_c(d, (640, 148), f'ask("{Q}")  ×  2', font(26, True, True), C['warn'])
    if k >= 3:
        rbox(d, (60, 205, 620, 520), 'box', hi=(k == 3))
        text_c(d, (340, 240), '1st call', font(30, True))
        text_c(d, (340, 278), 'cached = undefined', font(22, False, True), C['muted'])
        for i, (n, ms, st) in enumerate([('cache', 1, 'blue'), ('retrieve', 2, 'acc')]):
            y = 335 + i * 62
            text_l(d, (95, y), n, font(25, True, True))
            d.rectangle((255, y - 16, 255 + ms * 130, y + 16), fill=C['blue'] if st == 'blue' else C['acc'])
            text_l(d, (255 + ms * 130 + 14, y), f'{ms} ms', font(23, True, True), C['muted'])
        text_c(d, (340, 485), 'full process', font(24, True), C['muted'])
    if k >= 4:
        rbox(d, (660, 205, 1220, 520), 'acc', hi=(k == 4))
        text_c(d, (940, 240), '2nd call', font(30, True), C['acc'])
        text_c(d, (940, 278), 'cached = true', font(22, False, True), C['acc'])
        text_l(d, (695, 335), 'cache', font(25, True, True))
        d.rectangle((855, 319, 858, 351), fill=C['blue'])
        text_l(d, (873, 335), '0 ms', font(23, True, True), C['muted'])
        text_l(d, (695, 397), 'retrieve', font(25, True, True), C['line'])
        text_l(d, (855, 397), 'did not run', font(22, True), C['acc'])
        text_c(d, (940, 485), 'only the cache step', font(24, True), C['acc'])
    if k >= 5:
        text_c(d, (640, 560), 'no search  ·  no model  ·  no cost', font(34, True), C['acc'])
        text_c(d, (640, 600), '(offline here, so the times are tiny: with a real model, the skipped step is a slow, paid call)', font(18), C['muted'])
    return img, d


# ---------- scene 7 · real demo B ----------
B7 = ['But what counts as similar?',
      'We compare the saved question with four others, using the local embedder.',
      'The same question, without the accent and the question mark, scores 1.000: a hit.',
      'A question about taking vacation scores 0.672: below the threshold, a miss.',
      'Questions about reimbursement score near zero: a miss.',
      'An honest limit: the local embedder only matches near-identical text. A neural one would also match real paraphrases.']
ROWS7 = [('Quantos dias de ferias eu tenho', 1.000), ('Quantos dias de ferias posso tirar?', 0.672),
         ('Qual o limite de reembolso para refeicoes?', 0.015), ('Como pedir reembolso de viagem?', 0.000)]


def s7(k):
    img, d = cv()
    text_c(d, (640, 70), 'What counts as similar?', font(44, True))
    if k >= 1:
        text_l(d, (60, 125), 'saved:', font(22, True), C['muted'])
        text_l(d, (150, 125), Q, font(26, True, True), C['warn'])
    if k >= 2:
        # escala 0..1 com o limiar 0.92
        x0, x1, y = 120, 1160, 205
        d.rectangle((x0, y - 5, x1, y + 5), fill=C['line'])
        thr = x0 + (x1 - x0) * 0.92
        d.rectangle((thr - 2, y - 24, thr + 2, y + 24), fill=C['warn'])
        text_c(d, (thr, y - 42), 'threshold 0.92', font(20, True), C['warn'])
        text_l(d, (x0 - 10, y + 40), '0', font(20, True), C['muted'])
        text_l(d, (x1 - 5, y + 40), '1', font(20, True), C['muted'])
        for i, (t, val) in enumerate(ROWS7):
            ry = 285 + i * 68
            rbox(d, (60, ry, 1220, ry + 54), 'box', r=10)
            text_l(d, (80, ry + 27), t, font(22, False, True))
            if k >= (3, 4, 5, 5)[i]:
                hit = val >= 0.92
                d.ellipse((x0 + (x1 - x0) * val - 9, y - 9, x0 + (x1 - x0) * val + 9, y + 9), fill=C['acc'] if hit else C['warn'])
                d.text((850, ry + 27), f'{val:.3f}', font=font(26, True, True), fill=C['ink'], anchor='lm')
                rbox(d, (980, ry + 6, 1200, ry + 48), 'acc' if hit else 'warn', r=10)
                text_c(d, (1090, ry + 27), 'HIT' if hit else 'miss', font(24, True), C['acc'] if hit else C['warn'])
    if k >= 6:
        text_c(d, (640, 590), 'local embedder: near-identical text only   ·   a neural one also finds paraphrases', font(22, True), C['blue'])
    return img, d


# ---------- scene 8 · cautions ----------
B8 = ['Three cautions.',
      'The threshold is a balance: too high, and the cache almost never hits; too low, and it answers the wrong question.',
      'If you re-index the documents, the cache must be cleared, or it returns old answers.',
      'And the cache lives only in memory: it disappears when the program ends.']


def s8(k):
    img, d = cv()
    text_c(d, (640, 85), 'Three cautions', font(50, True), C['warn'])
    if k >= 2:
        rbox(d, (60, 150, 1220, 270), 'warn', hi=(k == 2))
        text_l(d, (90, 188), '1   The threshold is a balance', font(30, True), C['warn'])
        text_l(d, (90, 237), 'too high: almost never hits     ·     too low: answers the wrong question', font(24))
    if k >= 3:
        rbox(d, (60, 295, 1220, 415), 'blue', hi=(k == 3))
        text_l(d, (90, 333), '2   Re-indexed the documents?  Clear the cache', font(30, True), C['blue'])
        text_l(d, (90, 382), 'otherwise it returns old answers', font(24))
    if k >= 4:
        rbox(d, (60, 440, 1220, 560), 'box', hi=(k == 4))
        text_l(d, (90, 478), '3   It lives only in memory', font(30, True))
        text_l(d, (90, 527), 'when the program ends, the cache disappears', font(24))
    return img, d


# ---------- scene 9 · wrap-up ----------
B9 = ['To sum up: the semantic cache reuses answers to similar questions.',
      'It checks scope, freshness, and similarity.',
      'Only answers with a valid citation are saved.',
      'In the next chapter, we will see the tracer, which measures time, tokens, and cost.',
      'See you there!']


def s9(k):
    img, d = cv()
    text_c(d, (640, 95), 'See you there!' if k >= 5 else 'Summing up', font(54, True), C['acc'] if k >= 5 else C['ink'])
    rows = [(1, 'acc', '1   Reuses the answer to a similar question'), (2, 'blue', '2   Checks scope · freshness · similarity (≥ 0.92)'),
            (3, 'warn', '3   Saves only answers with a valid citation'), (4, 'box', 'Next chapter:  the tracer (time, tokens, cost)')]
    for i, (kk, st, t) in enumerate(rows):
        if k >= kk:
            y = 165 + i * 105
            rbox(d, (130, y, 1150, y + 82), st, hi=(k == kk))
            text_l(d, (170, y + 41), t, font(28, True))
    return img, d


SCENES = [(B1, s1), (B2, s2), (B3, s3), (B4, s4), (B5, s5), (B6, s6), (B7, s7), (B8, s8), (B9, s9)]

if __name__ == '__main__':
    work = os.environ.get('VIDEO_WORKDIR', os.path.join(HERE, '_work', f'cap09_en_{VOICE}'))
    if len(sys.argv) > 1 and sys.argv[1] == 'preview':
        preview(SCENES, os.path.join(work, 'preview'))
        print('preview saved in', os.path.join(work, 'preview'))
    else:
        build(SCENES, os.path.join(HERE, 'saida', f'cap09_en_{VOICE}.mp4'), work, TAG)
