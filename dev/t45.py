# contrast audit: every visible text vs its real background, all themes x modes x some accent colours
import asyncio,json,sys
from playwright.async_api import async_playwright
from fontroute import setup
JS=r"""(where)=>{
 const parse=s=>{const m=s.match(/rgba?\(([^)]+)\)/);if(!m)return null;const p=m[1].split(/[ ,\/]+/).filter(Boolean).map(Number);return [p[0],p[1],p[2],p.length>3?p[3]:1];};
 const toRgb=c=>{const cv=document.createElement('canvas').getContext('2d');cv.fillStyle=c;cv.fillRect(0,0,1,1);const d=cv.getImageData(0,0,1,1).data;return [d[0],d[1],d[2],d[3]/255];};
 const col=s=>{const p=parse(s);if(p&&!/color\(|oklch|oklab|lab\(/.test(s))return p;return toRgb(s);};
 const blend=(f,b)=>[0,1,2].map(i=>f[i]*f[3]+b[i]*(1-f[3])).concat(1);
 const L=c=>{const a=c.slice(0,3).map(v=>{v/=255;return v<=.03928?v/12.92:((v+.055)/1.055)**2.4});return .2126*a[0]+.7152*a[1]+.0722*a[2];};
 const ratio=(a,b)=>{const x=L(a),y=L(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05);};
 const bgOf=e=>{const st=[];for(let p=e;p;p=p.parentElement){const c=getComputedStyle(p);if(c.backgroundImage!=='none'&&/url|gradient/.test(c.backgroundImage)&&p!==document.body&&p!==document.documentElement)return null;const b=col(c.backgroundColor);if(b[3]>0)st.push(b);if(b[3]>=.99)break;}
   let r=col(getComputedStyle(document.body).backgroundColor);if(r[3]<1)r=[255,255,255,1];for(let i=st.length-1;i>=0;i--)r=blend(st[i],r);return r;};
 const out=[];const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;
 while(n=w.nextNode()){const t=n.nodeValue.trim();if(!t)continue;const e=n.parentElement;if(!e)continue;const r=e.getBoundingClientRect();if(!r.width||!r.height||r.bottom<0||r.top>innerHeight)continue;
  const c=getComputedStyle(e);if(c.visibility==='hidden'||e.closest('[hidden],canvas,svg,option,.vh,[aria-hidden=true]'))continue;
  let op=1;for(let p=e;p;p=p.parentElement)op*=+getComputedStyle(p).opacity;if(op<.5)continue; // deliberately faded (locked/disabled) items
  const x=r.left+Math.min(r.width/2,20),y=r.top+r.height/2,top=document.elementFromPoint(x,y);if(!top||!(top===e||e.contains(top)||top.contains(e)))continue;
  const bg=bgOf(e);if(!bg)continue;let fg=col(c.color);fg[3]*=op;fg=blend(fg,bg);
  const big=parseFloat(c.fontSize)>=24||(parseFloat(c.fontSize)>=18.6&&+c.fontWeight>=700);const need=big?3:4.5,rt=ratio(fg,bg);
  if(rt<need)out.push(`${rt.toFixed(2)} "${t.slice(0,40)}" <${e.tagName.toLowerCase()}.${(e.className||'').toString().split(' ')[0]}>`);}
 return [...new Set(out)];}"""
CONF=[('candy','light',None),('candy','dark',None),('classic','light',None),('classic','dark',None),('pixel','dark',None),('scrapbook','light',None),('garden','light',None),('rose','dark',None),
      ('candy','light','#E9A23B'),('candy','dark','#2B2B2B'),('classic','light','#FF7A45'),('candy','light','#2FA36B'),('candy','dark','#6C3CF0')]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); rep={}
        for sk,mode,acc in CONF:
            c=await b.new_context(viewport={'width':390,'height':844},locale='en-GB',service_workers='block'); await setup(c)
            pg=await c.new_page(); await pg.goto('http://localhost:8765/#supporter-preview'); await pg.wait_for_timeout(2300)
            while await pg.is_visible('#tourModal'): await pg.click('#tourNext'); await pg.wait_for_timeout(40)
            await pg.evaluate(f"""()=>{{S.meta.skin='{sk}';S.meta.theme='{mode}';S.meta.accent={json.dumps(acc)};applyTheme();renderView();}}""") if False else None
            # set via storage + reload (S is not global)
            await pg.evaluate("""([sk,mode,acc])=>new Promise(res=>{const r=indexedDB.open('doodle-days',1);r.onsuccess=()=>{const st=r.result.transaction('kv','readwrite').objectStore('kv');const g=st.get('meta');g.onsuccess=()=>{const m=g.result;m.skin=sk;m.theme=mode;m.accent=acc;st.put(m,'meta');st.transaction.oncomplete=()=>res();};};})""",[sk,mode,acc])
            await pg.reload(); await pg.wait_for_timeout(2300)
            key=f'{sk}-{mode}-{acc or "default"}'; res={}
            async def chk(name):
                await pg.wait_for_timeout(350); r=await pg.evaluate(JS,name)
                if r: res[name]=r; await pg.screenshot(path=f'shots10/{key}-{name}.png')
            await chk('month')
            await pg.click('.tab[data-view=settings]'); await chk('settings-top')
            await pg.evaluate("document.querySelector('#buyOpts')&&document.querySelector('#buyOpts').scrollIntoView({block:'center'})"); await chk('settings-supporter')
            await pg.keyboard.press('Escape'); await pg.wait_for_timeout(200)
            await pg.click('.tab[data-view=month]'); await pg.click('#view-month .shcal'); await chk('share'); await pg.keyboard.press('Escape')
            await pg.click('.tcard .x >> nth=0'); await chk('activity'); await pg.keyboard.press('Escape')
            await pg.click('.day >> nth=9'); await chk('day')
            rep[key]=res; await c.close()
        await b.close()
        for k,v in rep.items():
            for n,r in v.items(): print(k,n,r[:8])
        json.dump(rep,open('shots10/report.json','w'),indent=1)
import os; os.makedirs('shots10',exist_ok=True); asyncio.run(main())
