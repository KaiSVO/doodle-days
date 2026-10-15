import asyncio
from playwright.async_api import async_playwright
from fontroute import setup
async def stroke(pg,X,Y,W,H,k):
    await pg.mouse.move(X+W*.2,Y+H*(.3+k*.05)); await pg.mouse.down()
    for t in range(1,8): await pg.mouse.move(X+W*(.2+t*.08),Y+H*(.3+((t+k)%3)*.15),steps=3)
    await pg.mouse.up()
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); errs=[]
        c=await b.new_context(viewport={'width':1280,'height':900},locale='en-GB',service_workers='block',accept_downloads=True); await setup(c)
        pg=await c.new_page(); pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('http://localhost:8765/#supporter-preview'); await pg.wait_for_timeout(2800)
        while await pg.is_visible('#tourModal'): await pg.click('#tourNext'); await pg.wait_for_timeout(100)
        # add doodles on a few October days so the month look-back has 6
        for n in [10,11,13,14,15,18,19]:
            await pg.click(f'.day >> nth={n}'); await pg.wait_for_timeout(250)
            bx=await pg.locator('#pad').bounding_box(); await stroke(pg,bx['x'],bx['y'],bx['width'],bx['height'],n)
            await pg.wait_for_timeout(250)
        await pg.click('#revealBtn'); await pg.wait_for_timeout(500)
        async with pg.expect_download() as dl: await pg.click('#rvSave')
        await (await dl.value).save_as('shots5/month-full.png')
        await pg.keyboard.press('Escape'); await pg.click('.tab[data-view=year]'); await pg.wait_for_timeout(300)
        async with pg.expect_download() as dl: await pg.click('#posterBtn')
        await (await dl.value).save_as('shots5/year-full.png')
        print('ERR',errs); await b.close()
asyncio.run(main())
