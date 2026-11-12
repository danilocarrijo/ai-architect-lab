"""Chapter 2 · The documents: the raw material (English, voice: Zira by default).

Usage:   python cap02_en.py preview
         python cap02_en.py                      # saida\\cap02_en_zira.mp4
         set VOICE=david && python cap02_en.py   # male voice
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
# Spoken-only fixes (the subtitles keep the original text).
engine.SPEECH = [
    (r'loader\.js', 'loader dot J S'), (r'\.md\b', ' dot M D'), (r'\bHR\b', 'H R'), (r'\bMCP\b', 'M C P'),
    (r'\bnpm\b', 'N P M'),
]
TAG = 'Chapter 2 · The documents: the raw material'


def cv():
    return canvas(TAG)


# ---------- scene 1 · opening ----------
B1 = ['Hello!',
      'In the previous chapter, you saw the journey of a question.',
      "Now, let's look at the start of that journey: the documents.",
      'They are the raw material of the assistant.',
      'You will see how they are written, and how the code reads them.']


def s1(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 200), 'The documents', font(70, True))
    if k >= 4:
        text_c(d, (640, 280), 'the raw material of the assistant', font(36), C['acc'])
    if k >= 2:
        box(d, 150, 355, 400, 90, 'Chapter 1', 'the journey of a question', 'box', hi=(k == 2), tsize=27, ssize=20)
    if k >= 3:
        arrow(d, [(565, 400), (715, 400)], C['ink'], 5)
        box(d, 730, 355, 400, 90, 'Chapter 2', 'the documents', 'acc', hi=(k == 3), tsize=27, ssize=20)
    if k >= 5:
        text_c(d, (640, 540), 'How they are written   ·   How the code reads them', font(30, True), C['muted'])
    return img, d


# ---------- scene 2 · the library analogy ----------
B2 = ['Think of a library.',
      'The documents are the textbooks.',
      'Everything the assistant can state comes from them.',
      'If a rule is not in any document, the assistant must say it does not know.',
      'It cannot make things up.',
      'That is why the quality of the answers starts with the quality of the documents.']


def s2(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 95), 'The library analogy', font(48, True))
    if k >= 2:
        rbox(d, (150, 150, 1130, 240), 'acc', hi=(k == 2))
        text_c(d, (640, 195), 'Documents   =   the textbooks of the library', font(33, True))
    if k >= 3:
        rbox(d, (150, 265, 1130, 355), 'box', hi=(k == 3))
        text_c(d, (640, 310), 'Every answer comes from the documents', font(33, True))
    if k >= 4:
        rbox(d, (150, 380, 1130, 485), 'warn', hi=(k in (4, 5)))
        text_c(d, (640, 420 if k >= 5 else 432), 'Rule not in any document?   →   "I don\'t know"', font(33, True), C['warn'])
        if k >= 5:
            text_c(d, (640, 458), 'No making things up.', font(28), C['warn'])
    if k >= 6:
        rbox(d, (150, 515, 1130, 595), 'blue', hi=True)
        text_c(d, (640, 555), 'Quality of the answers   =   quality of the documents', font(31, True), C['blue'])
    return img, d


# ---------- scene 3 · the four documents ----------
B3 = ['Our project has four documents, all in the data folder: vacation, home office, reimbursement, and IT support.',
      'They are made up, just for study.',
      'To use this with your company, just replace the content, keeping the format.']
DOCS = [('ferias.md', 'vacation policy', 'dept: rh', 'box'), ('home-office.md', 'remote and hybrid work', 'dept: rh', 'acc'),
        ('reembolso.md', 'expense reimbursement', 'dept: financeiro', 'blue'), ('ti-suporte.md', 'IT support and security', 'dept: ti', 'warn')]


def s3(k):
    img, d = cv()
    text_c(d, (640, 95), 'Four documents in data/', font(48, True))
    if k >= 1:
        for i, (name, what, dept, st) in enumerate(DOCS):
            x = 60 + i * 295
            rbox(d, (x, 190, x + 270, 400), st, hi=(k == 1))
            text_c(d, (x + 135, 245), name, font(25, True, True))
            text_c(d, (x + 135, 305), what, font(23))
            text_c(d, (x + 135, 355), dept, font(23, False, True), C['muted'])
    if k >= 2:
        text_c(d, (640, 470), 'made-up content, just for study', font(34, True), C['warn'])
    if k >= 3:
        text_c(d, (640, 540), 'replace the content   ·   keep the format', font(34, True), C['acc'])
    return img, d


# ---------- scene 4 · the Markdown format ----------
B4 = ['The documents are written in Markdown, a simple text format.',
      'A pound sign at the start of a line marks a title. Two pound signs mark a section.',
      'And, at the top of each file, there is a special block, between two lines of three dashes.',
      'It is called frontmatter, and it holds information about the document: the title, the department, and the update date.']
FERIAS = ['---', 'title: Política de Férias', 'dept: rh', 'updated: 2026-01-10', '---', '# Política de Férias', '',
          '## Direito a férias', 'Todo colaborador CLT tem direito a 30 dias...', '', '## Como solicitar',
          'A solicitação deve ser feita no portal...']


def s4(k):
    img, d = cv()
    bands = []
    if k == 2:
        bands = [(5, 5, BAND_TEAL), (7, 7, BAND_BLUE), (10, 10, BAND_BLUE)]
    elif k == 3:
        bands = [(0, 4, BAND_TEAL)]
    elif k >= 4:
        bands = [(1, 3, BAND_TEAL)]
    ys = code_panel(d, 'data/ferias.md', FERIAS, bands, x1=1190)
    if k == 2:
        for i, t in [(5, '←  title'), (7, '←  section'), (10, '←  section')]:
            text_l(d, (800, ys[i]), t, font(25, True), (130, 225, 215))
    if k == 3:
        text_l(d, (800, ys[2]), '←  frontmatter', font(27, True), (130, 225, 215))
    if k >= 4:
        for i, t in [(1, '←  title'), (2, '←  department'), (3, '←  update date')]:
            text_l(d, (800, ys[i]), t, font(25, True), (130, 225, 215))
    return img, d


# ---------- scene 5 · why the header matters ----------
B5 = ['This header is not decoration.',
      'The department field will let us search only the HR documents, for example.',
      'And each section, those lines with two pound signs, will be the cutting point of the next chapter: each section becomes a searchable piece.']
SECTIONS = ['Direito a férias', 'Como solicitar', 'Abono pecuniário', 'Pagamento']


def s5(k):
    img, d = cv()
    text_c(d, (640, 95), 'Why the header matters', font(48, True))
    if k >= 1:
        rbox(d, (60, 160, 620, 590), 'box', hi=(k == 1))
        text_c(d, (340, 205), 'The header (frontmatter)', font(30, True), C['blue'])
        text_c(d, (340, 275), 'dept: rh', font(34, True, True))
    if k >= 2:
        arrow(d, [(340, 310), (340, 380)], C['blue'], 5)
        rbox(d, (110, 390, 570, 470), 'blue', hi=(k == 2))
        text_c(d, (340, 430), 'search only the HR documents', font(27, True), C['blue'])
    if k >= 3:
        rbox(d, (660, 160, 1220, 590), 'acc', hi=(k == 3))
        text_c(d, (940, 205), 'The sections  (##)', font(30, True), C['acc'])
        for i, s in enumerate(SECTIONS):
            rbox(d, (700, 245 + i * 62, 1180, 295 + i * 62), 'box')
            text_c(d, (940, 270 + i * 62), s, font(25, True))
        text_c(d, (940, 530), '4 sections   →   4 searchable pieces', font(27, True), C['acc'])
    return img, d


# ---------- scene 6 · the code that reads them ----------
B6 = ['Now, the code.',
      'The file loader.js does two things.',
      'The first is to separate the header from the text.',
      'It looks for the three opening dashes, the content, and the three closing dashes, using a regular expression, which is a text search pattern.',
      'The second is to repeat this for every file in the folder that ends in .md, reading all of them at the same time.']
LOADER = ['function parseFrontmatter(raw) {',
          "  const m = raw.match(/^---\\n([\\s\\S]*?)\\n---\\n([\\s\\S]*)$/);",
          '  // ... turns the header into { title, dept, updated }',
          '  return { meta, body: m[2] };', '}', '',
          'export async function loadDocuments(dir) {',
          "  const files = (await fs.readdir(dir)).filter((f) => f.endsWith('.md'));",
          '  return Promise.all(files.map(/* read each file */));', '}']


def s6(k):
    img, d = cv()
    if k >= 1:
        bands = {3: [(0, 4, BAND_TEAL)], 4: [(1, 1, BAND_TEAL)], 5: [(6, 9, BAND_BLUE)]}.get(k, [])
        ys = code_panel(d, 'src/rag/loader.js  (excerpt)', LOADER if k >= 2 else [], bands, size=24)
        if k == 4:
            text_c(d, (640, 575), 'regular expression:   ---   content   ---', font(26, True), (130, 225, 215))
        if k >= 5:
            text_c(d, (640, 575), 'every .md file, all at the same time', font(26, True), (130, 225, 215))
    return img, d


# ---------- scene 7 · the result ----------
B7 = ['The result is a list of documents.',
      'Each one has four fields.',
      'An identifier, and the file name.',
      'The metadata, which is the header.',
      'And the body, which is the text.',
      'Running the project, the four documents are found: vacation and home office, from the HR department; reimbursement, from finance; and IT support, from the IT department.']
OBJ = ['{', '  id:     "ferias",', '  source: "ferias.md",', '  meta:   { title: "Política de Férias",',
       '            dept: "rh", updated: "2026-01-10" },', '  body:   "# Política de Férias ..."', '}']
FOUND = [('ferias', 'rh'), ('home-office', 'rh'), ('reembolso', 'financeiro'), ('ti-suporte', 'ti')]


def s7(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 95), 'The result of loadDocuments', font(44, True))
    if k >= 2:
        bands = {3: [(1, 2, BAND_TEAL)], 4: [(3, 4, BAND_BLUE)], 5: [(5, 5, BAND_AMBER)]}.get(k, [])
        ys = code_panel(d, 'one document', OBJ, bands, size=25, y0=250, x1=830)
        notes = {3: [(1, '←  identifier'), (2, '←  file name')], 4: [(3, '←  metadata (the header)')], 5: [(5, '←  body (the text)')]}
        if k < 6:
            for i, t in notes.get(k, []):
                text_l(d, (850, ys[i]), t, font(25, True), C['acc'])
    if k >= 6:
        rbox(d, (850, 150, 1244, 480), 'acc', hi=True)
        text_c(d, (1047, 190), '4 documents found', font(27, True), C['acc'])
        for i, (n, dept) in enumerate(FOUND):
            text_l(d, (872, 250 + i * 55), f'{n}', font(23, True, True))
            text_l(d, (1040, 250 + i * 55), f'({dept})', font(22, False, True), C['muted'])
    return img, d


# ---------- scene 8 · wrap-up ----------
B8 = ['To sum up: the documents are the source of everything the assistant knows.',
      'They are text files, with a header of information and sections with titles.',
      'The code reads each one and delivers the text and the metadata.',
      'In the next chapter, we will cut these documents into pieces, the chunks.',
      'See you there!']


def s8(k):
    img, d = cv()
    text_c(d, (640, 100), 'See you there!' if k >= 5 else 'Summing up', font(56, True), C['acc'] if k >= 5 else C['ink'])
    if k >= 1:
        rbox(d, (150, 170, 1130, 255), 'acc', hi=(k == 1))
        text_l(d, (190, 212), '1   Documents are the source of everything the assistant knows', font(28, True))
    if k >= 2:
        rbox(d, (150, 280, 1130, 365), 'box', hi=(k == 2))
        text_l(d, (190, 322), '2   Text files: a header  +  sections with titles', font(28, True))
    if k >= 3:
        rbox(d, (150, 390, 1130, 475), 'warn', hi=(k == 3))
        text_l(d, (190, 432), '3   The code reads each one:  text  +  metadata', font(28, True))
    if k >= 4:
        rbox(d, (150, 505, 1130, 590), 'blue', hi=(k == 4))
        text_l(d, (190, 547), 'Next chapter:  cutting the documents into chunks', font(28, True))
    return img, d


SCENES = [(B1, s1), (B2, s2), (B3, s3), (B4, s4), (B5, s5), (B6, s6), (B7, s7), (B8, s8)]

if __name__ == '__main__':
    work = os.environ.get('VIDEO_WORKDIR', os.path.join(HERE, '_work', f'cap02_en_{VOICE}'))
    if len(sys.argv) > 1 and sys.argv[1] == 'preview':
        preview(SCENES, os.path.join(work, 'preview'))
        print('preview saved in', os.path.join(work, 'preview'))
    else:
        build(SCENES, os.path.join(HERE, 'saida', f'cap02_en_{VOICE}.mp4'), work, TAG)
