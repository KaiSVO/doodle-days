import asyncio,json,base64
from playwright.async_api import async_playwright
K=json.load(open('i18n_keys.json'))['s']
LEFT="""(keys)=>{const set=new Set(keys),out=new Set();const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;
while(n=w.nextNode()){const t=n.nodeValue.trim();if(!t||!set.has(t))continue;const el=n.parentElement;if(!el||el.closest('[hidden]')||el.closest('script,style'))continue;const r=el.getBoundingClientRect();if(r.width&&r.height)out.add(t);}return [...out];}"""
async def run(p,loc,code):
    b=await p.chromium.launch(); errs=[]
    c=await b.new_context(accept_downloads=True,viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True,locale=loc)
    pg=await c.new_page(); pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.goto('http://localhost:8765/'); await pg.wait_for_timeout(2600)
    await pg.screenshot(path=f'shots4/{code}-tour.png')
    while await pg.is_visible('#tourModal'): await pg.click('#tourNext'); await pg.wait_for_timeout(120)
    await pg.wait_for_timeout(300); await pg.screenshot(path=f'shots4/{code}-month.png')
    left=set(await pg.evaluate(LEFT,K))
    await pg.click('.tab[data-view=week]'); await pg.wait_for_timeout(300); await pg.screenshot(path=f'shots4/{code}-week.png')
    left|=set(await pg.evaluate(LEFT,K))
    await pg.click('.tab[data-view=year]'); await pg.wait_for_timeout(300); await pg.screenshot(path=f'shots4/{code}-year.png')
    await pg.click('.tab[data-view=list]'); await pg.wait_for_timeout(300); await pg.screenshot(path=f'shots4/{code}-plans.png')
    left|=set(await pg.evaluate(LEFT,K))
    await pg.click('.tab[data-view=settings]'); await pg.wait_for_timeout(300); await pg.screenshot(path=f'shots4/{code}-settings.png',full_page=True)
    left|=set(await pg.evaluate(LEFT,K))
    await pg.click('#setClose'); await pg.click('.tab[data-view=month]'); await pg.wait_for_timeout(200)
    await pg.click('.day >> nth=12'); await pg.wait_for_timeout(400); await pg.screenshot(path=f'shots4/{code}-day.png')
    left|=set(await pg.evaluate(LEFT,K))
    async with pg.expect_download() as dl: await pg.click('#shareDay')
    await (await dl.value).save_as(f'shots4/{code}-share.png')
    lang=await pg.evaluate("document.documentElement.lang"); sp=await pg.evaluate("localStorage.getItem('dd-splash')")
    print(code,'LANG=',lang,'errs=',errs,'english left=',sorted(left-{'Doodle Days','Supporter','LV'}),'splash=',(sp or '')[:80])
    await b.close()
async def main():
    async with async_playwright() as p:
        for loc,code in [('en-GB','en'),('uk-UA','uk'),('es-ES','es'),('pt-BR','pt'),('de-DE','de'),('fr-FR','fr'),('pl-PL','pl')]:
            await run(p,loc,code)
asyncio.run(main())
