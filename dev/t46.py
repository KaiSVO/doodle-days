# font x space sweep: overlap/clip sweep (t42 detector) + text spilling out of buttons/chips, across widest/tallest font picks and theme fonts
import asyncio,json,sys
from playwright.async_api import async_playwright
from fontroute import setup
src=open('t42.py').read(); DETECT=src[src.index('DETECT=r"""')+11:src.index('"""',src.index('DETECT=r"""')+11)]
SPILL=r"""()=>{const out=[];for(const e of document.querySelectorAll('button,.btn,.chip,.tab,.tool,.bopt,.sh-way,.ipk,.fontopt,.skin,.chipbtn,.finchip,.qmore,.wd-act,.evline,.wd-ev,.done,label')){
 if(e.closest('.day,.evline,.wd-ev,.tc-name')||getComputedStyle(e).overflow!=='visible')continue;const r=e.getBoundingClientRect();if(!r.width||!r.height||r.bottom<0||r.top>innerHeight)continue;const c=getComputedStyle(e);if(c.visibility==='hidden'||e.closest('[hidden]'))continue;
 const rg=document.createRange();rg.selectNodeContents(e);for(const q of rg.getClientRects()){if(q.width<2)continue;
  if(q.top<r.top-2||q.bottom>r.bottom+2||q.left<r.left-2||q.right>r.right+2){out.push(`SPILL "${e.textContent.trim().slice(0,30)}" <${e.tagName.toLowerCase()}.${(e.className||'').toString().split(' ')[0]}> by ${Math.round(Math.max(r.top-q.top,q.bottom-r.bottom,r.left-q.left,q.right-r.right))}px`);break;}}}
 return [...new Set(out)];}"""
CONF=[('unbounded+plexmono','candy','unbounded','plexmono'),('doodle+montalt','candy','doodle','montalt'),('pacifico+merriweather','candy','pacifico','merriweather'),
      ('lobster+balsamiq','candy','lobster','balsamiq'),('amatic+kurale','candy','amatic','kurale'),('yeseva+playpen','candy','yeseva','playpen'),
      ('pixel-theme','pixel','',''),('rose-theme','rose','',''),('scrapbook-theme','scrapbook','','')]
import sys
RUNS=([(c,loc,390) for c in CONF for loc in ['uk-UA','de-DE']] if 'all' in sys.argv else [(CONF[2],'uk-UA',390),(CONF[3],'de-DE',390)])+[(CONF[0],'de-DE',1280),(CONF[6],'uk-UA',1280),(CONF[2],'uk-UA',1280)]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); report={}
        for (name,skin,fh,fb),loc,W in RUNS:
            c=await b.new_context(viewport={'width':W,'height':844 if W<500 else 900},locale=loc,service_workers='block',has_touch=W<500); await setup(c)
            pg=await c.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
            await pg.goto('http://localhost:8765/#supporter-preview'); await pg.wait_for_timeout(2300)
            while await pg.is_visible('#tourModal'): await pg.click('#tourNext'); await pg.wait_for_timeout(40)
            await pg.evaluate("""([sk,fh,fb])=>new Promise(res=>{const r=indexedDB.open('doodle-days',1);r.onsuccess=()=>{const st=r.result.transaction('kv','readwrite').objectStore('kv');const g=st.get('meta');g.onsuccess=()=>{const m=g.result;m.skin=sk;m.fontHead=fh;m.fontBody=fb;m.tourDone=false;st.put(m,'meta');st.transaction.oncomplete=()=>res();};};})""",[skin,fh,fb])
            await pg.reload(); await pg.wait_for_timeout(3000); await pg.evaluate("document.fonts.ready")
            key=f'{name}-{loc[:2]}-{W}'; res={}
            async def snap(n):
                await pg.wait_for_timeout(400); r=(await pg.evaluate(DETECT,n))+(await pg.evaluate(SPILL))
                if r: res[n]=r; await pg.screenshot(path=f'shots11/{key}-{n}.png')
            async def esc(): await pg.keyboard.press('Escape'); await pg.wait_for_timeout(250)
            async def tc(sel):
                try: await pg.click(sel,timeout=1500); return True
                except Exception: return False
            k=0
            if await tc('.tab[data-view=settings]'):
                if await tc('#tourBtn'):
                    while await pg.is_visible('#tourModal') and k<14: await snap(f'tour{k}'); await pg.click('#tourNext'); k+=1; await pg.wait_for_timeout(450)
            await esc()
            for v in ['month','week','year','list','notes','settings']:
                await tc(f'.tab[data-view={v}]'); await snap(v)
                if v=='month':
                    await tc('.day >> nth=9'); await snap('dayPanel'); await esc()
                    if await tc('#newTracker'): await snap('trackerModal'); await esc()
                    if await tc('#revealBtn'): await snap('reveal'); await esc()
                    if await tc('#view-month .shcal'): await pg.wait_for_timeout(500); await snap('share'); await esc()
                    if await tc('#searchBtn'): await snap('search'); (await tc('#gsFiltBtn')) and await snap('searchFilters'); await esc(); await tc('#searchBtn') if await pg.is_visible('#gsearch') else None
                if v=='settings':
                    await pg.evaluate("document.querySelector('.support').scrollIntoView()"); await snap('settings-support')
                    for bt in ['#faqBtn','#binBtn','#fbBtn']:
                        if await tc(bt): await snap(bt[1:]); await esc()
            if errs: res['_errors']=errs
            report[key]=res; await c.close(); print(key, sum(len(v) for v in res.values()), flush=True)
        await b.close(); json.dump(report,open('shots11/report.json','w'),ensure_ascii=False,indent=1)
import os; os.makedirs('shots11',exist_ok=True); asyncio.run(main())
