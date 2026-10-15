import json,re,sys
K=json.load(open('i18n_keys.json')); S=K['s']; P=K['p']
ph=lambda t:sorted(re.findall(r'\{\w+\}',t))
out={}; bad=0
for lang in ['uk','es','pt','de','fr','pl']:
    s={}; p={}
    for ln in open(f'i18n/{lang}.txt',encoding='utf-8'):
        ln=ln.rstrip('\n')
        if not ln.strip(): continue
        if ln.startswith('P|'):
            parts=ln.split('|'); key=parts[1]; f=parts[2:]
            cats=['one','other'] if len(f)==2 else ['one','few','many','other']
            if len(f) not in (2,4) or key not in P: print(lang,'bad P',ln); bad+=1; continue
            p[key]=dict(zip(cats,f))
            for x in f:
                if ph(x)!=ph(P[key]['other']) and ph(x)!=ph(P[key]['one']): print(lang,'P ph',key,x); bad+=1
        else:
            i,t=ln.split('|',1); i=int(i); t=t.replace('\\n','\n')
            if ph(t)!=ph(S[i]): print(lang,i,'ph',S[i],'=>',t); bad+=1
            s[S[i]]=t
    miss=[i for i,e in enumerate(S) if e not in s]; pm=[k for k in P if k not in p]
    if miss or pm: print(lang,'missing',miss[:10],pm); bad+=1
    out[lang]={'s':s,'p':p}
src=open('src.html',encoding='utf-8').read()
j=json.dumps(out,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
a=src.index('/*__I18N__*/')+12; b=src.index('/*__END__*/',a)
src2=src[:a]+j+src[b:]
open('src.html','w',encoding='utf-8').write(src2)
print('bad',bad,'size',len(j))
