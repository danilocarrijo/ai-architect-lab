"""Chapter 12 · MCP: one tool, many clients (English, voice: Zira by default).

Usage:   python cap12_en.py preview
         python cap12_en.py                      # saida\\cap12_en_zira.mp4
         set VOICE=david && python cap12_en.py   # male voice
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
    (r'\bMCP\b', 'M C P'), (r'stdio', 'standard I O'), (r'stdout', 'standard out'), (r'stderr', 'standard error'),
    (r'lookup_cep', 'lookup C E P'), (r'search_policies', 'search policies'), (r'create_ticket', 'create ticket'),
    (r'registerTool', 'register tool'), (r'createTools', 'create tools'), (r'pickTools', 'pick tools'),
    (r'listTools', 'list tools'), (r'callTool', 'call tool'), (r'\bHTTP\b', 'H T T P'), (r'\bCEP\b', 'C E P'),
    (r'\bnpm\b', 'N P M'),
]
TAG = 'Chapter 12 · MCP: one tool, many clients'
NOTE = (130, 225, 215)
WARN_L = (255, 200, 120)


def cv():
    return canvas(TAG)


# ---------- scene 1 · opening ----------
B1 = ['Hello!',
      'In the previous chapter, you saw agents and their tools.',
      'Now, a question: how can other programs use those same tools?',
      'The answer is MCP, and in this chapter you will build a server for it.']


def s1(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 200), 'MCP', font(84, True))
    if k >= 3:
        text_c(d, (640, 285), 'one tool, many clients', font(38), C['acc'])
    if k >= 2:
        box(d, 150, 355, 400, 90, 'Chapter 11', 'agents and tools', 'box', hi=(k == 2), tsize=27, ssize=20)
    if k >= 3:
        arrow(d, [(565, 400), (715, 400)], C['ink'], 5)
        box(d, 730, 355, 400, 90, 'Chapter 12', 'sharing the tools', 'blue', hi=(k == 3), tsize=27, ssize=20)
    if k >= 4:
        text_c(d, (640, 540), 'Model Context Protocol', font(32, True), C['muted'])
    return img, d


# ---------- scene 2 · the standard outlet ----------
B2 = ['Think of MCP as the standard outlet.',
      'You build the appliance, the tool, once.',
      'Any program with the right plug, like Claude Code or Claude Desktop, can use it, without an adapter.',
      'Without MCP, you would write a different integration for each AI program.',
      'With MCP, you run a server that announces your tools in a standard format.']
PROGS = ['Claude Code', 'Claude Desktop', 'another client']


def s2(k):
    img, d = cv()
    text_c(d, (640, 80), 'MCP: the standard outlet', font(46, True))
    if k in (2, 3):
        rbox(d, (240, 200, 1040, 300), 'acc', hi=True)
        text_c(d, (640, 250), 'build the appliance (the tool)  once', font(33, True), C['acc'])
    if k == 3:
        rbox(d, (240, 340, 1040, 440), 'blue', hi=True)
        text_c(d, (640, 390), 'any program with the right plug can use it', font(33, True), C['blue'])
    if k >= 4:
        rbox(d, (40, 140, 620, 570), 'warn', hi=(k == 4))
        text_c(d, (330, 175), 'without MCP', font(30, True), C['warn'])
        for i, t in enumerate(PROGS):
            box(d, 65, 225 + i * 85, 170, 52, t, '', 'box', tsize=18)
        for j in range(2):
            box(d, 450, 255 + j * 105, 140, 52, 'your tools' if j == 0 else 'tools', '', 'acc', tsize=19)
        for i in range(3):
            for j in range(2):
                d.line((237, 251 + i * 85, 448, 281 + j * 105), fill=C['warn'], width=2)
        text_c(d, (330, 535), 'a different integration for each pair', font(22, True), C['warn'])
    if k >= 5:
        rbox(d, (660, 140, 1240, 570), 'acc', hi=(k == 5))
        text_c(d, (950, 175), 'with MCP', font(30, True), C['acc'])
        for i, t in enumerate(PROGS):
            box(d, 685, 225 + i * 85, 170, 52, t, '', 'box', tsize=18)
            d.line((857, 251 + i * 85, 925, 340), fill=C['acc'], width=3)
        box(d, 925, 305, 90, 70, 'MCP', '', 'blue', tsize=24)
        for j in range(2):
            box(d, 1065, 255 + j * 105, 150, 52, 'your tools' if j == 0 else 'tools', '', 'acc', tsize=19)
            d.line((1017, 340, 1063, 281 + j * 105), fill=C['acc'], width=3)
        text_c(d, (950, 535), 'one standard plug', font(22, True), C['acc'])
    return img, d


# ---------- scene 3 · the server in code ----------
B3 = ['Here is the MCP server, in code.',
      'It loads the retriever, as always.',
      'It creates a server, with a name and a version.',
      'Then it takes the same tools of the agent, and registers each one on the server.',
      'Finally, it opens the conversation through the terminal, which is called stdio, and waits for requests.']
SRV = ['const { retriever } = await loadRetriever();', "const server = new McpServer({ name: 'helpdesk', version: '1.0.0' });", '',
       'for (const t of createTools({ retriever })) {', '  server.registerTool(',
       '    t.name, { description: t.description, inputSchema: t.schema },',
       "    async (args) => ({ content: [{ type: 'text', text: await t.run(args) }] }));", '}', '',
       'await server.connect(new StdioServerTransport());', "console.error('MCP helpdesk pronto (stdio)');"]


def s3(k):
    img, d = cv()
    bands = {2: [(0, 0, BAND_TEAL)], 3: [(1, 1, BAND_BLUE)], 4: [(3, 7, BAND_AMBER)], 5: [(9, 9, BAND_TEAL)]}.get(k, [])
    ys = code_panel(d, 'src/mcp/server.js  (formatted)', SRV, bands, size=20, line_h=32, y0=206)
    notes = {4: (3, '←  the same tools as the agent'), 5: (9, '←  stdio: talks through the terminal')}
    if k in notes:
        i, t = notes[k]
        text_l(d, (700 if k == 4 else 700, ys[i] + (0 if k == 4 else 0)), t, font(21, True), NOTE)
    return img, d


# ---------- scene 4 · the golden rule ----------
B4 = ['Now, a golden rule.',
      'The conversation with the client travels through standard output.',
      'So nothing else may be written there. Logs go to standard error.',
      'Writing anything else on standard output would corrupt the conversation.']


def s4(k):
    img, d = cv()
    text_c(d, (640, 85), 'The golden rule of stdio', font(46, True))
    if k >= 2:
        rbox(d, (60, 150, 620, 400), 'blue', hi=(k == 2))
        text_c(d, (340, 195), 'stdout', font(40, True, True), C['blue'])
        text_c(d, (340, 260), 'the conversation', font(30, True))
        text_c(d, (340, 305), 'with the client', font(30, True))
        text_c(d, (340, 360), 'protocol only', font(24), C['muted'])
    if k >= 3:
        rbox(d, (660, 150, 1220, 400), 'acc', hi=(k == 3))
        text_c(d, (940, 195), 'stderr', font(40, True, True), C['acc'])
        text_c(d, (940, 260), 'your logs', font(30, True))
        d.rounded_rectangle((690, 295, 1190, 365), 12, fill=C['code_bg'])
        text_c(d, (940, 330), "console.error('MCP helpdesk pronto')", font(21, False, True), NOTE)
    if k >= 4:
        rbox(d, (150, 450, 1130, 560), 'warn', hi=True)
        text_c(d, (640, 490), 'anything else on stdout', font(31, True), C['warn'])
        text_c(d, (640, 530), 'corrupts the conversation', font(31, True), C['warn'])
    return img, d


# ---------- scene 5 · real demo ----------
B5 = ["Let's try it for real.",
      'I wrote a small MCP client, and connected it to our server.',
      'First, it asks: which tools do you have?',
      'The server answers: three tools: search_policies, create_ticket, and lookup_cep.',
      'Notice that the third one, lookup_cep, we added in a later chapter, and the server code was not edited.',
      'Then, the client calls search_policies, asking about resetting a password.',
      'And it receives the text of the policy.']
TOOLS5 = [('search_policies', 'query, dept'), ('create_ticket', 'title, description, priority'), ('lookup_cep', 'cep')]


def s5(k):
    img, d = cv()
    text_c(d, (640, 70), 'A real MCP client talking to our server', font(38, True))
    d.rounded_rectangle((60, 115, 1220, 595), 18, fill=C['code_bg'])
    if k >= 2:
        text_l(d, (90, 150), '[server stderr]  MCP helpdesk pronto (stdio)', font(21, False, True), (150, 170, 185))
        text_l(d, (90, 195), '> client.listTools()', font(26, True, True), C['code_ink'])
    if k >= 4:
        text_l(d, (90, 240), 'tools:  3', font(24, True, True), NOTE)
        for i, (n, a) in enumerate(TOOLS5):
            y = 285 + i * 44
            if k >= 5 and i == 2:
                d.rectangle((75, y - 20, 1205, y + 20), fill=BAND_AMBER)
            text_l(d, (110, y), f'- {n}', font(24, False, True), C['code_ink'])
            text_l(d, (440, y), f'args: {a}', font(21, False, True), (150, 170, 185))
        if k >= 5:
            text_l(d, (860, 285 + 2 * 44), '←  added later, server unchanged', font(20, True), WARN_L)
    if k >= 6:
        text_l(d, (90, 440), "> client.callTool('search_policies', { query: 'resetar senha', dept: 'ti' })", font(21, True, True), C['code_ink'])
    if k >= 7:
        text_l(d, (90, 490), '(ti-suporte.md > Reset de senha) A senha corporativa expira', font(22, False, True), NOTE)
        text_l(d, (90, 525), 'a cada 90 dias. Para redefinir, acesse senha.acme.example ou...', font(22, False, True), NOTE)
        text_l(d, (90, 570), 'real output of the project, not a mock-up', font(18), (150, 170, 185))
    return img, d


# ---------- scene 6 · using it in a client ----------
B6 = ['To use it in a client, like Claude Code or Claude Desktop, add this to its configuration.',
      'Adjust the path to where your project is.',
      'The client starts the server by itself, and talks to it through stdio.']
JSON6 = ['{', '  "mcpServers": {', '    "helpdesk": {', '      "command": "node",',
         '      "args": ["D:/Projetos/ai-architect-lab/src/mcp/server.js"]', '    }', '  }', '}']


def s6(k):
    img, d = cv()
    bands = {2: [(3, 4, BAND_AMBER)], 3: [(2, 2, BAND_TEAL)]}.get(k, [])
    ys = code_panel(d, 'the MCP client configuration  (JSON)', JSON6, bands if k >= 1 else [], size=24, line_h=40, y0=215)
    if k == 2:
        text_l(d, (130, 535), 'adjust this path to where your project is', font(26, True), WARN_L)
    if k == 3:
        text_l(d, (130, 535), 'the client launches the server and talks through stdio', font(26, True), NOTE)
    return img, d


# ---------- scene 7 · one registry, two routes ----------
B7 = ['The same tools reach two routes.',
      'The agent receives only the tools on its own list, through pickTools.',
      'The MCP server registers all of them.',
      'To add a tool, you write the file and add it to the registry. Neither the agent nor the server needs to change.',
      'A third route, like an HTTP API, would only need to call createTools.']


def s7(k):
    img, d = cv()
    text_c(d, (640, 70), 'One registry, two routes', font(44, True))
    if k >= 1:
        rbox(d, (440, 120, 840, 290), 'acc', hi=(k == 1))
        text_c(d, (640, 150), 'createTools()', font(28, True))
        for i, t in enumerate(['search_policies', 'create_ticket', 'lookup_cep']):
            rbox(d, (475, 175 + i * 36, 805, 205 + i * 36), 'box', r=8)
            text_c(d, (640, 190 + i * 36), t, font(19, True, True))
    if k >= 2:
        box(d, 50, 160, 260, 110, 'runAgent', 'only the agent\'s tools', 'acc', hi=(k == 2), tsize=26, ssize=19)
        arrow(d, [(438, 205), (314, 205)], C['ink'], 4, head=11)
        text_c(d, (376, 185), 'pickTools()', font(17, True, True), C['muted'])
    if k >= 3:
        box(d, 970, 160, 260, 110, 'MCP server', 'all of them', 'blue', hi=(k == 3), tsize=26, ssize=19)
        arrow(d, [(842, 205), (966, 205)], C['ink'], 4, head=11)
        text_c(d, (904, 185), 'registerTool()', font(17, True, True), C['muted'])
        box(d, 970, 360, 260, 70, 'Claude Code / Desktop', '', 'box', tsize=20)
        arrow(d, [(1100, 362), (1100, 272)], C['ink'], 4, head=11)
        box(d, 50, 360, 260, 70, 'node src/cli.js agent', '', 'box', tsize=18)
        arrow(d, [(180, 362), (180, 272)], C['ink'], 4, head=11)
    if k >= 4:
        rbox(d, (330, 470, 950, 560), 'warn', hi=True)
        text_c(d, (640, 500), 'add one line in tools/index.js', font(26, True), C['warn'])
        text_c(d, (640, 536), 'both routes see the new tool', font(26, True), C['warn'])
    if k >= 5:
        rbox(d, (470, 340, 810, 420), 'box')
        dashed(d, (640, 292), (640, 338), C['muted'], 3)
        text_c(d, (640, 366), 'a third route', font(22, True), C['muted'])
        text_c(d, (640, 398), 'HTTP API  (future)', font(20, True, True), C['muted'])
    return img, d


# ---------- scene 8 · a caution ----------
B8 = ['One caution.',
      'When a client calls the tools through MCP, the agent is not involved.',
      'Its input guardrail, and its hooks, do not run.',
      'The client decides what to ask.',
      'So the tools themselves must be safe, and sensitive actions need their own protection.']


def s8(k):
    img, d = cv()
    text_c(d, (640, 85), 'A caution', font(50, True), C['warn'])
    if k >= 2:
        rbox(d, (60, 150, 620, 400), 'acc', hi=(k == 2))
        text_c(d, (340, 190), 'through the agent', font(28, True), C['acc'])
        for i, t in enumerate(['user', 'checkInput + hooks', 'tool']):
            box(d, 100 + 0, 225 + i * 55, 480, 44, t, '', 'warn' if i == 1 else 'box', tsize=21)
    if k >= 3:
        rbox(d, (660, 150, 1220, 400), 'warn', hi=(k == 3))
        text_c(d, (940, 190), 'through MCP', font(28, True), C['warn'])
        for i, t in enumerate(['MCP client', 'no guardrails, no hooks', 'tool']):
            box(d, 700, 225 + i * 55, 480, 44, t, '', 'box' if i != 1 else 'blue', tsize=21)
    if k >= 4:
        text_c(d, (940, 430), 'the client decides what to ask', font(26, True), C['warn'])
    if k >= 5:
        rbox(d, (150, 480, 1130, 565), 'warn', hi=True)
        text_c(d, (640, 522), 'the tools must be safe on their own', font(33, True), C['warn'])
    return img, d


# ---------- scene 9 · wrap-up ----------
B9 = ['To sum up: MCP is the standard outlet for tools.',
      'Our server takes the same tools of the agent, and offers them to any MCP client.',
      'The golden rule: only the protocol goes through standard output.',
      'In the next chapter, we will see the same agent running on LangChain and LangGraph.',
      'See you there!']


def s9(k):
    img, d = cv()
    text_c(d, (640, 95), 'See you there!' if k >= 5 else 'Summing up', font(54, True), C['acc'] if k >= 5 else C['ink'])
    rows = [(1, 'blue', '1   MCP:  the standard outlet for tools'), (2, 'acc', '2   Our server offers the agent\'s tools to any client'),
            (3, 'warn', '3   stdout is for the protocol only,  logs go to stderr'), (4, 'box', 'Next chapter:  the same agent on LangChain and LangGraph')]
    for i, (kk, st, t) in enumerate(rows):
        if k >= kk:
            y = 165 + i * 105
            rbox(d, (130, y, 1150, y + 82), st, hi=(k == kk))
            text_l(d, (170, y + 41), t, font(27, True))
    return img, d


SCENES = [(B1, s1), (B2, s2), (B3, s3), (B4, s4), (B5, s5), (B6, s6), (B7, s7), (B8, s8), (B9, s9)]

if __name__ == '__main__':
    work = os.environ.get('VIDEO_WORKDIR', os.path.join(HERE, '_work', f'cap12_en_{VOICE}'))
    if len(sys.argv) > 1 and sys.argv[1] == 'preview':
        preview(SCENES, os.path.join(work, 'preview'))
        print('preview saved in', os.path.join(work, 'preview'))
    else:
        build(SCENES, os.path.join(HERE, 'saida', f'cap12_en_{VOICE}.mp4'), work, TAG)
