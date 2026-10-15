# UI overlap/clipping sweep: every view + modal, 7 languages, phone + desktop
import asyncio,json
from playwright.async_api import async_playwright
from fontroute import setup
LOCS=[('en-GB','en'),('uk-UA','uk'),('es-ES','es'),('pt-BR','pt'),('de-DE','de'),('fr-FR','fr'),('pl-PL','pl')]
SIZES=[(390,844),(1280,900)]
DETECT=r"""(name)=>{
 const vis=e=>{const r=e.getBoundingClientRect(),c=getComputedStyle(e);return r.width>0&&r.height>0&&c.visibility!=='hidden'&&+c.opacity>0.05};
 const top=(e,r)=>{const x=r.left+r.width/2,y=r.top+r.height/2;if(x<0||y<0||x>innerWidth||y>innerHeight)return false;const t=document.elementFromPoint(x,y);return t&&(t===e||e.contains(t)||t.contains(e))};
 const items=[];const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;
 while(n=w.nextNode()){if(!n.nodeValue.trim())continue;const e=n.parentElement;if(!e||!vis(e)||(e.closest('details:not([open])')&&!e.closest('summary'))||e.closest('svg,script,style,[aria-hidden=true],canvas'))continue;
  const rg=document.createRange();rg.selectNodeContents(n);for(let r of rg.getClientRects()){let L=r.left,T=r.top,R=r.right,B=r.bottom;for(let p=e;p&&p!==document.body;p=p.parentElement){const c=getComputedStyle(p);if(c.overflowX!=='visible'||c.overflowY!=='visible'){const q=p.getBoundingClientRect();L=Math.max(L,q.left);T=Math.max(T,q.top);R=Math.min(R,q.right);B=Math.min(B,q.bottom);}}
  r={left:L,top:T,right:R,bottom:B,width:R-L,height:B-T,raw:r};if(r.width<3||r.height<3)continue;if(!top(e,r))continue;items.push({e,r,t:n.nodeValue.trim().slice(0,40)});}}
 const out=[];
 for(let i=0;i<items.length;i++)for(let j=i+1;j<items.length;j++){const a=items[i],b=items[j];if(a.e===b.e||a.e.contains(b.e)||b.e.contains(a.e))continue;
  const ox=Math.min(a.r.right,b.r.right)-Math.max(a.r.left,b.r.left),oy=Math.min(a.r.bottom,b.r.bottom)-Math.max(a.r.top,b.r.top);
  if(ox>3&&oy>Math.min(a.r.height,b.r.height)*.35)out.push(`OVERLAP "${a.t}" × "${b.t}"`);}
 const seen=new Set();
 for(const {e,r:rc,t} of items){const r=rc.raw;if(e.closest('[style*=line-clamp]')||[...function*(){for(let p=e;p&&p!==document.body;p=p.parentElement)yield p}()].some(p=>{const c=getComputedStyle(p);return c.webkitLineClamp!=='none'||c.textOverflow==='ellipsis'}))continue;let p=e;while(p&&p!==document.body){const c=getComputedStyle(p);
   if(c.overflowX!=='visible'||c.overflowY!=='visible'){const pr=p.getBoundingClientRect();
     const clipX=c.overflowX!=='visible'&&c.overflowX!=='auto'&&c.overflowX!=='scroll', clipY=c.overflowY!=='visible'&&c.overflowY!=='auto'&&c.overflowY!=='scroll';
     if(((clipX&&(r.right>pr.right+1||r.left<pr.left-1))||(clipY&&(r.bottom>pr.bottom+2||r.top<pr.top-2)))&&!seen.has(e)){seen.add(e);out.push(`CLIP "${t}" in <${p.tagName.toLowerCase()} ${p.id?'#'+p.id:p.className}>`);}
     break;}p=p.parentElement;}
  if(r.right>innerWidth+1&&!seen.has(e)){seen.add(e);out.push(`OFFSCREEN "${t}"`);}}
 return out;}"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); report={}
        for loc,tag in LOCS:
          for W,H in SIZES:
            c=await b.new_context(viewport={'width':W,'height':H},locale=loc,service_workers='block',has_touch=W<500); await setup(c)
            pg=await c.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
            await pg.goto('http://localhost:8765/#supporter-preview'); await pg.wait_for_timeout(2500)
            res={}
            async def snap(name):
                await pg.wait_for_timeout(450); r=await pg.evaluate(DETECT,name)
                if r: res[name]=r
                await pg.screenshot(path=f'shots7/{tag}-{W}-{name}.png')
            # tour steps
            k=0
            while await pg.is_visible('#tourModal'):
                await snap(f'tour{k}'); await pg.click('#tourNext'); k+=1; await pg.wait_for_timeout(150)
            async def esc():
                await pg.keyboard.press('Escape'); await pg.wait_for_timeout(250)
            async def tryclick(sel):
                try: await pg.click(sel,timeout=1500); return True
                except Exception as e: res.setdefault('_missing',[]).append(sel); return False
            for v in ['month','week','year','list','notes','settings']:
                await tryclick(f'.tab[data-view={v}]'); await snap(v)
                if v=='month':
                    await tryclick('.day >> nth=9'); await snap('dayPanel')
                    await tryclick('#stickerBtn') if await pg.is_visible('#stickerBtn') else None; await snap('dayTray'); await esc(); await esc()
                    if await tryclick('#newTracker'): await snap('trackerModal'); await esc()
                    if await tryclick('#revealBtn'): await snap('reveal'); await esc()
                    if await tryclick('#view-month .shcal'):
                        await pg.wait_for_timeout(600); await snap('share'); await tryclick('.sh-way[data-w=ics]'); await snap('shareIcs'); await esc()
                    if await tryclick('#searchBtn'):
                        await snap('search')
                        if await tryclick('#gsFiltBtn'): await snap('searchFilters')
                        await esc()
                    await tryclick('#searchBtn') if await pg.is_visible('#gsearch') else None
                if v=='settings':
                    for bt in ['#faqBtn','#binBtn','#fbBtn']:
                        if await tryclick(bt): await snap(bt[1:]); await esc()
            res['_errors']=errs; report[f'{tag}-{W}']=res; await c.close()
        await b.close()
        json.dump(report,open('shots7/report.json','w'),ensure_ascii=False,indent=1)
        for k,v in report.items():
            for n,r in v.items():
                if r: print(k,n,r[:6])
import os; os.makedirs('shots7',exist_ok=True); asyncio.run(main())
