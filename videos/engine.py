"""Motor das videoaulas: desenha slides animados, gera a narração e monta o MP4.

Como funciona:
  - Cada cena é uma lista de "batidas" (uma frase de narração por batida) e uma função draw(k) que
    desenha o slide mostrando só os elementos das batidas 0..k. A cada frase um elemento novo aparece
    (com um fade curto), então a animação fica em sincronia com a fala.
  - A voz vem do Windows (Microsoft Maria Desktop, pt-BR). Cada frase vira um WAV, e a duração do WAV
    define quanto tempo a batida dura.
  - O ffmpeg (do pacote imageio-ffmpeg) junta imagens e áudio num MP4.
Requisitos: Windows, Pillow e imageio-ffmpeg (veja videos/README.md).
"""
import json
import math
import os
import re
import subprocess
import wave

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 720
FPS = 15
FADE = 0.4      # duração do fade de cada elemento novo (s)
PAUSE = 0.28    # silêncio depois de cada frase (s)
SUB_H = 92      # altura da barra de legenda

C = dict(
    bg=(244, 246, 249), ink=(21, 33, 44), muted=(85, 100, 111), card=(255, 255, 255), line=(195, 205, 215),
    acc=(11, 122, 117), acc_soft=(223, 241, 239), warn=(180, 83, 9), warn_soft=(251, 238, 219),
    blue=(36, 87, 197), blue_soft=(227, 235, 251), code_bg=(16, 26, 35), code_ink=(226, 236, 243),
)
STYLE = {  # nome -> (preenchimento, contorno)
    'box': (C['card'], C['ink']), 'acc': (C['acc_soft'], C['acc']),
    'warn': (C['warn_soft'], C['warn']), 'blue': (C['blue_soft'], C['blue']),
}
_FONTS = 'C:/Windows/Fonts/'


def font(size, bold=False, mono=False):
    name = ('consolab.ttf' if bold else 'consola.ttf') if mono else ('segoeuib.ttf' if bold else 'segoeui.ttf')
    return ImageFont.truetype(_FONTS + name, size)


# ---------- desenho ----------
def canvas(tag=None):
    img = Image.new('RGB', (W, H), C['bg'])
    d = ImageDraw.Draw(img)
    if tag:
        d.text((40, 30), tag, font=font(20), fill=C['muted'], anchor='lm')
    return img, d


def rbox(d, box, style='box', hi=False, r=16, w=3):
    fill, line = STYLE[style]
    if hi:  # destaque: contorno mais grosso e uma "sombra" colorida
        x0, y0, x1, y1 = box
        d.rounded_rectangle((x0 - 6, y0 - 6, x1 + 6, y1 + 6), r + 6, outline=line, width=2)
        w = 5
    d.rounded_rectangle(box, r, fill=fill, outline=line, width=w)


def text_c(d, xy, s, f, fill=None):
    d.text(xy, s, font=f, fill=fill or C['ink'], anchor='mm')


def text_l(d, xy, s, f, fill=None):
    d.text(xy, s, font=f, fill=fill or C['ink'], anchor='lm')


def wrap(d, s, f, maxw):
    lines, cur = [], ''
    for word in s.split():
        t = (cur + ' ' + word).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def box(d, x, y, w, h, title, sub='', style='box', hi=False, tsize=24, ssize=17):
    rbox(d, (x, y, x + w, y + h), style, hi)
    if sub:
        text_c(d, (x + w / 2, y + h * 0.38), title, font(tsize, True))
        text_c(d, (x + w / 2, y + h * 0.70), sub, font(ssize), C['muted'])
    else:
        text_c(d, (x + w / 2, y + h / 2), title, font(tsize, True))


def dashed(d, p1, p2, color, w=4, dash=14, gap=9):
    (x1, y1), (x2, y2) = p1, p2
    length = math.hypot(x2 - x1, y2 - y1)
    if not length:
        return
    ux, uy, pos = (x2 - x1) / length, (y2 - y1) / length, 0
    while pos < length:
        e = min(pos + dash, length)
        d.line((x1 + ux * pos, y1 + uy * pos, x1 + ux * e, y1 + uy * e), fill=color, width=w)
        pos += dash + gap


