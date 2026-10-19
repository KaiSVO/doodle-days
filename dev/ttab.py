# tablet store screenshots (landscape 16:9) from the live repo build
import asyncio,sys
from playwright.async_api import async_playwright
from fontroute import setup
OUT=sys.argv[1]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        c=await b.new_context(viewport={'width':1280,'height':720},device_scale_factor=2,has_touch=True,locale='en-GB',service_workers='block'); await setup(c)
        pg=await c.new_page()
        await pg.goto('http://localhost:8766/#supporter-preview'); await pg.wait_for_timeout(2600)
        while await pg.is_visible('#tourModal'): await pg.click('#tourNext'); await pg.wait_for_timeout(100)
        await pg.add_style_tag(content='#banner,#revealBanner,#backupBanner,#rateBanner,.toast,.banner{display:none!important}')
        await pg.click('.day >> nth=9'); await pg.wait_for_timeout(500)
        bx=await pg.locator('#pad').bounding_box()
        await pg.click('.qs >> nth=0'); await pg.tap('#pad',position={'x':bx['width']*.82,'y':bx['height']*.22})
        await pg.click('.qs >> nth=1'); await pg.tap('#pad',position={'x':bx['width']*.16,'y':bx['height']*.74})
        await pg.wait_for_timeout(600); await pg.evaluate("const c=document.getElementById('cheer');if(c)c.hidden=true")
        await pg.evaluate("scrollTo(0,0)"); await pg.screenshot(path=f'{OUT}/r1.png')
        await pg.click('.tab[data-view=week]'); await pg.wait_for_timeout(400); await pg.evaluate("scrollTo(0,0)"); await pg.screenshot(path=f'{OUT}/r2.png')
        await pg.click('.tab[data-view=year]'); await pg.wait_for_timeout(500); await pg.evaluate("scrollTo(0,document.querySelector('.ym[data-m=\"6\"]').offsetTop-90)"); await pg.wait_for_timeout(300); await pg.screenshot(path=f'{OUT}/r3.png')
        await pg.click('.tab[data-view=notes]'); await pg.wait_for_timeout(400)
        try:
            await pg.click('#view-notes .note, #view-notes .nitem, #view-notes button.item >> nth=0',timeout=2000); await pg.wait_for_timeout(600)
        except Exception as e: print('note open failed',e)
        await pg.screenshot(path=f'{OUT}/r4.png'); await pg.keyboard.press('Escape'); await pg.wait_for_timeout(300)
        await pg.evaluate("document.documentElement.dataset.skin='rose';document.documentElement.dataset.theme='dark'")
        await pg.click('.tab[data-view=month]'); await pg.wait_for_timeout(400); await pg.evaluate("scrollTo(0,0)"); await pg.wait_for_timeout(300)
        await pg.screenshot(path=f'{OUT}/r5.png')
        await b.close()
asyncio.run(main())
