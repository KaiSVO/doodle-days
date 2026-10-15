import os,re,glob,urllib.parse
G='/tmp/claude-0/gfonts/ofl'
def faces(fam):
    d=os.path.join(G,fam.lower().replace(' ',''))
    out=[]
    for f in sorted(glob.glob(d+'/*.ttf')):
        b=os.path.basename(f)
        if 'Italic' in b: continue
        if '[' in b: out.append((f,'100 1000'))
        else:
            w={'Thin':100,'ExtraLight':200,'Light':300,'Regular':400,'Medium':500,'SemiBold':600,'Bold':700,'ExtraBold':800,'Black':900}
            m=re.search(r'-(\w+)\.ttf$',b); out.append((f,str(w.get(m.group(1),400)) if m else '400'))
    return out
async def css_route(route):
    q=urllib.parse.parse_qs(urllib.parse.urlparse(route.request.url).query)
    css=''
    for fam in q.get('family',[]):
        name=fam.split(':')[0]
        for f,w in faces(name):
            css+=f"@font-face{{font-family:'{name}';font-style:normal;font-weight:{w};font-display:swap;src:url(https://fonts.gstatic.com/local{f}) format('truetype');}}\n"
    await route.fulfill(status=200,body=css,headers={'content-type':'text/css','access-control-allow-origin':'*'})
async def font_route(route):
    p=urllib.parse.urlparse(route.request.url).path.replace('/local','',1)
    if os.path.exists(p): await route.fulfill(status=200,body=open(p,'rb').read(),headers={'content-type':'font/ttf','access-control-allow-origin':'*'})
    else: await route.fulfill(status=404)
async def setup(ctx):
    await ctx.route('https://fonts.googleapis.com/**',css_route)
    await ctx.route('https://fonts.gstatic.com/**',font_route)
