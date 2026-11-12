"""Chapter 6 (part 2) · Hybrid search: the fusion and the final score (English, voice: Zira by default).

Usage:   python cap06b_en.py preview
         python cap06b_en.py                      # saida\\cap06b_en_zira.mp4
         set VOICE=david && python cap06b_en.py   # male voice
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
    (r'BM25', 'B M 25'), (r'\bRRF\b', 'R R F'), (r'6\.089', 'six point zero eight nine'), (r'1/(\d+)', r'1 over \1'),
    (r'\bnpm\b', 'N P M'),
]
TAG = 'Chapter 6 · Hybrid search, part 2: the fusion and the final score'
NOTE = (130, 225, 215)
Q = 'Quantos dias de férias eu tenho?'    # the real question used in the project's tests


def cv():
    return canvas(TAG)


# ---------- scene 1 · opening ----------
B1 = ['Hello!',
      'In the previous video, we met the two jurors of the hybrid search.',
      'Each one hands in a ranking.',
      'Now, we will see how the rankings are merged, how the final score is computed, and what the search finally returns.']


def s1(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 200), 'Hybrid search', font(76, True))
    if k >= 2:
        text_c(d, (640, 282), 'part 2:  the fusion and the final score', font(36), C['acc'])
    if k >= 2:
        box(d, 150, 355, 400, 90, 'Part 1', 'the two jurors', 'box', hi=(k == 2), tsize=27, ssize=20)
    if k >= 3:
        arrow(d, [(565, 400), (715, 400)], C['ink'], 5)
        box(d, 730, 355, 400, 90, 'Part 2', 'merging the rankings', 'acc', hi=(k == 3), tsize=27, ssize=20)
    if k >= 4:
        text_c(d, (640, 540), 'The merge   ·   The final score   ·   The result', font(32, True), C['muted'])
    return img, d


# ---------- scene 2 · the scale problem ----------
B2 = ['First, a problem.',
      'The two jurors use different scales.',
      'The cosine goes from zero to one.',
      'BM25 has no fixed limit: it gave 2.9 for this question, and 6.089 in the previous video.',
      'So, comparing the scores directly makes no sense.',
      'The RRF solves this by looking only at the position of each chunk in each ranking.']
VEC = [('ferias#0', '0.432'), ('ferias#1', '0.385'), ('ferias#2', '0.320')]
LEX = [('ferias#0', '2.919'), ('ferias#3', '2.707'), ('ferias#2', '2.682')]


def s2(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 80), 'A scale problem', font(48, True))
    if k >= 2:
        text_c(d, (640, 125), f'real data for:  {Q}', font(22, False, True), C['muted'])
        for x, st, title, rows in [(60, 'blue', 'Vector search  ·  cosine', VEC), (660, 'warn', 'BM25  ·  score', LEX)]:
            rbox(d, (x, 150, x + 560, 450), st, hi=(k == (3 if st == 'blue' else 4)))
            text_c(d, (x + 280, 190), title, font(28, True), C['blue'] if st == 'blue' else C['warn'])
            for i, (cid, val) in enumerate(rows):
                text_l(d, (x + 50, 255 + i * 55), f'{i + 1}   {cid}', font(27, False, True))
                d.text((x + 510, 255 + i * 55), val, font=font(30, True, True), fill=C['ink'], anchor='rm')
    if k >= 3:
        text_c(d, (340, 425), 'always between 0 and 1', font(23, True), C['blue'])
    if k >= 4:
        text_c(d, (940, 425), 'no fixed limit  (6.089 last time)', font(23, True), C['warn'])
    if k == 5:
        rbox(d, (150, 490, 1130, 570), 'warn', hi=True)
        text_c(d, (640, 530), 'comparing the scores directly makes no sense', font(31, True), C['warn'])
    if k >= 6:
        rbox(d, (150, 490, 1130, 570), 'acc', hi=True)
        text_c(d, (640, 530), 'RRF:  use only the position  (1st, 2nd, 3rd ...)', font(31, True), C['acc'])
    return img, d


# ---------- scene 3 · RRF in code ----------
B3 = ['Here is the RRF, in code.',
      'Each chunk gets 1 divided by 60 plus its position, for every ranking it appears in.',
      'And the scores are added up.',
      'A chunk well placed in both lists is added twice.']
RRF = ['export function rrf(lists, k = 60) {', '  const scores = new Map();', '  for (const list of lists)',
       '    list.forEach((r, i) =>', '      scores.set(r.id, (scores.get(r.id) ?? 0) + 1 / (k + i + 1)));',
       '  return [...scores]', '    .map(([id, score]) => ({ id, score }))', '    .sort((a, b) => b.score - a.score);', '}']


def s3(k):
    img, d = cv()
    bands = {2: [(4, 4, BAND_TEAL)], 3: [(4, 4, BAND_AMBER)], 4: [(2, 4, BAND_BLUE)]}.get(k, [])
    ys = code_panel(d, 'src/rag/retriever.js  (rrf, formatted)', RRF, bands, size=22)
    if k == 2:
        text_l(d, (945, ys[4]), '←  1 / (60 + position)', font(20, True), NOTE)
    if k == 3:
        text_l(d, (945, ys[4]), '←  added to what it had', font(20, True), (255, 200, 120))
    if k == 4:
        text_l(d, (910, ys[2]), '←  once per ranking', font(22, True), NOTE)
    return img, d


# ---------- scene 4 · a real example ----------
B4 = ['An example, with real numbers from our question.',
      'The chunk about the right to vacation is first in the vector ranking, and first in BM25.',
      'It gets 1/61 plus 1/61: 0.0328.',
      'The chunk about how to request vacation is second in the vector ranking, and fourth in BM25.',
      'It gets 1/62 plus 1/64: 0.0318.',
      'The first chunk wins, because both jurors put it on top.']


def s4(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 80), 'A real example', font(48, True))
        for x, t in [(60, 'chunk'), (480, 'vector'), (630, 'BM25'), (800, 'calculation'), (1100, 'RRF')]:
            text_l(d, (x, 150), t, font(22, True), C['muted'])
        d.line((60, 172, 1230, 172), fill=C['line'], width=2)
    rows = [('ferias#0  ·  Direito a férias', '1st', '1st', '1/61 + 1/61', '0.0328', 'acc'),
            ('ferias#1  ·  Como solicitar', '2nd', '4th', '1/62 + 1/64', '0.0318', 'box')]
    for i, (c, v, b, calc, sc, st) in enumerate(rows):
        if k >= (2 if i == 0 else 4):
            y = 195 + i * 105
            rbox(d, (45, y, 1245, y + 85), st, hi=(k == (2 if i == 0 else 4) or (k == 6 and i == 0)))
            text_l(d, (65, y + 42), c, font(23, True))
            text_l(d, (480, y + 42), v, font(27, True, True))
            text_l(d, (630, y + 42), b, font(27, True, True))
            if k >= (3 if i == 0 else 5):
                text_l(d, (800, y + 42), calc, font(26, False, True))
                text_l(d, (1100, y + 42), sc, font(32, True, True), C['acc'] if i == 0 else C['ink'])
    if k >= 6:
        W = 900
        for i, (lab, val, col) in enumerate([('ferias#0', 0.0328, C['acc']), ('ferias#1', 0.0318, C['muted'])]):
            y = 430 + i * 60
            text_l(d, (60, y), lab, font(23, True, True))
            d.rectangle((230, y - 16, 230 + W * val / 0.0328, y + 16), fill=col)
            text_l(d, (230 + W * val / 0.0328 + 15, y), f'{val:.4f}', font(24, True, True), col)
        text_c(d, (640, 575), 'both jurors put it on top   →   it wins', font(30, True), C['acc'])
    return img, d


# ---------- scene 5 · rerank and cut ----------
B5 = ['After the RRF, the rerank looks at the question again.',
      'The final score mixes two things.',
      '70 percent is how much of the question\'s words the chunk covers, giving more weight to rare words.',
      '30 percent is the cosine.',
      'Finally, chunks with a score below 0.05 are discarded, and only the first four are kept.']


def s5(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 80), 'Rerank and cut', font(48, True))
    if k >= 2:
        d.rounded_rectangle((90, 130, 1190, 215), 18, fill=C['code_bg'])
        text_c(d, (640, 172), 'score  =  0.7 × coverage  +  0.3 × cosine', font(34, True, True), NOTE)
    if k >= 3:
        d.rectangle((90, 250, 790, 330), fill=C['acc_soft'], outline=C['acc'], width=4)
        text_c(d, (440, 280), '70%  ·  word coverage', font(28, True), C['acc'])
        text_c(d, (440, 313), 'rare words weigh more', font(20), C['muted'])
    if k >= 4:
        d.rectangle((790, 250, 1190, 330), fill=C['blue_soft'], outline=C['blue'], width=4)
        text_c(d, (990, 280), '30%  ·  cosine', font(28, True), C['blue'])
    if k >= 5:
        d.rounded_rectangle((90, 385, 1190, 490), 18, fill=C['code_bg'])
        text_l(d, (115, 410), 'src/config.js', font(20, False, True), (150, 170, 185))
        txt = 'retrieval: { topKCandidates: 12, topK: 4, rrfK: 60, minScore: 0.05 }'
        f, x0, y = font(27, False, True), 115, 458
        for sub, col in [('topK: 4', BAND_BLUE), ('minScore: 0.05', BAND_AMBER)]:
            i = txt.index(sub)
            xa = x0 + d.textlength(txt[:i], font=f)
            d.rectangle((xa - 5, y - 20, xa + d.textlength(sub, font=f) + 5, y + 20), fill=col)
        d.text((x0, y), txt, font=f, fill=C['code_ink'], anchor='lm')
        text_c(d, (640, 560), 'cut:   score ≥ 0.05   ·   at most 4 chunks', font(32, True), C['warn'])
    return img, d


# ---------- scene 6 · the retrieve method ----------
B6 = ['All of this is put together in the retrieve method, the one function the rest of the project calls.',
      'It embeds the question.',
      'It asks the two jurors for 12 candidates each.',
      'It merges them with the RRF.',
      'It reranks, applies the cut, and returns the top four.']
RET = ['async retrieve(query, { filter, k = this.cfg.topK } = {}) {',
       '  const [qv] = await this.embedder.embed([query]);',
       '  const vec = this.store.search(qv, n, allow);    // juror 1',
       '  const lex = this.bm25.search(query, n, allow);  // juror 2',
       '  const candidates = rrf([vec, lex], this.cfg.rrfK);',
       '  return this.rerank(query, candidates)',
       '    .filter((c) => c.score >= this.cfg.minScore)',
       '    .slice(0, k);', '}']


def s6(k):
    img, d = cv()
    bands = {2: [(1, 1, BAND_TEAL)], 3: [(2, 3, BAND_BLUE)], 4: [(4, 4, BAND_TEAL)], 5: [(5, 7, BAND_AMBER)]}.get(k, [])
    ys = code_panel(d, 'src/rag/retriever.js  (retrieve, condensed)', RET, bands, size=22)
    notes = {2: (1, '←  question → vector'), 3: (3, '←  n = 12 each'), 4: (4, '←  merge the two lists'), 5: (6, '←  cut: score ≥ 0.05')}
    if k in notes:
        i, t = notes[k]
        text_l(d, (870, ys[i]), t, font(22, True), NOTE)
    return img, d


# ---------- scene 7 · the real result ----------
B7 = ['Now, a real result.',
      'The question: how many vacation days do I get?',
      'The search returns four chunks, all from the vacation document.',
      'The best one, with a final score of 0.292, is the section about the right to vacation.',
      'It is exactly the chunk that says thirty days.']
RES = [('ferias#0', 'Direito a férias', '0.432', '0.0328', '0.292'), ('ferias#1', 'Como solicitar', '0.385', '0.0318', '0.278'),
       ('ferias#2', 'Abono pecuniário', '0.320', '0.0317', '0.258'), ('ferias#3', 'Pagamento', '0.309', '0.0318', '0.255')]


def s7(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 80), 'A real result', font(48, True))
    if k >= 2:
        rbox(d, (240, 120, 1040, 175), 'warn')
        text_c(d, (640, 148), Q, font(28, True, True), C['warn'])
    if k >= 3:
        for x, t in [(75, '#'), (130, 'chunk'), (330, 'section'), (650, 'cosine'), (800, 'RRF'), (960, 'final')]:
            text_l(d, (x, 215), t, font(21, True), C['muted'])
        d.line((60, 235, 1230, 235), fill=C['line'], width=2)
        for i, (cid, sec, cos, rrf, fin) in enumerate(RES):
            y = 250 + i * 75
            top = (i == 0 and k >= 4)
            rbox(d, (60, y, 1230, y + 62), 'acc' if top else 'box', hi=(top and k == 4))
            text_l(d, (75, y + 31), str(i + 1), font(26, True))
            text_l(d, (130, y + 31), cid, font(24, True, True))
            text_l(d, (330, y + 31), sec, font(24))
            text_l(d, (650, y + 31), cos, font(25, False, True))
            text_l(d, (800, y + 31), rrf, font(25, False, True))
            text_l(d, (960, y + 31), fin, font(28, True, True), C['acc'] if top else C['ink'])
    if k >= 5:
        text_c(d, (640, 590), 'contains:  "Todo colaborador CLT tem direito a 30 dias de férias..."', font(24, True, True), C['acc'])
    return img, d


# ---------- scene 8 · wrap-up ----------
B8 = ['To sum up: the RRF merges the two rankings using only the positions.',
      'The rerank computes the final score: 70 percent word coverage, 30 percent cosine.',
      'A cut keeps only chunks above 0.05, and at most four.',
      'In the next chapter, we will use these chunks to build the prompt, and finally ask the language model.',
      'See you there!']


def s8(k):
    img, d = cv()
    text_c(d, (640, 100), 'See you there!' if k >= 5 else 'Summing up', font(56, True), C['acc'] if k >= 5 else C['ink'])
    rows = [(1, 'acc', '1   RRF merges the rankings using only positions'), (2, 'box', '2   Rerank:  70% word coverage  +  30% cosine'),
            (3, 'warn', '3   Cut:  score ≥ 0.05,  at most 4 chunks'), (4, 'blue', 'Next chapter:  the prompt and the language model')]
    for i, (kk, st, t) in enumerate(rows):
        if k >= kk:
            y = 170 + i * 110
            rbox(d, (130, y, 1150, y + 85), st, hi=(k == kk))
            text_l(d, (170, y + 42), t, font(28, True))
    return img, d


SCENES = [(B1, s1), (B2, s2), (B3, s3), (B4, s4), (B5, s5), (B6, s6), (B7, s7), (B8, s8)]

if __name__ == '__main__':
    work = os.environ.get('VIDEO_WORKDIR', os.path.join(HERE, '_work', f'cap06b_en_{VOICE}'))
    if len(sys.argv) > 1 and sys.argv[1] == 'preview':
        preview(SCENES, os.path.join(work, 'preview'))
        print('preview saved in', os.path.join(work, 'preview'))
    else:
        build(SCENES, os.path.join(HERE, 'saida', f'cap06b_en_{VOICE}.mp4'), work, TAG)
