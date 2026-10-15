import asyncio
from playwright.async_api import async_playwright
FIND="new Promise(r=>{const o=indexedDB.open('doodle-days',1);o.onsuccess=()=>{const g=o.result.transaction('kv').objectStore('kv').getAll();g.onsuccess=()=>r(g.result.some(v=>v&&v.note==='quick thought'))}})"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); c=await b.new_context(viewport={'width':1280,'height':860},service_workers='block'); pg=await c.new_page()
        await pg.goto('http://localhost:8765/'); await pg.wait_for_timeout(2600)
        while await pg.is_visible('#tourModal'): await pg.click('#tourNext'); await pg.wait_for_timeout(120)
        await pg.click('.day >> nth=15'); await pg.wait_for_timeout(300)
        await pg.fill('#note','quick thought')
        print('before flush saved:',await pg.evaluate(FIND))
        await pg.evaluate("dispatchEvent(new Event('pagehide'))"); await pg.wait_for_timeout(50)
        print('after flush saved:',await pg.evaluate(FIND))
        await b.close()
asyncio.run(main())
