"""Builds the subtle background silhouette tiles for each theme as CSS."""
import urllib.parse

# Each motif is drawn in a 100x100 box; "C" is replaced by the colour.
F = 'fill="C"'
S = 'fill="none" stroke="C" stroke-linecap="round" stroke-linejoin="round"'
def px(rows, cell=10):
    out = []
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch == '#': out.append(f'<rect x="{x*cell}" y="{y*cell}" width="{cell}" height="{cell}"/>')
    return f'<g {F}>' + ''.join(out) + '</g>'

MOTIFS = {
 'candy': [
  f'<path {F} fill-rule="evenodd" d="M50 8a30 30 0 1 1 0 60a30 30 0 1 1 0-60zM50 20a18 18 0 1 0 0 36a18 18 0 1 0 0-36zM50 30a8 8 0 1 1 0 16a8 8 0 1 1 0-16z"/><rect {F} x="46" y="66" width="8" height="32" rx="4"/>',
  f'<path {F} d="M30 50a20 15 0 1 0 40 0a20 15 0 1 0-40 0zM32 50L8 34L12 50L8 66zM68 50L92 34L88 50L92 66z"/>',
  f'<path {F} d="M50 86C22 66 10 46 20 31C30 17 46 22 50 35C54 22 70 17 80 31C90 46 78 66 50 86Z"/>',
  f'<path {F} d="M24 52h52l-8 40h-36zM22 50c0-16 10-26 28-26s28 10 28 26z"/><circle {F} cx="50" cy="18" r="7"/>',
  f'<g {F}><rect x="18" y="20" width="22" height="8" rx="4" transform="rotate(30 29 24)"/><rect x="58" y="30" width="22" height="8" rx="4" transform="rotate(-25 69 34)"/><rect x="30" y="62" width="22" height="8" rx="4" transform="rotate(-50 41 66)"/><rect x="62" y="70" width="22" height="8" rx="4" transform="rotate(15 73 74)"/></g>',
  f'<path {F} fill-rule="evenodd" d="M50 14a36 36 0 1 1 0 72a36 36 0 1 1 0-72zM50 24a26 26 0 1 0 0 52a26 26 0 1 0 0-52z"/><circle {F} cx="38" cy="38" r="6"/>',
 ],
 'pixel': [
  px([".##.##.", "#######", "#######", ".#####.", "..###..", "...#..."], 13),
  px(["..###..", ".#####.", "##.#.##", "##.#.##", "##.#.##", ".#####.", "..###.."], 13),
  px(["...#...", "...#...", "#######", ".#####.", "..###..", ".##.##.", "#.....#"], 13),
  px(["..###..", ".#####.", "#######", ".#####.", "..###..", "...#..."], 13),
  px(["..###..", "...#...", "..###..", ".#####.", "#######", "#######", ".#####."], 13),
  px(["...#...", "...#...", ".#####.", "...#...", "...#..."], 15),
 ],
 'classic': [
  f'<path {S} stroke-width="7" d="M30 78a12 12 0 1 0 0.1 0M70 78a12 12 0 1 0 0.1 0M38 68L78 14M62 68L22 14"/>',
  f'<g transform="rotate(-35 50 50)"><rect {F} x="40" y="8" width="20" height="62" rx="3"/><path {F} d="M40 72h20L50 94z"/></g>',
  f'<path {F} d="M26 18h48v10h-6v44h6v10H26V72h6V28h-6z"/>',
  f'<path {F} fill-rule="evenodd" d="M50 14a36 36 0 1 1 0 72a36 36 0 1 1 0-72zM42 40a5 5 0 1 0 0.1 0M58 40a5 5 0 1 0 0.1 0M42 58a5 5 0 1 0 0.1 0M58 58a5 5 0 1 0 0.1 0z"/>',
  f'<g transform="rotate(30 50 50)"><rect {F} x="44" y="6" width="12" height="52" rx="5"/><rect {F} x="41" y="56" width="18" height="10"/><path {F} d="M41 66h18l-3 18q-6 10-12 0z"/></g>',
  f'<g transform="rotate(-20 50 50)"><rect {F} x="10" y="38" width="80" height="24" rx="3"/></g>',
 ],
 'scrapbook': [
  f'<path {S} stroke-width="6" d="M38 30v42a12 12 0 0 0 24 0V22a8 8 0 0 0-16 0v46"/>',
  f'<path {F} d="M10 36l6-6 6 6 6-6 6 6 6-6 6 6 6-6 6 6 6-6 6 6 6-6 6 6 6-6v34l-6 6-6-6-6 6-6-6-6 6-6-6-6 6-6-6-6 6-6-6-6 6-6-6-6 6z" transform="rotate(-12 50 50)"/>',
  f'<path {F} fill-rule="evenodd" d="M20 14h60v72H20zM28 22v44h44V22z"/>',
  f'<path {F} fill-rule="evenodd" d="M14 26h72v50H14zM20 32l30 22 30-22z"/>',
  f'<path {F} fill-rule="evenodd" d="M50 16a34 34 0 1 1 0 68a34 34 0 1 1 0-68zM43 43a5 5 0 1 0 0.1 0M57 43a5 5 0 1 0 0.1 0M43 57a5 5 0 1 0 0.1 0M57 57a5 5 0 1 0 0.1 0z"/>',
  f'<path {F} d="M50 10l9 26h27l-22 16 8 26-22-16-22 16 8-26-22-16h27z"/>',
 ],
 'garden': [
  f'<path {F} d="M18 82C18 42 48 16 86 14C86 52 60 82 18 82Z"/><path {S} stroke-width="4" d="M14 88L60 42"/>',
  f'<path {S} stroke-width="4" d="M50 94Q48 50 58 8"/><g {F}><ellipse cx="40" cy="74" rx="12" ry="5" transform="rotate(-25 40 74)"/><ellipse cx="62" cy="68" rx="12" ry="5" transform="rotate(25 62 68)"/><ellipse cx="42" cy="54" rx="11" ry="5" transform="rotate(-30 42 54)"/><ellipse cx="62" cy="48" rx="11" ry="5" transform="rotate(30 62 48)"/><ellipse cx="46" cy="34" rx="9" ry="4" transform="rotate(-35 46 34)"/><ellipse cx="64" cy="28" rx="9" ry="4" transform="rotate(35 64 28)"/></g>',
  f'<g {F}><ellipse cx="50" cy="24" rx="9" ry="16"/><ellipse cx="50" cy="76" rx="9" ry="16"/><ellipse cx="24" cy="50" rx="16" ry="9"/><ellipse cx="76" cy="50" rx="16" ry="9"/><ellipse cx="32" cy="32" rx="9" ry="16" transform="rotate(-45 32 32)"/><ellipse cx="68" cy="68" rx="9" ry="16" transform="rotate(-45 68 68)"/><ellipse cx="68" cy="32" rx="9" ry="16" transform="rotate(45 68 32)"/><ellipse cx="32" cy="68" rx="9" ry="16" transform="rotate(45 32 68)"/></g>',
  f'<g {F}><ellipse cx="50" cy="58" rx="24" ry="17"/><ellipse cx="38" cy="32" rx="14" ry="10" transform="rotate(-30 38 32)"/><ellipse cx="62" cy="32" rx="14" ry="10" transform="rotate(30 62 32)"/></g>',
  f'<path {F} fill-rule="evenodd" d="M58 30a26 26 0 1 1 0 52H14q-6 0-4-6l8-4a26 26 0 0 1 40-42zM58 44a12 12 0 1 0 0.1 0z"/><path {S} stroke-width="4" d="M22 70L14 50M28 68L26 46"/>',
  f'<path {F} d="M14 50Q14 20 50 18Q86 20 86 50z"/><path {F} d="M40 50h20v34q-10 6-20 0z"/>',
 ],
 'rose': [
  f'<path {F} fill-rule="evenodd" d="M50 14c18 0 32 12 32 28c0 18-14 30-32 30S18 60 18 42c0-16 14-28 32-28zM50 28c-8 0-14 6-14 13s6 13 14 13 14-6 14-13c0-4-3-7-7-7s-6 3-6 6"/><path {S} stroke-width="5" d="M50 72v24"/>',
  f'<path {S} stroke-width="5" d="M30 94Q50 60 46 10"/><path {F} d="M44 50Q20 44 18 26Q38 28 44 50z"/><path {F} d="M49 30l8-6-4 9zM42 70l-9 3 6-8z"/>',
  f'<path {F} d="M50 12C70 30 74 56 50 88C26 56 30 30 50 12z"/>',
  f'<path {F} d="M64 12A40 40 0 1 0 90 70A32 32 0 1 1 64 12Z"/>',
  f'<path {F} d="M50 20l6 24 24 6-24 6-6 24-6-24-24-6 24-6z"/>',
  f'<path {F} d="M50 86C22 66 10 46 20 31C30 17 46 22 50 35C54 22 70 17 80 31C90 46 78 66 50 86Z"/>',
 ],
}

