"""Chapter 17 · From laboratory to production (English, voice: Zira by default)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine  # noqa: E402
from engine import C, arrow, box, build, canvas, font, preview, rbox, text_c, text_l  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
VOICES = {'zira': 'Microsoft Zira Desktop', 'david': 'Microsoft David Desktop'}
VOICE = os.environ.get('VOICE', 'zira').lower()
engine.SINGLE_VOICE = VOICES[VOICE]
engine.SPEECH = [
    (r'\bBM25\b', 'B M twenty five'), (r'pgvector', 'P G vector'), (r'Qdrant', 'Quadrant'), (r'\bAPI\b', 'A P I'), (r'\bLLM\b', 'L L M'),
    (r'\bHTTP\b', 'H T T P'), (r'PostgreSQL', 'Postgres Q L'), (r'OpenSearch', 'Open Search'), (r'LangSmith', 'Lang Smith'),
    (r'Langfuse', 'Lang fuse'), (r'OpenTelemetry', 'Open Telemetry'), (r'\bRedis\b', 'Redis'), (r'embed\(texts\)', 'embed texts'),
    (r'LocalHashEmbedder', 'Local Hash Embedder'), (r'VoyageEmbedder', 'Voyage Embedder'), (r'\bnpm\b', 'N P M'),
    (r'LangGraph', 'Lang Graph'), (r'client\.js', 'client dot J S'),
]
TAG = 'Chapter 17 · From laboratory to production'
NOTE = (130, 225, 215)
WARN_L = (255, 200, 120)


def cv():
    return canvas(TAG)


B1 = ['Hello!',
      'This project is a laboratory: it exists to help you understand the architecture.',
      'A production system has the same architecture, but each piece is swapped for a sturdier version, and new layers appear.',
      'Think of a model building, and the real building.']


def s1(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 195), 'Laboratory → production', font(66, True))
    if k >= 2:
        box(d, 150, 330, 400, 100, 'Laboratory', 'to understand', 'acc', hi=(k == 2), tsize=30, ssize=20)
    if k >= 3:
        box(d, 730, 330, 400, 100, 'Production', 'same plan, sturdier parts', 'blue', hi=(k == 3), tsize=30, ssize=20)
    if k >= 4:
        text_c(d, (640, 520), 'a cardboard model   →   the real building', font(30, True), C['muted'])
    return img, d


B2 = ['The good news: the project was written so that these swaps stay local.',
      'Each piece has an interface, a format of input and output, and the rest of the code only knows the interface.',
      'You already saw this with the embedder: the local one and the Voyage one have the same embed method.',
      'So swapping one for the other touches nothing else.']


def s2(k):
    img, d = cv()
    text_c(d, (640, 70), 'Swaps stay local', font(48, True))
    if k >= 2:
        rbox(d, (60, 130, 1220, 230), 'blue', hi=(k == 2))
        text_c(d, (640, 165), 'each piece = an interface', font(30, True), C['blue'])
        text_c(d, (640, 205), 'the rest of the code knows only the interface', font(23))
    if k >= 3:
        box(d, 90, 290, 330, 90, 'LocalHashEmbedder', 'embed(texts)', 'acc', hi=(k == 3), tsize=21, ssize=20)
        box(d, 860, 290, 330, 90, 'VoyageEmbedder', 'embed(texts)', 'warn', hi=(k == 3), tsize=22, ssize=20)
        arrow(d, [(445, 320), (835, 320)], C['ink'], 4, head=11)
        arrow(d, [(835, 352), (445, 352)], C['ink'], 4, head=11)
    if k >= 4:
        rbox(d, (200, 440, 1080, 520), 'acc', hi=True)
        text_c(d, (640, 480), 'swap one for the other  →  nothing else changes', font(28, True), C['acc'])
    return img, d


SWAPS = [('Embeddings', 'word hash', 'neural model', 'VoyageEmbedder exists'), ('Vector store', 'JSON file in memory', 'vector database', 'same methods'),
         ('BM25', 'hand-made', 'database full-text', 'keep search()'), ('Rerank', 'word coverage', 'cross-encoder or LLM', 'only rerank()'),
         ('LLM', 'complete()', 'retries and fallback', 'only client.js'), ('Guardrails', 'regular expressions', 'regex + AI classifier', 'inside checkInput'),
         ('Cache', 'in memory', 'shared store, e.g. Redis', 'get and set'), ('Trace', 'terminal report', 'observability tool', 'TracerHandler'),
         ('Tickets', 'simulated array', 'real ticket API', 'only run()')]
B3 = ['Piece by piece, here is what changes.',
      'Embeddings: from a word hash, to a neural model that understands synonyms. The Voyage class already exists.',
      'The vector store: from a file in memory, to a vector database.',
      'B M twenty five: from hand-made, to the full-text search of the database.',
      'Rerank: from word coverage, to a dedicated model.',
      'The L L M: the same, plus retries and a fallback, all inside client dot J S.',
      'Guardrails: regular expressions, plus an A I classifier.',
      'The cache: from memory, to a shared store, invalidated when you reindex.',
      'The trace: from a terminal report, to an observability tool. The tracer handler is the connection point.',
      'And the tickets: from a simulated array, to the real ticket system. Only the body of run changes.']


def s3(k):
    img, d = cv()
    text_c(d, (640, 55), 'Piece by piece', font(42, True))
    text_l(d, (60, 105), 'piece', font(20, True), C['muted'])
    text_l(d, (270, 105), 'laboratory', font(20, True), C['acc'])
    text_l(d, (560, 105), 'production', font(20, True), C['blue'])
    text_l(d, (940, 105), 'what to touch', font(20, True), C['warn'])
    for i, (p, a, b, c) in enumerate(SWAPS):
        if k >= i + 2:
            y = 130 + i * 55
            rbox(d, (40, y, 1240, y + 48), 'acc' if k == i + 2 else 'box', r=8)
            text_l(d, (60, y + 24), p, font(21, True))
            text_l(d, (270, y + 24), a, font(19, False, True))
            text_l(d, (560, y + 24), b, font(19, False, True), C['blue'])
            text_l(d, (940, y + 24), c, font(18, False, True), C['warn'])
    return img, d


MISSING = [('HTTP interface', 'today: terminal and MCP only'), ('Authentication', 'dept would come from user identity'),
           ('Conversation memory', 'each question is independent'), ('Incremental reindex', 'today: npm run ingest rebuilds all'),
           ('Human approval', 'not implemented (hooks show where)'), ('Streaming + resilience', 'retries, rate limits'),
           ('Answer evaluation', 'today: retrieval only'), ('Operations', 'deploy, alerts, audit log')]
B4 = ['Now, what a real system has, and this project does not.',
      'These are whole layers, and none of them swaps a piece: they are additions.',
      'An H T T P interface, because today there is only the terminal and M C P.',
      'Authentication and permissions: the department filter exists, but nobody checks who is asking.',
      'Conversation memory: today, every question is independent.',
      'Incremental reindexing: today, ingest rebuilds everything.',
      'Human approval before risky tools. The hooks chapter shows where it plugs in, but it is not implemented.',
      'Streaming and resilience.',
      'Answer evaluation, because the eval measures only the search.',
      'And operations: deployment, alerts, and an audit log.']


def s4(k):
    img, d = cv()
    text_c(d, (640, 55), 'What a real system adds', font(42, True))
    if k >= 2:
        text_c(d, (640, 100), 'not swaps: additions', font(22), C['muted'])
    for i, (t, sub) in enumerate(MISSING):
        if k >= i + 3:
            col, row = i % 2, i // 2
            x = 40 + col * 600
            y = 135 + row * 118
            box(d, x, y, 580, 100, t, sub, 'warn' if i == 4 else 'box', hi=(k == i + 3), tsize=24, ssize=18)
    return img, d


ORDER = [('1', 'Run with a real key and a neural embedder', 'then run ingest and eval: confirms the real paths', 'acc'),
         ('2', 'Grow the golden set', 'hard questions: synonyms, acronyms, ambiguity', 'blue'),
         ('3', 'Swap the vector store for a real database', 'follow the interface', 'warn'),
         ('4', 'Put an HTTP API in front', 'a small server that calls ask()', 'acc'),
         ('5', 'Add conversation memory', 'first in the LangGraph engine', 'blue'),
         ('6', 'Connect external observability', 'send the trace to a dedicated tool', 'warn')]
B5 = ['If you wanted to take the project further, this order gives the biggest gain first.',
      'One: run with a real key and a neural embedder, then ingest and evaluate. This confirms the paths that, today, were only tested with fake models.',
      'Two: grow the golden set with hard questions.',
      'Three: swap the vector store for a real database.',
      'Four: put an H T T P A P I in front.',
      'Five: add conversation memory.',
      'Six: connect external observability.',
      'Notice that steps one and two need almost no code, and they teach the most. In A I systems, measure before you optimize.']


def s5(k):
    img, d = cv()
    text_c(d, (640, 55), 'A sensible order', font(44, True))
    for i, (n, t, sub, st) in enumerate(ORDER):
        if k >= i + 2:
            y = 105 + i * 82
            rbox(d, (60, y, 1220, y + 70), st, hi=(k == i + 2), r=12)
            text_l(d, (85, y + 35), n, font(30, True), C[st])
            text_l(d, (135, y + 22), t, font(23, True))
            text_l(d, (135, y + 51), sub, font(17), C['muted'])
    if k >= 8:
        text_c(d, (640, 606), 'measure before you optimize', font(24, True), NOTE)
    return img, d


B6 = ['To sum up: why does the project not need to be rewritten for production?',
      'Because each piece talks to the others through a stable interface.',
      'What changes is the inside of each file. The architecture stays.',
      'In the next chapter, we build the whole application from zero, file by file. See you there!']


def s6(k):
    img, d = cv()
    text_c(d, (640, 90), 'See you there!' if k >= 4 else 'Summing up', font(52, True), C['acc'] if k >= 4 else C['ink'])
    rows = [(2, 'acc', 'Stable interfaces:  embed(texts) · search(...) · complete(...)'), (3, 'blue', 'Swap the inside of a file  ·  the architecture stays'),
            (4, 'box', 'Next chapter:  building the app from zero, file by file')]
    for i, (kk, st, t) in enumerate(rows):
        if k >= kk:
            y = 190 + i * 115
            rbox(d, (110, y, 1170, y + 88), st, hi=(k == kk))
            text_l(d, (150, y + 44), t, font(26, True))
    return img, d


SCENES = [(B1, s1), (B2, s2), (B3, s3), (B4, s4), (B5, s5), (B6, s6)]

if __name__ == '__main__':
    work = os.environ.get('VIDEO_WORKDIR', os.path.join(HERE, '_work', f'cap17_en_{VOICE}'))
    if len(sys.argv) > 1 and sys.argv[1] == 'preview':
        preview(SCENES, os.path.join(work, 'preview'))
        print('preview saved in', os.path.join(work, 'preview'))
    else:
        build(SCENES, os.path.join(HERE, 'saida', f'cap17_en_{VOICE}.mp4'), work, TAG)
