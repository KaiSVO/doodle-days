import asyncio,sys
from playwright.async_api import async_playwright
async def run(p,loc,vw,tag):
    b=await p.chromium.launch(); errs=[]
    mob=vw[0]<700
    c=await b.new_context(viewport={'width':vw[0],'height':vw[1]},device_scale_factor=2 if mob else 1,is_mobile=mob,has_touch=mob,locale=loc)
    pg=await c.new_page(); pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.goto('http://localhost:8765/'); await pg.wait_for_timeout(2600)
    while await pg.is_visible('#tourModal'): await pg.click('#tourNext'); await pg.wait_for_timeout(120)
    await pg.screenshot(path=f'shots4/s-{tag}-0.png')
    await pg.click('#searchBtn'); await pg.wait_for_timeout(200)
    await pg.keyboard.type('pottery' if loc.startswith('en') else 'кераміки'); await pg.wait_for_timeout(400)
    print(tag,'count:',await pg.text_content('#gsCount'),'glow month:',await pg.locator('.day.glow').count(),'list items:',await pg.locator('#gsList .item').count())
    await pg.screenshot(path=f'shots4/s-{tag}-1.png')
    await pg.click('#gsList .item >> nth=0'); await pg.wait_for_timeout(600)
    await pg.screenshot(path=f'shots4/s-{tag}-2.png')
    if mob: await pg.click('#closePanel'); await pg.wait_for_timeout(300)
    await pg.click('#gsNext'); await pg.wait_for_timeout(500); await pg.click('#gsNext'); await pg.wait_for_timeout(500)
    print(tag,'sel after next x2:',await pg.evaluate("document.querySelector('.day.sel')&&document.querySelector('.day.sel').getAttribute('aria-label')"),'panel open:',await pg.evaluate("document.getElementById('panel').classList.contains('open')"))
    await pg.click('.tab[data-view=year]'); await pg.wait_for_timeout(500)
    print(tag,'glow year:',await pg.locator('.px.glow').count())
    await pg.screenshot(path=f'shots4/s-{tag}-year.png')
    await pg.click('.tab[data-view=week]'); await pg.wait_for_timeout(300)
    print(tag,'glow week:',await pg.locator('.wday.glow').count())
    await pg.screenshot(path=f'shots4/s-{tag}-week.png')
    await pg.click('.tab[data-view=list]'); await pg.wait_for_timeout(400)
    print(tag,'plans view, bar still open:',await pg.is_visible('#gsearch'),'searching cls:',await pg.evaluate("document.body.classList.contains('searching')"))
    await pg.click('.tab[data-view=month]'); await pg.wait_for_timeout(200)
    await pg.keyboard.press('Control+k'); await pg.wait_for_timeout(200); await pg.keyboard.type('zzzz'); await pg.wait_for_timeout(400)
    print(tag,'none:',await pg.text_content('#gsCount'),'dimmed:',await pg.evaluate("document.body.classList.contains('searching')"))
    await pg.keyboard.press('Escape'); await pg.wait_for_timeout(200)
    print(tag,'closed:',await pg.is_hidden('#gsearch'),'ERR',errs)
    await b.close()
async def main():
    async with async_playwright() as p:
        await run(p,'uk-UA',(390,844),'uk')
asyncio.run(main())
