#!/usr/bin/env python3
"""生成 GitHub Profile 像素动画横幅 banner.svg（纯 SMIL 动画，无外部依赖，GitHub camo 可渲染）
输出: ../assets/banner.svg
"""
import random, os
random.seed(2026)

W, H = 1200, 340
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "banner.svg")

# ---------- 5x7 点阵字体 ----------
FONT = {
    'H': ["10001","10001","10001","11111","10001","10001","10001"],
    'M': ["10001","11011","10101","10101","10001","10001","10001"],
    'I': ["11111","00100","00100","00100","00100","00100","11111"],
    'N': ["10001","11001","11001","10101","10011","10011","10001"],
    'D': ["11110","10001","10001","10001","10001","10001","11110"],
    'E': ["11111","10000","10000","11110","10000","10000","11111"],
    'G': ["01110","10001","10000","10111","10001","10001","01110"],
    'A': ["01110","10001","10001","11111","10001","10001","10001"],
    'V': ["10001","10001","10001","10001","10001","01010","00100"],
    'L': ["10000","10000","10000","10000","10000","10000","11111"],
    'O': ["01110","10001","10001","10001","10001","10001","01110"],
    'P': ["10001","10001","10001","11111","10001","10000","10000"],
    'R': ["11110","10001","10001","11110","10100","10010","10001"],
    'S': ["01111","10000","10000","01110","00001","00001","11110"],
    'T': ["11111","00100","00100","00100","00100","00100","00100"],
    'u': ["00000","00000","10001","10001","10001","10011","01101"],
    'a': ["00000","00000","01110","00001","01111","10001","01111"],
    'n': ["00000","00000","10110","11001","10001","10001","10001"],
    'o': ["00000","00000","01110","10001","10001","10001","01110"],
    'v': ["00000","00000","10001","10001","10001","01010","00100"],
    ' ': ["00000","00000","00000","00000","00000","00000","00000"],
}

def text_blocks(text, justify="left"):
    """把字符串转为块坐标系列表 [(col,row)]"""
    blocks = []
    col = 0
    for ch in text:
        for r, row in enumerate(FONT[ch]):
            for c, v in enumerate(row):
                if v == '1':
                    blocks.append((col + c, r))
        col += 6  # 字宽 5 + 间隔 1
    return blocks, col - 1  # 总列数（-1 去掉最后间隔）

def render_text(svg, text, x0, y0, px, colors, shadow=None, glow=None, glow_filt=""):
    """渲染文字为像素块。colors: 单色 str 或按行的列表"""
    blocks, _ = text_blocks(text)
    out = []
    if glow:
        out.append(f'<g filter="url(#{glow_filt})" opacity="0.55">')
        for (c, r) in blocks:
            out.append(f'<rect x="{x0+c*px}" y="{y0+r*px}" width="{px}" height="{px}" fill="{glow}"/>')
        out.append('</g>')
    if shadow:
        dx, dy = shadow[0], shadow[1]
        sc = shadow[2]
        out.append(f'<g transform="translate({dx},{dy})">')
        for (c, r) in blocks:
            out.append(f'<rect x="{x0+c*px}" y="{y0+r*px}" width="{px}" height="{px}" fill="{sc}"/>')
        out.append('</g>')
    for (c, r) in blocks:
        col = colors[r] if isinstance(colors, list) else colors
        out.append(f'<rect x="{x0+c*px}" y="{y0+r*px}" width="{px}" height="{px}" fill="{col}"/>')
    return "\n".join(out)

def text_width(text, px):
    _, cols = text_blocks(text)
    return cols * px + px

# ---------- 构建 SVG ----------
s = []
s.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="monospace">')
s.append(f'''<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#0a0e14"/><stop offset="0.75" stop-color="#0c1219"/><stop offset="1" stop-color="#101a26"/>
  </linearGradient>
  <filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
    <feGaussianBlur stdDeviation="7" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="b"/></feMerge>
  </filter>
  <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">
    <rect width="4" height="4" fill="none"/>
    <rect width="4" height="1.2" y="0" fill="#000000" opacity="0.16"/>
  </pattern>
  <clipPath id="typeclip"><rect x="0" y="0" width="0" height="{H}">
    <animate attributeName="width" to="640" dur="2.6s" begin="1.2s" fill="freeze"
      calcMode="discrete" values="0;20;40;60;80;100;120;140;160;180;200;220;240;260;280;300;320;340;360;380;400;420;440;460;480;500;520;540;560;580;600;620;640"/>
  </rect></clipPath>
</defs>''')

