"""Build profile-dark.svg / profile-light.svg for Elijah's GitHub profile README.

Run from anywhere: python3 generator/build_profile.py
Writes the SVGs to the repo root.
"""
import html
import os
import render_ascii

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

ART_WIDTH = 46
PANEL_WIDTH = 62
CHAR_W = 7.85       # ~0.6em advance at 13px (Menlo / DejaVu / Courier New)
LINE_H = 17.5
PAD_X, PAD_Y = 24, 26
FONT = "Menlo, 'DejaVu Sans Mono', 'Liberation Mono', 'Courier New', monospace"

DARK = dict(bg="#0d1117", border="#30363d", art="#8b949e",
            key="#ff7b72", dots="#484f58", val="#79c0ff",
            header="#ffa657", rule="#3d444d", section="#7ee787", plain="#c9d1d9")
LIGHT = dict(bg="#ffffff", border="#d0d7de", art="#57606a",
             key="#cf222e", dots="#d0d7de", val="#0969da",
             header="#bc4c00", rule="#d0d7de", section="#1a7f37", plain="#1f2328")

# (label, value) -> ". label: ..dots.. value"
def kv(label, value):
    lead = f". {label}: "
    dots = PANEL_WIDTH - len(lead) - len(value) - 1
    if dots < 2:
        raise ValueError(f"line too long: {label}: {value} ({-dots + 2} over)")
    return [("key", lead), ("dots", "." * dots + " "), ("val", value)]

def section(title):
    bar = PANEL_WIDTH - len(title) - 3
    return [("section", f"─ {title} "), ("rule", "─" * bar)]

def blank():
    return []

PANEL = [
    [("header", "elijah@walker "), ("rule", "─" * (PANEL_WIDTH - 14))],
    kv("OS", "macOS, Windows, Linux"),
    kv("Host", "The University of Texas at Dallas"),
    kv("Kernel", "B.S. Computer Science, Dec 2026"),
    kv("Shell", "SWE Intern @ Microsoft (Excel, Power BI)"),
    kv("Shell.History", "Goldman Sachs, Bell Textron"),
    kv("IDE", "VS Code, Visual Studio, Xcode"),
    blank(),
    section("Skills"),
    kv("Languages", "Java, C++, Python, C#, TypeScript"),
    kv("Languages.Also", "JavaScript, C, SQL, Swift, Bash, PHP"),
    kv("Frameworks", "React, Next.js, Node.js, Flask, PyTorch"),
    kv("Cloud.Data", "Azure, PostgreSQL, Elasticsearch, Supabase"),
    kv("Tools", "Git, Docker, Kubernetes, Figma"),
    blank(),
    section("Leadership"),
    kv("President", "ACM @ UT Dallas — 800+ members"),
    kv("Events", "HackUTD, 50+ campus events / year"),
    blank(),
    section("Contact"),
    kv("Email", "hello@elijahwalker.me"),
    kv("Web", "elijahwalker.me"),
    kv("LinkedIn", "in/elijahtruthwalker"),
    kv("GitHub", "elijahtwalker"),
]

def build(theme, colors, invert):
    if invert:
        render_ascii.RAMP = render_ascii.BASE_RAMP[::-1]
    else:
        render_ascii.RAMP = render_ascii.BASE_RAMP
    art = render_ascii.render(ART_WIDTH, gamma=1.6)

    rows = max(len(art), len(PANEL))
    width = PAD_X * 2 + (ART_WIDTH + 2 + PANEL_WIDTH) * CHAR_W
    height = PAD_Y * 2 + rows * LINE_H
    panel_x = PAD_X + (ART_WIDTH + 2) * CHAR_W
    # vertically center the shorter column
    art_y0 = PAD_Y + (rows - len(art)) / 2 * LINE_H + 12
    panel_y0 = PAD_Y + (rows - len(PANEL)) / 2 * LINE_H + 12

    out = []
    out.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" '
        f'viewBox="0 0 {width:.0f} {height:.0f}" font-family="{FONT}" font-size="13">')
    out.append(f'<rect width="100%" height="100%" rx="10" fill="{colors["bg"]}" '
               f'stroke="{colors["border"]}"/>')
    out.append('<style>text{white-space:pre}</style>')

    for i, line in enumerate(art):
        if not line.strip():
            continue
        y = art_y0 + i * LINE_H
        out.append(f'<text x="{PAD_X}" y="{y:.1f}" xml:space="preserve" '
                   f'fill="{colors["art"]}">{html.escape(line)}</text>')

    for i, parts in enumerate(PANEL):
        if not parts:
            continue
        y = panel_y0 + i * LINE_H
        spans = "".join(
            f'<tspan fill="{colors[cls]}"'
            + (' font-weight="bold"' if cls in ("header", "section") else "")
            + f'>{html.escape(txt)}</tspan>'
            for cls, txt in parts)
        out.append(f'<text x="{panel_x:.1f}" y="{y:.1f}" xml:space="preserve">{spans}</text>')

    out.append("</svg>")
    with open(os.path.join(ROOT, f"profile-{theme}.svg"), "w") as f:
        f.write("\n".join(out))
    print(f"profile-{theme}.svg: {width:.0f}x{height:.0f}, art {len(art)} rows, panel {len(PANEL)} rows")

render_ascii.BASE_RAMP = render_ascii.RAMP
build("dark", DARK, invert=True)
build("light", LIGHT, invert=False)