SPOTS = [(70, 80, 1.0, -15), (260, 50, .8, 20), (380, 200, 1.0, -28), (150, 250, .9, 12),
         (310, 345, .75, 35), (45, 370, .85, -8), (215, 150, .55, 0), (395, 405, .5, 18),
         (120, 420-12, .45, 40)]
TILE = 440

def tile(kind, colours):
    parts = []
    m = MOTIFS[kind]
    for i, (x, y, s, r) in enumerate(SPOTS):
        size = 64 * s
        c = colours[i % len(colours)]
        body = m[i % len(m)].replace('"C"', f'"{c}"')
        # draw near edges twice so the pattern wraps seamlessly
        for ox in (0, -TILE, TILE):
            for oy in (0, -TILE, TILE):
                cx, cy = x + ox, y + oy
                if -size < cx < TILE + size and -size < cy < TILE + size:
                    parts.append(f'<g transform="translate({cx-size/2:.1f} {cy-size/2:.1f}) rotate({r} {size/2:.1f} {size/2:.1f}) scale({size/100:.3f})">{body}</g>')
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{TILE}" height="{TILE}" viewBox="0 0 {TILE} {TILE}">{"".join(parts)}</svg>'
    return 'url("data:image/svg+xml,' + urllib.parse.quote(svg, safe=' /=:,.-') + '")'

