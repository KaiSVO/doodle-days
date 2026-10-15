import os; os.makedirs('dist', exist_ok=True)
src = open('src.html').read().replace('/*__STICKER_STYLES__*/', open('sticker_styles.js').read().strip()).replace('/*__ICONS__*/', open('icons.js').read().strip())
head, body = src.split('<!--BODY-->')
html = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, viewport-fit=cover">\n'
        + head + '\n</head>\n<body>\n' + body + '\n</body>\n</html>\n')
open('dist/index.html', 'w').write(html)
open('preview.html', 'w').write(head + body)
