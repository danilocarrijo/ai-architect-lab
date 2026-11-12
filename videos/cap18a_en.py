"""Chapter 18, part A · Building the app from zero: steps 1 to 10 (English, voice: Zira by default)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cap18_common as cc  # noqa: E402
from cap18_common import C, NOTE, box, canvas, font, make_scene, rbox, text_c, text_l  # noqa: E402
from engine import build, preview  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
TAG = 'Chapter 18a · Building it from zero'
VOICE = cc.VOICE


def cv():
    return canvas(TAG)


B1 = ['Hello!',
      'Now, a different kind of chapter: we build the whole application from zero, file by file.',
      'There are twenty steps. In this first part, we do steps one to ten. In the second part, steps eleven to twenty.',
      'Each step creates files, explains what they do, and ends with a check you can run.']


def s1(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 190), 'Building it from zero', font(66, True))
    if k >= 2:
        text_c(d, (640, 275), 'file by file, in the right order', font(34), C['acc'])
    if k >= 3:
        box(d, 150, 380, 420, 100, 'Part A', 'steps 1 to 10', 'acc', hi=(k == 3), tsize=32, ssize=22)
        box(d, 710, 380, 420, 100, 'Part B', 'steps 11 to 20', 'blue', hi=(k == 3), tsize=32, ssize=22)
    if k >= 4:
        text_c(d, (640, 550), 'create files  ·  understand them  ·  run a check', font(28, True), C['muted'])
    return img, d


B2 = ['Three rules of the game.',
      'One: the order matters. Each file only uses files that were created before it.',
      'Two: if you see "cannot find module", a file is missing, or a path has a typo.',
      'Three: without an A P I key, everything works, except the generation by the model, and the agent. The checks need no key.',
      'The whole source is about one thousand lines of code, across thirty two files.']


def s2(k):
    img, d = cv()
    text_c(d, (640, 70), 'Three rules', font(46, True))
    rows = [(2, 'acc', '1   The order matters', 'each file only uses files created before it'),
            (3, 'blue', '2   "Cannot find module"', 'a file is missing, or a path has a typo'),
            (4, 'warn', '3   No API key needed for the checks', 'only the model generation and the agent need one')]
    for i, (kk, st, t, sub) in enumerate(rows):
        if k >= kk:
            y = 140 + i * 120
            box(d, 100, y, 1080, 100, t, sub, st, hi=(k == kk), tsize=29, ssize=21)
    if k >= 5:
        text_c(d, (640, 540), 'about 1,000 lines of source  ·  32 files', font(30, True), NOTE)
    return img, d


# (n, title, files, purpose lines, uses, verify lines, beats)
STEPS = [
    (1, 'Prepare the project', [('package.json', 27)],
     ['Folders, scripts (start, ingest, eval, test, mcp)', 'and all the libraries, installed once'], '', ['npm install finishes without errors'],
     ['Step one: prepare the project.', 'You create the folders, and the package dot json file, with twenty seven lines.',
      'It defines the scripts, like start, ingest, eval, test, and mcp, and lists the libraries, including LangChain, used only in step nineteen.',
      'The check: run npm install, and it finishes without errors.']),
    (2, 'Write the documents', [('data/ferias.md', 18), ('data/home-office.md', 18), ('data/reembolso.md', 18), ('data/ti-suporte.md', 18)],
     ['The raw material: four policies, in Markdown,', 'each one with four sections marked by ##'], '', ['4 files in data/, 18 lines each'],
     ['Step two: write the documents.', 'Four Markdown files, with eighteen lines each: vacation, home office, reimbursement, and IT support.',
      'This is the raw material. Each one has four sections, marked with two hash signs, and the next steps cut the text exactly there.',
      'The check: four files in the data folder.']),
    (3, 'Configuration and text utilities', [('src/config.js', 17), ('src/rag/text.js', 14)],
     ['Every knob in one place: chunk size 600, overlap 100,', 'topK 4, cache threshold 0.92', 'plus tokenize: lower case, no accents, no stop words'], '',
     ['tokenize("Quantos dias de férias eu tenho?")', '→ quant · dias · feria · eu · tenho'],
     ['Step three: configuration and text utilities.', 'Two small files: config dot J S, with seventeen lines, and text dot J S, with fourteen.',
      'The config gathers every knob in one place: chunk size, overlap, top k, and the cache threshold. The text file turns a sentence into clean words.',
      'The check: the question about vacation days becomes five tokens.']),
    (4, 'Load and cut the documents', [('src/rag/loader.js', 22), ('src/rag/chunker.js', 41)],
     ['The loader reads data/*.md and splits metadata', 'The chunker cuts by ## sections, up to 600 characters'], 'config, text', ['4 documents  →  16 chunks (4 sections each)'],
     ['Step four: load and cut the documents.', 'The loader, with twenty two lines, reads the files. The chunker, with forty one, cuts each document by section.',
      'A section is never cut in the middle without need: the limit is six hundred characters, with an overlap of one hundred.',
      'The check: four documents become sixteen chunks.']),
    (5, 'Embeddings: text into numbers', [('src/rag/embeddings.js', 57)],
     ['LocalHashEmbedder: 512 dimensions, no network', 'VoyageEmbedder: optional, with a key', 'createEmbedder() picks one'], 'text', ['similar texts score high, unrelated texts 0.000'],
     ['Step five: embeddings, which turn text into numbers.', 'One file with fifty seven lines.',
      'The local embedder has five hundred twelve dimensions and needs no network. The Voyage one is optional. And a factory function picks which one to use.',
      'The check: similar texts have a high cosine, and unrelated texts, zero.']),
    (6, 'Store vectors, search by words', [('src/rag/vectorstore.js', 41), ('src/rag/bm25.js', 33)],
     ['VectorStore: add, save, load, search by cosine', 'BM25: search by exact words, with scores'], 'embeddings', ['BM25("resetar senha")  →  ti-suporte#0, score 6.089'],
     ['Step six: store the vectors, and search by words.', 'The vector store, with forty one lines, and B M twenty five, with thirty three.',
      'One finds by meaning, with cosine similarity. The other finds by exact words. Together, they will be the hybrid search.',
      'The check: searching for "resetar senha" returns the IT support document first, with score six point zero eight nine.']),
    (7, 'Hybrid search and ingest', [('src/rag/retriever.js', 46), ('src/rag/index.js', 35)],
     ['HybridRetriever: vector + BM25, merged by RRF,', 'reranked, then cut', 'buildIndex() and loadRetriever()'], 'steps 4 to 6',
     ['npm run ingest', '4 documentos -> 16 chunks (embedder: local-hash-512)'],
     ['Step seven: the hybrid search, and the ingest.', 'The retriever, with forty six lines, and the index file, with thirty five.',
      'The retriever merges the two searches by rank, reranks, and cuts. The index file builds the index, and loads it later.',
      'The check: npm run ingest prints four documents, sixteen chunks.']),
    (8, 'Guardrails', [('src/guardrails/index.js', 38)],
     ['checkInput: blocks injection, hides PII', 'sanitizeContext: removes hostile lines', 'checkOutput: requires a valid citation'], '', ['4 tests in test/guardrails.test.js'],
     ['Step eight: guardrails.', 'One file, with thirty eight lines, and three inspectors: for the input, for the retrieved content, and for the output.',
      'It blocks prompt injection, hides personal data, removes hostile lines, and requires a valid citation.',
      'The check: the four guardrail tests.']),
    (9, 'Observability: the Tracer', [('src/observability/trace.js', 33)],
     ['Spans with time, addUsage for tokens,', 'costUSD from the pricing table, a text report'], 'config', ['1200 in + 300 out tokens  →  US$ 0.0081'],
     ['Step nine: observability, with the Tracer.', 'One file, thirty three lines.',
      'It measures the time of each step, counts tokens, and computes the cost with the price table, then prints a report.',
      'The check: twelve hundred tokens in, and three hundred out, cost eighty one ten-thousandths of a dollar.']),
    (10, 'Semantic cache', [('src/rag/cache.js', 19)],
     ['Reuses an answer when a new question is', 'almost identical: cosine ≥ 0.92, TTL 10 minutes'], 'embeddings, config', ['cosine: same text 1.000 · near 0.672 · unrelated 0.015 / 0.000'],
     ['Step ten: the semantic cache.', 'One file, nineteen lines.',
      'It saves answers, and returns one again when a new question is almost identical: cosine at least zero point nine two, within ten minutes.',
      'The check: the same text scores one. The cache only answers when the score is above the threshold.']),
]

B3 = ['That is the first half: ten steps, and about four hundred lines.',
      'You now have the whole retrieval pipeline: documents, chunks, vectors, hybrid search, guardrails, tracer, and cache.',
      'In part B, we add the model, the question flow, the evaluation, the agent, the M C P server, the command line, the second engine, and the tests.',
      'See you there!']


def s_end(k):
    img, d = cv()
    text_c(d, (640, 90), 'See you in part B!' if k >= 4 else 'Half way there', font(52, True), C['acc'] if k >= 4 else C['ink'])
    rows = [(2, 'acc', 'Done:  documents · chunks · vectors · hybrid search'), (2, 'acc', 'Done:  guardrails · tracer · semantic cache'),
            (3, 'blue', 'Next:  model · ask · eval · agents · MCP · CLI · LangGraph · tests')]
    for i, (kk, st, t) in enumerate(rows):
        if k >= kk:
            y = 190 + i * 110
            rbox(d, (110, y, 1170, y + 86), st, hi=(k == kk))
            text_l(d, (150, y + 43), t, font(25, True))
    return img, d


SCENES = [(B1, s1), (B2, s2)] + [(s[6], make_scene(s, TAG)[1]) for s in STEPS] + [(B3, s_end)]

if __name__ == '__main__':
    work = os.environ.get('VIDEO_WORKDIR', os.path.join(HERE, '_work', f'cap18a_en_{VOICE}'))
    if len(sys.argv) > 1 and sys.argv[1] == 'preview':
        preview(SCENES, os.path.join(work, 'preview'))
        print('preview saved in', os.path.join(work, 'preview'))
    else:
        build(SCENES, os.path.join(HERE, 'saida', f'cap18a_en_{VOICE}.mp4'), work, TAG)
