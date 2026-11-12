"""Chapter 4 · Embeddings: turning text into numbers (English, voice: Zira by default).

Usage:   python cap04_en.py preview
         python cap04_en.py                      # saida\\cap04_en_zira.mp4
         set VOICE=david && python cap04_en.py   # male voice
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine  # noqa: E402
from engine import (BAND_TEAL, C, arrow, box, build, canvas, dashed, font, preview, rbox, text_c,  # noqa: E402
                    text_l)

HERE = os.path.dirname(os.path.abspath(__file__))
VOICES = {'zira': 'Microsoft Zira Desktop', 'david': 'Microsoft David Desktop'}
VOICE = os.environ.get('VOICE', 'zira').lower()
engine.SINGLE_VOICE = VOICES[VOICE]
engine.SPEECH = [(r'\bAPI\b', 'A P I'), (r'\bMCP\b', 'M C P'), (r'\bnpm\b', 'N P M')]   # spoken-only fixes
TAG = 'Chapter 4 · Embeddings: turning text into numbers'
NOTE = (130, 225, 215)
Q1 = 'Quantos dias de férias eu tenho?'          # the real sentences used in the project's test
Q2 = 'Quantos dias de ferias posso tirar?'
Q3 = 'Como pedir reembolso de viagem?'


def cv():
    return canvas(TAG)


# ---------- scene 1 · opening ----------
B1 = ['Hello!',
      'In the previous chapter, we cut the documents into chunks.',
      'Now, we need a way for the computer to compare those pieces of text.',
      'The answer is embeddings: turning text into numbers.',
      'You will see the idea, the code, and a real test, with results.']


def s1(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 200), 'Embeddings', font(76, True))
    if k >= 4:
        text_c(d, (640, 282), 'turning text into numbers', font(36), C['acc'])
    if k >= 2:
        box(d, 150, 355, 400, 90, 'Chapter 3', 'chunks', 'box', hi=(k == 2), tsize=27, ssize=20)
    if k >= 3:
        arrow(d, [(565, 400), (715, 400)], C['ink'], 5)
        box(d, 730, 355, 400, 90, 'Chapter 4', 'embeddings', 'acc', hi=(k == 3), tsize=27, ssize=20)
    if k >= 5:
        text_c(d, (640, 540), 'The idea   ·   The code   ·   A real test', font(32, True), C['muted'])
    return img, d


# ---------- scene 2 · what is an embedding ----------
B2 = ['Computers compare numbers easily, but texts, not so much.',
      'The solution is to translate each text into a list of numbers.',
      'That list is called an embedding.',
      'In our project, it has 512 numbers.',
      'And there is a golden rule: similar texts produce similar lists.']


def s2(k):
    img, d = cv()
    text_c(d, (640, 90), 'What is an embedding?', font(48, True))
    if k >= 1:
        rbox(d, (60, 170, 520, 290), 'box', hi=(k == 1))
        text_c(d, (290, 215), Q1, font(26, True))
        text_c(d, (290, 255), '(a text)', font(20), C['muted'])
    if k >= 2:
        arrow(d, [(540, 230), (620, 230)], C['ink'], 5)
        text_c(d, (580, 200), 'translate', font(18, True), C['muted'])
        rbox(d, (640, 170, 1230, 290), 'acc', hi=(k == 2))
        text_c(d, (935, 230), '[ 0,  0.31,  0,  0.07,  0,  ... ]', font(28, True, True), C['acc'])
    if k >= 3:
        text_c(d, (935, 320), 'an embedding', font(30, True), C['acc'])
    if k >= 4:
        text_c(d, (935, 360), '512 numbers', font(34, True), C['blue'])
    if k >= 5:
        rbox(d, (60, 410, 1230, 590), 'blue', hi=True)
        text_c(d, (640, 445), 'golden rule:  similar texts  →  similar lists', font(32, True), C['blue'])
        text_l(d, (110, 510), 'text A  →  [ 0,  0.31,  0,  0.07, ... ]', font(24, False, True))
        text_l(d, (110, 553), 'text B  →  [ 0,  0.29,  0,  0.08, ... ]', font(24, False, True))
        text_c(d, (640, 531), '≈', font(60, True), C['blue'])
        text_l(d, (700, 531), 'similar', font(26, True), C['blue'])
        text_c(d, (1135, 335), '(illustration)', font(18), C['muted'])
    return img, d


# ---------- scene 3 · the map analogy ----------
B3 = ['Imagine a map where each text is a point.',
      'Texts about the same subject end up as neighbors.',
      'Texts about different subjects are far apart.',
      'A question about vacation days sits near another question about vacation, and far from a question about reimbursement.',
      'To measure the distance between two points, we use the cosine: close to one means very similar; close to zero means unrelated.']


def dot(d, xy, col, r=14):
    d.ellipse((xy[0] - r, xy[1] - r, xy[0] + r, xy[1] + r), fill=col, outline=C['ink'], width=3)


def s3(k):
    img, d = cv()
    text_c(d, (640, 90), 'The map analogy', font(48, True))
    if k >= 1:
        rbox(d, (60, 140, 1220, 560), 'box')
    A, B, Cc = (260, 270), (400, 340), (940, 440)
    if k >= 2:
        dot(d, A, C['acc'])
        dot(d, B, C['acc'])
        text_l(d, (285, 270), 'How many vacation days do I get?', font(22, True))
        text_l(d, (425, 340), 'Can I take vacation?', font(22, True))
    if k >= 3:
        dot(d, Cc, C['warn'])
        d.text((915, 440), 'How do I request reimbursement?', font=font(22, True), fill=C['ink'], anchor='rm')
    if k >= 4:
        d.ellipse((190, 215, 600, 390), outline=C['acc'], width=4)
        text_c(d, (395, 412), 'neighbors', font(28, True), C['acc'])
        dashed(d, (440, 360), (905, 432), C['warn'], 3)
        text_c(d, (680, 372), 'far apart', font(28, True), C['warn'])
    if k >= 5:
        text_c(d, (640, 596), 'cosine:   close to 1 = very similar   ·   close to 0 = unrelated', font(26, True), C['blue'])
    return img, d


# ---------- scene 4 · two translators ----------
B4 = ['The project has two translators, the embedders.',
      'The first is local: it runs on your computer, without internet and without a key.',
      'The second uses the Voyage AI service, which has a neural model, and needs a key.',
      'We will study the first one, because we can see how it works inside.']


def s4(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 90), 'Two translators (embedders)', font(48, True))
    if k >= 2:
        rbox(d, (60, 150, 620, 560), 'acc', hi=(k == 4))
        text_c(d, (340, 200), 'Local embedder', font(36, True), C['acc'])
        for i, t in enumerate(['•  runs on your computer', '•  no internet, no key', '•  simple: counts words']):
            text_l(d, (100, 285 + i * 65), t, font(28))
    if k >= 3:
        rbox(d, (660, 150, 1220, 560), 'blue')
        text_c(d, (940, 200), 'Voyage embedder', font(36, True), C['blue'])
        for i, t in enumerate(['•  online service (Voyage AI)', '•  needs an API key', '•  neural model: understands meaning']):
            text_l(d, (700, 285 + i * 65), t, font(28))
    if k >= 4:
        text_c(d, (340, 595), 'we will study this one', font(30, True), C['acc'])
    return img, d


# ---------- scene 5 · preparing the text ----------
B5 = ['Before turning into numbers, the text goes through a preparation.',
      'First, everything becomes lowercase and the accents are removed.',
      'Then, words that are too common, like of, for, and with, are thrown away, because they do not help find anything.',
      'Finally, each word with more than five letters is cut down to five.',
      'Look at the example on screen: a question about vacation days becomes a short list of five tokens.']
ROWS5 = [(Q1, 'the question'), ('quantos dias de ferias eu tenho', 'lowercase, no accents'),
         ('quantos dias ferias eu tenho', 'drop very common words'), ('quant · dias · feria · eu · tenho', 'cut at 5 letters  =  tokens')]


def s5(k):
    img, d = cv()
    text_c(d, (640, 85), 'Preparing the text', font(46, True))
    for i, (t, lab) in enumerate(ROWS5):
        if k >= i + 1:
            y = 140 + i * 105
            rbox(d, (60, y, 800, y + 80), 'acc' if i == 3 else 'box', hi=(k == i + 1 or (k == 5 and i == 3)))
            text_l(d, (90, y + 40), t, font(30, True, True))
            text_l(d, (830, y + 40), lab, font(25, True), C['muted'])
            if i:
                arrow(d, [(430, y - 22), (430, y - 3)], C['ink'], 4, head=10)
    if k >= 5:
        text_c(d, (640, 590), '5 tokens', font(36, True), C['acc'])
    return img, d


# ---------- scene 6 · the 512 drawers ----------
B6 = ['Now, the transformation.',
      'The vector has 512 positions, like 512 drawers, all starting at zero.',
      'For each word, a hash function picks a drawer, always the same drawer for the same word, and adds one to it.',
      'Besides the words, the code also counts every piece of three letters, with a smaller weight, to tolerate small typos.',
      'At the end, the vector is adjusted to have length one, so that the size of the text does not disturb the comparison.']
TOK = ['quant', 'dias', 'feria', 'eu', 'tenho']
TARGET = [1, 3, 6, 8, 10]
TRI = [('fer', 2), ('eri', 5), ('ria', 7)]


def s6(k):
    img, d = cv()
    text_c(d, (640, 85), 'The transformation', font(46, True))
    sq = lambda i: 125 + i * 85
    if k >= 2:
        text_c(d, (1165, 348), '512 drawers', font(26, True), C['muted'])
        text_c(d, (1165, 378), '(vector positions)', font(20), C['muted'])
        for i in range(12):
            hit = (k >= 3 and i in TARGET)
            tri = (k >= 4 and any(i == j for _, j in TRI))
            rbox(d, (sq(i) - 35, 400, sq(i) + 35, 470), 'acc' if hit else ('warn' if tri else 'box'), hi=False)
            lab = '1' if hit else ('0.15' if tri else '0')
            text_c(d, (sq(i), 435), lab, font(26 if len(lab) == 1 else 20, True))
        text_c(d, (sq(12) + 20, 435), '...', font(34, True), C['muted'])
    if k >= 3:
        for i, t in enumerate(TOK):
            x = 185 + i * 215
            rbox(d, (x - 90, 160, x + 90, 215), 'box', hi=(k == 3))
            text_c(d, (x, 188), t, font(28, True, True))
            arrow(d, [(x, 218), (sq(TARGET[i]), 394)], C['acc'], 3, head=10)
        text_c(d, (640, 135), 'hash(word)  →  a drawer,  +1', font(24, True), C['acc'])
    if k >= 4:
        for t, j in TRI:
            rbox(d, (sq(j) - 40, 515, sq(j) + 40, 560), 'warn', hi=(k == 4))
            text_c(d, (sq(j), 538), t, font(24, True, True), C['warn'])
            arrow(d, [(sq(j), 513), (sq(j), 476)], C['warn'], 3, head=9)
        text_l(d, (850, 538), '3-letter pieces:  +0.15', font(24, True), C['warn'])
    if k >= 5:
        text_c(d, (640, 596), 'finally:  scale the vector to length 1', font(28, True), C['blue'])
    return img, d


# ---------- scene 7 · the cosine ----------
B7 = ['How do we compare two vectors? With the cosine.',
      'The code multiplies the two vectors, position by position, and adds everything up.',
      'The result is between zero and one: the closer to one, the more similar.',
      'Now, a real test.',
      'Two questions about vacation days give zero point six seven two.',
      'A question about vacation days and a question about expense reimbursement give zero.']
COS = ['export const cosine = (a, b) => {', '  let s = 0;', '  for (let i = 0; i < a.length; i++) s += a[i] * b[i];',
       '  return s;', '};']


def s7(k):
    img, d = cv()
    if k >= 1:
        d.rounded_rectangle((90, 100, 1190, 296), 18, fill=C['code_bg'])
        d.rounded_rectangle((90, 100, 1190, 142), 18, fill=(29, 44, 56))
        text_l(d, (120, 121), 'src/rag/embeddings.js', font(21, False, True), C['code_ink'])
        if k == 2:
            d.rectangle((100, 208, 1180, 236), fill=BAND_TEAL)
        for i, line in enumerate(COS):
            text_l(d, (125, 166 + i * 28), line, font(22, False, True), C['code_ink'])
    if k >= 3:
        d.rectangle((300, 318, 980, 332), fill=C['line'])
        d.rectangle((300, 318, 300 + 680 * 0.0 + 4, 332), fill=C['warn'])
        text_l(d, (300, 350), '0  =  unrelated', font(24, True), C['warn'])
        d.text((980, 350), '1  =  identical', font=font(24, True), fill=C['acc'], anchor='rm')
    if k >= 4:
        text_c(d, (640, 396), 'A real test', font(32, True))
    for i, (other, val) in enumerate([(Q2, 0.672), (Q3, 0.0)]):
        if k >= 5 + i:
            y = 440 + i * 85
            text_l(d, (90, y), f'{Q1}   vs   {other}', font(22, False, True), C['ink'])
            d.rounded_rectangle((90, y + 20, 1000, y + 46), 8, fill=C['card'], outline=C['line'], width=2)
            if val:
                d.rounded_rectangle((90, y + 20, 90 + 910 * val, y + 46), 8, fill=C['acc'])
            text_l(d, (1030, y + 33), f'{val:.3f}', font(36, True), C['acc'] if val else C['warn'])
    return img, d


# ---------- scene 8 · the honest limit ----------
B8 = ['But beware of an honest limit.',
      'This local translator only counts words and pieces of words.',
      'It does not understand meaning.',
      'For it, rest and vacation have nothing to do with each other.',
      'It is good for studying the idea, and it works because our project has few documents.',
      'For real quality, there is the second translator, which uses a neural model, and understands synonyms.',
      'You just set the Voyage API key.',
      'The rest of the code does not change, because both translators have the same interface.']


def s8(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 85), 'An honest limit', font(48, True), C['warn'])
    if k >= 2:
        rbox(d, (60, 150, 620, 440), 'acc')
        text_c(d, (340, 190), 'Local embedder', font(32, True), C['acc'])
        text_l(d, (95, 255), '•  only counts words', font(27))
    if k >= 3:
        text_l(d, (95, 305), '•  does not understand meaning', font(27, True), C['warn'])
    if k >= 4:
        rbox(d, (90, 350, 590, 425), 'warn', hi=(k == 4))
        text_c(d, (340, 388), '"descanso"   ≠   "férias"', font(30, True), C['warn'])
    if k >= 5:
        text_c(d, (340, 470), 'fine for studying: few documents', font(25, True), C['muted'])
    if k >= 6:
        rbox(d, (660, 150, 1220, 440), 'blue', hi=(k == 6))
        text_c(d, (940, 190), 'Voyage embedder', font(32, True), C['blue'])
        text_l(d, (695, 255), '•  neural model', font(27))
        text_l(d, (695, 305), '•  understands synonyms', font(27, True), C['blue'])
        text_c(d, (940, 388), '"descanso"   ≈   "férias"', font(30, True), C['blue'])
    if k >= 7:
        text_c(d, (940, 480), 'set  VOYAGE_API_KEY', font(27, True, True), C['blue'])
    if k >= 8:
        rbox(d, (150, 520, 1130, 595), 'box', hi=True)
        text_c(d, (640, 558), 'same interface:   embed(texts)   →   nothing else changes', font(28, True))
    return img, d


# ---------- scene 9 · wrap-up ----------
B9 = ['To sum up: an embedding is the translation of a text into a list of numbers, in which similar texts produce similar lists.',
      'We measure similarity with the cosine.',
      'Our local translator is simple, and does not understand meaning; the Voyage one does.',
      'In the next chapter, we will store these vectors in an index.',
      'See you there!']


def s9(k):
    img, d = cv()
    text_c(d, (640, 100), 'See you there!' if k >= 5 else 'Summing up', font(56, True), C['acc'] if k >= 5 else C['ink'])
    rows = [('acc', '1   Embedding = text as a list of numbers'), ('box', '2   Similarity is measured with the cosine'),
            ('warn', '3   Local: simple, no meaning  ·  Voyage: understands meaning'), ('blue', 'Next chapter:  storing the vectors in an index')]
    for i, (st, t) in enumerate(rows):
        if k >= i + 1:
            y = 170 + i * 110
            rbox(d, (130, y, 1150, y + 85), st, hi=(k == i + 1))
            text_l(d, (170, y + 42), t, font(28, True))
    return img, d


SCENES = [(B1, s1), (B2, s2), (B3, s3), (B4, s4), (B5, s5), (B6, s6), (B7, s7), (B8, s8), (B9, s9)]

if __name__ == '__main__':
    work = os.environ.get('VIDEO_WORKDIR', os.path.join(HERE, '_work', f'cap04_en_{VOICE}'))
    if len(sys.argv) > 1 and sys.argv[1] == 'preview':
        preview(SCENES, os.path.join(work, 'preview'))
        print('preview saved in', os.path.join(work, 'preview'))
    else:
        build(SCENES, os.path.join(HERE, 'saida', f'cap04_en_{VOICE}.mp4'), work, TAG)
