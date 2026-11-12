"""Chapter 6 (part 1) · Hybrid search: the two jurors (English, voice: Zira by default).

Usage:   python cap06a_en.py preview
         python cap06a_en.py                      # saida\\cap06a_en_zira.mp4
         set VOICE=david && python cap06a_en.py   # male voice
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine  # noqa: E402
from engine import C, arrow, box, build, canvas, dashed, font, preview, rbox, text_c, text_l  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
VOICES = {'zira': 'Microsoft Zira Desktop', 'david': 'Microsoft David Desktop'}
VOICE = os.environ.get('VOICE', 'zira').lower()
engine.SINGLE_VOICE = VOICES[VOICE]
engine.SPEECH = [   # spoken-only fixes (the subtitles keep the original text)
    (r'BM25', 'B M 25'), (r'\bRRF\b', 'R R F'), (r'6\.089', 'six point zero eight nine'), (r'\bMCP\b', 'M C P'),
    (r'\bP3\b', 'P 3'), (r'\bnpm\b', 'N P M'),
]
TAG = 'Chapter 6 · Hybrid search, part 1: the two jurors'
NOTE = (130, 225, 215)


def cv():
    return canvas(TAG)


def hl_text(d, x, y, text, words, f, fill=None, band=(255, 226, 150)):
    """Escreve `text` em (x, y) (âncora esquerda/meio) com um fundo marcador atrás das palavras de `words`."""
    low = text.lower()
    for w in words:
        i = 0
        while (i := low.find(w.lower(), i)) >= 0:
            xa = x + d.textlength(text[:i], font=f)
            xb = xa + d.textlength(text[i:i + len(w)], font=f)
            d.rectangle((xa - 3, y - 17, xb + 3, y + 17), fill=band)
            i += len(w)
    d.text((x, y), text, font=f, fill=fill or C['ink'], anchor='lm')


# ---------- scene 1 · opening ----------
B1 = ['Hello!',
      'In the previous chapter, we stored the vectors in an index.',
      'Now comes the heart of the whole system: the search.',
      'The project uses a hybrid search: two different methods, and then a fusion.',
      'This is the first of two videos about it.']


def s1(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 200), 'Hybrid search', font(76, True))
    if k >= 4:
        text_c(d, (640, 282), 'part 1:  the two jurors', font(38), C['acc'])
    if k >= 2:
        box(d, 150, 355, 400, 90, 'Chapter 5', 'the index', 'box', hi=(k == 2), tsize=27, ssize=20)
    if k >= 3:
        arrow(d, [(565, 400), (715, 400)], C['ink'], 5)
        box(d, 730, 355, 400, 90, 'Chapter 6', 'the search', 'acc', hi=(k == 3), tsize=27, ssize=20)
    if k >= 5:
        text_c(d, (640, 540), 'Part 1: two methods   ·   Part 2: the fusion', font(32, True), C['muted'])
    return img, d


# ---------- scene 2 · the whole picture ----------
B2 = ['Here is the whole picture.',
      'The question becomes a vector, and goes to two searches at the same time.',
      'The vector search, and the BM25 word search.',
      'Each one returns up to 12 candidates.',
      'Then, the RRF merges the two lists, the rerank reorders them, and a cut keeps the best 4.',
      'In this video, we look at the first two boxes. In the next, the rest.']


def s2(k):
    img, d = cv()
    text_c(d, (640, 85), 'The whole picture', font(46, True))
    if k >= 1:
        box(d, 40, 290, 150, 90, 'Question', 'cleaned', 'box', hi=(k == 1), tsize=24, ssize=16)
    if k >= 2:
        arrow(d, [(190, 335), (225, 335), (225, 205), (258, 205)], C['ink'], 4, head=11)
        arrow(d, [(225, 335), (225, 465), (258, 465)], C['ink'], 4, head=11)
        box(d, 260, 160, 320, 90, 'Vector search' if k >= 3 else '?', 'cosine' if k >= 3 else '', 'blue', hi=(k == 3), tsize=26, ssize=17)
        box(d, 260, 420, 320, 90, 'BM25 search' if k >= 3 else '?', 'exact words' if k >= 3 else '', 'blue', hi=(k == 3), tsize=26, ssize=17)
    if k >= 4:
        for y in (205, 465):
            text_c(d, (620, y - 22), 'top 12', font(21, True), C['blue'])
    if k >= 5:
        arrow(d, [(580, 205), (630, 205), (630, 335), (676, 335)], C['ink'], 4, head=11)
        arrow(d, [(580, 465), (630, 465), (630, 335)], C['ink'], 4, head=11)
        box(d, 680, 290, 120, 90, 'RRF', 'merges', 'acc', hi=(k == 5), tsize=26, ssize=16)
        arrow(d, [(800, 335), (858, 335)], C['ink'], 4, head=11)
        box(d, 860, 285, 180, 100, 'Rerank', 'reorders', 'acc', hi=(k == 5), tsize=26, ssize=16)
        arrow(d, [(1040, 335), (1098, 335)], C['ink'], 4, head=11)
        box(d, 1100, 285, 140, 100, 'Cut', 'top 4', 'warn', hi=(k == 5), tsize=26, ssize=16)
    if k >= 6:
        text_c(d, (420, 135), 'PART 1  (this video)', font(25, True), C['blue'])
        text_c(d, (970, 245), 'PART 2  (next video)', font(25, True), C['acc'])
    return img, d


# ---------- scene 3 · the jurors analogy ----------
B3 = ['Think of two jurors judging the same cards.',
      'The first judges by meaning: it is the vector search.',
      'The second judges by exact words: it is BM25.',
      'Each one hands in a ranking.',
      'A third, the RRF, will merge the rankings, and a final reviewer, the rerank, gives the final score.']


def s3(k):
    img, d = cv()
    text_c(d, (640, 85), 'Two jurors, the same cards', font(46, True))
    if k >= 1:
        for i in range(3):
            rbox(d, (540 + i * 12, 130 + i * 8, 740 + i * 12, 190 + i * 8), 'box')
        text_c(d, (640, 232), 'the same chunks', font(24, True), C['muted'])
        box(d, 80, 280, 500, 90, 'Juror 1', 'judges by MEANING  ·  vector search' if k >= 2 else '', 'blue', hi=(k == 2), tsize=28, ssize=19)
        box(d, 700, 280, 500, 90, 'Juror 2', 'judges by EXACT WORDS  ·  BM25' if k >= 3 else '', 'warn', hi=(k == 3), tsize=28, ssize=19)
    if k >= 4:
        for x, rows, st in [(80, ['1   card C', '2   card A', '3   card F'], 'blue'), (700, ['1   card A', '2   card D', '3   card C'], 'warn')]:
            rbox(d, (x, 390, x + 500, 520), st, hi=(k == 4))
            text_l(d, (x + 30, 415), 'ranking', font(20, True), C['muted'])
            for i, r in enumerate(rows):
                text_l(d, (x + 30, 452 + i * 28), r, font(24, True, True))
        text_c(d, (1135, 535), '(illustration)', font(17), C['muted'])
    if k >= 5:
        arrow(d, [(330, 522), (430, 548)], C['ink'], 3, head=9)
        arrow(d, [(950, 522), (850, 548)], C['ink'], 3, head=9)
        rbox(d, (300, 550, 980, 612), 'acc', hi=True)
        text_c(d, (640, 581), 'RRF merges  →  rerank gives the final score', font(27, True), C['acc'])
    return img, d


# ---------- scene 4 · juror 1: vector search ----------
B4 = ['The first juror: the vector search.',
      'We already saw it in the previous chapter.',
      'It turns the question into a vector, and finds the chunks with the most similar vector.',
      'It is good for paraphrases: for example, time off and vacation.',
      'As we saw, our local embedder does not know that; a neural one does.']


def s4(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 85), 'Juror 1: the vector search', font(46, True), C['blue'])
    if k >= 2:
        rbox(d, (380, 135, 900, 190), 'blue')
        text_c(d, (640, 162), 'Chapter 5:  VectorStore.search', font(26, True, True), C['blue'])
    if k >= 3:
        xs = [40, 340, 640, 940]
        for i, (t, sub) in enumerate([('the question', ''), ('its vector', '512 numbers'), ('cosine', 'with every chunk'), ('top 12', 'most similar')]):
            box(d, xs[i], 235, 270, 90, t, sub, 'box' if i == 0 else 'blue', hi=(k == 3), tsize=25, ssize=17)
            if i:
                arrow(d, [(xs[i] - 40, 280), (xs[i] - 6, 280)], C['ink'], 4, head=10)
    if k >= 4:
        rbox(d, (60, 380, 620, 580), 'acc', hi=(k == 4))
        text_c(d, (340, 420), 'good for paraphrases', font(28, True), C['acc'])
        text_c(d, (340, 495), '"time off"   ≈   "vacation"', font(34, True))
    if k >= 5:
        rbox(d, (660, 380, 1220, 475), 'warn', hi=(k == 5))
        text_c(d, (940, 410), 'local embedder', font(26, True), C['warn'])
        text_c(d, (940, 447), 'only shared words: misses it', font(22), C['warn'])
        rbox(d, (660, 490, 1220, 585), 'blue', hi=(k == 5))
        text_c(d, (940, 520), 'neural embedder (Voyage)', font(26, True), C['blue'])
        text_c(d, (940, 557), 'understands synonyms: finds it', font(22), C['blue'])
    return img, d


# ---------- scene 5 · juror 2: BM25 ----------
B5 = ['The second juror: BM25.',
      'BM25 is a classic algorithm for searching text by words.',
      'It gives more points to chunks that contain the words of the question.',
      'And it gives much more weight to rare words.',
      'A rare word, like password or P3, is worth much more than a common one, like days.',
      'It is great for acronyms, codes, and exact names, where search by meaning tends to fail.']
WEIGHTS = [('senha  (password)', 1, 2.43), ('p3', 2, 1.92), ('dias  (days)', 10, 0.48)]


def s5(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 85), 'Juror 2: BM25', font(46, True), C['warn'])
    if k >= 2:
        rbox(d, (360, 135, 920, 190), 'warn')
        text_c(d, (640, 162), 'a classic text-search algorithm', font(26, True), C['warn'])
    if k >= 3:
        rbox(d, (60, 215, 640, 420), 'box', hi=(k == 3))
        text_l(d, (85, 250), 'chunk:  ti-suporte#0', font(20, True), C['muted'])
        hl_text(d, 85, 295, 'Suporte de TI > Reset de senha', ['reset', 'senha'], font(24, False, True))
        hl_text(d, 85, 345, 'A senha corporativa expira a', ['senha'], font(24, False, True))
        text_l(d, (85, 392), 'question words:  resetar · senha', font(20, True), C['warn'])
    if k >= 4:
        rbox(d, (680, 215, 1230, 505), 'warn', hi=(k == 5))
        text_c(d, (955, 243), 'weight of each word  (real data)', font(22, True), C['warn'])
        for i, (w, n, idf) in enumerate(WEIGHTS):
            y = 288 + i * 62
            text_l(d, (705, y), w, font(21, True, True))
            d.text((1208, y), f'in {n} of 16 chunks', font=font(19), fill=C['muted'], anchor='rm')
            d.rectangle((705, y + 20, 705 + 400 * idf / 2.43, y + 38), fill=C['warn'] if idf > 1 else C['line'])
            text_l(d, (705 + 400 * idf / 2.43 + 10, y + 29), f'{idf:.2f}', font(22, True), C['warn'] if idf > 1 else C['muted'])
        if k >= 5:
            text_c(d, (955, 481), 'rare  =  heavy      common  =  light', font(23, True), C['warn'])
    if k >= 6:
        for i, t in enumerate(['acronyms', 'codes', 'exact names']):
            rbox(d, (60 + i * 225, 545, 265 + i * 225, 600), 'warn', hi=True)
            text_c(d, (162 + i * 225, 572), t, font(25, True), C['warn'])
        text_l(d, (760, 572), 'where meaning search tends to fail', font(23, True), C['muted'])
    return img, d


# ---------- scene 6 · a real BM25 result ----------
B6 = ["Let's see a real result.",
      'We ask BM25 about resetting a password.',
      'Only one chunk contains both words: the password reset section of the IT support document.',
      'Its score is 6.089.',
      'Notice that this is not a number between zero and one, like the cosine. The two jurors speak different scales.']


def s6(k):
    img, d = cv()
    text_c(d, (640, 85), 'A real BM25 result', font(46, True))
    if k >= 2:
        d.rounded_rectangle((90, 140, 1190, 260), 18, fill=C['code_bg'])
        text_l(d, (125, 180), "bm25.search('resetar senha', 3)", font(30, False, True), C['code_ink'])
        if k >= 3:
            text_l(d, (125, 232), "→  [ 'ti-suporte#0  6.089' ]", font(30, True, True), NOTE)
    if k >= 3:
        rbox(d, (90, 300, 700, 480), 'acc', hi=(k == 3))
        text_l(d, (115, 335), 'ti-suporte#0', font(26, True, True), C['acc'])
        text_l(d, (115, 380), 'Suporte de TI > Reset de senha', font(24, False, True))
        text_l(d, (115, 425), '"A senha corporativa expira a...', font(22, False, True), C['muted'])
    if k >= 4:
        rbox(d, (760, 300, 1190, 480), 'warn', hi=(k == 4))
        text_c(d, (975, 340), 'BM25 score', font(26, True), C['warn'])
        text_c(d, (975, 410), '6.089', font(68, True), C['warn'])
    if k >= 5:
        text_c(d, (640, 540), 'cosine:  0 to 1      BM25:  any size', font(32, True), C['blue'])
        text_c(d, (640, 590), 'different scales', font(26), C['muted'])
    return img, d


# ---------- scene 7 · why two methods ----------
B7 = ['So, why not use only the vector search?',
      'Because it can fail with exact terms, like a code or an acronym.',
      'BM25 gets those right.',
      'And the vector search gets the paraphrases right.',
      'Together, they cover each other\'s failures.']


def s7(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 85), 'Why two methods?', font(48, True))
    if k >= 2:
        rbox(d, (60, 150, 620, 530), 'blue', hi=(k == 2))
        text_c(d, (340, 190), 'Vector search', font(32, True), C['blue'])
        text_c(d, (340, 250), 'can miss exact terms', font(26, True), C['warn'])
        text_c(d, (340, 295), '"TCK-1001"      "P3"', font(26, True, True), C['warn'])
    if k >= 3:
        rbox(d, (660, 150, 1220, 530), 'warn', hi=(k == 3))
        text_c(d, (940, 190), 'BM25', font(32, True), C['warn'])
        text_c(d, (940, 250), 'gets exact terms right', font(26, True), C['acc'])
        text_c(d, (940, 295), '"TCK-1001"      "P3"', font(26, True, True), C['acc'])
    if k >= 4:
        text_c(d, (340, 380), 'gets paraphrases right', font(26, True), C['acc'])
        text_c(d, (340, 425), '"time off"  ≈  "vacation"', font(26, True))
        text_c(d, (940, 380), 'can miss paraphrases', font(26, True), C['warn'])
        text_c(d, (940, 425), '"time off"  ≠  "vacation"', font(26, True))
    if k >= 5:
        rbox(d, (150, 550, 1130, 612), 'acc', hi=True)
        text_c(d, (640, 581), 'together, they cover each other\'s failures', font(30, True), C['acc'])
    return img, d


# ---------- scene 8 · wrap-up ----------
B8 = ['To sum up: the hybrid search uses two jurors.',
      'The vector search judges by meaning.',
      'BM25 judges by exact words, giving more weight to rare ones.',
      'Each one hands in a list of up to 12 candidates.',
      'In the next video, we will see how these two lists are merged, and how the final score is computed.',
      'See you there!']


def s8(k):
    img, d = cv()
    text_c(d, (640, 100), 'See you there!' if k >= 6 else 'Summing up', font(56, True), C['acc'] if k >= 6 else C['ink'])
    rows = [(2, 'blue', '1   Vector search: judges by meaning'), (3, 'warn', '2   BM25: exact words, rare ones weigh more'),
            (4, 'box', '3   Each hands in up to 12 candidates'), (5, 'acc', 'Next video:  merging the lists, the final score')]
    for i, (kk, st, t) in enumerate(rows):
        if k >= kk:
            y = 170 + i * 110
            rbox(d, (130, y, 1150, y + 85), st, hi=(k == kk))
            text_l(d, (170, y + 42), t, font(28, True))
    return img, d


SCENES = [(B1, s1), (B2, s2), (B3, s3), (B4, s4), (B5, s5), (B6, s6), (B7, s7), (B8, s8)]

if __name__ == '__main__':
    work = os.environ.get('VIDEO_WORKDIR', os.path.join(HERE, '_work', f'cap06a_en_{VOICE}'))
    if len(sys.argv) > 1 and sys.argv[1] == 'preview':
        preview(SCENES, os.path.join(work, 'preview'))
        print('preview saved in', os.path.join(work, 'preview'))
    else:
        build(SCENES, os.path.join(HERE, 'saida', f'cap06a_en_{VOICE}.mp4'), work, TAG)
