import asyncio
from playwright.async_api import async_playwright
from fontroute import setup
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); errs=[]
        for skin in ['candy','rose']:
            c=await b.new_context(viewport={'width':1280,'height':900},locale='en-GB',service_workers='block',accept_downloads=True); await setup(c)
            pg=await c.new_page(); pg.on('pageerror',lambda e:errs.append(str(e)))
            await pg.goto('http://localhost:8765/#supporter-preview'); await pg.wait_for_timeout(2800)
            while await pg.is_visible('#tourModal'): await pg.click('#tourNext'); await pg.wait_for_timeout(100)
            if skin=='rose':
                await pg.click('.tab[data-view=settings]'); await pg.click('.skin:has-text("Midnight rose")'); await pg.click('#setClose'); await pg.wait_for_timeout(300)
            await pg.click('#revealOpen' if await pg.is_visible('#revealOpen') else '#revealBtn'); await pg.wait_for_timeout(500)
            async with pg.expect_download() as dl: await pg.click('#rvSave')
            await (await dl.value).save_as(f'shots5/month-{skin}.png')
            await pg.keyboard.press('Escape'); await pg.wait_for_timeout(200)
            await pg.click('.tab[data-view=year]'); await pg.wait_for_timeout(300)
            async with pg.expect_download() as dl: await pg.click('#posterBtn')
            await (await dl.value).save_as(f'shots5/year-{skin}.png')
            await c.close()
        print('ERR',errs); await b.close()
asyncio.run(main())
