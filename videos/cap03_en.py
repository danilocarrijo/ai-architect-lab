"""Chapter 3 · Chunks: cutting documents into useful pieces (English, voice: Zira by default).

Usage:   python cap03_en.py preview
         python cap03_en.py                      # saida\\cap03_en_zira.mp4
         set VOICE=david && python cap03_en.py   # male voice
"""
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine  # noqa: E402
from engine import (BAND_AMBER, BAND_BLUE, BAND_TEAL, C, arrow, box, build, canvas, code_panel, dashed,  # noqa: E402
                    font, preview, rbox, text_c, text_l)

HERE = os.path.dirname(os.path.abspath(__file__))
VOICES = {'zira': 'Microsoft Zira Desktop', 'david': 'Microsoft David Desktop'}
VOICE = os.environ.get('VOICE', 'zira').lower()
engine.SINGLE_VOICE = VOICES[VOICE]
engine.SPEECH = [(r'\bMCP\b', 'M C P'), (r'\bnpm\b', 'N P M')]   # spoken-only fixes (subtitles keep the text)
TAG = 'Chapter 3 · Chunks: cutting documents into pieces'
NOTE = (130, 225, 215)   # light teal for notes drawn on dark panels


def cv():
    return canvas(TAG)


def shade(img, rect, rgba, outline):
    """Retângulo translúcido (para marcar a área de overlap)."""
    ov = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ImageDraw.Draw(ov).rectangle(rect, fill=rgba, outline=outline, width=3)
    img.paste(ov, (0, 0), ov)


# ---------- scene 1 · opening ----------
B1 = ['Hello!',
      'In the previous chapter, you saw the documents that feed the assistant.',
      'Now, we will give them their first treatment: cutting each document into smaller pieces.',
      'Those pieces are called chunks.',
      'You will understand why they exist, how the code creates them, and what goes inside each one.']


def s1(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 200), 'Chunks', font(76, True))
    if k >= 4:
        text_c(d, (640, 282), 'cutting documents into useful pieces', font(36), C['acc'])
    if k >= 2:
        box(d, 150, 355, 400, 90, 'Chapter 2', 'the documents', 'box', hi=(k == 2), tsize=27, ssize=20)
    if k >= 3:
        arrow(d, [(565, 400), (715, 400)], C['ink'], 5)
        box(d, 730, 355, 400, 90, 'Chapter 3', 'chunks', 'acc', hi=(k == 3), tsize=27, ssize=20)
    if k >= 5:
        text_c(d, (640, 540), 'Why   ·   How   ·   What goes inside', font(32, True), C['muted'])
    return img, d


# ---------- scene 2 · the card-file analogy ----------
B2 = ['Imagine you have four whole textbooks.',
      'Nobody reads the whole textbook to find an answer.',
      'So, you cut each section onto a card, and write on top which textbook and which chapter it came from.',
      'Then you keep the cards in a card file.',
      'Each of those cards is a chunk.']
BOOKS = ['ferias', 'home-office', 'reembolso', 'ti-suporte']
CARDS = ['ferias · Direito a férias', 'ferias · Como solicitar', 'ferias · Pagamento',
         'reembolso · Prazo', 'ti-suporte · SLA de chamados', 'home-office · Segurança']


