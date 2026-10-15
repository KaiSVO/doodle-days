import asyncio
from playwright.async_api import async_playwright
CMP="""(()=>{const t=TSEL&&document.querySelector(TSEL);const h=document.getElementById('coachHole');if(!t)return 'no target';const a=t.getBoundingClientRect(),b=h.getBoundingClientRect();return Math.round(Math.abs(a.left-8-b.left)+Math.abs(a.top-8-b.top)+Math.abs(a.width+16-b.width)+Math.abs(a.height+16-b.height));})()"""
SEL=[None,'#grid','.card:has(#pad)','#tools','section:has(#note)','section:has(#chips)','section:has(#dayCols)','.tcard','#searchBtn','.tabs','.tab[data-view=settings]',None]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        c=await b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True,service_workers='block'); pg=await c.new_page()
        await pg.goto('http://localhost:8765/'); await pg.wait_for_timeout(2800)
        seq=[1,2,3,4,5,6,7,6,5,4,3,2,1,2,3]; cur=0
        for target in seq:
            await pg.click('#tourNext' if target>cur else '#tourBack'); cur=target
            await pg.wait_for_timeout(1000)
            js=CMP.replace('TSEL',repr(SEL[cur]) if SEL[cur] else 'null')
            print(cur, await pg.evaluate(js), end=' | ')
        await b.close()
asyncio.run(main())
