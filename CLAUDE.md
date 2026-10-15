# Doodle Days: handoff notes for Claude

A free calendar you can draw in, for artists and crafters. Single-file PWA, live at https://doodle-days.vercel.app/ (Vercel deploys this repo's root on every push to `main`). Owner: KaiSVO (contact sidelock24@gmail.com). The owner doesn't code: explain things in plain words, show changes (screenshots) and **wait for an explicit "push it" before pushing to GitHub**.

## Repo layout
- Repo root = what users get: `index.html` (built, do not hand-edit), `sw.js`, `manifest.webmanifest`, `privacy.html`, `icons/`, `vercel.json`.
- `dev/` = source and tools (excluded from Vercel by `.vercelignore`):
  - `src.html`: the app source (HTML + CSS + JS in one file).
  - `sticker_styles.js` (sticker finishes) and `icons.py` → `icons.js` (activity/plan icon set) are injected by `build.py`.
  - `i18n_keys.json` (`s`: index-aligned English strings, `p`: plurals) + `i18n/<lang>.txt` (`index|text`, `P|key|forms`) for uk, es, pt, de, fr, pl. `i18n_build.py` injects them into `src.html` between `/*__I18N__*/` and `/*__END__*/`.
  - `t*.py`: Playwright checks (serve the built page on localhost:8765; `fontroute.py` serves Google Fonts from a local copy).
  - `store/`: Play Store listing text, screenshots, feature graphic.

## Release routine
```
cd dev
python3 icons.py            # only if icons changed
python3 i18n_build.py       # must print "bad 0"
python3 build.py            # writes dev/dist/index.html
cp dist/index.html ../index.html
```
Then bump `APP_VERSION` in `src.html` (currently 3.9.2) and the cache name in `../sw.js` (currently `doodle-days-v34`) every release, or phones keep the old version.
New UI text: add the English string to `src.html` (wrapped in `tx('…')` for JS), append it to `i18n_keys.json` `s`, and add `index|translation` lines to all six `i18n/*.txt`. Ukrainian uses the polite "ви"; es/pt/de/fr/pl use informal you. Literal string edits: the I18N JSON inside src.html also contains English keys, so anchor replacements on code, not on bare strings.
Checks worth running after UI changes: `t42.py` (overlap/clipping sweep, 7 languages, phone + desktop), `t45.py` (contrast in every theme/accent), `t41.py` (saved month/year/day images), `t44.py` (icons + Supporter billing with a mocked Play), `t43.py` (share calendar), `t37.py` (guided tour).

## Product decisions (keep)
- Everything stays on the device (IndexedDB); no analytics, no server. Privacy policy says so.
- Trackers are called **Activities**. Plans show a triangle or the plan's icon.
- Themes: Candy pop (bubbly, polka dots, sticker-edged cells, lime active tab), Pixel quest, Classic (paper planner: ruled paper, joined grid, square corners) are free; Scrapbook, Cosy garden, Midnight rose are Supporter. `inkGuard()` keeps all text ≥4.5:1 contrast for any theme/accent.
- Theme fonts lacking Cyrillic/Polish have companions in the stacks (Nunito, Caveat, Lora, IBM Plex Mono, Press Start 2P).
- Sticker finishes: Classic + Vinyl free; Hand-painted, Paper cut-out, Enamel pin Supporter. Picker lives in the sticker trays.
- Activity/plan icons: 8 free + Studio, Everyday, Shop packs (Supporter). Unset icons are guessed from the name.
- Share my calendar (free): picture of month/week/picked dates, or plans as an .ics file. Live link waits for sync.
- **Supporter** via Google Play Billing (Digital Goods API, works in the Play Store build only):
  - `supporter_monthly` $0.99, `supporter_yearly` $5.99 (UI shows "Just $0.50 a month, 50% off"; launch offer $2.99 first year set in Play Console), `supporter` lifetime $21.99 ("Includes every future extra").
  - Purchases are re-checked on start; a lapsed subscription switches paid extras back to free ones.
- Android package name: `io.github.kaisvo.doodledays` (fixed forever).

## Status (mid-October 2026)
- Personal Play Console account verified; app being created; store-listing answers drafted in chat (data safety: no data collected; target audience 13+; App access "Yes" with reviewer note; promo code for reviewers to add once products exist).
- Next: build the Android package with pwabuilder.com from the Vercel URL (Play Billing on), upload to Internal testing, then add `/.well-known/assetlinks.json` with **both** the upload key and Google's app-signing SHA-256 fingerprints, create the three products, then a closed test with 12+ testers for 14 days.
- Later: Phase 2 sync via Sign in with Google + the user's own Google Drive (appDataFolder), which also enables the Live link; iOS app (Capacitor, StoreKit, Sign in with Apple).