def s2(k):
    img, d = cv()
    text_c(d, (640, 95), 'The card-file analogy', font(46, True))
    if k >= 1:
        for i, b in enumerate(BOOKS):
            x = 60 + i * 130
            rbox(d, (x, 210, x + 110, 400), ['box', 'acc', 'blue', 'warn'][i], hi=(k == 1))
            text_c(d, (x + 55, 305), b, font(17, True, True))
        text_c(d, (310, 440), 'four whole textbooks', font(27), C['muted'])
    if k == 2:
        text_c(d, (310, 500), 'Nobody reads it all.', font(34, True), C['warn'])
    if k >= 4:
        rbox(d, (680, 170, 1245, 455), 'acc', hi=(k == 4))
        text_c(d, (962, 198), 'the card file', font(24, True), C['acc'])
    if k >= 3:
        arrow(d, [(595, 305), (670, 305)], C['ink'], 5)
        text_c(d, (632, 270), 'cut', font(22, True), C['muted'])
        for i, c in enumerate(CARDS):
            x, y = 695 + (i % 2) * 272, 225 + (i // 2) * 72
            rbox(d, (x, y, x + 260, y + 56), 'box', hi=(k == 5 and i == 2))
            text_c(d, (x + 130, y + 28), c, font(18, True))
    if k >= 5:
        text_c(d, (962, 510), 'each card   =   one chunk', font(34, True), C['acc'])
    return img, d


# ---------- scene 3 · why cut ----------
B3 = ['Why cut? There are three reasons.',
      'First, cost. The model charges per token, which is, roughly, a piece of a word. Handing over only the relevant passage is cheaper than handing over the whole document.',
      'Second, precision. With a small piece, the answer can cite exactly where it came from: for example, the vacation file, Payment section.',
      'Third, search quality. A piece about payment does not get mixed with a piece about selling vacation days.']
WHY = [('1   Cost', 'the model charges per token: send only what is relevant', 'acc'),
       ('2   Precision', 'the answer can cite the exact source:  ferias.md  >  Pagamento', 'blue'),
       ('3   Search quality', 'a Payment piece is not mixed with a "selling vacation days" piece', 'warn')]


def s3(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 95), 'Why cut into pieces?', font(48, True))
    for i, (t, sub, st) in enumerate(WHY):
        if k >= i + 2:
            y = 160 + i * 140
            rbox(d, (130, y, 1150, y + 115), st, hi=(k == i + 2))
            text_l(d, (170, y + 38), t, font(34, True))
            text_l(d, (170, y + 82), sub, font(25), C['muted'])
    return img, d


# ---------- scene 4 · size rules ----------
B4 = ['How does the system decide the size?',
      'By the rules in the configuration file.',
      'Each chunk has, at most, 600 characters.',
      'And there is a second number: 100. It is the overlap.',
      'When a section is too long and has to be split, the last 100 characters of a piece are repeated at the start of the next piece.',
      'This prevents an important sentence from being cut in half, without the context that explains it.']


def s4(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 85), 'The size rules', font(46, True))
    if k >= 2:
        d.rounded_rectangle((90, 135, 1190, 255), 18, fill=C['code_bg'])
        text_l(d, (120, 160), 'src/config.js', font(21, False, True), (150, 170, 185))
        f, x0, y = font(36, False, True), 125, 215
        txt = 'chunk: { maxChars: 600, overlapChars: 100 },'

        def hl(sub, col):
            i = txt.index(sub)
            xa = x0 + d.textlength(txt[:i], font=f)
            d.rectangle((xa - 6, y - 26, xa + d.textlength(sub, font=f) + 6, y + 26), fill=col)
        if k == 3:
            hl('maxChars: 600', BAND_TEAL)
        if k == 4:
            hl('overlapChars: 100', BAND_AMBER)
        d.text((x0, y), txt, font=f, fill=C['code_ink'], anchor='lm')
    if k >= 5:
        shade(img, (560, 330, 760, 560), (180, 83, 9, 70), C['warn'])
        text_c(d, (660, 305), 'overlap: 100 characters repeated', font(24, True), C['warn'])
        rbox(d, (180, 345, 760, 425), 'acc')
        text_c(d, (470, 385), 'piece 1   ·   up to 600 characters', font(25, True))
        rbox(d, (560, 465, 1140, 545), 'blue')
        text_c(d, (850, 505), 'piece 2', font(25, True))
    if k >= 6:
        text_c(d, (640, 590), 'no sentence is cut in half without its context', font(28, True), C['acc'])
    return img, d


# ---------- scene 5 · cutting by section ----------
B5 = ['But the cut is not blind.',
      'The code respects the structure of the document.',
      'First, it splits the text into sections, cutting before every line that starts with two pound signs.',
      'Each section gets the name that comes after the pound signs.',
      'Empty sections are ignored.']
FERIAS = ['---', 'title: Política de Férias', 'dept: rh', 'updated: 2026-01-10', '---', '# Política de Férias', '',
          '## Direito a férias', 'Todo colaborador CLT tem direito a 30 dias...', '', '## Como solicitar',
          'A solicitação deve ser feita no portal...']


