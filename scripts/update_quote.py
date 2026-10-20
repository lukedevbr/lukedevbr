"""Gera assets/quote.svg com a frase do dia (ciclo determinístico, sem repetir)."""
import json
import textwrap
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
quotes = json.loads((ROOT / "quotes.json").read_text(encoding="utf-8"))

# Uma frase por dia; só repete depois de passar por toda a lista.
q = quotes[date.today().toordinal() % len(quotes)]

lines = textwrap.wrap(f"“{q['text']}”", width=36)
W, LH = 420, 22
H = 24 + len(lines) * LH + 16 + 20 + 18

body = "".join(
    f'<text x="22" y="{36 + i * LH}" fill="#C9D1D9" font-size="15" font-style="italic">{escape(l)}</text>'
    for i, l in enumerate(lines)
)
author_y = 36 + len(lines) * LH + 12

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Random Dev Quote">
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#141B45"/><stop offset="1" stop-color="#0A1128"/></linearGradient></defs>
<rect x="0.75" y="0.75" width="{W - 1.5}" height="{H - 1.5}" rx="10" fill="url(#bg)" stroke="#1B2A55" stroke-width="1.5"/>
<g font-family="'Segoe UI',Helvetica,Arial,sans-serif">{body}
<text x="{W - 22}" y="{author_y}" text-anchor="end" fill="#8B949E" font-size="13">— {escape(q['author'])}</text></g>
</svg>'''

out = ROOT / "assets" / "quote.svg"
out.parent.mkdir(exist_ok=True)
out.write_text(svg, encoding="utf-8")
print("Frase do dia:", q["text"], "-", q["author"])
