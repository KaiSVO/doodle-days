# Spooky season sticker pack: writes the pack JSON (used by add step) and a preview sheet
import json,math,sys
O='stroke="#2B2B2B" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"'
D='#2B2B2B'
def web():
    c=50; R=[14,27,40]; n=8; out=[]
    pts=lambda r:[(c+r*math.cos(2*math.pi*i/n-math.pi/2),c+r*math.sin(2*math.pi*i/n-math.pi/2)) for i in range(n)]
    for (x,y) in pts(44): out.append(f'M50 50L{x:.1f} {y:.1f}')
    for r in R:
        p=pts(r); s=f'M{p[0][0]:.1f} {p[0][1]:.1f}'
        for i in range(1,n+1):
            a=p[i-1]; b=p[i%n]; mx=(a[0]+b[0])/2; my=(a[1]+b[1])/2; qx=mx+(c-mx)*.18; qy=my+(c-my)*.18
            s+=f'Q{qx:.1f} {qy:.1f} {b[0]:.1f} {b[1]:.1f}'
        out.append(s)
    return f'<path d="{"".join(out)}" fill="none" stroke="#6F6A80" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/><path d="M50 50L50 66" stroke="{D}" stroke-width="2"/><circle cx="50" cy="73" r="9" fill="#3A3340" {O}/><path d="M42 69l-8-5M42 76l-9 2M58 69l8-5M58 76l9 2" stroke="{D}" stroke-width="3" stroke-linecap="round"/>'
