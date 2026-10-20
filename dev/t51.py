# notes get watercolour + crayon: Supporter preview draws with both, free shows the stars and the Supporter toast; day brushes still work
import asyncio,sys
from playwright.async_api import async_playwright
from fontroute import setup
OUT=sys.argv[1] if len(sys.argv)>1 else '.'
async def stroke(pg,pts):
    await pg.mouse.move(*pts[0]); await pg.mouse.down()
    for p in pts[1:]: await pg.mouse.move(*p,steps=8)
    await pg.mouse.up(); await pg.wait_for_timeout(120)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); errs=[]
        for hashv,tag in [('#supporter-preview','sup'),('','free')]:
            c=await b.new_context(viewport={'width':390,'height':844},has_touch=True,locale='en-GB',service_workers='block'); await setup(c)
            pg=await c.new_page(); pg.on('pageerror',lambda e:errs.append(str(e)))
            await pg.goto('http://localhost:8765/'+hashv); await pg.wait_for_timeout(2500)
            while await pg.is_visible('#tourModal'): await pg.click('#tourNext'); await pg.wait_for_timeout(40)
            await pg.click('.tab[data-view=notes]'); await pg.click('#newNote'); await pg.wait_for_timeout(300)
            await pg.fill('#noteTitle','Brush test'); await pg.click('#ndDraw'); await pg.wait_for_timeout(200)
            print(tag,'note tools:',await pg.eval_on_selector_all('#noteTools .trow:first-child .ib','els=>els.map(e=>e.getAttribute("aria-label")+(e.classList.contains("paid")?"★":""))'))
            bx=await pg.locator('#notePad').bounding_box(); X,Y,W=bx['x'],bx['y'],bx['width']
            if tag=='sup':
                for k,(tool,col) in enumerate([('Watercolour',1),('Watercolour',2),('Crayon',4),('Crayon',5)]):
                    await pg.click(f'#noteTools [aria-label={tool}]'); await pg.click(f'#noteTools .sw >> nth={col}')
                    y=Y+60+k*55; await stroke(pg,[(X+30,y),(X+W*.4,y+25),(X+W*.85,y-10)])
                await pg.click('#noteTools .ib >> nth=-1') if False else None
                n=await pg.evaluate("(()=>{const c=document.getElementById('notePad'),d=c.getContext('2d').getImageData(0,0,c.width,400).data;let a=0,part=0;for(let i=3;i<d.length;i+=4){if(d[i])a++;if(d[i]>0&&d[i]<200)part++;}return [a,part]})()")
                print('painted pixels, semi-transparent (wash):',n)
                await pg.locator('.notedlg').screenshot(path=f'{OUT}/note-brushes.png')
                await pg.click('#noteDone'); await pg.wait_for_timeout(400); print('saved with doodle:',await pg.locator('.ncard .nc-pic').count())
            else:
                await pg.click('#noteTools [aria-label=Watercolour]'); await pg.wait_for_timeout(200); print('free toast:',await pg.text_content('#toast'))
                await pg.locator('#noteTools').screenshot(path=f'{OUT}/note-tools-free.png')
            await c.close()
        print('errors',errs); await b.close()
asyncio.run(main())