THEMES = [
 # selector, kind, colours, wash
 (':root', 'classic', ['rgba(31,92,74,.075)'], 'linear-gradient(180deg,rgba(233,162,59,.07),transparent 45%)'),
 (':root[data-theme="dark"]', 'classic', ['rgba(114,199,166,.07)'], 'linear-gradient(180deg,rgba(240,180,87,.05),transparent 45%)'),
 (':root[data-skin="candy"]', 'candy', ['rgba(108,60,240,.075)', 'rgba(255,122,198,.11)'], 'radial-gradient(120% 70% at 0% 0%,rgba(255,122,198,.14),transparent 60%),radial-gradient(90% 60% at 100% 100%,rgba(108,60,240,.10),transparent 60%)'),
 (':root[data-skin="candy"][data-theme="dark"]', 'candy', ['rgba(182,156,255,.08)', 'rgba(255,122,198,.08)'], 'radial-gradient(120% 70% at 0% 0%,rgba(255,122,198,.10),transparent 60%),radial-gradient(90% 60% at 100% 100%,rgba(108,60,240,.18),transparent 60%)'),
 (':root[data-skin="pixel"]', 'pixel', ['rgba(255,209,102,.075)', 'rgba(6,214,160,.07)'], 'linear-gradient(180deg,rgba(6,214,160,.06),transparent 40%,rgba(255,209,102,.05))'),
 (':root[data-skin="scrapbook"]', 'scrapbook', ['rgba(160,100,60,.09)', 'rgba(216,79,120,.08)'], 'radial-gradient(100% 60% at 50% 0%,rgba(255,250,240,.55),transparent 70%)'),
 (':root[data-skin="garden"]', 'garden', ['rgba(94,127,88,.10)', 'rgba(231,169,184,.16)'], 'linear-gradient(180deg,rgba(231,169,184,.12),transparent 40%,rgba(94,127,88,.08))'),
 (':root[data-skin="rose"]', 'rose', ['rgba(224,41,74,.10)', 'rgba(255,143,163,.06)'], 'radial-gradient(110% 70% at 100% 0%,rgba(224,41,74,.14),transparent 70%),radial-gradient(110% 70% at 0% 100%,rgba(224,41,74,.09),transparent 70%)'),
]

def css():
    out = ['/* theme backdrops: soft colour wash + faint silhouettes that match each theme */',
           'body::before{content:"";position:fixed;inset:0;z-index:-1;pointer-events:none;background-image:var(--deco,none),var(--wash,none);background-size:440px 440px,100% 100%,100% 100%,100% 100%;background-repeat:repeat,no-repeat,no-repeat,no-repeat}']
    for sel, kind, cols, wash in THEMES:
        out.append(f'{sel}{{--deco:{tile(kind, cols)};--wash:{wash}}}')
    return '\n'.join(out)

if __name__ == '__main__':
    open('deco.css', 'w').write(css())
    print(len(css()))