def s5(k):
    img, d = cv()
    bands = {3: [(7, 7, BAND_BLUE), (10, 10, BAND_BLUE)], 4: [(7, 7, BAND_TEAL), (10, 10, BAND_TEAL)],
             5: [(5, 6, BAND_AMBER)]}.get(k, [])
    ys = code_panel(d, 'data/ferias.md', FERIAS, bands)
    if k >= 3:
        for i in (7, 10):
            dashed(d, (100, ys[i] - 18), (1180, ys[i] - 18), (255, 170, 70), 3)
        text_l(d, (800, ys[7] - 40), 'cut', font(22, True), (255, 170, 70))
        text_l(d, (800, ys[10] - 40), 'cut', font(22, True), (255, 170, 70))
    if k >= 4:
        text_l(d, (800, ys[7]), '←  section name', font(25, True), NOTE)
        text_l(d, (800, ys[10]), '←  section name', font(25, True), NOTE)
    if k >= 5:
        text_l(d, (800, ys[5]), '←  only a title: ignored', font(25, True), (255, 200, 120))
    return img, d


# ---------- scene 6 · long sections ----------
B6 = ['Only then, the code looks at the size.',
      'If the section has more than 600 characters, a separate function splits the text into sentences, and builds the pieces sentence by sentence, applying the overlap.',
      'This way, we never cut a sentence in the middle.',
      'In our four documents, every section fits within the limit, so this case never happens.',
      'But the code is ready for it.']
SPLIT = ['function splitLong(text, max, overlap) {',
         '  if (text.length <= max) return [text];',
         r"  const sentences = text.match(/[^.!?]+[.!?]+\s*|[^.!?]+$/g) ?? [text];",
         '  const out = [];', "  let cur = '';", '  for (const s of sentences) {',
         '    if ((cur + s).length > max && cur) {', '      out.push(cur.trim());',
         '      cur = cur.slice(-overlap) + s;', '    } else cur += s;', '  }']


def s6(k):
    img, d = cv()
    bands = {2: [(1, 1, BAND_BLUE), (5, 9, BAND_TEAL)], 3: [(2, 2, BAND_TEAL)]}.get(k, [])
    code_panel(d, 'src/rag/chunker.js  (splitLong, excerpt)', SPLIT, bands, size=22)
    if k == 2:
        text_c(d, (640, 590), 'more than 600?  →  split by sentence, with overlap', font(26, True), NOTE)
    if k == 3:
        text_c(d, (640, 590), 'it cuts between sentences, never inside one', font(26, True), NOTE)
    if k >= 4:
        text_c(d, (640, 590), 'our sections are all short: this path is not triggered here', font(26, True), (255, 200, 120))
    if k >= 5:
        text_c(d, (640, 590), 'but it is ready for longer documents', font(26, True), NOTE)
    return img, d


# ---------- scene 7 · contextual header ----------
B7 = ['Now, an important detail.',
      'Each chunk gets, at the start of its text, a header with the document title and the section name, separated by a greater-than sign.',
      'This is called contextual chunking.',
      'Without it, a piece that says only: up to two days before the start, would not make clear what subject it is about.',
      'The header carries the context along with the card.']


def s7(k):
    img, d = cv()
    text_c(d, (640, 95), 'The contextual header', font(48, True))
    if k >= 4:
        rbox(d, (60, 160, 560, 500), 'warn', hi=(k == 4))
        text_c(d, (310, 205), 'a piece without context', font(27, True), C['warn'])
        text_c(d, (310, 300), '"... up to 2 days before', font(26))
        text_c(d, (310, 340), 'the start ..."', font(26))
        text_c(d, (310, 430), 'about what?', font(40, True), C['warn'])
    if k >= 2:
        rbox(d, (620, 160, 1230, 500), 'acc', hi=(k == 2))
        text_c(d, (925, 205), 'a chunk  (ferias#3)' if k < 5 else 'the same piece, with context', font(27, True), C['acc'])
        d.rounded_rectangle((650, 245, 1200, 305), 10, fill=C['acc_soft'], outline=C['acc'], width=3)
        text_c(d, (925, 275), 'Política de Férias  >  Pagamento', font(26, True, True), C['acc'])
        text_c(d, (925, 360), 'O pagamento das férias ocorre', font(22))
        text_c(d, (925, 395), 'até 2 dias antes do início...', font(22))
    if k >= 3:
        text_c(d, (925, 450), 'contextual chunking', font(30, True), C['acc'])
    if k >= 5:
        text_c(d, (640, 560), 'the header carries the context along with the card', font(31, True), C['blue'])
    return img, d


