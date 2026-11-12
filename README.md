# ai-architect-lab

Projeto de estudo: um helpdesk interno com **RAG híbrido**, **guardrails**, **observabilidade**, **agente com tool use** e **servidor MCP**. Funciona offline (sem chave de API) para ingestão, busca, avaliação e testes.

## Requisitos

- Node.js 20+ (testado na 24)
- Opcional: `GEMINI_API_KEY` (plano gratuito do Google AI Studio) ou `ANTHROPIC_API_KEY` (respostas geradas pelo LLM e agente)
- Opcional: `VOYAGE_API_KEY` (embeddings neurais no lugar do embedder local)

## Início rápido

```bash
npm install
npm run ingest                      # indexa data/*.md em .cache/index.json
npm start "Quantos dias de férias eu tenho?"
npm start                           # modo interativo (digite "sair" para encerrar)
npm test                            # testes unitários
npm run eval                        # hit@k e MRR da recuperação
```

Com `GEMINI_API_KEY` (ou `ANTHROPIC_API_KEY`) definida:

```bash
node src/cli.js agent "Preciso abrir um chamado para resetar minha senha"
```

Sem a chave, `npm start` responde em **modo extrativo** (devolve o melhor trecho recuperado, com citação) e o comando `agent` não está disponível.

## Variáveis de ambiente

| Variável | Efeito |
|---|---|
| `GEMINI_API_KEY` (ou `GOOGLE_API_KEY`) | Ativa geração com Gemini e o agente. Tem prioridade sobre a Anthropic |
| `GEMINI_MODEL` | Troca o modelo Gemini (padrão `gemini-3.8-flash`, em `src/config.js`) |
| `ANTHROPIC_API_KEY` | Ativa geração com Claude e o agente (usada se não houver chave Gemini) |
| `LLM_MODEL` | Troca o modelo Claude (padrão em `src/config.js`) |
| `VOYAGE_API_KEY` | Usa embeddings Voyage; o índice é reconstruído se o embedder mudar |

## Arquitetura

```
pergunta
  -> guardrails de entrada (vazia, longa, prompt injection, redação de PII)
  -> cache semântico
  -> retriever híbrido: vetorial + BM25 -> RRF -> rerank -> corte por relevância
  -> prompt com fontes numeradas (conteúdo recuperado tratado como dado)
  -> Claude (ou resposta extrativa offline)
  -> guardrail de saída (exige citação [n] válida; redige PII)
  -> trace (tempo por etapa, tokens, custo estimado)
```

| Pasta | Conteúdo |
|---|---|
| `data/` | Documentos de política em Markdown, com frontmatter (`title`, `dept`, `updated`) |
| `src/rag/` | Loader, chunker por seção, embeddings, vector store, BM25, retriever, cache semântico |
| `src/guardrails/` | PII, detecção de injection, sanitização de contexto, checagem de saída |
| `src/observability/` | `Tracer` com spans, tokens e custo (preços ilustrativos em `config.js`) |
| `src/llm/` | Cliente Anthropic e fluxo `ask` completo |
| `src/agent/tools/` | Uma ferramenta por arquivo + `index.js` (registro) |
| `src/agent/agents/` | Um agente por arquivo (`helpdesk`, `triage`, `cep`) + `index.js` (registro) |
| `src/agent/runner.js` | Loop genérico que executa qualquer agente (LLM injetável) |
| `src/mcp/` | Servidor MCP via stdio, reutilizando as ferramentas do agente |
| `src/eval/` | Conjunto dourado e script de avaliação |
| `test/` | Testes com `node:test` |

## Ferramentas (agente e MCP)

- `search_policies(query, dept?)`: busca nas políticas; `dept` filtra por `rh`, `ti` ou `financeiro`.
- `create_ticket(title, description, priority?)`: abre um chamado **simulado** (guardado só em memória).
- `lookup_cep(cep)`: consulta um CEP na API pública **ViaCEP** (sem chave). Exemplo de ferramenta que chama uma API externa em vez do índice vetorial; o `fetch` é injetável, então os testes não usam a internet.

## Agentes

```bash
node src/cli.js agents                                  # lista os agentes
node src/cli.js agent "Como peço férias?"               # agente helpdesk (padrão)
node src/cli.js agent --name triage "A VPN caiu para o time todo"
node src/cli.js agent --name cep "Qual o endereço do CEP 01310-100?"   # chama a API externa ViaCEP
```

Há duas engines para executar o mesmo agente, com as mesmas ferramentas e guardrails:

```bash
node src/cli.js agent "Como peço férias?"                       # native: loop próprio (src/agent/runner.js)
node src/cli.js agent --engine langgraph "Como peço férias?"    # LangChain/LangGraph (src/agent/langgraph/)
```

A engine `langgraph` usa `createAgent` (LangChain 1.x), `ChatAnthropic`/`ChatGoogleGenerativeAI` e adapta as ferramentas existentes para `tool()`; os spans e tokens continuam indo para o `Tracer` via callback. Os testes usam o `fakeModel` do LangChain.

Um agente é só dados (`name`, `description`, `system`, `tools`, `maxSteps`); o `runner.js` executa qualquer um e só libera as ferramentas listadas nele.

### Hooks (engine `langgraph`)

A engine LangGraph usa o *middleware* do LangChain como hooks: funções que o framework chama em volta de cada ferramenta (`src/agent/langgraph/hooks.js`). Os padrão, em ordem (o primeiro é o mais externo):

| Hook | O que faz |
|---|---|
| `auditToolCalls` | registra cada chamada de ferramenta (nome, argumentos, status, tempo); a CLI imprime o resultado |
| `limitTicketsPerRun` | **valida em código** que só 1 chamado seja aberto por pedido (o prompt do agente `triage` só *pede* isso) |
| `sanitizeToolResults` | passa o resultado das ferramentas pelo `sanitizeContext` antes de o LLM lê-lo |

`runAgentLangGraph(agent, pergunta, { hooks })` aceita uma lista própria; `hooks: []` roda sem nenhum. O runner `native` **não tem** hooks.

### Adicionar uma ferramenta ou um agente

- **Ferramenta**: crie `src/agent/tools/minha-tool.js` exportando uma fábrica `createMinhaTool(deps)` e registre-a em `tools/index.js`. Agentes e servidor MCP passam a enxergá-la.
- **Agente**: crie `src/agent/agents/meu-agente.js` e registre-o em `agents/index.js`, listando em `tools` os nomes permitidos.

## Usar o servidor MCP

```bash
npm run mcp
```

Exemplo de configuração em um cliente MCP (ajuste o caminho):

```json
{
  "mcpServers": {
    "helpdesk": {
      "command": "node",
      "args": ["D:/Projetos/ai-architect-lab/src/mcp/server.js"]
    }
  }
}
```

## Adicionar documentos

1. Crie um `.md` em `data/` com frontmatter `title`, `dept` e `updated`, e seções `##`.
2. Rode `npm run ingest`.
3. Inclua perguntas em `src/eval/golden.js` e rode `npm run eval`.

## Limitações conhecidas

- O embedder local (hashing) não é semântico; serve para estudar a interface. Para qualidade real, use Voyage.
- O vector store é força-bruta em JSON; em produção use pgvector, Qdrant etc.
- O cache semântico vive só na memória do processo.
- A avaliação cobre apenas a recuperação, não a qualidade das respostas geradas.
- O caminho com Claude e o agente ainda não foram exercitados contra a API real.
- A engine `langgraph` foi testada só com modelo falso; falta rodá-la com uma chave real.