def arrow(d, pts, color=None, w=4, dash=False, head=14):
    color = color or C['ink']
    for a, b in zip(pts, pts[1:]):
        if dash:
            dashed(d, a, b, color, w)
        else:
            d.line((*a, *b), fill=color, width=w)
    (x1, y1), (x2, y2) = pts[-2], pts[-1]
    ang = math.atan2(y2 - y1, x2 - x1)
    left = (x2 - head * math.cos(ang - 0.45), y2 - head * math.sin(ang - 0.45))
    right = (x2 - head * math.cos(ang + 0.45), y2 - head * math.sin(ang + 0.45))
    d.polygon([(x2, y2), left, right], fill=color)


def code_panel(d, title, lines, bands=(), size=25, line_h=34, y0=208, x1=1190):
    """Painel escuro de código. bands: [(linha_ini, linha_fim, (r, g, b))] destaca blocos de linhas.
    Devolve a coordenada y do centro de cada linha (útil para escrever anotações ao lado)."""
    d.rounded_rectangle((90, 130, x1, 610), 18, fill=C['code_bg'])
    d.rounded_rectangle((90, 130, x1, 182), 18, fill=(29, 44, 56))
    text_l(d, (120, 156), title, font(24, False, True), C['code_ink'])
    for a, b, col in bands:
        d.rectangle((100, y0 - line_h / 2 + a * line_h, x1 - 10, y0 - line_h / 2 + (b + 1) * line_h), fill=col)
    for i, line in enumerate(lines):
        text_l(d, (125, y0 + i * line_h), line, font(size, False, True), C['code_ink'])
    return [y0 + i * line_h for i in range(len(lines))]


BAND_TEAL, BAND_BLUE, BAND_AMBER = (24, 74, 82), (30, 52, 110), (98, 62, 20)


def subtitle(img, text):
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    od.rectangle((0, H - SUB_H, W, H), fill=(16, 26, 35, 232))
    img.paste(ov, (0, 0), ov)
    d = ImageDraw.Draw(img)
    f = font(27)
    lines = wrap(d, text, f, W - 120)[:3]
    y0 = H - SUB_H / 2 - (len(lines) - 1) * 17
    for i, ln in enumerate(lines):
        d.text((W / 2, y0 + i * 34), ln, font=f, fill=(255, 255, 255), anchor='mm')


# ---------- narração (voz do Windows) ----------
# Vozes instaladas no Windows. Com EN_VOICE definida, as palavras em inglês de EN_TERMS são faladas por ela
# (a voz muda no meio da frase); com EN_VOICE = None, a voz portuguesa fala tudo, com a grafia "abrasileirada"
# de EN_RESPELL. A legenda sempre mostra o texto original.
PT_VOICE = 'Microsoft Maria Desktop'
EN_VOICE = os.environ.get('EN_VOICE') or None      # ex.: 'Microsoft David Desktop' ou 'Microsoft Zira Desktop'
SINGLE_VOICE = None  # se definida, ESTA voz fala o texto inteiro (use em vídeos 100% em inglês)

# Siglas soletradas e nomes: valem sempre, na voz portuguesa.
SPEECH = [
    (r'R-A-G', 'érre á gê'), (r'C-P-F', 'cê pê éfe'), (r'M-C-P', 'ême cê pê'), (r'n-p-m', 'ene pê ême'),
    (r'cli ponto jota-ésse', 'cê éle í ponto jota ésse'), (r'Claude', 'Clód'), (r'Gemini', 'Gêmini'),
]
# Termos em inglês: com voz inglesa são falados por ela; sem ela, usam a grafia abrasileirada.
EN_RESPELL = {
    'run-agent': 'rân êidjent', 'helpdesk': 'rélp désk', 'guardrail': 'gárd-reil', 'chunks': 'tchânks',
    'chunk': 'tchânk', 'embedding': 'embédin', 'prompt': 'prômpt', 'retriever': 'ritríver', 'ask': 'ásk',
    'ingest': 'ingést', 'agent': 'êidjent',
}
EN_SPOKEN = {'run-agent': 'run agent'}   # ajustes para a voz inglesa (o resto é falado como está escrito)
_EN_RE = re.compile(r'\b(' + '|'.join(sorted(map(re.escape, EN_RESPELL), key=len, reverse=True)) + r')\b', re.I)


