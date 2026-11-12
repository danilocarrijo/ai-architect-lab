"""Shared pieces for chapter 18 (build the app from zero): one slide template per step, driven by data."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine  # noqa: E402
from engine import C, box, canvas, font, rbox, text_c, text_l  # noqa: E402

VOICES = {'zira': 'Microsoft Zira Desktop', 'david': 'Microsoft David Desktop'}
VOICE = os.environ.get('VOICE', 'zira').lower()
engine.SINGLE_VOICE = VOICES[VOICE]
engine.SPEECH = [
    (r'package\.json', 'package dot json'), (r'config\.js', 'config dot J S'), (r'text\.js', 'text dot J S'), (r'loader\.js', 'loader dot J S'),
    (r'chunker\.js', 'chunker dot J S'), (r'embeddings\.js', 'embeddings dot J S'), (r'vectorstore\.js', 'vector store dot J S'),
    (r'bm25\.js', 'B M twenty five dot J S'), (r'retriever\.js', 'retriever dot J S'), (r'index\.js', 'index dot J S'),
    (r'guardrails/index\.js', 'guardrails index dot J S'), (r'trace\.js', 'trace dot J S'), (r'cache\.js', 'cache dot J S'),
    (r'client\.js', 'client dot J S'), (r'gemini\.js', 'gemini dot J S'), (r'ask\.js', 'ask dot J S'), (r'golden\.js', 'golden dot J S'),
    (r'run\.js', 'run dot J S'), (r'runner\.js', 'runner dot J S'), (r'server\.js', 'server dot J S'), (r'cli\.js', 'C L I dot J S'),
    (r'hooks\.js', 'hooks dot J S'), (r'model\.js', 'model dot J S'), (r'tools\.js', 'tools dot J S'),
    (r'\bBM25\b', 'B M twenty five'), (r'\bRRF\b', 'R R F'), (r'\bMCP\b', 'M C P'), (r'\bAPI\b', 'A P I'), (r'\bLLM\b', 'L L M'),
    (r'\bnpm\b', 'N P M'), (r'LangGraph', 'Lang Graph'), (r'LangChain', 'Lang Chain'), (r'\bCEP\b', 'C E P'), (r'\bPII\b', 'P I I'),
    (r'Tracer', 'Tracer'), (r'\bTTL\b', 'T T L'), (r'\bCLI\b', 'C L I'), (r'\bPDF\b', 'P D F'),
]
NOTE = (130, 225, 215)
WARN_L = (255, 200, 120)


def step_scene(n, total, title, files, purpose, uses, verify, tag):
    """Return a draw(k) for one step. `files` = [(path, lines)], `purpose`/`verify` = [short lines]."""
    nf, npu, nv = len(files), len(purpose), len(verify)
    # pick the roomiest layout that still fits above the subtitle bar
    for pitch, hdr, lh, fs in [(52, 52, 30, 22), (44, 48, 28, 20), (36, 44, 26, 18), (30, 42, 25, 17)]:
        need = 170 + nf * pitch + 12 + hdr + lh * npu + 12 + (hdr + lh * nv if nv else 0)
        if need <= 612:
            break

    def draw(k):
        img, d = canvas(tag)
        for i in range(total):
            x = 60 + i * (1160 // (total - 1))
            d.ellipse((x - 9, 49, x + 9, 67), fill=C['acc'] if i + 1 == n else (C['line'] if i + 1 > n else C['blue']))
        text_c(d, (640, 118), f'Step {n} · {title}', font(40, True))
        if k >= 2:
            for i, (p, l) in enumerate(files):
                y = 170 + i * pitch
                rbox(d, (60, y, 1220, y + pitch - 8), 'acc' if k == 2 else 'box', r=8)
                text_l(d, (85, y + (pitch - 8) // 2 + 2), p, font(fs, False, True))
                w = max(10, int(l * 2.4))
                d.rounded_rectangle((920, y + (pitch - 8) // 2 - 9, 920 + w, y + (pitch - 8) // 2 + 9), 6, fill=C['blue'])
                text_l(d, (920 + w + 10, y + (pitch - 8) // 2), f'{l} lines', font(fs - 3, True), C['muted'])
        y0 = 170 + nf * pitch + 12
        if k >= 3:
            h = hdr + lh * npu
            rbox(d, (60, y0, 1220, y0 + h), 'blue', hi=(k == 3), r=10)
            text_l(d, (85, y0 + hdr // 2), 'What it does', font(fs - 2, True), C['blue'])
            if uses:
                text_l(d, (800, y0 + hdr // 2), 'uses: ' + uses, font(fs - 4, True), C['muted'])
            for i, ln in enumerate(purpose):
                text_l(d, (85, y0 + hdr + lh * i + lh // 2 - 4), ln, font(fs))
        if k >= 4 and verify:
            y1 = y0 + hdr + lh * npu + 12
            h = hdr + lh * nv
            rbox(d, (60, y1, 1220, y1 + h), 'warn', hi=(k == 4), r=10)
            text_l(d, (85, y1 + hdr // 2), 'Verify', font(fs - 2, True), C['warn'])
            for i, ln in enumerate(verify):
                text_l(d, (85, y1 + hdr + lh * i + lh // 2 - 4), ln, font(fs - 1, False, True))
        return img, d
    return draw


def make_scene(step, tag, total=20):
    n, title, files, purpose, uses, verify, beats = step
    return beats, step_scene(n, total, title, files, purpose, uses, verify, tag)
