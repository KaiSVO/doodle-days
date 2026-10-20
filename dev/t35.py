import asyncio
from playwright.async_api import async_playwright
async def skip(pg):
    await pg.wait_for_timeout(2600)
    while await pg.is_visible('#tourModal'): await pg.click('#tourNext'); await pg.wait_for_timeout(120)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); errs=[]
        c=await b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True,locale='en-GB',service_workers='block')
        pg=await c.new_page(); pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('http://localhost:8765/#supporter-preview'); await skip(pg)
        await pg.click('.day >> nth=12'); await pg.wait_for_timeout(400)
        await pg.click('#tools [aria-label=Stickers]'); await pg.wait_for_timeout(300)
        await pg.click('#tray .finchip[aria-label="Enamel pin"]'); await pg.wait_for_timeout(400)
        bx=await pg.locator('#pad').bounding_box()
        await pg.tap('#pad',position={'x':bx['width']*.8,'y':bx['height']*.25}); await pg.wait_for_timeout(300)
        await pg.locator('#pad').locator('..').scroll_into_view_if_needed()
        await pg.screenshot(path='shots5/tray-finish.png')
        await pg.locator('#tray').screenshot(path='shots5/tray-finish-only.png')
        await pg.click('#closePanel'); await pg.wait_for_timeout(200)
        # notes stickers
        await pg.click('.tab[data-view=notes]'); await pg.click('#newNote'); await pg.wait_for_timeout(300)
        await pg.fill('#noteTitle','Market stall'); await pg.click('#noteText'); await pg.keyboard.type('Bring the mugs and price tags')
        await pg.click('#ndDraw'); await pg.click('#noteTools [aria-label=Stickers]'); await pg.wait_for_timeout(300)
        await pg.click('#noteTray .packtabs .chipbtn >> nth=2'); await pg.wait_for_timeout(200)
        await pg.click('#noteTray .stk >> nth=1'); await pg.wait_for_timeout(200)
        pb=await pg.locator('#ndPage').bounding_box()
        await pg.mouse.click(pb['x']+pb['width']*.78,pb['y']+60); await pg.wait_for_timeout(200)
        await pg.click('#noteTray .finchip[aria-label="Hand-painted"]'); await pg.wait_for_timeout(300)
        await pg.click('#noteTray .stk >> nth=10'); await pg.mouse.click(pb['x']+pb['width']*.3,pb['y']+170); await pg.wait_for_timeout(300)
        await pg.locator('.notedlg').screenshot(path='shots5/note-stickers.png')
        await pg.click('#noteDone'); await pg.wait_for_timeout(300)
        print('note doodle saved:',await pg.locator('.ncard .nc-pic').count())
        print('ERR',errs); await c.close()
        # free user
        c=await b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,locale='en-GB',service_workers='block'); pg=await c.new_page()
        await pg.goto('http://localhost:8765/'); await skip(pg)
        await pg.click('.day >> nth=12'); await pg.click('#tools [aria-label=Stickers]'); await pg.wait_for_timeout(300)
        await pg.click('#tray .finchip[aria-label="Paper cut-out"]'); await pg.wait_for_timeout(300)
        print('free toast:',await pg.text_content('#toast'))
        await b.close()
asyncio.run(main())
