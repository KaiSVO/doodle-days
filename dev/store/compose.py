from PIL import Image, ImageDraw, ImageFont, ImageFilter
FR='/tmp/claude-0/gfonts/ofl/fredoka/Fredoka[wdth,wght].ttf'
def font(sz,w=700):
    f=ImageFont.truetype(FR,sz)
    ax=[a['name'] if isinstance(a['name'],str) else a['name'].decode() for a in f.get_variation_axes()]
    f.set_variation_by_axes([w if 'eight' in n or n==b'wght' else 100 for n in ax])
    return f
def mat(W,H,bg,line):
    im=Image.new('RGB',(W,H),bg); d=ImageDraw.Draw(im,'RGBA')
    for x in range(0,W,36): d.line([(x,0),(x,H)],fill=line)
    for y in range(0,H,36): d.line([(0,y),(W,y)],fill=line)
    return im
def rounded(img,r):
    m=Image.new('L',img.size,0); ImageDraw.Draw(m).rounded_rectangle([0,0,img.size[0]-1,img.size[1]-1],r,fill=255)
    out=img.convert('RGBA'); out.putalpha(m); return out
def paste_shadow(base,img,xy,blur=30,off=18,alpha=110):
    sh=Image.new('RGBA',(img.size[0]+blur*4,img.size[1]+blur*4),(0,0,0,0))
    a=img.split()[-1].point(lambda v:alpha if v else 0)
    sh.paste(Image.new('RGBA',img.size,(20,8,50,255)),(blur*2,blur*2),a)
    sh=sh.filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(sh,(xy[0]-blur*2,xy[1]-blur*2+off)); base.alpha_composite(img,xy)
def wrap(d,text,f,maxw):
    words=text.split(); lines=[]; cur=''
    for w in words:
        t=(cur+' '+w).strip()
        if d.textlength(t,font=f)>maxw and cur: lines.append(cur); cur=w
        else: cur=t
    lines.append(cur); return lines
SHOTS=[('raw1-month','A calendar you can draw in',None),
       ('raw2-day','Doodle, add stickers and jot down your day',None),
       ('raw3-activities','Build little streaks for what you make',None),
       ('raw4-week','Plan classes, fairs and deadlines',None),
       ('raw5-year','Watch your year fill up',None),
       ('raw6-rose','Themes, fonts and stickers for every mood','rose')]
for i,(raw,cap,th) in enumerate(SHOTS,1):
    W,H=1080,1920
    bg,line,fg=((15,10,12),(224,41,74,30),(255,227,234)) if th=='rose' else ((108,60,240),(255,255,255,24),(255,255,255))
    im=mat(W,H,bg,line).convert('RGBA'); d=ImageDraw.Draw(im)
    f=font(70)
    lines=wrap(d,cap,f,W-110); y=130
    for l in lines:
        d.text((W/2,y),l,font=f,fill=fg,anchor='ma'); y+=88
    shot=Image.open(raw+'.png').convert('RGB')
    sw=820; sh=int(shot.height*sw/shot.width); shot=shot.resize((sw,sh),Image.LANCZOS)
    top=max(y+50,380)
    shot=rounded(shot,46)
    paste_shadow(im,shot,((W-sw)//2,top))
    im.convert('RGB').save(f'screenshot-{i}.png')
# feature graphic 1024x500
W,H=1024,500
im=mat(W,H,(108,60,240),(255,255,255,24)).convert('RGBA'); d=ImageDraw.Draw(im)
d.text((60,150),'Doodle Days',font=font(84),fill='white')
d.text((64,262),'A calendar you can draw in',font=font(36,500),fill=(255,255,255,235))
d.text((64,318),'Doodle · plan · track your making',font=font(26,500),fill=(255,255,255,190))
shot=Image.open('raw2-day.png').convert('RGB'); shot=shot.crop((0,0,shot.width,int(shot.width*1.25)))
sw=300; shot=shot.resize((sw,int(shot.height*sw/shot.width)),Image.LANCZOS); shot=rounded(shot,30).rotate(-6,expand=True,resample=Image.BICUBIC)
paste_shadow(im,shot,(690,60),blur=20,off=12)
for name,(x,y,s,r) in {'st-heart':(640,30,110,-12),'st-star':(920,340,120,14),'st-yarn':(600,350,120,8)}.items():
    st=Image.open(name+'.png').convert('RGBA').resize((s,s),Image.LANCZOS).rotate(r,expand=True,resample=Image.BICUBIC)
    im.alpha_composite(st,(x,y))
im.convert('RGB').save('feature-graphic.png')
print('done')
