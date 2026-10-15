import asyncio
from playwright.async_api import async_playwright
INK="(()=>{const c=document.getElementById('pad'),d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;let n=0;for(let i=3;i<d.length;i+=4)if(d[i])n++;return n;})()"
async def touch(cdp,typ,pts):
    await cdp.send('Input.dispatchTouchEvent',{'type':typ,'touchPoints':[{'x':x,'y':y,'id':i} for i,(x,y) in enumerate(pts)]})
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); errs=[]
        c=await b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True,locale='en-GB',service_workers='block')
        pg=await c.new_page(); pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('http://localhost:8765/#supporter-preview'); await pg.wait_for_timeout(2600)
        while await pg.is_visible('#tourModal'): await pg.click('#tourNext'); await pg.wait_for_timeout(120)
        await pg.click('.day >> nth=8'); await pg.wait_for_timeout(500)
        cdp=await c.new_cdp_session(pg)
        bx=await pg.locator('#pad').bounding_box(); cx,cy=bx['x']+bx['width']/2,bx['y']+bx['height']/2
        print('start ink',await pg.evaluate(INK))
        await touch(cdp,'touchStart',[(cx-80,cy)])
        for k in range(1,12): await touch(cdp,'touchMove',[(cx-80+k*14,cy+k*3)])
        await touch(cdp,'touchEnd',[]); await pg.wait_for_timeout(300)
        a=await pg.evaluate(INK); print('after stroke',a)
        # two-finger tap
        await touch(cdp,'touchStart',[(cx,cy+40)]); await touch(cdp,'touchStart',[(cx,cy+40),(cx+60,cy+40)]); await pg.wait_for_timeout(60)
        await touch(cdp,'touchEnd',[]); await pg.wait_for_timeout(300)
        print('after 2-finger tap',await pg.evaluate(INK))
        # three-finger tap
        await touch(cdp,'touchStart',[(cx,cy)]); await touch(cdp,'touchStart',[(cx,cy),(cx+50,cy)]); await touch(cdp,'touchStart',[(cx,cy),(cx+50,cy),(cx+100,cy)]); await pg.wait_for_timeout(60)
        await touch(cdp,'touchEnd',[]); await pg.wait_for_timeout(300)
        print('after 3-finger tap (redo)',await pg.evaluate(INK))
        # three-finger swipe left
        pts=[(cx,cy),(cx+50,cy),(cx+100,cy)]
        await touch(cdp,'touchStart',pts[:1]); await touch(cdp,'touchStart',pts[:2]); await touch(cdp,'touchStart',pts)
        for k in range(1,8): await touch(cdp,'touchMove',[(x-k*15,y) for x,y in pts])
        await touch(cdp,'touchEnd',[]); await pg.wait_for_timeout(300)
        print('after 3-finger swipe left',await pg.evaluate(INK))
        # sticker finish: painted preview + place
        await pg.click('#closePanel'); await pg.click('.day >> nth=9'); await pg.wait_for_timeout(500)
        await pg.click('.tool:has-text("Stickers")'); await pg.click('#tray .finchip[aria-label="Hand-painted"]'); await pg.wait_for_timeout(300)
        await pg.click('.qs >> nth=0'); await pg.wait_for_timeout(200)
        for (dx,dy) in [(-120,-40),(0,10),(120,-20)]:
            await touch(cdp,'touchStart',[(cx+dx,cy+dy)]); await touch(cdp,'touchEnd',[]); await pg.wait_for_timeout(250)
        await pg.wait_for_timeout(400); await pg.locator('#pad').screenshot(path='shots5/painted-on-page.png')
        await pg.locator('#quick').screenshot(path='shots5/quick-row.png')
        await c.close()
        # desktop ctrl+z
        c=await b.new_context(viewport={'width':1280,'height':860},locale='en-GB',service_workers='block'); pg=await c.new_page(); pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('http://localhost:8765/'); await pg.wait_for_timeout(2600)
        while await pg.is_visible('#tourModal'): await pg.click('#tourNext'); await pg.wait_for_timeout(120)
        bx=await pg.locator('#pad').bounding_box(); cx,cy=bx['x']+bx['width']/2,bx['y']+bx['height']/2
        base=await pg.evaluate(INK)
        await pg.mouse.move(cx-50,cy); await pg.mouse.down(); await pg.mouse.move(cx+50,cy,steps=8); await pg.mouse.up(); await pg.wait_for_timeout(200)
        s1=await pg.evaluate(INK); await pg.keyboard.press('Control+z'); await pg.wait_for_timeout(200); s2=await pg.evaluate(INK)
        await pg.keyboard.press('Control+Shift+z'); await pg.wait_for_timeout(200); s3=await pg.evaluate(INK)
        print('desktop',base,s1,s2,s3)
        print('ERR',errs); await b.close()
asyncio.run(main())
