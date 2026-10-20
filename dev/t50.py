# Halloween: Spooky season pack in the tray, a sticker placed, Halloween paper on a day + a note, saved image keeps the paper
import asyncio,sys
from playwright.async_api import async_playwright
from fontroute import setup
OUT=sys.argv[1] if len(sys.argv)>1 else '.'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); errs=[]
        c=await b.new_context(viewport={'width':390,'height':844},has_touch=True,locale='en-GB',service_workers='block'); await setup(c)
        pg=await c.new_page(); pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else None)
        await pg.goto('http://localhost:8765/#supporter-preview'); await pg.wait_for_timeout(2500)
        while await pg.is_visible('#tourModal'): await pg.click('#tourNext'); await pg.wait_for_timeout(40)
        await pg.click('.day >> nth=12'); await pg.wait_for_timeout(400)
        await pg.click('#tools [aria-label=Paper]'); await pg.click('#tools .tpop .pp >> nth=4'); await pg.wait_for_timeout(200)
        await pg.click('#tools [aria-label=Stickers]'); await pg.click('.packtabs .chipbtn >> nth=1'); await pg.wait_for_timeout(300)
        print('spooky stickers in tray:',await pg.locator('#tray .stk').count())
        await pg.locator('#tray').screenshot(path=f'{OUT}/tray.png')
        bx=await pg.locator('#pad').bounding_box()
        for k,(fx,fy) in enumerate([(.25,.45),(.55,.35),(.8,.6)]):
            await pg.click(f'#tray .stk >> nth={k}'); await pg.click('#pad',position={'x':bx['width']*fx,'y':bx['height']*fy}); await pg.wait_for_timeout(150)
            await pg.click('.card .stkf-b.ok') ; await pg.wait_for_timeout(150)
        await pg.locator('#tools').locator('..').screenshot(path=f'{OUT}/day.png')
        await pg.click('#shareDay'); await pg.wait_for_timeout(1800); await pg.screenshot(path=f'{OUT}/share.png')
        await pg.keyboard.press('Escape'); await pg.wait_for_timeout(200)
        await pg.keyboard.press('Escape'); await pg.click('.tab[data-view=notes]'); await pg.click('#newNote'); await pg.wait_for_timeout(300)
        await pg.fill('#noteTitle','Halloween party'); await pg.click('#noteText'); await pg.keyboard.type('Costumes\nPumpkin carving\nCandy')
        await pg.click('#ndPaper .ib'); await pg.click('#ndPaperTray .pp >> nth=4'); await pg.wait_for_timeout(300)
        await pg.locator('.notedlg').screenshot(path=f'{OUT}/note.png')
        print('errors',errs); await b.close()
asyncio.run(main())
