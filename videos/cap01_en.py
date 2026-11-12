"""Chapter 1 · The journey of a question (English version, same slides as cap01.py).

Usage:   python cap01_en.py preview
         python cap01_en.py                 # voice: Microsoft Zira (default)
         set VOICE=david && python cap01_en.py    # or the male voice, Microsoft David
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine  # noqa: E402
from engine import C, arrow, box, build, canvas, font, preview, rbox, text_c, text_l  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
VOICES = {'zira': 'Microsoft Zira Desktop', 'david': 'Microsoft David Desktop'}
VOICE = os.environ.get('VOICE', 'zira').lower()
engine.SINGLE_VOICE = VOICES[VOICE]          # the English voice reads EVERYTHING
# Spoken-only fixes (the subtitles keep the original text): acronyms and file names the voice would mangle.
engine.SPEECH = [
    (r'\bMCP\b', 'M C P'), (r'cli\.js', 'C L I dot J S'), (r'\bnpm\b', 'N P M'), (r'\bRAG\b', 'rag'),
    (r'runAgent', 'run agent'),
]

TAG = 'Chapter 1 · The journey of a question'


def cv():
    return canvas(TAG)


# ---------- reusable pieces: the two "lanes" of the chapter diagram ----------
LANE1 = [('Documents', 'data/*.md', 'box'), ('Chunks', 'pieces per section', 'acc'),
         ('Embeddings', 'text becomes numbers', 'acc'), ('Index', '.cache/index.json', 'blue')]
LANE2 = [('Question', 'from the user', 'box'), ('Guardrail', 'input', 'warn'), ('Search', 'right chunks', 'acc'),
         ('Prompt', 'sources + question', 'box'), ('LLM', 'writes the answer', 'acc'),
         ('Guardrail', 'output', 'warn'), ('Answer', 'with [citation]', 'box')]
L1X, L1W = [65, 371, 677, 983], 250
L2X, L2W = [57 + i * 170 for i in range(7)], 146


def lane1(d, n, hi=None, y=190, h=96, tsize=24, ssize=17):
    for i, (t, s, st) in enumerate(LANE1[:n]):
        box(d, L1X[i], y, L1W, h, t, s, st, hi=(hi == i), tsize=tsize, ssize=ssize)
        if i:
            arrow(d, [(L1X[i - 1] + L1W + 8, y + h / 2), (L1X[i] - 8, y + h / 2)], C['ink'], 4, head=12)


def lane2(d, shown, hi=None, y=430, h=96):
    for i, (t, s, st) in enumerate(LANE2):
        if i in shown:
            box(d, L2X[i], y, L2W, h, t, s, st, hi=(hi == i), tsize=22, ssize=15)
            if i - 1 in shown:
                arrow(d, [(L2X[i - 1] + L2W + 3, y + h / 2), (L2X[i] - 3, y + h / 2)], C['ink'], 3, head=9)


# ---------- scene 1 · opening ----------
B1 = ['Hello!',
      'In this chapter, you will follow the journey of a question inside our helpdesk assistant.',
      'From the moment someone types a question, until the answer shows up on screen, with its source cited.',
      'By the end, you will know the steps, and the order they happen in.']


def s1(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 235), 'The journey of a question', font(68, True))
    if k >= 2:
        text_c(d, (640, 318), 'inside the helpdesk assistant', font(36), C['acc'])
    if k >= 3:
        box(d, 150, 395, 340, 96, 'User question', '', 'box', hi=(k == 3), tsize=27)
        arrow(d, [(505, 443), (775, 443)], C['ink'], 5)
        box(d, 790, 395, 340, 96, 'Answer with cited source', '', 'acc', hi=(k == 3), tsize=25)
    if k >= 4:
        text_c(d, (640, 560), 'Which steps   ·   In what order', font(30, True), C['muted'])
    return img, d


# ---------- scene 2 · the problem and RAG ----------
B2 = ['First, a quick reminder.',
      "A language model, like Claude or Gemini, writes text very well, but it does not know your company's rules.",
      'If you ask how many vacation days you are entitled to, it may make up an answer that sounds right, and is wrong.',
      'The solution is called RAG.',
      'The idea is simple: before answering, the system looks up the right passages in the company documents, and hands those passages to the model.',
      'Like an open-book exam.']


def s2(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 95), 'A quick reminder', font(46, True))
    if k >= 2:
        rbox(d, (60, 150, 610, 590), 'box')
        text_c(d, (335, 200), 'Language model', font(32, True), C['blue'])
        text_l(d, (100, 270), '•  Writes text very well', font(27))
        text_l(d, (100, 325), "•  Doesn't know company rules", font(27))
    if k >= 3:
        rbox(d, (90, 385, 580, 565), 'warn', hi=(k == 3))
        text_c(d, (335, 428), '"How many vacation days do I get?"', font(25, True))
        text_c(d, (335, 485), 'Made-up answer:', font(26, True), C['warn'])
        text_c(d, (335, 525), 'sounds right, but is wrong', font(25), C['warn'])
    if k >= 4:
        rbox(d, (670, 150, 1220, 590), 'acc', hi=(k == 4))
        text_c(d, (945, 205), 'RAG', font(54, True), C['acc'])
        text_c(d, (945, 255), 'Retrieval-Augmented Generation', font(21), C['muted'])
    if k >= 5:
        for i, s in enumerate(['1   Search the documents', '2   Hand the passages to the model', '3   Answer based on them']):
            text_l(d, (705, 330 + i * 65), s, font(27))
    if k >= 6:
        text_c(d, (945, 540), 'like an open-book exam', font(26, True), C['acc'])
    return img, d


# ---------- scene 3 · two moments ----------
B3 = ['The whole project happens in two clearly separate moments.',
      'The first is the before.',
      'It happens only once, when you run the command npm run ingest, and it prepares the documents to be searched.',
      'The second is the after.',
      'It happens on every question, and it is an assembly line that ends in an answer.',
      'Keep this split in mind: prepare once, answer many times.']


def s3(k):
    img, d = cv()
    if k >= 1:
        text_l(d, (65, 150), 'BEFORE' if k < 3 else 'BEFORE   ·   once   ·   npm run ingest', font(28, True), C['acc'])
        text_l(d, (57, 390), 'AFTER' if k < 5 else 'AFTER   ·   every question', font(28, True), C['warn'])
    if k >= 2:
        lane1(d, 4, hi=(0 if k == 2 else None))
    if k >= 4:
        lane2(d, set(range(7)))
    if k == 6:
        text_c(d, (640, 590), 'Prepare once   ·   Answer many times', font(34, True), C['acc'])
    return img, d


# ---------- scene 4 · the "before" ----------
B4 = ["Let's go to the first moment.",
      "Everything starts with the documents: text files with the company's policies.",
      'The system cuts each document into small pieces, called chunks.',
      'Then, it turns the text of each piece into a list of numbers, the embedding, which lets us measure when two texts are similar.',
      'Finally, it saves everything in a file, the index.',
      'That file is the result of the first moment.']
CAP4 = ['company policies', 'small cards, by section', 'list of 512 numbers', 'result of the 1st moment']


def s4(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 105), 'Before: preparing the index', font(48, True), C['acc'])
        text_c(d, (640, 160), 'happens once  ·  npm run ingest', font(25), C['muted'])
    if k >= 2:
        lane1(d, k - 1, hi=(k - 2), y=250, h=130, tsize=28, ssize=19)
        for i in range(min(k - 1, 4)):
            text_c(d, (L1X[i] + L1W / 2, 412), CAP4[i], font(22), C['muted'])
    if k == 6:
        text_c(d, (640, 520), 'the index is what the search will consult', font(32, True), C['blue'])
    return img, d


# ---------- scene 5 · the "after" ----------
B5 = ['Now, the second moment: what happens when someone asks a question.',
      'First, the question goes through the input guardrail, a safety check.',
      'It blocks empty or suspicious requests, and hides personal data, such as national ID numbers.',
      'Next, the search looks in the index for the most relevant passages.',
      'Those passages are assembled into a prompt, together with the question.',
      'The model writes the answer based only on them.',
      'And, before it reaches the user, the output guardrail checks whether the answer cites a valid source.',
      'Only then does it appear.']
VIS5 = {1: {0}, 2: {0, 1}, 3: {0, 1}, 4: {0, 1, 2}, 5: {0, 1, 2, 3}, 6: {0, 1, 2, 3, 4}, 7: {0, 1, 2, 3, 4, 5}, 8: set(range(7))}
NEW5 = {1: 0, 2: 1, 4: 2, 5: 3, 6: 4, 7: 5, 8: 6}


def s5(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 105), 'After: on every question', font(48, True), C['warn'])
        text_c(d, (640, 160), 'the assembly line that ends in an answer', font(25), C['muted'])
        lane2(d, VIS5[k], hi=NEW5.get(k), y=270, h=120)
    if k >= 3:
        text_c(d, (L2X[1] + L2W / 2, 430), 'blocks empty or suspicious input', font(21, True), C['warn'])
        text_c(d, (L2X[1] + L2W / 2, 462), 'hides personal data', font(21), C['warn'])
    if k >= 7:
        text_c(d, (L2X[5] + L2W / 2, 430), 'checks the citation [n]', font(21, True), C['warn'])
    return img, d


# ---------- scene 6 · the index links both moments ----------
B6 = ['Notice this dashed arrow.',
      'It is the link between the two moments: the search consults the index that was created earlier.',
      'Without it, the search would have nowhere to look.']


def s6(k):
    img, d = cv()
    text_l(d, (65, 150), 'BEFORE', font(28, True), C['acc'])
    text_l(d, (57, 390), 'AFTER', font(28, True), C['warn'])
    lane1(d, 4, hi=(3 if k == 3 else None))
    lane2(d, set(range(7)), hi=(2 if k == 3 else None))
    if k >= 1:
        arrow(d, [(1108, 292), (1108, 352), (L2X[2] + L2W / 2, 352), (L2X[2] + L2W / 2, 424)], C['blue'], 5, dash=True)
    if k >= 2:
        text_c(d, (790, 328), 'the search consults the index created earlier', font(24, True), C['blue'])
    return img, d


# ---------- scene 7 · map of the pieces ----------
B7 = ['Now, the same idea seen through the code pieces.',
      'There are two entry points: the command line, and the MCP server, which we will see later.',
      'From the command line, there are two ways of talking to the model.',
      'The first is the ask function, for questions and answers.',
      'The second is runAgent, for agent mode, where the model decides what to do.',
      'Both use the same retriever, the component that does the search.',
      'And the agent and the MCP server use the same tools.',
      'Write it once, and it works in both places.']


def s7(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 80), 'The map of the pieces', font(44, True))
    if k >= 2:
        box(d, 250, 125, 280, 66, 'CLI', 'src/cli.js', 'box', hi=(k == 2), tsize=26, ssize=17)
        box(d, 700, 125, 280, 66, 'MCP server', 'src/mcp/server.js', 'blue', hi=(k == 2), tsize=26, ssize=17)
    if k >= 3:
        arrow(d, [(390, 193), (390, 225), (200, 225), (200, 252)], C['ink'], 4, head=12)
        arrow(d, [(390, 193), (390, 225), (530, 225), (530, 252)], C['ink'], 4, head=12)
        box(d, 70, 255, 260, 66, 'ask()', 'questions and answers', 'box', hi=(k == 4), tsize=26, ssize=16)
        box(d, 400, 255, 260, 66, 'runAgent()', 'agent mode', 'acc', hi=(k == 5), tsize=26, ssize=16)
    if k >= 5:
        box(d, 1010, 255, 190, 66, 'LLM', 'Gemini or Claude', 'box', tsize=26, ssize=16)
        arrow(d, [(666, 288), (1004, 288)], C['ink'], 4, head=12)
        text_c(d, (752, 268), 'messages + tools', font(17), C['muted'])
    if k >= 6:
        box(d, 300, 470, 460, 62, 'Hybrid retriever', 'vector + BM25 → RRF → rerank', 'box', hi=(k == 6), tsize=25, ssize=16)
        arrow(d, [(200, 323), (200, 501), (294, 501)], C['ink'], 4, head=12)
    if k >= 7:
        box(d, 680, 365, 290, 66, 'Tools', 'search_policies · create_ticket', 'acc', hi=(k == 7), tsize=26, ssize=15)
        arrow(d, [(840, 193), (840, 359)], C['ink'], 4, head=12)
        text_l(d, (852, 230), 'tools/call', font(17), C['muted'])
        arrow(d, [(530, 323), (530, 398), (674, 398)], C['ink'], 4, head=12)
        arrow(d, [(820, 433), (820, 501), (766, 501)], C['ink'], 4, head=12)
    if k >= 8:
        rbox(d, (70, 560, 1210, 612), 'warn', hi=True)
        text_c(d, (640, 586), 'Cross-cutting layers:  Guardrails  ·  Cache  ·  Tracer  ·  config.js', font(24, True), C['warn'])
    return img, d


# ---------- scene 8 · the cli.js file ----------
B8 = ['The entry point of everything is the file cli.js.',
      'It reads what you type in the terminal and decides the path.',
      'If it is the word ingest, it builds the index.',
      'If it is agent, it runs an agent.',
      'Anything else is treated as a question and goes to the ask function.',
      'For now, do not worry about the code details: in the next chapters, we will open each piece.']
CODE = ["if (cmd === 'ingest') {", "  await buildIndex({ log: console.log });", "} else if (cmd === 'agent') {",
        "  // runs an agent", "} else {", "  const { ask } = await createAssistant();",
        "  print(await ask(q));   // answers the question", "}"]
HL8 = {3: (0, 1), 4: (2, 3), 5: (4, 7)}


def s8(k):
    img, d = cv()
    if k >= 1:
        d.rounded_rectangle((90, 130, 1190, 610), 18, fill=C['code_bg'])
        d.rounded_rectangle((90, 130, 1190, 182), 18, fill=(29, 44, 56))
        text_l(d, (120, 156), 'src/cli.js  (simplified excerpt)', font(24, False, True), C['code_ink'])
    if k >= 2:
        if k in HL8:
            a, b = HL8[k]
            d.rectangle((100, 205 + a * 46, 1180, 205 + (b + 1) * 46), fill=(24, 74, 82))
        for i, line in enumerate(CODE):
            text_l(d, (125, 228 + i * 46), line, font(30, False, True), C['code_ink'])
    return img, d


# ---------- scene 9 · wrap-up ----------
B9 = ['To sum up: the project has two moments.',
      'Prepare the index, once.',
      'And answer each question, going through safety, search, model, and a final check.',
      'In the next chapter, we will look at the documents that feed the system.',
      'See you there!']


def s9(k):
    img, d = cv()
    text_c(d, (640, 105), 'See you there!' if k >= 5 else 'Summing up', font(56, True), C['acc'] if k >= 5 else C['ink'])
    if k >= 2:
        rbox(d, (150, 180, 1130, 280), 'acc', hi=(k == 2))
        text_l(d, (190, 230), '1   Prepare the index, once', font(32, True))
    if k >= 3:
        rbox(d, (150, 315, 1130, 415), 'warn', hi=(k == 3))
        text_l(d, (190, 365), '2   Answer each question:  safety → search → model → check', font(29, True))
    if k >= 4:
        rbox(d, (150, 455, 1130, 555), 'blue', hi=(k == 4))
        text_l(d, (190, 505), 'Next chapter:  the documents that feed the system', font(30, True))
    return img, d


SCENES = [(B1, s1), (B2, s2), (B3, s3), (B4, s4), (B5, s5), (B6, s6), (B7, s7), (B8, s8), (B9, s9)]

if __name__ == '__main__':
    work = os.environ.get('VIDEO_WORKDIR', os.path.join(HERE, '_work', f'cap01_en_{VOICE}'))
    if len(sys.argv) > 1 and sys.argv[1] == 'preview':
        preview(SCENES, os.path.join(work, 'preview'))
        print('preview saved in', os.path.join(work, 'preview'))
    else:
        build(SCENES, os.path.join(HERE, 'saida', f'cap01_en_{VOICE}.mp4'), work, TAG)
