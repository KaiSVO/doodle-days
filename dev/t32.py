import asyncio
from playwright.async_api import async_playwright
IDB="""(k)=>new Promise(r=>{const o=indexedDB.open('doodle-days',1);o.onsuccess=()=>{const g=o.result.transaction('kv').objectStore('kv').get(k);g.onsuccess=()=>r(g.result||null);};})"""
async def skip(pg):
    await pg.wait_for_timeout(2600)
    while await pg.is_visible('#tourModal'): await pg.click('#tourNext'); await pg.wait_for_timeout(120)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); errs=[]
        c=await b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True,locale='en-GB',service_workers='block')
        pg=await c.new_page(); pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('http://localhost:8765/'); await skip(pg)
        # notes
        await pg.click('.tab[data-view=notes]'); await pg.wait_for_timeout(300); await pg.screenshot(path='shots5/notes-empty.png')
        await pg.click('#newNote'); await pg.wait_for_timeout(300)
        await pg.fill('#noteTitle','Market stall ideas'); await pg.click('#noteText'); await pg.keyboard.type('Bring the blue mugs, price tags, tablecloth with daisies')
        await pg.wait_for_timeout(500); await pg.screenshot(path='shots5/note-editor.png')
        await pg.click('#noteDone'); await pg.wait_for_timeout(300)
        for t,x in [('Shopping list','yarn, glue, 2 canvases'),('Gift ideas','Mum: knitted scarf')]:
            await pg.click('#newNote'); await pg.wait_for_timeout(200); await pg.fill('#noteTitle',t); await pg.click('#noteText'); await pg.keyboard.type(x); await pg.click('#noteDone'); await pg.wait_for_timeout(200)
        await pg.screenshot(path='shots5/notes-list.png')
        print('cards:',await pg.locator('.ncard').count())
        await pg.click('.ncard:has-text("Gift ideas")'); await pg.wait_for_timeout(300); await pg.click('#noteArch'); await pg.wait_for_timeout(300)
        print('after archive cards:',await pg.locator('.ncard').count(),'toggle:',await pg.text_content('#noteArchTgl'))
        await pg.click('.ncard:has-text("Shopping list")'); await pg.click('#noteDel'); await pg.click('#noteDel'); await pg.wait_for_timeout(300)
        print('after delete:',await pg.locator('.ncard').count(),'toast:',await pg.text_content('#toast'))
        await pg.click('#toast button'); await pg.wait_for_timeout(300); print('after undo:',await pg.locator('.ncard').count())
        print('stored notes:',await pg.evaluate("new Promise(r=>{const o=indexedDB.open('doodle-days',1);o.onsuccess=()=>{const g=o.result.transaction('kv').objectStore('kv').getAllKeys();g.onsuccess=()=>r(g.result.filter(k=>k.startsWith('n:')).length)}})"))
        # search: recent + filters
        await pg.click('.tab[data-view=month]'); await pg.click('#searchBtn'); await pg.wait_for_timeout(400)
        print('recent rows:',await pg.locator('#gsList .item').count()); await pg.screenshot(path='shots5/search-recent.png')
        await pg.click('#gsFiltBtn'); await pg.wait_for_timeout(200)
        await pg.click('#gfTypes .chip:has-text("Notes")'); await pg.click('#gfTypes .chip:has-text("Plans")'); await pg.click('#gfTypes .chip:has-text("Day colours")')
        await pg.select_option('#gfWhen','past'); await pg.wait_for_timeout(200)
        await pg.select_option('#gfAct',label='Knitting'); await pg.wait_for_timeout(400)
        print('filtered count:',await pg.text_content('#gsCount'),'glow:',await pg.locator('.day.glow').count())
        await pg.screenshot(path='shots5/search-filters.png',full_page=False)
        await pg.select_option('#gfWhen','custom'); await pg.fill('#gfFrom','2026-10-01'); await pg.fill('#gfTo','2026-10-03'); await pg.locator('#gfTo').dispatch_event('change'); await pg.locator('#gfFrom').dispatch_event('change'); await pg.wait_for_timeout(300)
        print('custom count:',await pg.text_content('#gsCount'))
        await pg.click('#gfReset'); await pg.wait_for_timeout(200)
        await pg.fill('#gq','tablecloth'); await pg.wait_for_timeout(500)
        print('note search:',await pg.text_content('#gsCount'),'| notes section:',await pg.locator('#gsList .item:has-text("Market stall")').count())
        await pg.click('#gsList .item:has-text("Market stall")'); await pg.wait_for_timeout(400); print('opened note:',await pg.is_visible('#noteModal'))
        await pg.click('#noteDone'); 
        # flush test
        await pg.click('.day >> nth=15'); await pg.wait_for_timeout(300)
        await pg.fill('#note','quick thought'); await pg.evaluate("dispatchEvent(new Event('pagehide'))")
        await pg.wait_for_timeout(30)
        k=await pg.evaluate("(()=>{const e=document.querySelectorAll('.day:not(.out)');return null})()")
        print('ERR',errs); await c.close()
        # iOS Safari banner
        c=await b.new_context(viewport={'width':390,'height':844},user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1',is_mobile=True,has_touch=True,locale='en-GB',service_workers='block')
        pg=await c.new_page(); pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('http://localhost:8765/'); await skip(pg)
        print('ios banner:',await pg.is_visible('#iosBanner')); await pg.screenshot(path='shots5/ios-banner.png')
        print('ERR',errs); await b.close()
asyncio.run(main())
