# note paper with Supporter preview: pick dots, type, close, card shows paper, reopen keeps it
import asyncio,sys
from playwright.async_api import async_playwright
from fontroute import setup
OUT=sys.argv[1] if len(sys.argv)>1 else '.'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); errs=[]
        c=await b.new_context(viewport={'width':390,'height':844},has_touch=True,locale='en-GB',service_workers='block'); await setup(c)
        pg=await c.new_page(); pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('http://localhost:8765/#supporter-preview'); await pg.wait_for_timeout(2500)
        while await pg.is_visible('#tourModal'): await pg.click('#tourNext'); await pg.wait_for_timeout(40)
        await pg.click('.tab[data-view=notes]'); await pg.click('#newNote'); await pg.wait_for_timeout(300)
        await pg.fill('#noteTitle','Shopping list'); await pg.click('#noteText'); await pg.keyboard.type('Gouache\nBrushes\nKraft paper')
        await pg.click('#ndPaper .ib'); await pg.wait_for_timeout(200); await pg.locator('.notedlg').screenshot(path=f'{OUT}/note-type-tray.png'); await pg.click('#ndPaperTray .pp >> nth=2'); await pg.wait_for_timeout(300)
        print('page bg:',await pg.evaluate("getComputedStyle(document.getElementById('ndPage')).backgroundImage.slice(0,40)"))
        await pg.locator('.notedlg').screenshot(path=f'{OUT}/note-grid.png')
        await pg.click('#noteDone'); await pg.wait_for_timeout(500)
        print('card style:',(await pg.get_attribute('.ncard >> nth=0','style') or '')[:60])
        await pg.locator('#noteGrid').screenshot(path=f'{OUT}/note-cards.png')
        await pg.click('.ncard >> nth=0'); await pg.wait_for_timeout(400)
        print('reopened bg kept:','linear-gradient(rgba(70' in await pg.evaluate("document.getElementById('ndPage').style.backgroundImage"))
        print('errors',errs); await b.close()
asyncio.run(main())
