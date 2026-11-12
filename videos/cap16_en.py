"""Chapter 16 · Running everything (English, voice: Zira by default)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine  # noqa: E402
from engine import C, box, build, canvas, font, preview, rbox, text_c, text_l  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
VOICES = {'zira': 'Microsoft Zira Desktop', 'david': 'Microsoft David Desktop'}
VOICE = os.environ.get('VOICE', 'zira').lower()
engine.SINGLE_VOICE = VOICES[VOICE]
engine.SPEECH = [
    (r'\bnpm\b', 'N P M'), (r'GEMINI_API_KEY', 'Gemini A P I key'), (r'ANTHROPIC_API_KEY', 'Anthropic A P I key'), (r'\bAPI\b', 'A P I'),
    (r'\bMCP\b', 'M C P'), (r'LangGraph', 'Lang Graph'), (r'\bRAG\b', 'rag'), (r'\bRRF\b', 'R R F'), (r'ViaCEP', 'Via C E P'),
    (r'\bCEP\b', 'C E P'), (r'cli\.js', 'C L I dot J S'),
]
TAG = 'Chapter 16 · Running everything'
NOTE = (130, 225, 215)
WARN_L = (255, 200, 120)


def cv():
    return canvas(TAG)


B1 = ['Hello!',
      'We have studied every piece. Now it is time to run the whole project.',
      'This chapter is a map: which command to use for each goal, and which ones need an API key.',
      'And at the end, the six ideas that explain everything.']


def s1(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 200), 'Running everything', font(72, True))
    if k >= 3:
        text_c(d, (640, 290), 'which command, for which goal', font(36), C['acc'])
    if k >= 4:
        text_c(d, (640, 420), '6 ideas that explain the whole project', font(32, True), C['muted'])
    return img, d


# rows: (goal, command, needs key?)
BASIC = [('Install', 'npm install', False), ('Build the index', 'npm run ingest', False),
         ('Ask a question', 'npm start "Quantos dias de férias eu tenho?"', False), ('Interactive mode', 'npm start   (type "sair" to quit)', False)]
B2 = ['The first group needs no API key at all.',
      'Install the dependencies with npm install.',
      'Build the index with npm run ingest.',
      'Ask a question with npm start, followed by the question. Without a key, the answer is the best chunk found.',
      'Or run npm start alone for the interactive mode, and type sair to leave.']


def table(d, rows, k, k0, y0=150, rh=84, cmd_size=22, cx=330):
    for i, (g, c, key) in enumerate(rows):
        if k >= k0 + i:
            y = y0 + i * rh
            hi = (k == k0 + i)
            rbox(d, (40, y, 1240, y + rh - 14), 'acc' if hi else 'box', r=10)
            text_l(d, (65, y + (rh - 14) // 2), g, font(24, True), C['muted'])
            text_l(d, (cx, y + (rh - 14) // 2), c, font(cmd_size, False, True))
            text_l(d, (1030, y + (rh - 14) // 2), 'needs a key' if key else 'no key', font(21, True), C['warn'] if key else C['acc'])


def s2(k):
    img, d = cv()
    text_c(d, (640, 70), 'No key needed', font(46, True))
    if k >= 1:
        text_c(d, (640, 118), 'goal  →  command', font(22), C['muted'])
    table(d, BASIC, k, 2, y0=160, rh=100, cmd_size=22)
    return img, d


CHECK = [('Measure the search', 'npm run eval', False), ('Run the tests', 'npm test', False),
         ('List the agents', 'node src/cli.js agents', False), ('Start the MCP server', 'npm run mcp', False),
         ('Test the hooks only', 'node --test test/hooks.test.js', False)]
B3 = ['The second group also needs no key.',
      'npm run eval measures the search, as in chapter 14.',
      'npm test runs the twenty six tests.',
      'The agents command lists the three agents: helpdesk, triage, and cep.',
      'npm run mcp starts the M C P server, for clients like Claude Desktop.',
      'And you can run only the hook tests, with node dash dash test and the file name.']


def s3(k):
    img, d = cv()
    text_c(d, (640, 70), 'Also without a key', font(46, True))
    table(d, CHECK, k, 2, y0=130, rh=92, cmd_size=22)
    return img, d


B4 = ['Do you remember the agents command? Here is its real output.',
      'Three agents: helpdesk answers questions and opens tickets.',
      'Triage classifies an incident and opens a ticket with a priority.',
      'And cep looks up an address in an external A P I.',
      'Each one lists the tools it is allowed to use.']
AG = ['helpdesk   Responde dúvidas sobre políticas internas e abre chamados quando pedido.  [tools: search_policies, create_ticket]',
      'triage     Classifica um incidente de TI, consulta a política e abre um chamado com prioridade.  [tools: search_policies, create_ticket]',
      'cep        Consulta endereços por CEP em uma API externa (ViaCEP).  [tools: lookup_cep]']


def s4(k):
    img, d = cv()
    text_c(d, (640, 62), 'node src/cli.js agents', font(38, True, True))
    if k >= 2:
        d.rounded_rectangle((40, 110, 1240, 500), 18, fill=C['code_bg'])
    for i in range(3):
        if k >= i + 2:
            name, rest = AG[i][:11].strip(), AG[i][11:]
            desc, tools = rest.split('  [tools: ')
            y = 140 + i * 125
            if k == i + 2 or k == 5:
                d.rectangle((52, y - 12, 1228, y + 100), fill=(34, 64, 66))
            text_l(d, (70, y + 10), name, font(26, True, True), (150, 235, 180))
            text_l(d, (70, y + 48), desc.strip(), font(17, False, True), C['code_ink'])
            text_l(d, (70, y + 78), '[tools: ' + tools, font(17, True, True), (255, 200, 120) if k == 5 else (140, 180, 230))
    return img, d


KEY = [('Run an agent (own engine)', 'node src/cli.js agent "Preciso resetar minha senha"', True),
       ('Run an agent (LangGraph)', 'node src/cli.js agent --engine langgraph "..."', True),
       ('Pick an agent by name', 'node src/cli.js agent --name cep "CEP 01310-100?"', True)]
B5 = ['Running an agent is different: it needs a key, because the model must decide.',
      'Set a Gemini key or an Anthropic key in the environment.',
      'The basic form runs the agent with our own engine.',
      'Add the engine flag to use LangGraph instead.',
      'And the name flag picks another agent, like the C E P agent, which calls the external A P I.',
      'Without a key, the project stops right away, with a clear message.']


def s5(k):
    img, d = cv()
    text_c(d, (640, 70), 'Agents need a key', font(46, True))
    if k >= 2:
        rbox(d, (130, 118, 1150, 176), 'warn', hi=(k == 2))
        text_c(d, (640, 147), 'GEMINI_API_KEY   or   ANTHROPIC_API_KEY', font(26, True, True), C['warn'])
    table(d, KEY, k, 3, y0=205, rh=100, cmd_size=19, cx=440)
    if k >= 6:
        rbox(d, (60, 520, 1220, 595), 'box', hi=True)
        text_l(d, (85, 557), 'Error: O agente precisa de GEMINI_API_KEY (ou ANTHROPIC_API_KEY).', font(21, False, True), C['warn'])
    return img, d


B6 = ['Here is the real result of the ingest command.',
      'Four documents became sixteen chunks, with the local embedder.',
      'The embedder name matters: if it changes, the index is rebuilt automatically.',
      'And one honest remark: the agent commands were never run against a real key. They were tested only with fake models.']


def s6(k):
    img, d = cv()
    text_c(d, (640, 70), 'Real result · npm run ingest', font(42, True))
    if k >= 2:
        d.rounded_rectangle((100, 150, 1180, 260), 18, fill=C['code_bg'])
        text_l(d, (135, 205), '4 documentos -> 16 chunks (embedder: local-hash-512)', font(28, False, True), (150, 235, 180))
    if k >= 3:
        rbox(d, (100, 300, 1180, 390), 'blue', hi=(k == 3))
        text_c(d, (640, 345), 'embedder name changes  →  index rebuilt automatically', font(26, True), C['blue'])
    if k >= 4:
        rbox(d, (100, 430, 1180, 540), 'warn', hi=True)
        text_c(d, (640, 468), 'Never run with a real key:', font(27, True), C['warn'])
        text_c(d, (640, 508), 'the agent commands were tested only with fake models', font(23))
    return img, d


IDEAS = [('1', 'RAG', 'Search first, then generate. The model answers from what is on the table.', 'acc'),
         ('2', 'Hybrid search', 'Meaning plus exact words, merged by rank (RRF).', 'blue'),
         ('3', 'Agent', 'The model picks the steps in a loop, with a limit and restricted tools.', 'warn'),
         ('4', 'Guardrails', 'Input, retrieved content and output, each with its own inspector.', 'acc'),
         ('5', 'Observability', 'The Tracer measures time, tokens and cost of every run.', 'blue'),
         ('6', 'Swappable engine', 'Agents and tools are data: the engine that runs them can change.', 'warn')]
B7 = ['Now, the six ideas that explain everything.',
      'One: RAG. Search first, then generate.',
      'Two: hybrid search. Meaning plus exact words, merged by rank.',
      'Three: the agent. The model chooses the steps, inside a loop with a limit.',
      'Four: guardrails. Three inspectors: input, retrieved content, and output.',
      'Five: observability. The tracer measures time, tokens, and cost.',
      'Six: a swappable engine. Agents and tools are data, so the engine can change.']


def s7(k):
    img, d = cv()
    text_c(d, (640, 62), 'Six ideas', font(46, True))
    for i, (n, t, desc, st) in enumerate(IDEAS):
        if k >= i + 2:
            y = 115 + i * 85
            rbox(d, (60, y, 1220, y + 72), st, hi=(k == i + 2), r=12)
            text_l(d, (85, y + 36), n, font(30, True), C[{'acc': 'acc', 'blue': 'blue', 'warn': 'warn'}[st]])
            text_l(d, (135, y + 36), t, font(25, True))
            text_l(d, (420, y + 36), desc, font(19), C['muted'])
    return img, d


NEXT = [('Run npm start with different questions', 'compare with chapter 6'), ('Add a question to golden.js', 'run npm run eval'),
        ('Add a new document to data/', 'run npm run ingest, then ask'), ('Create a new tool', 'see it appear in the MCP server')]
B8 = ['To study further, try four things.',
      'Ask different questions, and compare with what chapter six predicted.',
      'Add a question to the golden set, and run the evaluation.',
      'Add a new document, run ingest, and ask about it.',
      'Create a new tool, and watch it appear in the M C P server.',
      'In the next chapter, we see what changes between this laboratory and a real production system. See you there!']


def s8(k):
    img, d = cv()
    text_c(d, (640, 70), 'Try it yourself' if k < 6 else 'See you there!', font(48, True), C['ink'] if k < 6 else C['acc'])
    for i, (t, sub) in enumerate(NEXT):
        if k >= i + 2:
            y = 140 + i * 100
            box(d, 100, y, 1080, 82, t, sub, ['acc', 'blue', 'warn', 'box'][i], hi=(k == i + 2), tsize=27, ssize=19)
    if k >= 6:
        text_c(d, (640, 570), 'Next chapter:  from the laboratory to production', font(26, True), C['muted'])
    return img, d


SCENES = [(B1, s1), (B2, s2), (B3, s3), (B4, s4), (B5, s5), (B6, s6), (B7, s7), (B8, s8)]

if __name__ == '__main__':
    work = os.environ.get('VIDEO_WORKDIR', os.path.join(HERE, '_work', f'cap16_en_{VOICE}'))
    if len(sys.argv) > 1 and sys.argv[1] == 'preview':
        preview(SCENES, os.path.join(work, 'preview'))
        print('preview saved in', os.path.join(work, 'preview'))
    else:
        build(SCENES, os.path.join(HERE, 'saida', f'cap16_en_{VOICE}.mp4'), work, TAG)
