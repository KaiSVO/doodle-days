# activity/plan icons + Supporter options (Play billing mocked)
import asyncio,json
from playwright.async_api import async_playwright
from fontroute import setup
MOCK="""(()=>{const owned=JSON.parse(localStorage.getItem('mockOwned')||'[]');
window.getDigitalGoodsService=async()=>({getDetails:async ids=>ids.map(id=>({itemId:id,price:{currency:'USD',value:{supporter_monthly:'0.99',supporter_yearly:'5.99',supporter:'14.99'}[id]},
  introductoryPrice:id==='supporter_yearly'?{currency:'USD',value:'2.99'}:null})),listPurchases:async()=>owned.map(itemId=>({itemId,purchaseToken:'x'}))});})()"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); errs=[]
        for loc,tag in [('en-GB','en'),('uk-UA','uk')]:
          for W,H in [(390,844),(1280,900)]:
            c=await b.new_context(viewport={'width':W,'height':H},locale=loc,service_workers='block'); await setup(c)
            await c.add_init_script(MOCK)
            pg=await c.new_page(); pg.on('pageerror',lambda e:errs.append(str(e)))
            await pg.goto('http://localhost:8765/'); await pg.wait_for_timeout(2500)
            while await pg.is_visible('#tourModal'): await pg.click('#tourNext'); await pg.wait_for_timeout(60)
            await pg.screenshot(path=f'shots9/{tag}-{W}-month.png',full_page=True)
            await pg.click('.tcard .x >> nth=2'); await pg.wait_for_timeout(300)   # edit 3rd activity
            await pg.click('#trIcons .ipk[aria-label] >> nth=12'); await pg.wait_for_timeout(200) # a paid one, locked
            await pg.screenshot(path=f'shots9/{tag}-{W}-trmodal.png')
            await pg.keyboard.press('Escape')
            await pg.click('.tab[data-view=week]'); await pg.wait_for_timeout(300)
            await pg.screenshot(path=f'shots9/{tag}-{W}-week.png')
            await pg.click('.tab[data-view=settings]'); await pg.wait_for_timeout(400)
            await pg.screenshot(path=f'shots9/{tag}-{W}-settings.png')
            if W==390 and tag=='en':
                # owned yearly -> unlocked, pick paid icon
                await pg.evaluate("localStorage.setItem('mockOwned','[\"supporter_yearly\"]')"); await pg.reload(); await pg.wait_for_timeout(2500)
                await pg.click('.tab[data-view=settings]'); await pg.wait_for_timeout(300)
                print('unlocked:',await pg.text_content('#buyOpts'),'| manage visible:',await pg.is_visible('#manageSub'))
                await pg.keyboard.press('Escape'); await pg.click('.tab[data-view=month]'); await pg.wait_for_timeout(300)
                await pg.click('.tcard .x >> nth=2'); await pg.wait_for_timeout(300)
                await pg.click('#trIcons [aria-label="Parcel"]'); await pg.click('#trForm button[type=submit]'); await pg.wait_for_timeout(400)
                await pg.click('.day >> nth=12'); await pg.wait_for_timeout(300); await pg.click('#addEv') if await pg.is_visible('#addEv') else None
                await pg.screenshot(path=f'shots9/{tag}-unlocked-month.png',full_page=True)
                # subscription ends
                await pg.evaluate("localStorage.setItem('mockOwned','[]')"); await pg.reload(); await pg.wait_for_timeout(2500)
                print('after lapse skin:',await pg.evaluate("document.documentElement.dataset.skin"),'| toast:',await pg.text_content('.toast') if await pg.is_visible('.toast') else None)
                await pg.screenshot(path=f'shots9/{tag}-lapsed-month.png',full_page=True)
            await c.close()
        print('ERR',errs); await b.close()
import os; os.makedirs('shots9',exist_ok=True); asyncio.run(main())