# 背景
s.append(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')

# ---- 星星（静态 + 闪烁）----
star_colors = ["#3ddc97", "#c9a04b", "#a78bfa", "#89f0c0", "#5b6b7c"]
for i in range(48):
    x = random.randint(10, W - 14)
    y = random.randint(14, 250)
    sz = random.choice([2, 2, 3, 3, 4])
    c = star_colors[random.randrange(len(star_colors))]
    if i < 16:  # 闪烁星
        dur = round(random.uniform(1.6, 3.4), 1)
        begin = round(random.uniform(0, 3), 1)
        s.append(f'<rect x="{x}" y="{y}" width="{sz}" height="{sz}" fill="{c}" opacity="0.3">'
                 f'<animate attributeName="opacity" values="0.06;1;0.06" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/></rect>')
    else:
        s.append(f'<rect x="{x}" y="{y}" width="{sz}" height="{sz}" fill="{c}" opacity="{round(random.uniform(0.18, 0.65), 2)}"/>')

# ---- 漂浮粒子（绿光点，升空循环）----
for i in range(14):
    x = random.randint(40, W - 40)
    y0 = random.randint(240, 310)
    dur = round(random.uniform(4.5, 8.0), 1)
    begin = round(random.uniform(0, 6), 1)
    rise = random.randint(60, 130)
    sz = random.choice([3, 3, 4])
    s.append(f'<rect x="{x}" y="{y0}" width="{sz}" height="{sz}" fill="#3ddc97" opacity="0">'
             f'<animate attributeName="opacity" values="0;0.85;0" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'
             f'<animateTransform attributeName="transform" type="translate" values="0,0;{random.randint(-14,14)},{rise}" '
             f'dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/></rect>')

# ---- 远层城市剪影 ----
s.append('<g fill="#0e1620">')
x = -20
while x < W:
    bw = random.randint(36, 84)
    bh = random.randint(28, 62)
    s.append(f'<rect x="{x}" y="{280 - bh}" width="{bw}" height="{bh + 60}"/>')
    x += bw + random.randint(2, 10)
s.append('</g>')

# ---- 近层城市剪影 + 窗户 ----
s.append('<g fill="#151f2c">')
x = -30
while x < W:
    bw = random.randint(44, 96)
    bh = random.randint(36, 74)
    top = 300 - bh
    s.append(f'<rect x="{x}" y="{top}" width="{bw}" height="{bh + 40}"/>')
    # 窗户
    for wy in range(top + 8, 300, 12):
        for wx in range(x + 6, x + bw - 8, 12):
            if random.random() < 0.30:
                wc = "#3ddc97" if random.random() < 0.6 else "#c9a04b"
                op = round(random.uniform(0.35, 0.9), 2)
                if random.random() < 0.2:  # 闪烁窗
                    d = round(random.uniform(1.4, 3.2), 1)
                    s.append(f'<rect x="{wx}" y="{wy}" width="4" height="4" fill="{wc}" opacity="{op}">'
                             f'<animate attributeName="opacity" values="{op};0.08;{op}" dur="{d}s" repeatCount="indefinite"/></rect>')
                else:
                    s.append(f'<rect x="{wx}" y="{wy}" width="4" height="4" fill="{wc}" opacity="{op}"/>')
    x += bw + random.randint(3, 12)
s.append('</g>')

# ---- 大字 HuanMoovo ----
NAME = "HuanMoovo"
PX = 20
name_w = text_width(NAME, PX)
nx = (W - name_w) // 2
ny = 54
row_colors = ["#8ff7c9", "#6aeba8", "#4de29a", "#3ddc97", "#33c489", "#2ba873", "#248f61"]
s.append(render_text(s, NAME, nx, ny, PX, row_colors, shadow=(4, 4, "#0d2b1f"), glow="#2ba873", glow_filt="glow"))
name_bottom = ny + 7 * PX

# ---- 打字机标语 ----
TAG = "INDIE GAME DEVELOPER"
TPX = 5
tag_w = text_width(TAG, TPX)
tx = (W - tag_w) // 2
ty = 218
s.append(f'<g clip-path="url(#typeclip)">')
s.append(render_text(s, TAG, tx, ty, TPX, "#c9a04b", shadow=(2, 2, "#3d2e10")))
s.append('</g>')
# 打字光标（随打字移动，完成后闪烁）
cx_end = tx + tag_w + 8
s.append(f'<rect x="{tx}" y="{ty - 2}" width="7" height="{7*TPX + 6}" fill="#3ddc97" opacity="0">'
         f'<animate attributeName="opacity" values="0;1" dur="0.01s" begin="1.2s" fill="freeze"/>'
         f'<animateTransform attributeName="transform" type="translate" to="{tag_w + 4},0" dur="2.6s" begin="1.2s" fill="freeze" calcMode="discrete" '
         f'values="0,0;30,0;60,0;90,0;120,0;150,0;180,0;210,0;240,0;270,0;300,0;330,0;360,0;390,0;420,0;450,0;480,0;510,0;540,0;570,0;600,0;630,0"/>'
         f'<animate attributeName="opacity" values="1;0;1" dur="0.9s" begin="3.9s" repeatCount="indefinite"/></rect>')

# ---- 小黏菌角色（左下角，浮动 + 眨眼）----
SLIME = [
    "................",
    "......GGGG......",
    "....GGggggGG....",
    "...GggggggggG...",
    "..GggggggggggG..",
    "..GggggggggggG..",
    ".GggEEggggEEggG.",
    ".GggEWggggEWggG.",
    ".GggggggggggggG.",
    ".GgggMggggMgggG.",
    ".GgggggMMggggG..",
    ".GgPggggggggPgG.",
    ".GggggggggggggG.",
    "..GggggggggggG..",
    "...GGggggggGG...",
    ".....GGGGGG....."
]
SLIME_PAL = {'G': '#2ba873', 'g': '#3ddc97', 'h': '#7cf5c0', 'E': '#0a0e14', 'W': '#ffffff', 'M': '#1a5c3a', 'P': '#ff9fb2'}
SPX = 8
sx0, sy0 = 40, 196
s.append(f'<g transform="translate({sx0},{sy0})">')
s.append(f'<animateTransform attributeName="transform" type="translate" values="{sx0},{sy0};{sx0},{sy0-8};{sx0},{sy0}" dur="3.4s" repeatCount="indefinite"/>')
# 光晕
s.append(f'<circle cx="{8*SPX}" cy="{9*SPX}" r="{7*SPX}" fill="#3ddc97" opacity="0.08"/>')
# 眨眼组（眼睛行，周期眨）
blink_rows = {6, 7}
for r, row in enumerate(SLIME):
    for c, ch in enumerate(row):
        if ch == '.':
            continue
        col = SLIME_PAL.get(ch)
        if not col:
            continue
        x, y = c * SPX, r * SPX
        if r in blink_rows and ch in ('E', 'W'):
            s.append(f'<rect x="{x}" y="{y}" width="{SPX}" height="{SPX}" fill="{col}">'
                     f'<animate attributeName="opacity" values="1;1;0;1;1" keyTimes="0;0.82;0.86;0.90;1" dur="4.4s" repeatCount="indefinite"/></rect>')
        else:
            s.append(f'<rect x="{x}" y="{y}" width="{SPX}" height="{SPX}" fill="{col}"/>')
s.append('</g>')

# ---- 扫描线覆盖 ----
s.append(f'<rect width="{W}" height="{H}" fill="url(#scan)"/>')

# ---- 边框 ----
s.append(f'<rect x="3" y="3" width="{W-6}" height="{H-6}" fill="none" stroke="#2a3442" stroke-width="3"/>')
# 四角装饰方块
for (ax, ay) in [(3, 3), (W-15, 3), (3, H-15), (W-15, H-15)]:
    s.append(f'<rect x="{ax}" y="{ay}" width="12" height="12" fill="#3ddc97"/>')

s.append('</svg>')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(s))

print(f"banner.svg 生成: {os.path.abspath(OUT)}")
print(f"尺寸: {W}x{H}, 文字宽: {name_w}px (字块 {PX}px), 标语宽: {tag_w}px")
print(f"文件大小: {os.path.getsize(OUT)} bytes")
