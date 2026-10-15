import asyncio
from playwright.async_api import async_playwright
from fontroute import setup
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        c=await b.new_context(viewport={'width':390,'height':760},device_scale_factor=3,is_mobile=True,has_touch=True,locale='en-GB',service_workers='block'); await setup(c)
        pg=await c.new_page()
        await pg.goto('http://localhost:8765/#supporter-preview'); await pg.wait_for_timeout(2600)
        while await pg.is_visible('#tourModal'): await pg.click('#tourNext'); await pg.wait_for_timeout(120)
        await pg.add_style_tag(content='#banner,#revealBanner,#backupBanner,#rateBanner,.toast{display:none!important}')
        await pg.wait_for_timeout(300)
        await pg.screenshot(path='store/raw1-month.png')
        # day with doodle + stickers
        await pg.click('.day >> nth=9'); await pg.wait_for_timeout(500)
        bx=await pg.locator('#pad').bounding_box()
        await pg.click('.qs >> nth=0'); await pg.tap('#pad',position={'x':bx['width']*.82,'y':bx['height']*.2})
        await pg.click('.qs >> nth=1'); await pg.tap('#pad',position={'x':bx['width']*.18,'y':bx['height']*.75})
        await pg.wait_for_timeout(600); await pg.evaluate("document.getElementById('cheer').hidden=true")
        await pg.screenshot(path='store/raw2-day.png')
        await pg.click('#closePanel'); await pg.wait_for_timeout(300)
        await pg.locator('.summary').scroll_into_view_if_needed(); await pg.evaluate("scrollBy(0,-60)"); await pg.wait_for_timeout(300)
        await pg.screenshot(path='store/raw3-activities.png')
        await pg.click('.tab[data-view=week]'); await pg.wait_for_timeout(300); await pg.evaluate("scrollTo(0,0)")
        await pg.screenshot(path='store/raw4-week.png')
        await pg.click('.tab[data-view=year]'); await pg.wait_for_timeout(500); await pg.evaluate("scrollTo(0,document.querySelector('.ym[data-m=\"6\"]').offsetTop-90)"); await pg.wait_for_timeout(300)
        await pg.screenshot(path='store/raw5-year.png')
        await pg.evaluate("document.documentElement.dataset.skin='rose';document.documentElement.dataset.theme='dark'")
        await pg.click('.tab[data-view=month]'); await pg.wait_for_timeout(300); await pg.evaluate("scrollTo(0,0)"); await pg.wait_for_timeout(300)
        await pg.screenshot(path='store/raw6-rose.png')
        await pg.evaluate("document.documentElement.dataset.skin='pixel'")
        await pg.wait_for_timeout(300); await pg.screenshot(path='store/raw7-pixel.png')
        await b.close()
asyncio.run(main())
