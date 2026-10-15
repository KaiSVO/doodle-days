import asyncio
from playwright.async_api import async_playwright
from fontroute import setup
async def skip(pg):
    await pg.wait_for_timeout(2600)
    while await pg.is_visible('#tourModal'): await pg.click('#tourNext'); await pg.wait_for_timeout(120)
HIDE='#banner,#revealBanner,#backupBanner,#rateBanner,#iosBanner,.toast,.cheer{display:none!important}'
async def stroke(pg,pts):
    await pg.mouse.move(*pts[0]); await pg.mouse.down()
    for p in pts[1:]: await pg.mouse.move(*p,steps=6)
    await pg.mouse.up(); await pg.wait_for_timeout(120)
async def ink(pg,hexv):
    r,g,bb=int(hexv[1:3],16),int(hexv[3:5],16),int(hexv[5:7],16)
    ok=await pg.evaluate(f"(()=>{{const b=[...document.querySelectorAll('#tools button')].find(b=>getComputedStyle(b).backgroundColor==='rgb({r}, {g}, {bb})');if(b){{b.click();return true}}return false}})()")
    if not ok: print('ink not found',hexv)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); errs=[]
        c=await b.new_context(viewport={'width':390,'height':780},device_scale_factor=2,is_mobile=True,has_touch=True,locale='en-GB',service_workers='block',accept_downloads=True); await setup(c)
        pg=await c.new_page(); pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('http://localhost:8765/#supporter-preview'); await skip(pg); await pg.add_style_tag(content=HIDE)
        # brushes & papers
        for n,paper in [(13,1),(14,2),(15,3)]:
            await pg.click(f'.day >> nth={n}'); await pg.wait_for_timeout(400)
            await pg.click('.tool:has-text("Pen")'); await pg.click(f'#paperPick .pp >> nth={paper}'); await pg.wait_for_timeout(200)
            bx=await pg.locator('#pad').bounding_box(); X,Y,W,H=bx['x'],bx['y'],bx['width'],bx['height']
            await ink(pg,'#3A7BD5'); await pg.click('.tool:has-text("Watercolour")'); await pg.click('#tools .size >> nth=2'); await stroke(pg,[(X+W*.08,Y+H*.25),(X+W*.3,Y+H*.18),(X+W*.55,Y+H*.3),(X+W*.85,Y+H*.2)])
            await ink(pg,'#D9577A'); await pg.click('.tool:has-text("Watercolour")'); await stroke(pg,[(X+W*.1,Y+H*.45),(X+W*.4,Y+H*.55),(X+W*.7,Y+H*.42),(X+W*.9,Y+H*.5)])
            await ink(pg,'#E9A23B'); await pg.click('.tool:has-text("Watercolour")'); await stroke(pg,[(X+W*.15,Y+H*.35),(X+W*.45,Y+H*.4)])
            await ink(pg,'#3E9B6E'); await pg.click('.tool:has-text("Crayon")'); await pg.click('#tools .size >> nth=1'); await stroke(pg,[(X+W*.08,Y+H*.75),(X+W*.3,Y+H*.68),(X+W*.5,Y+H*.8),(X+W*.75,Y+H*.7),(X+W*.92,Y+H*.78)])
            await ink(pg,'#8A5CC7'); await pg.click('.tool:has-text("Crayon")'); await stroke(pg,[(X+W*.12,Y+H*.88),(X+W*.5,Y+H*.9),(X+W*.85,Y+H*.86)])
            await pg.wait_for_timeout(400)
            await pg.locator('#pad').locator('..').screenshot(path=f'sup/brush-{paper}.png')
            if n==13: await pg.locator('#tools').screenshot(path='sup/tools.png'); await pg.locator('.doodle-head').screenshot(path='sup/paperpick.png')
            await pg.click('#closePanel'); await pg.wait_for_timeout(200)
        # poster
        await pg.set_viewport_size({'width':1280,'height':900})
        c2=pg
        await pg.click('.tab[data-view=year]'); await pg.wait_for_timeout(300)
        async with pg.expect_download() as dl: await pg.click('#posterBtn')
        await (await dl.value).save_as('sup/poster.png')
        print('ERR',errs); await b.close()
asyncio.run(main())
