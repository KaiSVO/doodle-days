import asyncio
from playwright.async_api import async_playwright
async def stroke(pg,pts):
    await pg.mouse.move(*pts[0]); await pg.mouse.down()
    for p in pts[1:]: await pg.mouse.move(*p,steps=4)
    await pg.mouse.up(); await pg.wait_for_timeout(150)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); errs=[]
        c=await b.new_context(viewport={'width':1280,'height':900},locale='en-GB',service_workers='block',accept_downloads=True)
        pg=await c.new_page(); pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('http://localhost:8765/'); await pg.wait_for_timeout(2600)
        while await pg.is_visible('#tourModal'): await pg.click('#tourNext'); await pg.wait_for_timeout(120)
        await pg.click('#tools [aria-label=Watercolour]'); await pg.wait_for_timeout(200)
        print('free toast:',await pg.text_content('#toast'))
        await pg.click('#tools [aria-label=Paper]'); await pg.click('#tools .tpop .pp >> nth=1'); await pg.wait_for_timeout(200); print('free paper toast:',await pg.text_content('#toast'))
        await pg.goto('http://localhost:8765/#supporter-preview'); await pg.reload(); await pg.wait_for_timeout(2600)
        await pg.click('.day >> nth=20'); await pg.wait_for_timeout(400)
        bx=await pg.locator('#pad').bounding_box(); X,Y,W,H=bx['x'],bx['y'],bx['width'],bx['height']
        await pg.click('#tools [aria-label=Paper]'); await pg.click('#tools .tpop .pp >> nth=1'); await pg.wait_for_timeout(200)
        await pg.click('#tools [aria-label=Watercolour]')
        await pg.click('#tools .t1 ~ .trow .ib >> nth=0')
        await stroke(pg,[(X+60,Y+80),(X+200,Y+120),(X+330,Y+90),(X+380,Y+160)])
        await pg.evaluate("[...document.querySelectorAll('#tools button')].find(b=>b.getAttribute('style')&&b.getAttribute('style').includes('3A7BD5'))?.click()")
        await stroke(pg,[(X+80,Y+200),(X+250,Y+230),(X+350,Y+220)])
        await pg.click('#tools [aria-label=Crayon]'); await pg.click('#tools .t1 ~ .trow .ib >> nth=0')
        await stroke(pg,[(X+60,Y+250),(X+180,Y+280),(X+300,Y+255),(X+390,Y+275)])
        await pg.click('#tools [aria-label=Pen]'); await stroke(pg,[(X+40,Y+40),(X+120,Y+40)])
        await pg.wait_for_timeout(500); await pg.locator('#pad').locator('..').screenshot(path='shots5/brush-kraft.png')
        for i,name in [(2,'grid'),(3,'dots')]:
            await pg.click('#tools [aria-label=Paper]'); await pg.click(f'#tools .tpop .pp >> nth={i}'); await pg.wait_for_timeout(300); await pg.locator('#pad').locator('..').screenshot(path=f'shots5/brush-{name}.png')
        await pg.click('#tools [aria-label=Paper]'); await pg.click('#tools .tpop .pp >> nth=1'); await pg.wait_for_timeout(500)
        await pg.locator('.day >> nth=20').screenshot(path='shots5/thumb-kraft.png')
        async with pg.expect_download() as dl: await pg.click('#shareDay')
        await (await dl.value).save_as('shots5/share-kraft.png')
        await pg.click('.tab[data-view=year]'); await pg.wait_for_timeout(300)
        async with pg.expect_download() as dl: await pg.click('#posterBtn')
        await (await dl.value).save_as('shots5/poster.png')
        print('ERR',errs); await b.close()
asyncio.run(main())
