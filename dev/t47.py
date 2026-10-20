# floating sticker: tap to place, pinch/twist with two fingers, ✓ to stamp; mouse handle on desktop; notes page too
import asyncio,sys
from playwright.async_api import async_playwright
from fontroute import setup
OUT=sys.argv[1] if len(sys.argv)>1 else '.'
async def touch(cdp,typ,pts):
    await cdp.send('Input.dispatchTouchEvent',{'type':typ,'touchPoints':[{'x':x,'y':y,'id':i} for i,(x,y) in pts]})
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); errs=[]
        c=await b.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True,locale='en-GB',service_workers='block'); await setup(c)
        pg=await c.new_page(); pg.on('pageerror',lambda e:errs.append(str(e))); cdp=await c.new_cdp_session(pg)
        await pg.goto('http://localhost:8765/'); await pg.wait_for_timeout(2500)
        while await pg.is_visible('#tourModal'): await pg.click('#tourNext'); await pg.wait_for_timeout(40)
        await pg.tap('.day >> nth=12'); await pg.wait_for_timeout(500)
        await pg.tap('.qs >> nth=0'); await pg.wait_for_timeout(200)
        await pg.locator('#pad').scroll_into_view_if_needed(); bx=await pg.locator('#pad').bounding_box()
        cx,cy=bx['x']+bx['width']*.5,bx['y']+bx['height']*.5
        blank=await pg.evaluate("document.getElementById('pad').toDataURL().length")
        await touch(cdp,'touchStart',[(0,(cx,cy))]); await touch(cdp,'touchEnd',[]); await pg.wait_for_timeout(300)
        r0=await pg.evaluate("(()=>{const e=document.querySelector('.card .stkf');return e&&!e.hidden?[e.style.width,e.style.transform]:null})()")
        print('placed floating:',r0,'| canvas unchanged:',await pg.evaluate("document.getElementById('pad').toDataURL().length")==blank)
        await pg.screenshot(path=f'{OUT}/s1-placed.png')
        # pinch: finger 1 on sticker, finger 2 off it; spread and twist
        await touch(cdp,'touchStart',[(0,(cx,cy))]); await pg.wait_for_timeout(50)
        await touch(cdp,'touchStart',[(0,(cx,cy)),(1,(cx+40,cy))]); await pg.wait_for_timeout(50)
        for t in range(1,11):
            await touch(cdp,'touchMove',[(0,(cx-6*t,cy-3*t)),(1,(cx+40+6*t,cy+9*t))]); await pg.wait_for_timeout(16)
        await touch(cdp,'touchEnd',[(0,(cx-60,cy-30))]); await touch(cdp,'touchEnd',[]); await pg.wait_for_timeout(300)
        r1=await pg.evaluate("(()=>{const e=document.querySelector('.card .stkf');return [e.style.width,e.style.transform,e.hidden]})()")
        print('after pinch:',r1); await pg.screenshot(path=f'{OUT}/s2-pinched.png')
        await pg.tap('.card .stkf-b.ok'); await pg.wait_for_timeout(400)
        print('stamped:',await pg.evaluate("document.getElementById('pad').toDataURL().length")!=blank,'| floater hidden:',await pg.evaluate("document.querySelector('.card .stkf').hidden"))
        await pg.screenshot(path=f'{OUT}/s3-stamped.png')
        # two-finger tap still undoes when no sticker is floating
        await touch(cdp,'touchStart',[(0,(cx-80,cy))]); await touch(cdp,'touchStart',[(0,(cx-80,cy)),(1,(cx+80,cy))]); await touch(cdp,'touchEnd',[(0,(cx-80,cy))]); await touch(cdp,'touchEnd',[]); await pg.wait_for_timeout(300)
        print('two-finger undo removed it:',await pg.evaluate("document.getElementById('pad').toDataURL().length")==blank)
        await c.close()
        # desktop: mouse handle rotate/scale
        c=await b.new_context(viewport={'width':1280,'height':900},locale='en-GB',service_workers='block'); await setup(c)
        pg=await c.new_page(); pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('http://localhost:8765/'); await pg.wait_for_timeout(2500)
        while await pg.is_visible('#tourModal'): await pg.click('#tourNext'); await pg.wait_for_timeout(40)
        await pg.click('.qs >> nth=1'); bx=await pg.locator('#pad').bounding_box()
        await pg.mouse.click(bx['x']+bx['width']*.4,bx['y']+bx['height']*.5); await pg.wait_for_timeout(200)
        hb=await pg.locator('.card .stkf-h').bounding_box(); hx,hy=hb['x']+hb['width']/2,hb['y']+hb['height']/2
        await pg.mouse.move(hx,hy); await pg.mouse.down(); await pg.mouse.move(hx+60,hy-40,steps=8); await pg.mouse.up(); await pg.wait_for_timeout(200)
        print('desktop handle:',await pg.evaluate("document.querySelector('.card .stkf').style.transform"))
        await pg.screenshot(path=f'{OUT}/s4-desktop.png',clip={'x':bx['x']-20,'y':bx['y']-60,'width':bx['width']+40,'height':bx['height']+80})
        await pg.click('#tools [aria-label=Pen]'); await pg.wait_for_timeout(200)
        print('tool switch stamps:',await pg.evaluate("document.querySelector('.card .stkf').hidden"))
        # notes page
        await pg.click('.tab[data-view=notes]'); await pg.click('#newNote'); await pg.wait_for_timeout(400)
        await pg.click('#ndDraw'); await pg.click('#noteTools [aria-label=Stickers]'); await pg.wait_for_timeout(200)
        nb=await pg.locator('#ndPage').bounding_box(); await pg.mouse.click(nb['x']+200,nb['y']+150); await pg.wait_for_timeout(200)
        print('notes floating:',await pg.evaluate("(()=>{const e=document.querySelector('#ndPage .stkf');return e&&!e.hidden})()"))
        await pg.screenshot(path=f'{OUT}/s5-notes.png',clip={'x':nb['x']-10,'y':nb['y']-10,'width':min(nb['width']+20,700),'height':360})
        await pg.click('#ndPage .stkf-b.ok'); await pg.wait_for_timeout(200)
        print('notes stamped, floater hidden:',await pg.evaluate("document.querySelector('#ndPage .stkf').hidden"))
        print('ERR',errs); await b.close()
asyncio.run(main())
