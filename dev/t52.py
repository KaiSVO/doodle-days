# note placeholder "Write something…" hides once the page has a drawing, comes back after undo, stays hidden on reopen
import asyncio,sys
from playwright.async_api import async_playwright
from fontroute import setup
OUT=sys.argv[1] if len(sys.argv)>1 else '.'
PH="getComputedStyle(document.getElementById('noteText'),'::before').content"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); errs=[]
        c=await b.new_context(viewport={'width':390,'height':844},has_touch=True,locale='en-GB',service_workers='block'); await setup(c)
        pg=await c.new_page(); pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('http://localhost:8765/'); await pg.wait_for_timeout(2500)
        while await pg.is_visible('#tourModal'): await pg.click('#tourNext'); await pg.wait_for_timeout(60)
        await pg.click('.tab[data-view=notes]'); await pg.click('#newNote'); await pg.wait_for_timeout(300)
        await pg.fill('#noteTitle','Sketch'); print('empty note shows hint:',await pg.evaluate(PH))
        await pg.click('#ndDraw'); bx=await pg.locator('#notePad').bounding_box(); X,Y=bx['x'],bx['y']
        await pg.mouse.move(X+60,Y+120); await pg.mouse.down(); await pg.mouse.move(X+250,Y+160,steps=10); await pg.mouse.up(); await pg.wait_for_timeout(200)
        print('after drawing:',await pg.evaluate(PH))
        await pg.locator('.notedlg').screenshot(path=f'{OUT}/note-drawn.png')
        await pg.click('#noteTools [aria-label=Undo]'); await pg.wait_for_timeout(200); print('after undo:',await pg.evaluate(PH))
        await pg.mouse.move(X+60,Y+120); await pg.mouse.down(); await pg.mouse.move(X+250,Y+160,steps=10); await pg.mouse.up(); await pg.wait_for_timeout(200)
        await pg.click('#noteDone'); await pg.wait_for_timeout(500); await pg.click('.ncard >> nth=0'); await pg.wait_for_timeout(500)
        print('reopened:',await pg.evaluate(PH))
        print('errors',errs); await b.close()
asyncio.run(main())
