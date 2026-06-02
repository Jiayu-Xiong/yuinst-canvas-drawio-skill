from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "stage3-reorg.svg"


def arc_path(cx, cy, r, start, end):
    import math

    def pt(deg):
        t = math.radians(deg)
        return cx + r * math.cos(t), cy + r * math.sin(t)

    x1, y1 = pt(start)
    x2, y2 = pt(end)
    large = 1 if abs(end - start) > 180 else 0
    sweep = 1 if end > start else 0
    return f"M {x1:.1f} {y1:.1f} A {r} {r} 0 {large} {sweep} {x2:.1f} {y2:.1f}"


svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="230" height="230" viewBox="0 0 230 230">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#202020"/>
    </marker>
    <linearGradient id="blue_box" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#f7fbff"/>
      <stop offset="1" stop-color="#e8f1ff"/>
    </linearGradient>
    <linearGradient id="teal_box" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#f8ffff"/>
      <stop offset="1" stop-color="#e4f7f5"/>
    </linearGradient>
    <linearGradient id="coral_box" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#fffafa"/>
      <stop offset="1" stop-color="#fff0ea"/>
    </linearGradient>
  </defs>

  <circle cx="115" cy="115" r="87" fill="none" stroke="#8fb3e8" stroke-width="1.4"/>
  <circle cx="115" cy="115" r="58" fill="none" stroke="#a9c4ee" stroke-width="1.1"/>

  <path d="{arc_path(115, 115, 76, 196, 238)}" fill="none" stroke="#202020" stroke-width="2.7" stroke-linecap="round" marker-end="url(#arrow)"/>
  <path d="{arc_path(115, 115, 76, 316, 358)}" fill="none" stroke="#202020" stroke-width="2.7" stroke-linecap="round" marker-end="url(#arrow)"/>
  <path d="{arc_path(115, 115, 76, 76, 118)}" fill="none" stroke="#202020" stroke-width="2.7" stroke-linecap="round" marker-end="url(#arrow)"/>

  <rect x="80" y="28" width="70" height="40" rx="8" fill="url(#blue_box)" stroke="#5f8ed8" stroke-width="1.5"/>
  <text x="115" y="45" text-anchor="middle" font-family="Bahnschrift, Arial, sans-serif" font-size="12" font-weight="700" fill="#123a63">Shared from</text>
  <text x="115" y="60" text-anchor="middle" font-family="Bahnschrift, Arial, sans-serif" font-size="15" font-weight="700" fill="#123a63">A</text>

  <rect x="145" y="140.5" width="70" height="40" rx="8" fill="url(#teal_box)" stroke="#45a9a6" stroke-width="1.5"/>
  <text x="180" y="155" text-anchor="middle" font-family="Bahnschrift, Arial, sans-serif" font-size="12" font-weight="700" fill="#11615e">Shared from</text>
  <text x="180" y="170" text-anchor="middle" font-family="Bahnschrift, Arial, sans-serif" font-size="15" font-weight="700" fill="#11615e">B</text>

  <rect x="15" y="140.5" width="70" height="40" rx="8" fill="url(#coral_box)" stroke="#f2765b" stroke-width="1.5"/>
  <text x="50" y="155" text-anchor="middle" font-family="Bahnschrift, Arial, sans-serif" font-size="12" font-weight="700" fill="#9b321f">Shared from</text>
  <text x="50" y="170" text-anchor="middle" font-family="Bahnschrift, Arial, sans-serif" font-size="15" font-weight="700" fill="#9b321f">C</text>

  <text x="115" y="103" text-anchor="middle" font-family="Bahnschrift, Arial, sans-serif" font-size="14" font-weight="700" fill="#111111">Dissociation /</text>
  <text x="115" y="122" text-anchor="middle" font-family="Bahnschrift, Arial, sans-serif" font-size="14" font-weight="700" fill="#111111">Self-consistent</text>
  <text x="115" y="141" text-anchor="middle" font-family="Bahnschrift, Arial, sans-serif" font-size="14" font-weight="700" fill="#111111">Reorganization</text>
</svg>
"""

OUT.write_text(svg, encoding="utf-8")
print(f"wrote {OUT}")
