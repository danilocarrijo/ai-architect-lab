"""Chapter 5 · The index: storing vectors to search later (English, voice: Zira by default).

Usage:   python cap05_en.py preview
         python cap05_en.py                      # saida\\cap05_en_zira.mp4
         set VOICE=david && python cap05_en.py   # male voice
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
    (r'index\.json', 'index dot json'), (r'\.cache', 'dot cache'), (r'BM25', 'B M 25'), (r'pgvector', 'P G vector'),
    (r'Qdrant', 'quadrant'), (r'\bnpm\b', 'N P M'), (r'\bHR\b', 'H R'), (r'\bAPI\b', 'A P I'),
]
TAG = 'Chapter 5 · The index: storing vectors to search later'
NOTE = (130, 225, 215)


def cv():
    return canvas(TAG)


# ---------- scene 1 · opening ----------
B1 = ['Hello!',
      'We already have the chunks and the embeddings.',
      'But where do we store all of this, so we can search it later?',
      'In this chapter, you will meet the index: the warehouse of the vectors.',
      'And you will see how all the previous steps come together in a single function.']


def s1(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 200), 'The index', font(76, True))
    if k >= 4:
        text_c(d, (640, 282), 'the warehouse of the vectors', font(36), C['acc'])
    if k >= 2:
        box(d, 150, 355, 400, 90, 'Chapters 3 and 4', 'chunks + embeddings', 'box', hi=(k == 2), tsize=27, ssize=20)
    if k >= 3:
        arrow(d, [(565, 400), (715, 400)], C['ink'], 5)
        box(d, 730, 355, 400, 90, 'Chapter 5', 'where do we store them?', 'acc', hi=(k == 3), tsize=27, ssize=20)
    if k >= 5:
        text_c(d, (640, 540), 'All the previous steps, in a single function', font(32, True), C['muted'])
    return img, d


# ---------- scene 2 · the card-file analogy ----------
B2 = ['Think of a card file.',
      'Each card is a chunk, and, together with it, we store its address on the map, the embedding.',
      'When someone asks a question, we calculate the address of the question, and look for the cards that are closest.']
CARDS = [('ferias · Direito a férias', '[0.1, 0, 0.4, ...]'), ('ferias · Pagamento', '[0, 0.3, 0.1, ...]'),
         ('reembolso · Prazo', '[0.5, 0, 0, ...]'), ('ti-suporte · VPN', '[0, 0.2, 0.6, ...]')]


def s2(k):
    img, d = cv()
    text_c(d, (640, 90), 'The card-file analogy', font(48, True))
    if k >= 1:
        rbox(d, (60, 140, 1220, 590), 'box')
    if k >= 2:
        text_l(d, (110, 172), 'the card  (a chunk)', font(20, True), C['muted'])
        text_l(d, (490, 172), 'its address on the map  (embedding)', font(20, True), C['muted'])
        for i, (t, v) in enumerate(CARDS):
            y = 195 + i * 92
            near = (k >= 3 and i < 2)
            rbox(d, (95, y, 770, y + 72), 'acc' if near else 'box', hi=(near and k == 3))
            text_l(d, (115, y + 36), t, font(24, True))
            d.line((470, y + 10, 470, y + 62), fill=C['line'], width=2)
            text_l(d, (490, y + 36), v, font(23, False, True), C['acc'])
    if k >= 3:
        rbox(d, (830, 195, 1190, 300), 'warn', hi=True)
        text_c(d, (1010, 228), 'the question', font(26, True), C['warn'])
        text_c(d, (1010, 268), '[0.1, 0.1, 0.4, ...]', font(23, False, True), C['warn'])
        arrow(d, [(822, 247), (778, 231)], C['warn'], 4, head=11)
        arrow(d, [(822, 275), (778, 323)], C['warn'], 4, head=11)
        text_c(d, (1010, 370), 'closest cards', font(30, True), C['acc'])
        text_c(d, (1010, 410), 'highlighted on the left', font(21), C['muted'])
        text_c(d, (1135, 565), '(illustration)', font(18), C['muted'])
    return img, d


# ---------- scene 3 · the VectorStore stores ----------
B3 = ['In the code, this card file is the VectorStore class.',
      'It keeps a list of items.',
      'The add method receives the chunks and the vectors, and stores each chunk together with its matching vector.',
      'Simple as that: the text, the metadata, and the vector stay together, in the same item.']
VS = ['export class VectorStore {', '  constructor() {', '    this.items = [];', '  }', '  add(chunks, vectors) {',
      '    chunks.forEach((c, i) =>', '      this.items.push({ ...c, vector: vectors[i] }));', '  }', '}']


def s3(k):
    img, d = cv()
    bands = {2: [(2, 2, BAND_TEAL)], 3: [(4, 7, BAND_BLUE)]}.get(k, [])
    ys = code_panel(d, 'src/rag/vectorstore.js  (simplified)', VS, bands, size=21, x1=810)
    if k == 2:
        text_l(d, (830, ys[2]), '←  the list', font(24, True), NOTE)
    if k >= 4:
        rbox(d, (840, 150, 1244, 470), 'acc', hi=True)
        text_c(d, (1042, 190), 'one item', font(30, True), C['acc'])
        for i, (t, st) in enumerate([('text  +  header', 'box'), ('metadata  (dept, ...)', 'box'), ('vector  (512 numbers)', 'blue')]):
            rbox(d, (870, 230 + i * 70, 1214, 285 + i * 70), st)
            text_c(d, (1042, 258 + i * 70), t, font(23, True))
        text_c(d, (1042, 450), 'together, in the same item', font(22, True), C['muted'])
    return img, d


# ---------- scene 4 · searching ----------
B4 = ['To search, the search method receives the question vector and the number of results we want.',
      'It calculates the cosine between the question and the vector of every chunk, sorts from the most similar to the least similar, and returns the first ones.',
      'It is exactly the cosine we saw in the previous chapter.']
SEARCH = ['search(qVec, k, allow) {', '  return this.items', '    .filter((i) => !allow || allow.has(i.id))',
          '    .map((i) => ({ id: i.id, score: cosine(qVec, i.vector) }))', '    .sort((a, b) => b.score - a.score)',
          '    .slice(0, k);', '}']


def s4(k):
    img, d = cv()
    bands = {1: [(0, 0, BAND_TEAL)], 2: [(3, 5, BAND_BLUE)], 3: [(3, 3, BAND_AMBER)]}.get(k, [])
    ys = code_panel(d, 'src/rag/vectorstore.js', SEARCH, bands, size=22, line_h=38, y0=212)
    if k == 1:
        text_l(d, (700, ys[0]), '←  question vector, how many results', font(23, True), NOTE)
    if k == 2:
        text_l(d, (910, ys[3]), '←  cosine with each chunk', font(21, True), NOTE)
        text_l(d, (910, ys[4]), '←  most similar first', font(21, True), NOTE)
        text_l(d, (910, ys[5]), '←  keep the top k', font(21, True), NOTE)
    if k == 3:
        text_l(d, (910, ys[3]), '←  the cosine from Chapter 4', font(21, True), (255, 200, 120))
    return img, d


# ---------- scene 5 · metadata filter ----------
B5 = ['There is also a filter by metadata.',
      'The filterIds method returns only the chunks whose header matches the filter, for example, department equals HR.',
      'This filter happens before the search, and that is important:',
      'besides reducing the work, it is the basis for access control, because documents from a department you cannot see are never even compared.']
DOCS = [('ferias', 'rh'), ('home-office', 'rh'), ('reembolso', 'financeiro'), ('ti-suporte', 'ti')]


def s5(k):
    img, d = cv()
    text_c(d, (640, 90), 'The metadata filter', font(48, True))
    if k >= 1:
        for i, (n, dept) in enumerate(DOCS):
            x = 60 + i * 295
            on = (k >= 2 and dept == 'rh')
            off = (k >= 2 and dept != 'rh')
            rbox(d, (x, 160, x + 270, 290), 'acc' if on else 'box', hi=(on and k == 2))
            col = C['line'] if off else C['ink']
            text_c(d, (x + 135, 205), n + '.md', font(25, True, True), col)
            text_c(d, (x + 135, 255), 'dept: ' + dept, font(23, False, True), C['line'] if off else C['muted'])
    if k >= 2:
        rbox(d, (330, 325, 950, 385), 'blue')
        text_c(d, (640, 355), "filter:   { dept: 'rh' }", font(30, True, True), C['blue'])
    if k >= 3:
        box(d, 130, 440, 430, 80, 'first: the filter', '', 'blue', hi=(k == 3), tsize=27)
        arrow(d, [(575, 480), (705, 480)], C['ink'], 5)
        box(d, 720, 440, 430, 80, 'then: the search', '', 'acc', hi=(k == 3), tsize=27)
    if k >= 4:
        text_c(d, (640, 565), 'less work   ·   the basis for access control', font(30, True), C['acc'])
        text_c(d, (640, 603), '(today the project does not check who is asking)', font(20), C['muted'])
    return img, d


# ---------- scene 6 · the whole ingestion ----------
B6 = ["Now, let's put everything together.",
      'The buildIndex function does the whole ingestion, in five steps.',
      'It reads the documents.',
      'Cuts them into chunks.',
      'Turns each chunk into a vector.',
      'Stores everything in the VectorStore.',
      'And saves it to disk.',
      'Each step is a stage you have already studied.',
      'When it runs, the project prints: four documents, sixteen chunks, and the name of the embedder used.']
STEPS = [('loadDocuments', 'reads the .md files', 'box', 'Chapter 2'), ('chunkDocument', 'cuts into chunks', 'acc', 'Chapter 3'),
         ('embedder.embed', 'text → vector', 'acc', 'Chapter 4'), ('store.add', 'chunk + vector', 'blue', 'this chapter'),
         ('store.save', 'writes index.json', 'blue', 'this chapter')]


def s6(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 85), 'buildIndex()', font(52, True, True), C['acc'])
        text_c(d, (640, 138), 'the whole ingestion in one function', font(26), C['muted'])
    for i, (t, sub, st, ch) in enumerate(STEPS):
        if k >= i + 3:
            x = 43 + i * 246
            box(d, x, 190, 210, 90, t, sub, st, hi=(k == i + 3), tsize=21, ssize=16)
            if i:
                arrow(d, [(x - 32, 235), (x - 6, 235)], C['ink'], 4, head=10)
            if k >= 8:
                text_c(d, (x + 105, 305), ch, font(21, True), C['muted'])
    if k >= 9:
        d.rounded_rectangle((90, 350, 1190, 520), 18, fill=C['code_bg'])
        text_l(d, (125, 395), '$ npm run ingest', font(30, False, True), (150, 170, 185))
        text_l(d, (125, 460), '4 documentos -> 16 chunks (embedder: local-hash-512)', font(30, True, True), NOTE)
    return img, d


# ---------- scene 7 · saving and loading ----------
B7 = ['The index is saved in a file called index.json, inside the .cache folder.',
      'Together with the vectors, the file records the name of the embedder.',
      'There is a reason for that: vectors from different embedders cannot be compared.',
      'So, when loading, if the name does not match, the system refuses the file and rebuilds the index.',
      'The same happens if the file does not exist yet.',
      'And one detail: the word index, the BM25, which we will see in the next chapter, is not saved to disk.',
      'It is built in memory, every time the system loads.']


def s7(k):
    img, d = cv()
    if k >= 1:
        rbox(d, (60, 150, 600, 350), 'blue', hi=(k == 1))
        text_c(d, (330, 182), '.cache/index.json', font(26, True, True), C['blue'])
        if k == 2:
            d.rectangle((75, 232, 585, 268), fill=(255, 226, 170))
        for i, t in enumerate(['{', '  "embedder": "local-hash-512",', '  "items": [ ... 16 chunks + vectors ]', '}']):
            text_l(d, (90, 215 + i * 36), t, font(22, False, True))
    if k >= 3:
        rbox(d, (60, 372, 600, 452), 'warn', hi=(k == 3))
        text_c(d, (330, 398), 'saved with: voyage-3    now: local-hash-512', font(22, True, True), C['warn'])
        text_c(d, (330, 430), 'vectors not comparable', font(22), C['warn'])
    if k >= 4:
        box(d, 660, 150, 570, 60, 'load the index', '', 'box', tsize=26)
        arrow(d, [(945, 213), (945, 240)], C['ink'], 4, head=10)
        box(d, 660, 243, 570, 68, 'same embedder name?', '', 'warn', hi=(k == 4), tsize=26)
        arrow(d, [(780, 314), (780, 350)], C['acc'], 4, head=10)
        arrow(d, [(1100, 314), (1100, 350)], C['warn'], 4, head=10)
        box(d, 660, 352, 270, 70, 'yes: use it', '', 'acc', tsize=24)
        box(d, 960, 352, 270, 70, 'no: refuse + rebuild', '', 'warn', hi=(k == 4), tsize=22)
    if k >= 5:
        rbox(d, (960, 450, 1230, 505), 'box', hi=(k == 5))
        text_c(d, (1095, 478), 'file missing', font(24, True))
        arrow(d, [(1095, 447), (1095, 427)], C['warn'], 4, head=10)
    if k >= 6:
        rbox(d, (60, 482, 600, 592), 'box', hi=(k == 6))
        dashed(d, (60, 482), (600, 482), C['muted'], 3)
        text_c(d, (330, 508), 'BM25  (word index)', font(26, True))
        text_c(d, (330, 541), 'NOT saved to disk', font(23, True), C['warn'])
    if k >= 7:
        text_c(d, (330, 572), 'built in memory, at every load', font(22, True), C['acc'])
    return img, d


# ---------- scene 8 · honest limit ----------
B8 = ['An honest limit: our VectorStore compares the question with every chunk.',
      'With sixteen, it is instant.',
      'With millions, it would be slow.',
      'In production, vector databases are used, like pgvector or Qdrant, with approximate indexes.',
      'The idea is the same; only the speed changes.']


def s8(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 90), 'An honest limit', font(48, True), C['warn'])
        text_c(d, (640, 150), 'compare the question with every chunk', font(30, True), C['muted'])
    if k >= 2:
        rbox(d, (60, 200, 620, 440), 'acc', hi=(k == 2))
        text_c(d, (340, 250), '16 chunks', font(44, True), C['acc'])
        text_c(d, (340, 320), 'instant', font(38, True))
    if k >= 3:
        rbox(d, (660, 200, 1220, 440), 'warn', hi=(k == 3))
        text_c(d, (940, 250), 'millions of chunks', font(40, True), C['warn'])
        text_c(d, (940, 320), 'slow', font(38, True), C['warn'])
    if k >= 4:
        rbox(d, (150, 470, 1130, 545), 'blue', hi=(k == 4))
        text_c(d, (640, 508), 'production:  a vector database  (pgvector, Qdrant)  +  approximate index', font(26, True), C['blue'])
    if k >= 5:
        text_c(d, (640, 590), 'same idea   ·   only the speed changes', font(30, True), C['acc'])
    return img, d


# ---------- scene 9 · wrap-up ----------
B9 = ['To sum up: the index stores each chunk with its vector, and searches for the most similar ones.',
      'buildIndex puts all the steps together and saves the result to disk.',
      'And a warning: if you edit a document, the index does not update by itself.',
      'You need to run the command npm run ingest again.',
      'In the next chapter, we will see the real search: two methods working together.',
      'See you there!']


def s9(k):
    img, d = cv()
    text_c(d, (640, 100), 'See you there!' if k >= 6 else 'Summing up', font(56, True), C['acc'] if k >= 6 else C['ink'])
    rows = [(1, 'acc', '1   Index = each chunk + its vector, searched by similarity'),
            (2, 'box', '2   buildIndex: all the steps  →  saved to disk'),
            (3, 'warn', '3   Edited a document?   →   run   npm run ingest   again'),
            (5, 'blue', 'Next chapter:  the real search, two methods together')]
    for i, (kk, st, t) in enumerate(rows):
        if k >= kk:
            y = 170 + i * 110
            rbox(d, (130, y, 1150, y + 85), st, hi=(k in (kk, 4) and i == 2) or (k == kk and i != 2))
            text_l(d, (170, y + 42), t, font(27, True))
    return img, d


SCENES = [(B1, s1), (B2, s2), (B3, s3), (B4, s4), (B5, s5), (B6, s6), (B7, s7), (B8, s8), (B9, s9)]

if __name__ == '__main__':
    work = os.environ.get('VIDEO_WORKDIR', os.path.join(HERE, '_work', f'cap05_en_{VOICE}'))
    if len(sys.argv) > 1 and sys.argv[1] == 'preview':
        preview(SCENES, os.path.join(work, 'preview'))
        print('preview saved in', os.path.join(work, 'preview'))
    else:
        build(SCENES, os.path.join(HERE, 'saida', f'cap05_en_{VOICE}.mp4'), work, TAG)
