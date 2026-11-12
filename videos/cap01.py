"""Capítulo 1 · A viagem de uma pergunta.  Uso:  python cap01.py preview   |   python cap01.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import C, arrow, box, build, canvas, font, preview, rbox, text_c, text_l  # noqa: E402

TAG = 'Capítulo 1 · A viagem de uma pergunta'
HERE = os.path.dirname(os.path.abspath(__file__))


def cv():
    return canvas(TAG)


# ---------- peças reutilizáveis: as duas "faixas" do diagrama do capítulo ----------
LANE1 = [('Documentos', 'data/*.md', 'box'), ('Chunks', 'pedaços por seção', 'acc'),
         ('Embeddings', 'texto vira números', 'acc'), ('Índice', '.cache/index.json', 'blue')]
LANE2 = [('Pergunta', 'do usuário', 'box'), ('Guardrail', 'de entrada', 'warn'), ('Busca', 'chunks certos', 'acc'),
         ('Prompt', 'fontes + pergunta', 'box'), ('LLM', 'escreve a resposta', 'acc'),
         ('Guardrail', 'de saída', 'warn'), ('Resposta', 'com [citação]', 'box')]
L1X, L1W = [65, 371, 677, 983], 250
L2X, L2W = [57 + i * 170 for i in range(7)], 146


def lane1(d, n, hi=None, y=190, h=96, tsize=24, ssize=17):
    for i, (t, s, st) in enumerate(LANE1[:n]):
        box(d, L1X[i], y, L1W, h, t, s, st, hi=(hi == i), tsize=tsize, ssize=ssize)
        if i:
            arrow(d, [(L1X[i - 1] + L1W + 8, y + h / 2), (L1X[i] - 8, y + h / 2)], C['ink'], 4, head=12)


def lane2(d, shown, hi=None, y=430, h=96):
    """shown: conjunto de índices visíveis da faixa 2."""
    for i, (t, s, st) in enumerate(LANE2):
        if i in shown:
            box(d, L2X[i], y, L2W, h, t, s, st, hi=(hi == i), tsize=22, ssize=15)
            if i - 1 in shown:
                arrow(d, [(L2X[i - 1] + L2W + 3, y + h / 2), (L2X[i] - 3, y + h / 2)], C['ink'], 3, head=9)


# ---------- cena 1 · abertura ----------
B1 = ['Olá!',
      'Neste capítulo, você vai acompanhar a viagem de uma pergunta dentro do nosso assistente de helpdesk.',
      'Do momento em que alguém digita uma dúvida, até a resposta aparecer na tela, com a fonte citada.',
      'Ao final, você vai saber quais são as etapas, e em que ordem elas acontecem.']


def s1(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 235), 'A viagem de uma pergunta', font(68, True))
    if k >= 2:
        text_c(d, (640, 318), 'dentro do assistente de helpdesk', font(36), C['acc'])
    if k >= 3:
        box(d, 150, 395, 340, 96, 'Dúvida do usuário', '', 'box', hi=(k == 3), tsize=27)
        arrow(d, [(505, 443), (775, 443)], C['ink'], 5)
        box(d, 790, 395, 340, 96, 'Resposta com fonte citada', '', 'acc', hi=(k == 3), tsize=25)
    if k >= 4:
        text_c(d, (640, 560), 'Quais são as etapas   ·   Em que ordem acontecem', font(30, True), C['muted'])
    return img, d


# ---------- cena 2 · o problema e o RAG ----------
B2 = ['Antes, uma lembrança rápida.',
      'Um modelo de linguagem, como o Claude ou o Gemini, escreve texto muito bem, mas não conhece as regras da sua empresa.',
      'Se você perguntar quantos dias de férias tem direito, ele pode inventar uma resposta que parece correta, e está errada.',
      'A solução se chama R-A-G.',
      'A ideia é simples: antes de responder, o sistema busca nos documentos da empresa os trechos certos, e entrega esses trechos ao modelo.',
      'Como numa prova com consulta.']


def s2(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 95), 'Uma lembrança rápida', font(46, True))
    if k >= 2:
        rbox(d, (60, 150, 610, 590), 'box')
        text_c(d, (335, 200), 'Modelo de linguagem', font(32, True), C['blue'])
        text_l(d, (100, 270), '•  Escreve texto muito bem', font(27))
        text_l(d, (100, 325), '•  Não conhece as regras da empresa', font(27))
    if k >= 3:
        rbox(d, (90, 385, 580, 565), 'warn', hi=(k == 3))
        text_c(d, (335, 428), '"Quantos dias de férias eu tenho?"', font(25, True))
        text_c(d, (335, 485), 'Resposta inventada:', font(26, True), C['warn'])
        text_c(d, (335, 525), 'parece certa, mas está errada', font(25), C['warn'])
    if k >= 4:
        rbox(d, (670, 150, 1220, 590), 'acc', hi=(k == 4))
        text_c(d, (945, 205), 'RAG', font(54, True), C['acc'])
        text_c(d, (945, 255), 'Retrieval-Augmented Generation', font(21), C['muted'])
    if k >= 5:
        for i, s in enumerate(['1   Buscar nos documentos', '2   Entregar os trechos ao modelo', '3   Responder com base neles']):
            text_l(d, (705, 330 + i * 65), s, font(27))
    if k >= 6:
        text_c(d, (945, 540), 'como numa prova com consulta', font(26, True), C['acc'])
    return img, d


# ---------- cena 3 · dois momentos ----------
B3 = ['Todo o projeto acontece em dois momentos bem separados.',
      'O primeiro é o antes.',
      'Ele acontece uma única vez, quando você roda o comando n-p-m run ingest, e prepara os documentos para serem pesquisados.',
      'O segundo é o depois.',
      'Ele acontece a cada pergunta, e é uma esteira que termina numa resposta.',
      'Guarde essa divisão: preparar uma vez, responder muitas vezes.']


def s3(k):
    img, d = cv()
    if k >= 1:
        text_l(d, (65, 150), 'ANTES' if k < 3 else 'ANTES   ·   uma vez   ·   npm run ingest', font(28, True), C['acc'])
        text_l(d, (57, 390), 'DEPOIS' if k < 5 else 'DEPOIS   ·   a cada pergunta', font(28, True), C['warn'])
    if k >= 2:
        lane1(d, 4, hi=(0 if k == 2 else None))
    if k >= 4:
        lane2(d, set(range(7)), hi=(None))
    if k == 6:
        text_c(d, (640, 590), 'Preparar uma vez   ·   Responder muitas vezes', font(34, True), C['acc'])
    return img, d


# ---------- cena 4 · o "antes" ----------
B4 = ['Vamos ao primeiro momento.',
      'Tudo começa nos documentos: arquivos de texto com as políticas da empresa.',
      'O sistema corta cada documento em pedaços pequenos, chamados chunks.',
      'Depois, transforma o texto de cada pedaço numa lista de números, o embedding, que permite medir quando dois textos são parecidos.',
      'Por fim, guarda tudo num arquivo, o índice.',
      'Esse arquivo é o resultado do primeiro momento.']
CAP4 = ['políticas da empresa', 'fichas pequenas, por seção', 'lista de 512 números', 'o resultado do 1º momento']


def s4(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 105), 'Antes: preparar o índice', font(48, True), C['acc'])
        text_c(d, (640, 160), 'acontece uma vez  ·  npm run ingest', font(25), C['muted'])
    if k >= 2:
        lane1(d, k - 1, hi=(k - 2), y=250, h=130, tsize=28, ssize=19)
        for i in range(min(k - 1, 4)):
            text_c(d, (L1X[i] + L1W / 2, 412), CAP4[i], font(22), C['muted'])
    if k == 6:
        text_c(d, (640, 520), 'o índice é o que a busca vai consultar', font(32, True), C['blue'])
    return img, d


# ---------- cena 5 · o "depois" ----------
B5 = ['Agora, o segundo momento: o que acontece quando alguém faz uma pergunta.',
      'Primeiro, a pergunta passa pelo guardrail de entrada, uma verificação de segurança.',
      'Ele bloqueia pedidos vazios ou suspeitos, e esconde dados pessoais, como C-P-F.',
      'Em seguida, a busca procura no índice os trechos mais relevantes.',
      'Esses trechos são montados num prompt, junto com a pergunta.',
      'O modelo escreve a resposta com base apenas neles.',
      'E, antes de chegar ao usuário, o guardrail de saída confere se a resposta cita uma fonte válida.',
      'Só então ela aparece.']
VIS5 = {1: {0}, 2: {0, 1}, 3: {0, 1}, 4: {0, 1, 2}, 5: {0, 1, 2, 3}, 6: {0, 1, 2, 3, 4}, 7: {0, 1, 2, 3, 4, 5}, 8: set(range(7))}
NEW5 = {1: 0, 2: 1, 4: 2, 5: 3, 6: 4, 7: 5, 8: 6}


def s5(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 105), 'Depois: a cada pergunta', font(48, True), C['warn'])
        text_c(d, (640, 160), 'a esteira que termina numa resposta', font(25), C['muted'])
        lane2(d, VIS5[k], hi=NEW5.get(k), y=270, h=120)
    if k >= 3:
        text_c(d, (L2X[1] + L2W / 2, 430), 'bloqueia vazio ou suspeito', font(21, True), C['warn'])
        text_c(d, (L2X[1] + L2W / 2, 462), 'esconde dados pessoais (CPF)', font(21), C['warn'])
    if k >= 7:
        text_c(d, (L2X[5] + L2W / 2, 430), 'confere a citação [n]', font(21, True), C['warn'])
    return img, d


# ---------- cena 6 · o índice liga os dois momentos ----------
B6 = ['Repare nesta seta tracejada.',
      'Ela é a ligação entre os dois momentos: a busca consulta o índice que foi criado antes.',
      'Sem ele, a busca não teria onde procurar.']


def s6(k):
    img, d = cv()
    text_l(d, (65, 150), 'ANTES', font(28, True), C['acc'])
    text_l(d, (57, 390), 'DEPOIS', font(28, True), C['warn'])
    lane1(d, 4, hi=(3 if k == 3 else None))
    lane2(d, set(range(7)), hi=(2 if k == 3 else None))
    if k >= 1:
        arrow(d, [(1108, 292), (1108, 352), (L2X[2] + L2W / 2, 352), (L2X[2] + L2W / 2, 424)], C['blue'], 5, dash=True)
    if k >= 2:
        text_c(d, (790, 328), 'a busca consulta o índice criado antes', font(24, True), C['blue'])
    return img, d


# ---------- cena 7 · mapa das peças ----------
B7 = ['Agora, a mesma ideia vista pelas peças do código.',
      'Existem duas portas de entrada: a linha de comando, e o servidor M-C-P, que veremos mais à frente.',
      'Pela linha de comando, há duas formas de falar com o modelo.',
      'A primeira é a função ask, para perguntas e respostas.',
      'A segunda é a run-agent, para o modo agente, em que o modelo decide o que fazer.',
      'As duas usam o mesmo retriever, o componente que faz a busca.',
      'E o agente e o servidor M-C-P usam as mesmas ferramentas.',
      'Escreveu uma vez, funciona nos dois lugares.']


def s7(k):
    img, d = cv()
    if k >= 1:
        text_c(d, (640, 80), 'O mapa das peças', font(44, True))
    if k >= 2:
        box(d, 250, 125, 280, 66, 'CLI', 'src/cli.js', 'box', hi=(k == 2), tsize=26, ssize=17)
        box(d, 700, 125, 280, 66, 'Servidor MCP', 'src/mcp/server.js', 'blue', hi=(k == 2), tsize=26, ssize=17)
    if k >= 3:
        arrow(d, [(390, 193), (390, 225), (200, 225), (200, 252)], C['ink'], 4, head=12)
        arrow(d, [(390, 193), (390, 225), (530, 225), (530, 252)], C['ink'], 4, head=12)
    if k >= 3:
        box(d, 70, 255, 260, 66, 'ask()', 'perguntas e respostas', 'box', hi=(k == 4), tsize=26, ssize=16)
        box(d, 400, 255, 260, 66, 'runAgent()', 'modo agente', 'acc', hi=(k == 5), tsize=26, ssize=16)
    if k >= 5:
        box(d, 1010, 255, 190, 66, 'LLM', 'Gemini ou Claude', 'box', tsize=26, ssize=16)
        arrow(d, [(666, 288), (1004, 288)], C['ink'], 4, head=12)
        text_c(d, (752, 268), 'mensagens + tools', font(17), C['muted'])
    if k >= 6:
        box(d, 300, 470, 460, 62, 'Retriever híbrido', 'vetorial + BM25 → RRF → rerank', 'box', hi=(k == 6), tsize=25, ssize=16)
        arrow(d, [(200, 323), (200, 501), (294, 501)], C['ink'], 4, head=12)
    if k >= 7:
        box(d, 680, 365, 290, 66, 'Ferramentas', 'search_policies · create_ticket', 'acc', hi=(k == 7), tsize=26, ssize=15)
        arrow(d, [(840, 193), (840, 359)], C['ink'], 4, head=12)
        text_l(d, (852, 230), 'tools/call', font(17), C['muted'])
        arrow(d, [(530, 323), (530, 398), (674, 398)], C['ink'], 4, head=12)
        arrow(d, [(820, 433), (820, 501), (766, 501)], C['ink'], 4, head=12)
    if k >= 8:
        rbox(d, (70, 560, 1210, 612), 'warn', hi=True)
        text_c(d, (640, 586), 'Camadas transversais:  Guardrails  ·  Cache  ·  Tracer  ·  config.js', font(24, True), C['warn'])
    return img, d


# ---------- cena 8 · o arquivo cli.js ----------
B8 = ['O ponto de entrada de tudo é o arquivo cli ponto jota-ésse.',
      'Ele lê o que você digita no terminal e decide o caminho.',
      'Se for a palavra ingest, constrói o índice.',
      'Se for agent, executa um agente.',
      'Qualquer outra coisa é tratada como uma pergunta e vai para a função ask.',
      'Por enquanto, não se preocupe com os detalhes do código: nos próximos capítulos, vamos abrir cada peça.']
CODE = ["if (cmd === 'ingest') {", "  await buildIndex({ log: console.log });", "} else if (cmd === 'agent') {",
        "  // roda um agente", "} else {", "  const { ask } = await createAssistant();",
        "  print(await ask(q));   // responde a pergunta", "}"]
HL8 = {3: (0, 1), 4: (2, 3), 5: (4, 7)}


def s8(k):
    img, d = cv()
    if k >= 1:
        d.rounded_rectangle((90, 130, 1190, 610), 18, fill=C['code_bg'])
        d.rounded_rectangle((90, 130, 1190, 182), 18, fill=(29, 44, 56))
        text_l(d, (120, 156), 'src/cli.js  (trecho simplificado)', font(24, False, True), C['code_ink'])
    if k >= 2:
        if k in HL8:
            a, b = HL8[k]
            d.rectangle((100, 205 + a * 46, 1180, 205 + (b + 1) * 46), fill=(24, 74, 82))
        for i, line in enumerate(CODE):
            text_l(d, (125, 228 + i * 46), line, font(30, False, True), C['code_ink'])
    return img, d


# ---------- cena 9 · fechamento ----------
B9 = ['Resumindo: o projeto tem dois momentos.',
      'Preparar o índice, uma vez.',
      'E responder a cada pergunta, passando por segurança, busca, modelo, e uma checagem final.',
      'No próximo capítulo, vamos olhar os documentos que alimentam o sistema.',
      'Até lá!']


def s9(k):
    img, d = cv()
    text_c(d, (640, 105), 'Até lá!' if k >= 5 else 'Resumindo', font(56, True), C['acc'] if k >= 5 else C['ink'])
    if k >= 2:
        rbox(d, (150, 180, 1130, 280), 'acc', hi=(k == 2))
        text_l(d, (190, 230), '1   Preparar o índice, uma vez', font(32, True))
    if k >= 3:
        rbox(d, (150, 315, 1130, 415), 'warn', hi=(k == 3))
        text_l(d, (190, 365), '2   Responder a cada pergunta:  segurança → busca → modelo → checagem', font(29, True))
    if k >= 4:
        rbox(d, (150, 455, 1130, 555), 'blue', hi=(k == 4))
        text_l(d, (190, 505), 'Próximo capítulo:  os documentos que alimentam o sistema', font(30, True))
    return img, d


SCENES = [(B1, s1), (B2, s2), (B3, s3), (B4, s4), (B5, s5), (B6, s6), (B7, s7), (B8, s8), (B9, s9)]

if __name__ == '__main__':
    work = os.environ.get('VIDEO_WORKDIR', os.path.join(HERE, '_work', 'cap01'))
    if len(sys.argv) > 1 and sys.argv[1] == 'preview':
        preview(SCENES, os.path.join(work, 'preview'))
        print('prévia salva em', os.path.join(work, 'preview'))
    else:
        build(SCENES, os.path.join(HERE, 'saida', 'cap01.mp4'), work, TAG)
