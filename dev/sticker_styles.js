/* Sticker finishes: each takes a sticker's 100x100 SVG body and returns a full SVG with depth baked in.
   Works as an <img> data URI and when drawn onto a canvas, so the look survives in saved doodles. */
const ST_VIEW='-14 -14 128 128';
const stWrap=(defs,body)=>`<svg xmlns="http://www.w3.org/2000/svg" viewBox="${ST_VIEW}"><defs>${defs}</defs>${body}</svg>`;
const ST_INK='#2B2B2B';
// apply fn to every opening tag except <text>
const stTags=(b,fn)=>b.replace(/<(?!\/|text\b)[a-zA-Z][^>]*>/g,fn);
const stTint=(hex,a)=>{if(!/^#[0-9a-f]{6}$/i.test(hex))return hex;const n=parseInt(hex.slice(1),16);return '#'+[16,8,0].map(sh=>Math.round(((n>>sh)&255)*(1-a)+255*a).toString(16).padStart(2,'0')).join('');};
const stFillOf=t=>{const m=t.match(/\sfill="([^"]+)"/);return m?m[1]:null;};

const STICKER_STYLES={
  flat:b=>stWrap('',b),

  vinyl:b=>stWrap(`<filter id="v" x="-30%" y="-30%" width="160%" height="160%" color-interpolation-filters="sRGB">
<feMorphology in="SourceAlpha" operator="dilate" radius="6" result="d"/>
<feMorphology in="SourceAlpha" operator="dilate" radius="6.8" result="d2"/>
<feGaussianBlur in="d2" stdDeviation="2.4" result="db"/><feOffset in="db" dx="1.2" dy="3.2" result="so"/>
<feFlood flood-color="#2A1D14" flood-opacity=".3"/><feComposite in2="so" operator="in" result="shadow"/>
<feFlood flood-color="#E2DACF"/><feComposite in2="d2" operator="in" result="rim"/>
<feFlood flood-color="#FFFFFF"/><feComposite in2="d" operator="in" result="border"/>
<feGaussianBlur in="SourceAlpha" stdDeviation="3.2" result="ab"/>
<feSpecularLighting in="ab" surfaceScale="3.5" specularConstant=".8" specularExponent="20" lighting-color="#FFFFFF" result="spec"><fePointLight x="12" y="-24" z="64"/></feSpecularLighting>
<feComposite in="spec" in2="SourceAlpha" operator="in" result="specIn"/>
<feComposite in="SourceGraphic" in2="specIn" operator="arithmetic" k1="0" k2="1" k3=".5" k4="0" result="lit"/>
<feMerge><feMergeNode in="shadow"/><feMergeNode in="rim"/><feMergeNode in="border"/><feMergeNode in="lit"/></feMerge></filter>`,
  `<g filter="url(#v)">${b}</g>`),

  painted:b=>{
    const fills=b.replace(new RegExp(`stroke="${ST_INK}"`,'g'),'stroke="none"').replace(/<text[\s\S]*?<\/text>/g,'');
    const ink=stTags(b.replace(new RegExp(`stroke="${ST_INK}"`,'g'),'stroke="#3F322C"').replace(/stroke-width="([\d.]+)"/g,(m,w)=>`stroke-width="${Math.max(2,w*.72).toFixed(1)}"`),
      t=>t.replace(/\sfill="#[0-9A-Fa-f]{3,8}"/,' fill="none"'));
    return stWrap(`<filter id="wc" x="-20%" y="-20%" width="140%" height="140%" color-interpolation-filters="sRGB">
<feTurbulence type="fractalNoise" baseFrequency=".035" numOctaves="2" seed="4" result="n"/>
<feDisplacementMap in="SourceGraphic" in2="n" scale="7" xChannelSelector="R" yChannelSelector="G" result="w"/>
<feTurbulence type="fractalNoise" baseFrequency=".09" numOctaves="3" seed="9" result="g"/>
<feColorMatrix in="g" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  -1.3 0 0 0 1.45" result="ga"/>
<feComposite in="w" in2="ga" operator="in" result="wg"/>
<feGaussianBlur in="w" stdDeviation="2.4" result="wb"/>
<feComposite in="w" in2="wb" operator="out" result="edge"/>
<feColorMatrix in="edge" type="matrix" values=".6 0 0 0 0  0 .6 0 0 0  0 0 .6 0 0  0 0 0 1.4 0" result="edgeD"/>
<feMerge><feMergeNode in="wg"/><feMergeNode in="edgeD"/></feMerge></filter>
<filter id="ink" x="-20%" y="-20%" width="140%" height="140%">
<feTurbulence type="fractalNoise" baseFrequency=".06" numOctaves="2" seed="12" result="n"/>
<feDisplacementMap in="SourceGraphic" in2="n" scale="3.5" xChannelSelector="R" yChannelSelector="G"/></filter>`,
    `<g filter="url(#wc)" transform="translate(1.6 1.4)" opacity=".9" style="mix-blend-mode:multiply">${fills}</g><g filter="url(#ink)" opacity=".88">${ink}</g>`);
  },

  paper:b=>{
    let s=stTags(b,t=>{
      if(!t.includes(`stroke="${ST_INK}"`)) return t;
      const f=stFillOf(t);
      if(f&&f!=='none') return t.replace(`stroke="${ST_INK}"`,`stroke="${stTint(f,.4)}"`).replace(/stroke-width="[\d.]+"/,'stroke-width="2"');
      return t.replace(`stroke="${ST_INK}"`,'stroke="#8A6A50"');
    });
    s=s.replace(/<(path|circle|rect|polygon|ellipse|polyline|line)\b/g,'<$1 filter="url(#pc)"');
    return stWrap(`<filter id="pc" x="-25%" y="-25%" width="150%" height="150%" color-interpolation-filters="sRGB">
<feTurbulence type="fractalNoise" baseFrequency=".05" numOctaves="1" seed="2" result="cut"/>
<feDisplacementMap in="SourceGraphic" in2="cut" scale="2.2" xChannelSelector="R" yChannelSelector="G" result="w"/>
<feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="3" seed="5" result="t"/>
<feColorMatrix in="t" type="saturate" values="0" result="tg"/>
<feComposite in="w" in2="tg" operator="arithmetic" k1=".35" k2=".82" k3="0" k4="0" result="tex"/>
<feComposite in="tex" in2="w" operator="in" result="texIn"/>
<feDropShadow in="texIn" dx=".8" dy="2" stdDeviation="1.2" flood-color="#2A1C10" flood-opacity=".5"/></filter>`,s);
  },

  enamel:b=>{
    const s=b.replace(new RegExp(`stroke="${ST_INK}"`,'g'),'stroke="url(#gold)"').replace(/stroke-width="([\d.]+)"/g,(m,w)=>`stroke-width="${(w*1.4).toFixed(1)}"`);
    return stWrap(`<linearGradient id="gold" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="100" y2="100">
<stop offset="0" stop-color="#FFF4C2"/><stop offset=".28" stop-color="#E4B53F"/><stop offset=".52" stop-color="#A8760F"/><stop offset=".76" stop-color="#F6D978"/><stop offset="1" stop-color="#B5841B"/></linearGradient>
<filter id="en" x="-30%" y="-30%" width="160%" height="160%" color-interpolation-filters="sRGB">
<feColorMatrix in="SourceGraphic" type="saturate" values="1.15" result="sat"/>
<feGaussianBlur in="SourceAlpha" stdDeviation="1.8" result="b"/>
<feSpecularLighting in="b" surfaceScale="4.5" specularConstant="1.15" specularExponent="34" lighting-color="#FFFFFF" result="spec"><fePointLight x="18" y="-14" z="48"/></feSpecularLighting>
<feComposite in="spec" in2="SourceAlpha" operator="in" result="specIn"/>
<feComposite in="sat" in2="specIn" operator="arithmetic" k1="0" k2="1" k3=".75" k4="0" result="lit"/>
<feGaussianBlur in="SourceAlpha" stdDeviation="2" result="sb"/><feOffset in="sb" dx="1" dy="3" result="so"/>
<feFlood flood-color="#1E140A" flood-opacity=".38"/><feComposite in2="so" operator="in" result="shadow"/>
<feMerge><feMergeNode in="shadow"/><feMergeNode in="lit"/></feMerge></filter>`,
    `<g filter="url(#en)">${s}</g>`);
  }
};
const stickerURI=(style,body)=>'data:image/svg+xml;charset=utf-8,'+encodeURIComponent(STICKER_STYLES[style](body));
