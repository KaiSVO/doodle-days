# activity/plan icons: 24x24 single stroke paths. Free set + Supporter packs. Emits icons.js for build.
def C(cx,cy,r): return f"M{cx-r} {cy}a{r} {r} 0 1 0 {2*r} 0a{r} {r} 0 1 0 {-2*r} 0z"
FREE=[('brush','Brush',"M19 3l2 2-9.5 9.5-2-2zM9.5 12.5c-2 0-3.5 1.5-3.5 3.5 0 1.5-1 2.5-3 3 3.5 1.5 8 .5 8.5-4.5"),
 ('pencil','Pencil',"M16 3.5l4.5 4.5L8.5 20H4v-4.5zM13.5 6l4.5 4.5"),
 ('yarn','Yarn',C(12,12,9)+"M5.5 7.5c4 .5 8.5 4 10 12.5M3.5 13c4-.5 8.5 2 10.5 7.5M9.5 3.5c3 2.5 7.5 7 8.5 14.5"),
 ('needle','Sewing',C(12,12,8.5)+"M9.8 9.8h.01M14.2 9.8h.01M9.8 14.2h.01M14.2 14.2h.01"),
 ('camera','Camera',"M4 8h3l2-3h6l2 3h3v11H4z"+C(12,13.5,3.5)),
 ('book','Book',"M12 6c-2-1.5-5-2-8-1.5v14c3-.5 6 0 8 1.5 2-1.5 5-2 8-1.5v-14c-3-.5-6 0-8 1.5zM12 6v14"),
 ('star','Star',"M12 3l2.6 5.6 6 .7-4.5 4.1 1.2 6L12 16.4l-5.3 3 1.2-6-4.5-4.1 6-.7z"),
 ('heart','Heart',"M12 20s-8-4.8-8-10.5A4.5 4.5 0 0 1 12 7a4.5 4.5 0 0 1 8 2.5C20 15.2 12 20 12 20z")]
PACKS=[('studio','Studio',[
 ('palette','Palette',"M12 3a9 9 0 1 0 0 18c1.5 0 2-1 1.5-2.2-.6-1.4.4-2.8 2-2.8H18a3 3 0 0 0 3-3c0-5.5-4-10-9-10zM7.5 11.5h.01M10 7.5h.01M15 7.5h.01"),
 ('scissors','Scissors',C(6,6,2.5)+C(6,18,2.5)+"M8 7.5L20 17M8 16.5L20 7"),
 ('ruler','Ruler',"M3 16L16 3l5 5L8 21zM7 12l2 2M10 9l2 2M13 6l2 2"),
 ('nib','Pen nib',"M12 3l5 6.5L12 21 7 9.5z"+C(12,11,1.6)),
 ('vase','Pottery',"M9 3h6M9.5 3c.5 2.5-3.5 4.5-3.5 9.5 0 4.5 2.5 8.5 6 8.5s6-4 6-8.5c0-5-4-7-3.5-9.5M6.4 10h11.2"),
 ('frame','Frame',"M4 4h16v16H4zM7.5 16.5l3.5-4.5 2.5 3 2-2 1.5 3.5"+C(9,8.5,1.2)),
 ('spool','Spool',"M6 3h12M6 21h12M8 3v18M16 3v18M8 7l8 3M8 11l8 3M8 15l8 3"),
 ('sparkle','Sparkles',"M12 3l1.8 4.7 4.7 1.8-4.7 1.8L12 16l-1.8-4.7-4.7-1.8 4.7-1.8zM18.5 15.5l.8 2.2 2.2.8-2.2.8-.8 2.2-.8-2.2-2.2-.8 2.2-.8z")]),
 ('everyday','Everyday',[
 ('coffee','Coffee',"M5 9h11v5a5 5 0 0 1-5 5h-1a5 5 0 0 1-5-5zM16 10h1.5a2.5 2.5 0 0 1 0 5H16M8 3c-.8 1.2.8 2 0 3.5M11.5 3c-.8 1.2.8 2 0 3.5"),
 ('leaf','Plant',"M5 19C5 10 10 5 20 4c0 10-5 15-14 15zM5 19l9-9"),
 ('music','Music',"M9 18V5l11-2v13"+C(6.5,18,2.5)+C(17.5,16,2.5)),
 ('dumbbell','Workout',"M6 7v10M3.5 9.5v5M18 7v10M20.5 9.5v5M6 12h12"),
 ('moon','Moon',"M20 14.5A8.5 8.5 0 1 1 9.5 4a7 7 0 0 0 10.5 10.5z"),
 ('sun','Sun',C(12,12,4)+"M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.9 4.9l1.8 1.8M17.3 17.3l1.8 1.8M4.9 19.1l1.8-1.8M17.3 6.7l1.8-1.8"),
 ('home','Home',"M4 11l8-7 8 7M6 9.5V20h12V9.5M10 20v-6h4v6"),
 ('chat','Chat',"M4 5h16v11H9l-5 4z")]),
 ('shop','Shop',[
 ('parcel','Parcel',"M12 3l8 4.5v9L12 21l-8-4.5v-9zM4 7.5l8 4.5 8-4.5M12 12v9M8 5.3l8 4.5"),
 ('tag','Price tag',"M3 3h8l10 10-8 8L3 11z"+C(7.5,7.5,1.5)),
 ('cart','Cart',"M3 4h2.5l2.2 11h10.8l2-8H7"+C(9,19.5,1.5)+C(17,19.5,1.5)),
 ('coins','Money',"M4 7c0-1.7 3-3 7-3s7 1.3 7 3-3 3-7 3-7-1.3-7-3zM4 7v5c0 1.7 3 3 7 3s7-1.3 7-3V7M4 12v5c0 1.7 3 3 7 3s7-1.3 7-3v-5"),
 ('truck','Delivery',"M2 6h12v10H2zM14 9h4l3 3.5V16h-7"+C(6,17.5,2)+C(17,17.5,2)),
 ('mail','Mail',"M3 5h18v14H3zM3 5l9 7 9-7"),
 ('store','Shop front',"M3 9l1.5-5h15L21 9zM3 9a3 3 0 0 0 6 0 3 3 0 0 0 6 0 3 3 0 0 0 6 0M5 12v8h14v-8M10 20v-5h4v5"),
 ('megaphone','Promo',"M3 10v4h3l9 5V5L6 10zM18 9a3.5 3.5 0 0 1 0 6M7 14l1.5 6h2.5l-1.5-6")])]
import json
out={'free':[[i,n,d] for i,n,d in FREE],'packs':[[pid,pn,[[i,n,d] for i,n,d in it]] for pid,pn,it in PACKS]}
open('icons.js','w').write('const ICON_SET='+json.dumps(out,separators=(',',':'))+';\n')
if __name__=='__main__':
    # contact sheet for eyeballing
    allx=FREE+[x for _,_,it in PACKS for x in it]
    svg=['<svg xmlns="http://www.w3.org/2000/svg" width="800" height="%d" style="background:#fff">'%(((len(allx)+7)//8)*100)]
    for k,(i,n,d) in enumerate(allx):
        X=(k%8)*100+26;Y=(k//8)*100+14
        svg.append(f'<g transform="translate({X} {Y}) scale(2)"><path d="{d}" fill="none" stroke="#333" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></g><text x="{X+24}" y="{Y+76}" font-size="11" text-anchor="middle" font-family="sans-serif">{i}</text>')
    svg.append('</svg>');open('/tmp/claude-0/-home-claude-doodle-days/c1d4284c-43bc-57e1-a35d-117e78650fe1/scratchpad/icons.svg','w').write(''.join(svg))
