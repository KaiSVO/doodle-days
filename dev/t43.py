# share my calendar: picture (month/week/pick) and plans .ics, phone + desktop, en + uk
import asyncio
from playwright.async_api import async_playwright
from fontroute import setup
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); errs=[]
        for loc,tag in [('en-GB','en'),('uk-UA','uk'),('de-DE','de')]:
          for W,H in [(390,844),(1280,900)]:
            c=await b.new_context(viewport={'width':W,'height':H},locale=loc,service_workers='block',accept_downloads=True); await setup(c)
            pg=await c.new_page(); pg.on('pageerror',lambda e:errs.append(str(e)))
            await pg.goto('http://localhost:8765/'); await pg.wait_for_timeout(2500)
            while await pg.is_visible('#tourModal'): await pg.click('#tourNext'); await pg.wait_for_timeout(60)
            await pg.click('#view-month .shcal'); await pg.wait_for_timeout(900)
            await pg.screenshot(path=f'shots8/{tag}-{W}-sheet.png',full_page=False)
            async with pg.expect_download() as dl: await pg.click('#shGo')
            await (await dl.value).save_as(f'shots8/{tag}-{W}-month.png')
            if W==1280:
                await pg.click('#shRange [data-r=week]'); await pg.wait_for_timeout(600)
                async with pg.expect_download() as dl: await pg.click('#shGo')
                await (await dl.value).save_as(f'shots8/{tag}-week.png')
                await pg.click('#shNotes'); await pg.click('#shRange [data-r=pick]'); await pg.wait_for_timeout(600)
                async with pg.expect_download() as dl: await pg.click('#shGo')
                await (await dl.value).save_as(f'shots8/{tag}-pick.png')
                await pg.click('.sh-way[data-w=ics]'); await pg.click('#shRange [data-r=month]'); await pg.wait_for_timeout(300)
                await pg.screenshot(path=f'shots8/{tag}-ics-sheet.png')
                print(tag,'info:',await pg.text_content('#shInfo'))
                async with pg.expect_download() as dl: await pg.click('#shGo')
                await (await dl.value).save_as(f'shots8/{tag}.ics')
            await c.close()
        print('ERR',errs); await b.close()
import os; os.makedirs('shots8',exist_ok=True); asyncio.run(main())
