# Videoaulas (rascunho gerado por código)

Gera um vídeo MP4 a partir de cenas escritas em Python: slides animados (os elementos aparecem em sincronia com
cada frase), narração com a voz do Windows e legenda na tela. Serve como **rascunho** para validar roteiro,
ritmo e visual; as vozes são robóticas.

| Arquivo | O que é |
|---|---|
| `engine.py` | Motor: desenha os slides, gera a voz, monta o MP4 |
| `cap01_en.py` … `cap20_en.py` | Um roteiro por capítulo, **em inglês** (narração, legenda e slides), voz inglesa em todo o vídeo. O capítulo 6 tem `cap06a/b`; o 18 tem `cap18a/b` (usam `cap18_common.py`) |
| `cap01.py` | Capítulo 1 em português (voz Maria; termos em inglês saem mal) |
| `saida/` | Os vídeos gerados |

## Requisitos

- Windows. Vozes usadas (acompanham o sistema): **Microsoft Zira** e **David** (inglês), **Maria** (português)
- Python 3.10+ e dois pacotes: `pillow` e `imageio-ffmpeg` (este traz o ffmpeg embutido)

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install pillow imageio-ffmpeg
```

## Usar

```powershell
.venv\Scripts\python cap01_en.py preview        # salva um PNG por frase em _work\... (para olhar o visual)
.venv\Scripts\python cap01_en.py                # gera saida\cap01_en_zira.mp4 (voz feminina)
$env:VOICE='david'; .venv\Scripts\python cap01_en.py   # gera saida\cap01_en_david.mp4 (voz masculina)
```

`_work/` guarda arquivos temporários (imagens e áudio) e pode ser apagada.

## Criar outro capítulo

Copie `cap01_en.py`, troque o `TAG`, escreva as listas de frases (`B1`, `B2`, ...) e uma função `sN(k)` por cena.
Em `sN(k)`, `k` é quantas frases já foram ditas: desenhe só o que `k` permite (`if k >= 3: ...`) e o elemento
aparece quando a frase número 3 começa. Use `hi=(k == 3)` para destacar o que acabou de aparecer.

## Pronúncia

A legenda mostra o texto original; a fala pode usar outra grafia. Em `cap01_en.py`, a lista `engine.SPEECH` troca
termos **só na fala** (siglas como `MCP` viram `M C P`). Se uma palavra sair estranha, acrescente uma linha ali.
