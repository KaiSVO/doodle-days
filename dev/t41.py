import asyncio,sys
from playwright.async_api import async_playwright
from fontroute import setup
LOCS=[('en-GB','en'),('uk-UA','uk'),('es-ES','es'),('pt-BR','pt'),('de-DE','de'),('fr-FR','fr'),('pl-PL','pl')]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); errs=[]
        for loc,tag in LOCS:
            c=await b.new_context(viewport={'width':1280,'height':900},locale=loc,service_workers='block',accept_downloads=True); await setup(c)
            pg=await c.new_page(); pg.on('pageerror',lambda e:errs.append(str(e)))
            await pg.goto('http://localhost:8765/#supporter-preview'); await pg.wait_for_timeout(2800)
            while await pg.is_visible('#tourModal'): await pg.click('#tourNext'); await pg.wait_for_timeout(80)
            await pg.evaluate("""()=>new Promise(res=>{const r=indexedDB.open('doodle-days',1);r.onsuccess=()=>{const db=r.result,st=db.transaction('kv','readwrite').objectStore('kv');
              const n=new Date(),y=n.getFullYear(),m=n.getMonth(),K=(y,m,d)=>`${y}-${String(m+1).padStart(2,'0')}-${String(d).padStart(2,'0')}`;
              const names=['Вишивання хрестиком для подарунків','Acuarela botánica y caligrafía moderna','Kalligraphie und Handlettering','Pintura em aquarela','Szydełkowanie'];
              const g=st.get('meta');g.onsuccess=()=>{const meta=g.result||{};meta.trackers=names.map((nm,i)=>({id:'t'+i,name:nm,color:'#E07A5F',emoji:'✿'}));st.put(meta,'meta');
              for(let d=1;d<=20;d++)st.put({tags:names.map((_,i)=>'t'+i).filter((_,i)=>d%(i+1)===0),mood:null},'d:'+K(y,m,d));
              for(let d=1;d<=15;d++)st.put({tags:['t0']},'d:'+K(y,0,d));};
              st.transaction.oncomplete=()=>res();};})""")
            await pg.reload(); await pg.wait_for_timeout(2500)
            await pg.click('#revealBtn'); await pg.wait_for_timeout(400)
            await pg.click('#rvPrev') if False else None
            async with pg.expect_download() as dl: await pg.click('#rvSave')
            await (await dl.value).save_as(f'shots6/month-{tag}.png')
            await pg.keyboard.press('Escape')
            await pg.click('.tab[data-view=year]'); await pg.wait_for_timeout(200)
            async with pg.expect_download() as dl: await pg.click('#posterBtn')
            await (await dl.value).save_as(f'shots6/year-{tag}.png')
            await pg.click('.tab[data-view=month]'); await pg.click('.day >> nth=9'); await pg.wait_for_timeout(300)
            async with pg.expect_download() as dl: await pg.click('#shareDay')
            await (await dl.value).save_as(f'shots6/day-{tag}.png')
            await c.close()
        print('ERR',errs); await b.close()
asyncio.run(main())