def parts(text):
    """Divide a frase em trechos [(voz, texto)]. Sem EN_VOICE, é um trecho só, na voz portuguesa."""
    def pt(s):
        for pat, rep in SPEECH:
            s = re.sub(pat, rep, s)
        return s
    if SINGLE_VOICE:  # vídeo todo num idioma só (ex.: inglês): uma voz fala tudo, sem trocas
        return [(SINGLE_VOICE, pt(text))]
    if not EN_VOICE:
        return [(PT_VOICE, _EN_RE.sub(lambda m: EN_RESPELL[m.group(1).lower()], pt(text)))]
    out, pos = [], 0
    for m in _EN_RE.finditer(text):
        if m.start() > pos:
            out.append((PT_VOICE, pt(text[pos:m.start()])))
        out.append((EN_VOICE, EN_SPOKEN.get(m.group(1).lower(), m.group(1))))
        pos = m.end()
    if pos < len(text):
        out.append((PT_VOICE, pt(text[pos:])))
    return [(v, t) for v, t in out if t.strip()]


_PS = r"""
param($jsonPath)
Add-Type -AssemblyName System.Speech
$items = [IO.File]::ReadAllText($jsonPath, [Text.Encoding]::UTF8) | ConvertFrom-Json
$s = New-Object System.Speech.Synthesis.SpeechSynthesizer
$s.Rate = 0
# formato único para todas as vozes, para poder juntar os trechos
$fmt = New-Object System.Speech.AudioFormat.SpeechAudioFormatInfo(22050, [System.Speech.AudioFormat.AudioBitsPerSample]::Sixteen, [System.Speech.AudioFormat.AudioChannel]::Mono)
foreach ($it in $items) {
  $s.SelectVoice($it.voice)
  $s.SetOutputToWaveFile($it.path, $fmt)
  $s.Speak($it.text)
  $s.SetOutputToNull()
}
"""


def synth(items, workdir):
    """items: lista de (caminho_wav, texto). Cada frase vira um WAV (juntando os trechos de vozes diferentes)."""
    os.makedirs(workdir, exist_ok=True)
    jobs, plan = [], []
    for n, (path, text) in enumerate(items):
        ps_ = parts(text)
        files = []
        for j, (voice, t) in enumerate(ps_):
            fp = os.path.join(workdir, f'p_{n}_{j}.wav')
            jobs.append({'voice': voice, 'text': t, 'path': fp})
            files.append(fp)
        plan.append((path, files))
    jp, ps = os.path.join(workdir, 'tts.json'), os.path.join(workdir, 'tts.ps1')
    with open(jp, 'w', encoding='utf-8') as f:
        json.dump(jobs, f, ensure_ascii=False)
    with open(ps, 'w', encoding='utf-8-sig') as f:
        f.write(_PS)
    subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', ps, '-jsonPath', jp], check=True)
    for path, files in plan:  # junta os trechos de cada frase, com uma micropausa entre vozes
        with wave.open(files[0]) as w0:
            params = w0.getparams()
        gap = b'\x00' * (int(params.framerate * 0.04) * params.sampwidth * params.nchannels)
        with wave.open(path, 'wb') as out:
            out.setparams(params)
            for i, fp in enumerate(files):
                with wave.open(fp) as w:
                    out.writeframes(w.readframes(w.getnframes()))
                if i < len(files) - 1:
                    out.writeframes(gap)


