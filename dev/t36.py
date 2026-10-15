import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); errs=[]
        c=await b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True,locale='en-GB',service_workers='block')
        pg=await c.new_page(); pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('http://localhost:8765/'); await pg.wait_for_timeout(2600)
        while await pg.is_visible('#tourModal'): await pg.click('#tourNext'); await pg.wait_for_timeout(120)
        print('buttons:',await pg.locator('.tcard .done').all_text_contents())
        await pg.locator('.summary').scroll_into_view_if_needed(); await pg.locator('.tcard >> nth=1').screenshot(path='shots5/mark-done.png')
        await pg.click('.day >> nth=18'); await pg.wait_for_timeout(400)
        await pg.click('#chips .chip-add'); await pg.wait_for_timeout(300)
        print('modal visible over panel:',await pg.is_visible('#trModal'))
        await pg.fill('#trName','Pottery'); await pg.click('#trForm button[type=submit]'); await pg.wait_for_timeout(400)
        print('chip ticked:',await pg.locator('#chips .chip.on:has-text("Pottery")').count())
        await pg.locator('section:has(#chips)').screenshot(path='shots5/day-add-activity.png')
        print('ERR',errs); await b.close()
asyncio.run(main())