# ---------- scene 8 · the result ----------
B8 = ['And what does the result look like?',
      'Each chunk is an object with an identifier, the source document, the section name, the text, already with the header, and the metadata: department, date, and title.',
      'Running the project, each document produces four chunks, one per section.',
      'The four documents together produce sixteen chunks.']
CHUNK = ['{', '  id: "ferias#0",', '  docId: "ferias",', '  source: "ferias.md",', '  section: "Direito a férias",',
         '  text: "Política de Férias > Direito a férias\\n...",', '  meta: { dept: "rh", updated: "2026-01-10",',
         '          title: "Política de Férias" }', '}']


def s8(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 85), 'What a chunk looks like', font(44, True))
    if k >= 2:
        bands = [(1, 4, BAND_TEAL), (5, 5, BAND_AMBER), (6, 7, BAND_BLUE)] if k == 2 else []
        ys = code_panel(d, 'one chunk (from ferias.md)', CHUNK, bands, size=24, y0=215, x1=850)
        if k == 2:
            text_l(d, (870, ys[2]), '←  who it is', font(24, True), C['acc'])
            text_l(d, (870, ys[5]), '←  text + header', font(24, True), C['warn'])
            text_l(d, (870, ys[6] + 17), '←  metadata', font(24, True), C['blue'])
    if k >= 3:
        rbox(d, (880, 150, 1244, 380), 'acc', hi=(k == 3))
        text_c(d, (1062, 195), 'each document', font(26, True), C['acc'])
        text_c(d, (1062, 260), '4 sections', font(34, True))
        text_c(d, (1062, 320), '→  4 chunks', font(34, True), C['acc'])
    if k >= 4:
        rbox(d, (880, 405, 1244, 595), 'blue', hi=True)
        text_c(d, (1062, 450), '4 documents', font(30, True), C['blue'])
        text_c(d, (1062, 520), '=  16 chunks', font(40, True), C['blue'])
    return img, d


# ---------- scene 9 · wrap-up ----------
B9 = ['To sum up: we cut each document into cards, respecting the sections.',
      'The limit is 600 characters, with 100 of overlap when a split is needed.',
      'And each card carries a header with the title and the section.',
      'In the next chapter, we will turn the text of each chunk into numbers, the embeddings.',
      'See you there!']


def s9(k):
    img, d = cv()
    text_c(d, (640, 100), 'See you there!' if k >= 5 else 'Summing up', font(56, True), C['acc'] if k >= 5 else C['ink'])
    rows = [('acc', '1   Cut each document by section'), ('box', '2   Limit: 600 characters  ·  overlap: 100'),
            ('warn', '3   Each chunk carries a "title > section" header'), ('blue', 'Next chapter:  turning chunks into numbers (embeddings)')]
    for i, (st, t) in enumerate(rows):
        if k >= i + 1:
            y = 170 + i * 110
            rbox(d, (150, y, 1130, y + 85), st, hi=(k == i + 1))
            text_l(d, (190, y + 42), t, font(29, True))
    return img, d


SCENES = [(B1, s1), (B2, s2), (B3, s3), (B4, s4), (B5, s5), (B6, s6), (B7, s7), (B8, s8), (B9, s9)]

if __name__ == '__main__':
    work = os.environ.get('VIDEO_WORKDIR', os.path.join(HERE, '_work', f'cap03_en_{VOICE}'))
    if len(sys.argv) > 1 and sys.argv[1] == 'preview':
        preview(SCENES, os.path.join(work, 'preview'))
        print('preview saved in', os.path.join(work, 'preview'))
    else:
        build(SCENES, os.path.join(HERE, 'saida', f'cap03_en_{VOICE}.mp4'), work, TAG)