def wav_len(path):
    with wave.open(path) as w:
        return w.getnframes() / w.getframerate()


# ---------- montagem ----------
def build(scenes, out_mp4, workdir, tag, lead=0.7, tail=1.8):
    """scenes: lista de (beats, draw). beats: lista de frases; draw(k) -> (img, d) sem legenda."""
    os.makedirs(workdir, exist_ok=True)
    flat = [(si, k, text) for si, (beats, _) in enumerate(scenes) for k, text in enumerate(beats, start=1)]
    wavs = [os.path.join(workdir, f'a_{si}_{k}.wav') for si, k, _ in flat]
    synth([(p, t) for p, (_, _, t) in zip(wavs, flat)], workdir)
    durs = [wav_len(p) + PAUSE for p in wavs]

    # áudio contínuo: silêncio inicial + cada frase + pausa + silêncio final
    with wave.open(wavs[0]) as w0:
        params = w0.getparams()
    audio_path = os.path.join(workdir, 'audio.wav')
    sil = lambda sec: b'\x00' * (int(params.framerate * sec) * params.sampwidth * params.nchannels)
    with wave.open(audio_path, 'wb') as out:
        out.setparams(params)
        out.writeframes(sil(lead))
        for p in wavs:
            with wave.open(p) as w:
                assert w.getparams()[:3] == params[:3], 'formatos de áudio diferentes'
                out.writeframes(w.readframes(w.getnframes()))
            out.writeframes(sil(PAUSE))
        out.writeframes(sil(tail))

    # imagens: uma por (cena, batida), com legenda; depois fades entre elas
    entries, prev, i = [], None, 0
    imgdir = os.path.join(workdir, 'img')
    os.makedirs(imgdir, exist_ok=True)

    def save(img, name):
        p = os.path.join(imgdir, name)
        img.save(p)
        return p

    first = scenes[0][1](0)[0]
    prev = first
    entries.append((save(first, 'lead.png'), lead))
    n_fade = max(1, round(FADE * FPS))
    for (si, k, text), dur in zip(flat, durs):
        img, _ = scenes[si][1](k)
        subtitle(img, text)
        for j in range(1, n_fade + 1):
            entries.append((save(Image.blend(prev, img, j / n_fade), f'f{i:04d}_{j}.png'), 1 / FPS))
        entries.append((save(img, f'h{i:04d}.png'), max(dur - n_fade / FPS, 0.05)))
        prev, i = img, i + 1
    entries.append((save(prev, 'tail.png'), tail))

    lst = os.path.join(workdir, 'list.txt')
    with open(lst, 'w', encoding='utf-8') as f:
        for p, dur in entries:
            f.write(f"file '{p.replace(chr(92), '/')}'\nduration {dur:.4f}\n")
        f.write(f"file '{entries[-1][0].replace(chr(92), '/')}'\n")
    os.makedirs(os.path.dirname(out_mp4), exist_ok=True)
    subprocess.run([
        imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst,
        '-i', audio_path, '-vf', f'fps={FPS},format=yuv420p', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20',
        '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11',  # a voz do Windows sai baixa; isto leva ao volume padrão de vídeo
        '-ar', '44100', '-c:a', 'aac', '-b:a', '128k', '-shortest', out_mp4,
    ], check=True)
    total = lead + sum(durs) + tail
    print(f'ok: {out_mp4}  ({total / 60:.1f} min, {len(flat)} frases, {len(entries)} imagens)')
    return total


def preview(scenes, outdir, tag=None):
    """Salva um PNG por (cena, batida) para você olhar o visual antes de gerar o vídeo."""
    os.makedirs(outdir, exist_ok=True)
    for si, (beats, draw) in enumerate(scenes):
        for k in range(len(beats) + 1):
            img, _ = draw(k)
            if k:
                subtitle(img, beats[k - 1])
            img.save(os.path.join(outdir, f's{si + 1}_k{k}.png'))
