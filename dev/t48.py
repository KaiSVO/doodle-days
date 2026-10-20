# toolbar layout A: icon tools + undo/more, colours + size cycle + paper tray; notes page too
import asyncio,sys
from playwright.async_api import async_playwright
from fontroute import setup
OUT=sys.argv[1] if len(sys.argv)>1 else '.'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); errs=[]
        for W,H,tag,loc in [(390,844,'phone','en-GB'),(1280,900,'desk','en-GB'),(390,844,'phone-uk','uk-UA')]:
            c=await b.new_context(viewport={'width':W,'height':H},has_touch=W<500,locale=loc,service_workers='block'); await setup(c)
            pg=await c.new_page(); pg.on('pageerror',lambda e:errs.append(str(e)))
            await pg.goto('http://localhost:8765/'); await pg.wait_for_timeout(2500)
            while await pg.is_visible('#tourModal'): await pg.click('#tourNext'); await pg.wait_for_timeout(40)
            await pg.click('.day >> nth=12'); await pg.wait_for_timeout(500)
            t=pg.locator('#tools'); sec=pg.locator('#tools').locator('..')
            rows=await pg.evaluate("[...document.querySelectorAll('#tools .trow')].map(r=>Math.round(r.getBoundingClientRect().height))")
            print(tag,'row heights',rows)
            await sec.screenshot(path=f'{OUT}/{tag}-1.png')
            await pg.click('#tools [aria-label="Medium"], #tools [aria-label="Середній"]'); 
            sz=await pg.evaluate("document.querySelectorAll('#tools .trow')[1].querySelector('.ib').getAttribute('aria-label')"); print(tag,'size after tap:',sz)
            await pg.click('#tools .trow >> nth=1 >> .ib >> nth=1'); await pg.wait_for_timeout(200)
            print(tag,'paper tray buttons:',await pg.locator('#tools .tpop .pp').count())
            await sec.screenshot(path=f'{OUT}/{tag}-2-paper.png')
            await pg.click('#tools .tpop .pp >> nth=0'); await pg.wait_for_timeout(200)
            print(tag,'tray closed after pick:',await pg.locator('#tools .tpop').count()==0)
            await pg.click('#tools .trow >> nth=0 >> .ib >> nth=-1'); await pg.wait_for_timeout(200)
            await sec.screenshot(path=f'{OUT}/{tag}-3-more.png')
            # notes
            await pg.keyboard.press('Escape'); await pg.click('.tab[data-view=notes]'); await pg.wait_for_timeout(300)
            await pg.click('#newNote') if await pg.is_visible('#newNote') else await pg.click('.notes-head .btn >> nth=0')
            await pg.wait_for_timeout(400); await pg.click('#ndDraw'); await pg.wait_for_timeout(200)
            await pg.locator('#noteTools').screenshot(path=f'{OUT}/{tag}-4-notes.png')
            await pg.click('#ndPaper .ib'); await pg.wait_for_timeout(200)
            print(tag,'note paper tray:',await pg.locator('#ndPaperTray .pp').count(),await pg.get_attribute('#ndPaperTray .pp >> nth=0','aria-label'))
            await pg.click('#ndPaperTray .pp >> nth=3'); await pg.wait_for_timeout(200)
            print(tag,'paid paper toast:',await pg.text_content('#toast'))
            await pg.evaluate("S.meta.supporter=1") if False else None
            await pg.keyboard.press('Escape'); await pg.wait_for_timeout(300)
            await c.close()
        print('errors',errs); await b.close()
asyncio.run(main())
