"""Chapter 18, part B · Building the app from zero: steps 11 to 20 (English, voice: Zira by default)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cap18_common as cc  # noqa: E402
from cap18_common import C, NOTE, box, canvas, font, make_scene, rbox, text_c, text_l  # noqa: E402
from engine import build, preview  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
TAG = 'Chapter 18b · Building it from zero'
VOICE = cc.VOICE


def cv():
    return canvas(TAG)


B1 = ['Hello again!',
      'This is part B of building the application from zero.',
      'We continue from step eleven, with the whole retrieval pipeline already working.',
      'Now we add the model, the question flow, the evaluation, the agents, the server, the command line, the second engine, and the tests.']


def s1(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 190), 'Building it from zero · part B', font(60, True))
    if k >= 2:
        text_c(d, (640, 275), 'steps 11 to 20', font(36), C['acc'])
    if k >= 3:
        box(d, 150, 370, 420, 90, 'Part A  ✓', 'retrieval pipeline', 'acc', tsize=30, ssize=21)
    if k >= 4:
        box(d, 710, 370, 420, 90, 'Part B', 'model · agents · CLI · tests', 'blue', hi=True, tsize=30, ssize=21)
    return img, d


STEPS = [
    (11, 'Talk to the LLM', [('src/llm/client.js', 23), ('src/llm/gemini.js', 96)],
     ['client.js: the single door to the model, Gemini or Claude', 'gemini.js: adapter for the Gemini format, with retries'], 'config', ['hasLLM() is false without a key', '4 tests in test/gemini.test.js'],
     ['Step eleven: talk to the model.', 'Two files: client dot J S, with twenty three lines, and gemini dot J S, with ninety six.',
      'The client is the single door to the model: Gemini first, then Claude. The Gemini file translates formats, and retries when the service answers too many requests.',
      'The check: without a key, has L L M is false, and the four Gemini tests pass.']),
    (12, 'Question and answer', [('src/llm/ask.js', 57)],
     ['createAssistant(): cache → retrieve → model → check', 'Offline mode returns the best chunk, with a citation'], 'steps 4 to 11',
     ['"Quantos dias de férias eu tenho?"', '→ best chunk + [1]  ·  4 sources  ·  trace: cache, retrieve'],
     ['Step twelve: question and answer.', 'One file, ask dot J S, with fifty seven lines. It is the main flow we saw in chapter fifteen.',
      'It checks the input, consults the cache, retrieves chunks, calls the model if there is a key, checks the output, and saves in the cache.',
      'The check: without a key, you get the best chunk, with the citation one, four sources, and a trace with the cache and retrieve steps.']),
    (13, 'Measure the search quality', [('src/eval/golden.js', 14), ('src/eval/run.js', 18)],
     ['golden.js: 11 questions with the expected document', 'run.js: computes hit@4 and MRR'], 'step 7', ['npm run eval', 'hit@4: 100%   MRR: 1.00'],
     ['Step thirteen: measure the search quality.', 'The golden set, with fourteen lines, and the runner, with eighteen.',
      'Eleven questions, each one with the document that must appear. The script computes hit at four, and M R R.',
      'The check: npm run eval prints one hundred percent, and M R R one.']),
    (14, 'The agent tools', [('src/agent/tools/search-policies.js', 15), ('src/agent/tools/create-ticket.js', 17), ('src/agent/tools/lookup-cep.js', 24), ('src/agent/tools/index.js', 21)],
     ['Contract: { name, description, schema, run }', 'Each factory receives its dependencies', 'index.js: the registry, and pickTools()'], 'step 7',
     ['createTools() returns 3 tools', 'search_policies · create_ticket · lookup_cep'],
     ['Step fourteen: the agent tools.', 'Four files. Three tools, and a registry.',
      'Every tool has the same contract: name, description, schema, and run. And each factory receives what it needs, like the retriever, so tests can fake it.',
      'The check: create tools returns three tools.']),
    (15, 'The agents', [('src/agent/agents/helpdesk-agent.js', 10), ('src/agent/agents/triage-agent.js', 13), ('src/agent/agents/cep-agent.js', 11), ('src/agent/agents/index.js', 12)],
     ['An agent is data: name, description, system,', 'tools (least privilege), maxSteps', 'index.js: the registry, getAgent()'], 'step 14',
     ['getAgent("x") throws "desconhecido"', 'every agent has a full contract (agent test)'],
     ['Step fifteen: the agents.', 'Three agents and a registry. An agent is only data: a name, a description, instructions, the allowed tools, and a step limit.',
      'Each agent lists only the tools it needs. That is least privilege.',
      'The check: asking for an unknown agent throws an error, and every agent has the full contract.']),
    (16, 'The agent loop', [('src/agent/runner.js', 38)],
     ['runAgent(): checkInput, then a for loop', 'model → tool → result → model ... until text', 'maxSteps stops a stuck agent; errors become results'], 'steps 11, 14, 15, 8, 9',
     ['4 tests in test/agent.test.js', 'with a scripted model: no key needed'],
     ['Step sixteen: the agent loop.', 'Thirty eight lines. It is the heart of the agent, as in chapter eleven.',
      'It checks the input, then repeats: call the model, run the tool it asks for, and give the result back, until the model answers with text.',
      'The check: four tests, using a scripted model, so no key is needed.']),
    (17, 'The MCP server', [('src/mcp/server.js', 18)],
     ['Exposes the same tools to any MCP client', 'over stdio: stdout is the protocol, stderr for logs'], 'steps 7, 14', ['an MCP client lists 3 tools:', 'search_policies · create_ticket · lookup_cep'],
     ['Step seventeen: the M C P server.', 'Eighteen lines.',
      'It loops over the same tools, and registers each one. Any M C P client can then use them. Remember the golden rule: stdout is only for the protocol.',
      'The check: a client connected to it lists three tools.']),
    (18, 'The command line', [('src/cli.js', 52)],
     ['ingest · agents · agent [--name] [--engine]', 'anything else = a question, or interactive mode'], 'steps 7, 12, 15, 16',
     ['npm start "Quantos dias de férias eu tenho?"', 'node src/cli.js agents  →  helpdesk · triage · cep'],
     ['Step eighteen: the command line.', 'One file with fifty two lines. It reads the first word, and chooses the flow, as we saw in chapter fifteen.',
      'It also reads the flags: the agent name, and the engine.',
      'The check: ask a question, and list the agents.']),
    (19, 'Second engine: LangGraph', [('src/agent/langgraph/tools.js', 18), ('src/agent/langgraph/model.js', 21), ('src/agent/langgraph/runner.js', 88), ('src/agent/langgraph/hooks.js', 66)],
     ['tools.js: wraps our tools for LangChain', 'model.js: LangChain chat models', 'runner.js: createAgent + callbacks', 'hooks.js: validate, sanitize, audit'], 'steps 8, 9, 14, 15',
     ['3 tests in test/langgraph.test.js', '5 tests in test/hooks.test.js  (fake model)'],
     ['Step nineteen: the second engine, with Lang Graph.', 'Four files: the tools adapter, the model, the runner, and the hooks.',
      'The agents, the tools, and the guardrails stay the same. Only the loop is replaced, by create agent.',
      'The check: the Lang Graph tests and the hooks tests, all with a fake model.']),
    (20, 'Automated tests', [('test/agent.test.js', 57), ('test/cep.test.js', 65), ('test/gemini.test.js', 46), ('test/guardrails.test.js', 23), ('test/hooks.test.js', 56), ('test/langgraph.test.js', 48), ('test/rag.test.js', 29)],
     ['The built-in Node test runner; fake models,', 'a fake retriever and a fake fetch'], 'everything before', ['npm test', 'tests 26  ·  pass 26  ·  fail 0'],
     ['Step twenty: the automated tests.', 'Seven files, with three hundred twenty four lines in total.',
      'They use the Node test runner, with fake models, a fake retriever, and a fake fetch, so no key and no internet are needed.',
      'The check: npm test, with twenty six tests, all passing.']),
]

B3 = ['And that is the whole application: twenty steps, thirty two source files, about one thousand lines.',
      'Each file uses only the ones before it, and each step ends with a check.',
      'One honest remark: the checks of the agent and of the model, were done with fake models, never with a real key.',
      'This closes the series. Thank you for following along, and good luck with your studies!']


def s_end(k):
    img, d = cv()
    text_c(d, (640, 90), 'Thank you!' if k >= 4 else 'All 20 steps', font(56, True), C['acc'] if k >= 4 else C['ink'])
    rows = [(1, 'acc', '20 steps  ·  32 source files  ·  about 1,000 lines'), (2, 'blue', 'Each file uses only the ones before it'),
            (3, 'warn', 'Agent and model checks: fake models only, never a real key')]
    for i, (kk, st, t) in enumerate(rows):
        if k >= kk:
            y = 170 + i * 110
            rbox(d, (110, y, 1170, y + 86), st, hi=(k == kk))
            text_l(d, (150, y + 43), t, font(25, True))
    if k >= 4:
        text_c(d, (640, 540), 'good luck with your studies!', font(34, True), C['muted'])
    return img, d


SCENES = [(B1, s1)] + [(s[6], make_scene(s, TAG)[1]) for s in STEPS] + [(B3, s_end)]

if __name__ == '__main__':
    work = os.environ.get('VIDEO_WORKDIR', os.path.join(HERE, '_work', f'cap18b_en_{VOICE}'))
    if len(sys.argv) > 1 and sys.argv[1] == 'preview':
        preview(SCENES, os.path.join(work, 'preview'))
        print('preview saved in', os.path.join(work, 'preview'))
    else:
        build(SCENES, os.path.join(HERE, 'saida', f'cap18b_en_{VOICE}.mp4'), work, TAG)