P=[
 ('h-jack',f'<path d="M50 24Q48 12 56 8" fill="none" stroke="#5E9E62" stroke-width="6" stroke-linecap="round"/><ellipse cx="32" cy="58" rx="20" ry="28" fill="#F28C38" {O}/><ellipse cx="68" cy="58" rx="20" ry="28" fill="#F28C38" {O}/><ellipse cx="50" cy="58" rx="16" ry="32" fill="#F7A04E" {O}/><path d="M38 52l5-9 5 9zM52 52l5-9 5 9z" fill="{D}"/><path d="M38 62L42 67L46 62L50 67L54 62L58 67L62 62Q59 76 50 76Q41 76 38 62Z" fill="{D}"/><ellipse cx="50" cy="58" rx="16" ry="32" fill="none" {O}/>'),
 ('h-ghost',f'<path d="M24 88V44a26 26 0 0 1 52 0v44l-9-8-9 8-8-8-8 8-9-8z" fill="#FFFFFF" {O}/><ellipse cx="41" cy="46" rx="5" ry="7" fill="{D}"/><ellipse cx="59" cy="46" rx="5" ry="7" fill="{D}"/><ellipse cx="50" cy="62" rx="5" ry="6" fill="{D}"/><circle cx="34" cy="54" r="4" fill="#F4A6B8"/><circle cx="66" cy="54" r="4" fill="#F4A6B8"/>'),
 ('h-bat',f'<path d="M48 48C38 34 20 32 6 42c8 3 11 9 11 16 6-5 13-5 17 1 4-5 9-7 14-7zM52 48C62 34 80 32 94 42c-8 3-11 9-11 16-6-5-13-5-17 1-4-5-9-7-14-7z" fill="#5B4A72" {O}/><path d="M40 40l2-12 7 7h2l7-7 2 12v14a10 10 0 0 1-20 0z" fill="#4A3B5C" {O}/><circle cx="45" cy="46" r="3" fill="#FFE27A"/><circle cx="55" cy="46" r="3" fill="#FFE27A"/><path d="M46 56l2 3 2-3 2 3 2-3" fill="none" stroke="#fff" stroke-width="2" stroke-linejoin="round"/>'),
 ('h-cat',f'<path d="M60 82q28 2 26-24" fill="none" stroke="{D}" stroke-width="11" stroke-linecap="round"/><path d="M60 82q28 2 26-24" fill="none" stroke="#3A3340" stroke-width="5" stroke-linecap="round"/><path d="M30 90Q24 62 36 50L32 24l14 12h8l14-12-4 26Q76 62 70 90z" fill="#3A3340" {O}/><ellipse cx="43" cy="50" rx="5" ry="6" fill="#B5E36B"/><ellipse cx="57" cy="50" rx="5" ry="6" fill="#B5E36B"/><path d="M43 47v6M57 47v6" stroke="{D}" stroke-width="2.5" stroke-linecap="round"/><path d="M47 60l3 3 3-3" fill="none" stroke="#F4A6B8" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>'),
 ('h-hat',f'<ellipse cx="50" cy="78" rx="42" ry="11" fill="#5B3F8C" {O}/><path d="M28 78L46 18Q50 8 62 12Q54 15 54 24L72 78Q50 84 28 78Z" fill="#6B4FA0" {O}/><path d="M32 66Q50 71 68 66L71 75Q50 81 29 75Z" fill="#F28C38" {O}/><rect x="45" y="67" width="10" height="10" rx="2" fill="#FFE27A" stroke="#2B2B2B" stroke-width="3" stroke-linejoin="round"/>'),
 ('h-candycorn',f'<path d="M50 10L61.2 38H38.8Z" fill="#FFFFFF"/><path d="M38.8 38H61.2L70.8 62H29.2Z" fill="#F28C38"/><path d="M29.2 62H70.8L78 80Q50 92 22 80Z" fill="#F7C948"/><path d="M50 10L78 80Q50 92 22 80Z" fill="none" {O}/>'),
 ('h-web',web()),
 ('h-cauldron',f'<circle cx="38" cy="22" r="7" fill="#8FD67F" {O}/><circle cx="56" cy="14" r="5" fill="#8FD67F" {O}/><circle cx="62" cy="30" r="6" fill="#8FD67F" {O}/><path d="M20 46h60q4 30-12 40H32Q16 76 20 46z" fill="#3A3340" {O}/><path d="M28 86l-4 8M72 86l4 8" stroke="{D}" stroke-width="5" stroke-linecap="round"/><rect x="12" y="38" width="76" height="12" rx="6" fill="#5A5470" {O}/><path d="M24 44q10-6 20 0t20 0 16 0" fill="none" stroke="#8FD67F" stroke-width="4" stroke-linecap="round"/>'),
 ('h-candy',f'<path d="M32 50L10 34v32zM68 50l22-16v32z" fill="#9B6BD6" {O}/><ellipse cx="50" cy="50" rx="21" ry="17" fill="#F28C38" {O}/><path d="M40 41q-5 9 0 18M50 37q-5 13 0 26M60 41q-5 9 0 18" fill="none" stroke="#FFE27A" stroke-width="4" stroke-linecap="round"/><ellipse cx="50" cy="50" rx="21" ry="17" fill="none" {O}/>'),
 ('h-moon',f'<path d="M60 10A40 40 0 1 0 90 72A32 32 0 1 1 60 10Z" fill="#F7D774" {O}/><circle cx="36" cy="44" r="5" fill="#E8C35A"/><circle cx="44" cy="70" r="4" fill="#E8C35A"/><g transform="translate(80 30) scale(.85) translate(-68 -46)"><path d="M66 46c-4-5-10-5-14-2 3 1 4 4 4 6 3-2 6-1 7 1 1-2 2-3 3-5zm4 0c4-5 10-5 14-2-3 1-4 4-4 6-3-2-6-1-7 1-1-2-2-3-3-5z" fill="{D}"/><circle cx="68" cy="48" r="3.5" fill="{D}"/></g>'),
 ('h-potion',f'<rect x="42" y="8" width="16" height="10" rx="3" fill="#B98A5E" {O}/><path d="M44 18h12v14q22 10 18 34-4 24-24 24T26 66q-4-24 18-34z" fill="#C9F0D9" {O}/><path d="M29 62q21-8 42 0-1 22-21 24T29 62z" fill="#9B6BD6"/><circle cx="44" cy="70" r="3" fill="#E3D2FA"/><circle cx="56" cy="76" r="2" fill="#E3D2FA"/><path d="M44 18h12v14q22 10 18 34-4 24-24 24T26 66q-4-24 18-34z" fill="none" {O}/>'),
 ('h-boo',f'<path d="M14 24q0-10 10-10h52q10 0 10 10v34q0 10-10 10H46L30 84l2-16h-8q-10 0-10-10z" fill="#FFFFFF" {O}/><text x="50" y="49" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-weight="900" font-size="20" fill="#F28C38" stroke="{D}" stroke-width="1.2">BOO!</text>'),
]
if __name__=='__main__':
    out=sys.argv[1]
    cells=''.join(f'<div style="display:inline-block;text-align:center;margin:8px;font:11px sans-serif"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="110" height="110">{b}</svg><br>{i}</div>' for i,b in P)
    open(out,'w').write(f'<html><body style="background:#f3efe7;width:780px">{cells}</body></html>')
