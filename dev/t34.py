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
        await pg.goto('http://localhost:8765/'); await skip(pg)
        await pg.click('.tab[data-view=notes]'); await pg.click('#newNote'); await pg.wait_for_timeout(300)
        await pg.fill('#noteTitle','Market day')
        await pg.click('#noteText'); kb=pg.keyboard
        await kb.type('# To pack'); await kb.press('Enter')
        await kb.type('[] Mugs'); await kb.press('Enter'); await kb.type('Price tags'); await kb.press('Enter'); await kb.press('Enter')
        await kb.type('Remember: '); await pg.click('#noteBar .rtb-b'); await kb.type('bring change'); await pg.click('#noteBar .rtb-b'); await kb.press('Enter')
        await kb.type('- coffee'); await kb.press('Enter'); await kb.type('snacks')
        await pg.wait_for_timeout(200)
        print('html:',(await pg.inner_html('#noteText'))[:400])
        await pg.click('#noteText ul.checks li >> nth=0',position={'x':8,'y':10}); await pg.wait_for_timeout(100)
        await pg.click('#ndDraw'); await pg.wait_for_timeout(200)
        bx=await pg.locator('#ndPage').bounding_box()
        await pg.mouse.move(bx['x']+200,bx['y']+30); await pg.mouse.down(); await pg.mouse.move(bx['x']+320,bx['y']+90,steps=12); await pg.mouse.up()
        await pg.mouse.move(bx['x']+60,bx['y']+200); await pg.mouse.down(); await pg.mouse.move(bx['x']+300,bx['y']+215,steps=12); await pg.mouse.up()
        await pg.wait_for_timeout(300); await pg.locator('.notedlg').screenshot(path='shots5/note-rich.png')
        await pg.click('#noteDone'); await pg.wait_for_timeout(400)
        await pg.screenshot(path='shots5/notes-rich-list.png')
        await pg.reload(); await skip(pg); await pg.click('.tab[data-view=notes]'); await pg.click('.ncard >> nth=0'); await pg.wait_for_timeout(600)
        print('reloaded html has checks/h2/b:',await pg.evaluate("(()=>{const e=document.getElementById('noteText');return [!!e.querySelector('ul.checks li[data-done]'),!!e.querySelector('h2'),!!e.querySelector('b'),!!e.querySelector('ul:not(.checks) li')]})()"))
        print('doodle kept:',await pg.evaluate("(()=>{const c=document.getElementById('notePad'),d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;let n=0;for(let i=3;i<d.length;i+=4)if(d[i])n++;return n})()"))
        await pg.click('#noteDone')
        # day note
        await pg.click('.tab[data-view=month]'); await pg.click('.day >> nth=16'); await pg.wait_for_timeout(400)
        await pg.click('#note'); await pg.click('#dayNoteBar .rtb-h3'); await kb.type('Studio day'); await kb.press('Enter'); await pg.click('#dayNoteBar .rtb-ol'); await kb.type('Glaze bowls'); await kb.press('Enter'); await kb.type('Photograph mugs')
        await pg.wait_for_timeout(700); await pg.locator('section:has(#note)').screenshot(path='shots5/daynote-rich.png')
        await pg.click('#closePanel'); await pg.wait_for_timeout(500)
        await pg.reload(); await skip(pg); await pg.click('.day >> nth=16'); await pg.wait_for_timeout(500)
        print('day note html:',(await pg.inner_html('#note'))[:200])
        print('ERR',errs); await b.close()
asyncio.run(main())
