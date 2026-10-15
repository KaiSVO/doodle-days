import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); errs=[]
        for vw,tag,loc in [((390,844),'m','en-GB'),((1280,860),'d','en-GB'),((390,844),'uk','uk-UA')]:
            c=await b.new_context(viewport={'width':vw[0],'height':vw[1]},device_scale_factor=2 if vw[0]<500 else 1,is_mobile=vw[0]<500,has_touch=vw[0]<500,locale=loc,service_workers='block')
            pg=await c.new_page(); pg.on('pageerror',lambda e:errs.append(str(e)))
            await pg.goto('http://localhost:8765/'); await pg.wait_for_timeout(2800)
            n=0
            while await pg.is_visible('#tourModal'):
                if n==0 and tag=='m': await pg.click('.ct-looks .skin >> nth=1'); await pg.wait_for_timeout(300)
                await pg.wait_for_timeout(350)
                if tag!='uk' or n in (0,3,7): await pg.screenshot(path=f'shots5/tour/{tag}-{n:02d}.png')
                if n==4 and tag=='m': await pg.click('#tourBack'); await pg.wait_for_timeout(300); print('back to:',await pg.text_content('#tourTitle')); await pg.click('#tourNext'); await pg.wait_for_timeout(200)
                await pg.click('#tourNext'); n+=1
                if n>20: break
            print(tag,'steps:',n,'toured & panel closed:',await pg.evaluate("document.getElementById('panel').classList.contains('open')"),'skin:',await pg.evaluate('document.documentElement.dataset.skin'))
            await c.close()
        print('ERR',errs); await b.close()
asyncio.run(main())
