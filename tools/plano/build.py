"""Genera el README «plano técnico» como una sola hoja SVG.

Uso:
    python tools/plano/build.py --out dist/plano.svg [--snake dist/registro-de-obra.svg]

Sin --snake, la sección de contribuciones queda con un recuadro vacío.
Solo usa la biblioteca estándar: corre tal cual en GitHub Actions.
"""
import argparse
import base64
import re
from pathlib import Path
from xml.sax.saxutils import escape

FONTS_DIR = Path(__file__).parent / "fonts"

BLUE = "#0b3a6e"
INK = "#eaf4ff"
SOFT = "#bfe3ff"
MUTED = "#9cc8f0"
YELLOW = "#ffd166"
WHITE = "#ffffff"
W = 880

FONTS = {
    "BCB": "BarlowCondensed-Bold.woff",
    "BCS": "BarlowCondensed-SemiBold.woff",
    "SM": "SpaceMono-Regular.woff",
    "SMB": "SpaceMono-Bold.woff",
    "SG4": "SpaceGrotesk-400.woff",
    "SG7": "SpaceGrotesk-700.woff",
}

# Símbolo de puzzlecore en una grilla de 48 unidades.
MARK = "M12 6H30A9 9 0 0 1 39 15A9 9 0 0 0 39 33A9 9 0 0 1 30 42H12A9 9 0 0 1 3 33V15A9 9 0 0 1 12 6Z"

PIEZAS = [
    ("fleet-monitor", ["Lab de despliegue para flotas de nodos", "remotos con conectividad intermitente"], "Python · Docker · CI", False),
    ("purple-team-lab", ["Lab de ciberseguridad: atacar, detectar,", "ajustar reglas y volver a atacar"], "Suricata · Wazuh", False),
    ("personaltrainer-app", ["Rutinas, alumnos y progreso", "para entrenadores personales"], "React · Node · Prisma", True),
    ("gestionEducativa", ["Gestión de instituciones educativas", "con usuarios, roles y permisos"], "Django · Bootstrap", False),
]


def t(x, y, s, cls="sm", size=13, fill=INK, anchor="start", extra=""):
    return f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" {extra}>{escape(s)}</text>'


def logo(x, y, mark_px, font_px, gap):
    k = mark_px / 48
    base = y + mark_px / 2 + font_px * 0.36
    return (
        f'<g transform="translate({x} {y}) scale({k:.4f})"><path d="{MARK}" fill="#f3f5f8"/>'
        f'<circle cx="39" cy="24" r="5.5" fill="{YELLOW}"/></g>\n'
        f'<text x="{x + mark_px + gap}" y="{base:.1f}" class="sg4" font-size="{font_px}" fill="#f3f5f8" '
        f'letter-spacing="{-font_px * 0.04:.2f}">puzzle<tspan class="sg7" fill="{YELLOW}">core</tspan></text>'
    )


def section_title(letter, title, y):
    return (
        f'<circle cx="62" cy="{y - 8}" r="14" fill="none" stroke="{YELLOW}" stroke-width="2"/>\n'
        + t(62, y - 3, letter, cls="smb", size=12, fill=YELLOW, anchor="middle") + "\n"
        + t(88, y, title, cls="bcs", size=26, fill=WHITE, extra='letter-spacing="2"')
    )


# ---------- secciones: cada una devuelve (alto, cuerpo) ----------

def header():
    body = f"""
{logo(46, 30, 30, 22, 10)}
{t(832, 52, "HOJA 1/1", size=11, fill=MUTED, anchor="end")}
<g stroke="{MUTED}" stroke-width="1">
  <line x1="48" y1="80" x2="48" y2="96"/><line x1="832" y1="80" x2="832" y2="96"/>
  <line x1="48" y1="88" x2="360" y2="88"/><line x1="520" y1="88" x2="832" y2="88"/>
</g>
<path d="M48 88l8-4v8zM832 88l-8-4v8z" fill="{MUTED}"/>
{t(440, 92, "≈ 784 px · ESC 1:1", size=11, fill=MUTED, anchor="middle")}
{t(48, 200, "JULIÁN OLIVERA", cls="bcb", size=108, fill=WHITE, extra='letter-spacing="4"')}
<rect class="draw" x="48" y="214" width="784" height="3" fill="{YELLOW}"/>
{t(48, 244, "ESPEC.: SISTEMAS DE INFORMACIÓN · UADER", size=13, fill=SOFT, extra='letter-spacing="1"')}
{t(832, 244, "TIPO: FULLSTACK + SEGURIDAD", size=13, fill=SOFT, anchor="end", extra='letter-spacing="1"')}
{t(48, 276, "Me gusta entender cómo y por qué funcionan las cosas.", size=12, fill=MUTED)}
"""
    return 306, body


def box(x, y, w, h, tag, title, sub, dashed=False, tag_color=MUTED):
    dash = ' stroke-dasharray="6 5"' if dashed else ""
    stroke = MUTED if dashed else INK
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{BLUE}" fill-opacity=".9" stroke="{stroke}" stroke-width="2"{dash}/>\n'
        + t(x + 16, y + 24, tag, size=11, fill=tag_color) + "\n"
        + t(x + 16, y + 52, title, cls="bcs", size=24, fill=WHITE) + "\n"
        + t(x + 16, y + 74, sub, size=12, fill=SOFT)
    )


def moving_dot(x1, y1, x2, y2, dur, begin="0s"):
    attr, a, b = ("cx", x1, x2) if y1 == y2 else ("cy", y1, y2)
    return (
        f'<circle cx="{x1}" cy="{y1}" r="4" fill="{YELLOW}" filter="url(#glow)">'
        f'<animate attributeName="{attr}" from="{a}" to="{b}" dur="{dur}" begin="{begin}" repeatCount="indefinite"/></circle>'
    )


def arquitectura():
    y = 96
    body = f"""
{section_title("A", "VISTA DE ARQUITECTURA", 52)}
{box(48, y, 220, 92, "01 · CLIENTE", "React · TypeScript", "Tailwind · Vite")}
<line x1="268" y1="{y + 46}" x2="330" y2="{y + 46}" stroke="{INK}" stroke-width="2"/>
<path d="M330 {y + 46}l-8-4v8z" fill="{INK}"/>
{moving_dot(268, y + 46, 322, y + 46, "2.4s")}
{box(330, y, 220, 92, "02 · API", "Node · FastAPI", "Django · REST · Jest")}
<line x1="550" y1="{y + 46}" x2="612" y2="{y + 46}" stroke="{INK}" stroke-width="2"/>
<path d="M612 {y + 46}l-8-4v8z" fill="{INK}"/>
{moving_dot(550, y + 46, 604, y + 46, "2.4s", "1.2s")}
{box(612, y, 220, 92, "03 · DATOS", "Prisma · SQL", "PostgreSQL · SQLite")}
<line x1="440" y1="{y + 92}" x2="440" y2="{y + 150}" stroke="{INK}" stroke-opacity=".7" stroke-width="2"/>
{moving_dot(440, y + 92, 440, y + 150, "2s")}
{box(160, y + 150, 280, 92, "04 · AUTOMATIZACIÓN", "Python · Selenium", "PowerShell · Java · Qt", dashed=True)}
{box(440, y + 150, 280, 92, "05 · SEGURIDAD", "Suricata · Wazuh", "pfSense · OSINT · forense", dashed=True, tag_color=YELLOW)}
{t(48, 380, "NOTA: los módulos punteados se integran según el proyecto. Infra: Docker · GitHub Actions.", size=11, fill=MUTED)}
"""
    return 410, body


COLS = [(0, 70), (70, 230), (300, 380), (680, 200)]  # (x, ancho)


def piezas():
    head_h, row_h = 128, 76
    h = head_h + row_h * len(PIEZAS)
    body = section_title("B", "LISTA DE PIEZAS · PROYECTOS", 52) + "\n"
    body += f'<line x1="1" y1="88" x2="879" y2="88" stroke="{INK}" stroke-width="2"/>\n'
    body += f'<line x1="1" y1="{head_h}" x2="879" y2="{head_h}" stroke="{INK}" stroke-width="1.5"/>\n'
    for (x, _), label in zip(COLS, ["ÍTEM", "PIEZA", "DESCRIPCIÓN", "MATERIAL"]):
        body += t(x + 20, 113, label, size=11, fill=MUTED) + "\n"
        if x:
            body += f'<line x1="{x}" y1="88" x2="{x}" y2="{h}" stroke="{MUTED}"/>\n'
    for i, (name, desc, material, privado) in enumerate(PIEZAS):
        y = head_h + i * row_h
        if i:
            body += f'<line x1="1" y1="{y}" x2="879" y2="{y}" stroke="{MUTED}" stroke-opacity=".7"/>\n'
        body += t(COLS[0][0] + 20, y + 44, f"{i + 1:02d}", cls="smb", size=14, fill=YELLOW)
        body += t(COLS[1][0] + 18, y + (38 if privado else 44), name, cls="smb", size=14, fill=WHITE)
        if privado:
            body += t(COLS[1][0] + 18, y + 58, "REPO PRIVADO", size=10, fill=YELLOW)
        y0 = y + (44 if len(desc) == 1 else 36)
        for j, line in enumerate(desc):
            body += t(COLS[2][0] + 18, y0 + j * 18, line, size=12, fill=SOFT)
        body += t(COLS[3][0] + 18, y + 44, material, size=12, fill=INK) + "\n"
    return h, body


def registro(snake_svg):
    title_h, snake_h = 84, 180
    body = section_title("C", "REGISTRO DE OBRA · CONTRIBUCIONES", 52) + "\n"
    body += t(832, 52, "actualizado cada 12 h", size=11, fill=MUTED, anchor="end") + "\n"
    if snake_svg:
        inner = re.sub(r"^.*?<svg[^>]*>", "", snake_svg, count=1, flags=re.S)
        inner = re.sub(r"</svg>\s*$", "", inner.strip())
        vb = re.search(r'viewBox="([^"]+)"', snake_svg).group(1)
        body += f'<svg x="28" y="{title_h - 20}" width="{W - 56}" height="{snake_h + 8}" viewBox="{vb}" preserveAspectRatio="xMidYMid meet">{inner}</svg>\n'
    else:
        body += f'<rect x="48" y="{title_h}" width="784" height="{snake_h - 40}" fill="none" stroke="{MUTED}" stroke-dasharray="4 4"/>\n'
        body += t(440, title_h + (snake_h - 40) / 2 + 4, "[el workflow inserta aquí el gráfico de contribuciones]", size=11, fill=MUTED, anchor="middle")
    return title_h + snake_h, body


def rotulo():
    h, x0 = 150, 500
    body = f"""
<line x1="{x0}" y1="0" x2="{x0}" y2="{h}" stroke="{INK}" stroke-width="2"/>
<line x1="{x0 + 190}" y1="0" x2="{x0 + 190}" y2="{h}" stroke="{MUTED}"/>
<line x1="{x0}" y1="75" x2="879" y2="75" stroke="{MUTED}"/>
{logo(44, 26, 48, 36, 14)}
{t(48, 106, "Siempre buscando la estructura detrás del caos.", cls="bcs", size=19, fill=WHITE)}
{t(48, 130, "PROYECTOS Y CONTACTO ↓", size=11, fill=MUTED)}
"""
    cells = [
        (x0, 0, "PLANO Nº", "JO-001", WHITE, ""),
        (x0 + 190, 0, "DIBUJÓ", "J. OLIVERA", WHITE, ""),
        (x0, 75, "ESTADO", "EN CONSTRUCCIÓN", YELLOW, 'class="blink"'),
        (x0 + 190, 75, "REVISIÓN", "2026", WHITE, ""),
    ]
    for x, y, label, value, color, extra in cells:
        body += t(x + 16, y + 25, label, size=10, fill=MUTED)
        body += f'<g {extra}>{t(x + 16, y + 50, value, cls="smb", size=14, fill=color)}</g>\n'
    return h, body


# ---------- hoja ----------

def font_face(key):
    data = base64.b64encode((FONTS_DIR / FONTS[key]).read_bytes()).decode()
    return f"@font-face{{font-family:'{key}';src:url(data:font/woff;base64,{data}) format('woff');}}"


def build(snake_svg=None):
    sections = [header(), arquitectura(), piezas(), registro(snake_svg), rotulo()]
    total = sum(h for h, _ in sections)
    parts, y = [], 0
    for i, (h, body) in enumerate(sections):
        if i:
            parts.append(f'<line x1="1" y1="{y}" x2="{W - 1}" y2="{y}" stroke="{INK}" stroke-width="2"/>')
        parts.append(f'<g transform="translate(0 {y})">{body}</g>')
        y += h
    faces = "".join(font_face(k) for k in FONTS)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{total}" viewBox="0 0 {W} {total}">
<title>Julián Olivera · puzzlecore</title>
<style>{faces}
.bcb{{font-family:'BCB','Arial Narrow',sans-serif;font-weight:700}}
.bcs{{font-family:'BCS','Arial Narrow',sans-serif;font-weight:600}}
.sm{{font-family:'SM',ui-monospace,monospace}}
.smb{{font-family:'SMB',ui-monospace,monospace;font-weight:700}}
.sg4{{font-family:'SG4',sans-serif;font-weight:400}}
.sg7{{font-family:'SG7',sans-serif;font-weight:700}}
.draw{{transform-box:fill-box;transform-origin:left center;animation:draw 1.6s ease-out .2s both}}
@keyframes draw{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
.blink{{animation:blink 1.6s steps(1) infinite}}
@keyframes blink{{0%,60%{{opacity:1}}61%,100%{{opacity:.3}}}}
@media (prefers-reduced-motion: reduce){{.draw,.blink{{animation:none}}}}
</style>
<defs>
<pattern id="g" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="#ffffff" stroke-opacity=".07"/></pattern>
<pattern id="G" width="100" height="100" patternUnits="userSpaceOnUse"><path d="M100 0H0V100" fill="none" stroke="#ffffff" stroke-opacity=".14"/></pattern>
<filter id="glow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<rect width="{W}" height="{total}" fill="{BLUE}"/>
<rect width="{W}" height="{total}" fill="url(#g)"/>
<rect width="{W}" height="{total}" fill="url(#G)"/>
{chr(10).join(parts)}
<rect x="1" y="1" width="{W - 2}" height="{total - 2}" fill="none" stroke="{INK}" stroke-width="2"/>
<rect x="7" y="7" width="{W - 14}" height="{total - 14}" fill="none" stroke="{INK}" stroke-opacity=".45"/>
</svg>
"""


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--snake")
    a = ap.parse_args()
    snake = Path(a.snake).read_text(encoding="utf-8") if a.snake else None
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build(snake), encoding="utf-8")
    print(f"{out}: {out.stat().st_size // 1024} KB")
