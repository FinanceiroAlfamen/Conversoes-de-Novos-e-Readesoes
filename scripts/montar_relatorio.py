"""Gera um HTML autossuficiente com a base extraída e a identidade visual AlfaMen."""
from pathlib import Path
import re,json
from datetime import datetime
from zoneinfo import ZoneInfo
ROOT=Path(__file__).resolve().parents[1]
brand_path=ROOT/'assets/marca.json'
if brand_path.exists():
    brand=json.loads(brand_path.read_text(encoding='utf8'))
else:
    reference=ROOT/'referencia-novos.html'
    if not reference.exists():
        reference=Path('C:/Users/alfab/.codex/skills/padrao-alfamen-relatorios/assets/reference.html')
    source=reference.read_text(encoding='utf8')
    brand=dict(logo=re.search(r'<header class="hero">[\s\S]*?<img src="([^"]+)"',source)[1],
               font='\n'.join(re.findall(r'@font-face\{[^}]+\}',source)),
               texture=re.search(r'background-image:[^\n]+?url\([\x22\x27](data:image/[^\x22\x27]+)',source)[1])
    brand_path.write_text(json.dumps(brand),encoding='utf8')
logo,font,texture=brand['logo'],brand['font'],brand['texture']
data=json.loads((ROOT/'dados/bases.json').read_text(encoding='utf8'))
try: date=datetime.now(ZoneInfo('America/Sao_Paulo')).strftime('%d/%m/%Y')
except Exception: date='13/10/2026'
data['extractedAt']=date
css=(ROOT/'assets/styles.css').read_text(encoding='utf8').replace('__TEXTURE__',texture)
html=(ROOT/'assets/template.html').read_text(encoding='utf8')
for key,value in {'__LOGO__':logo,'__FONT__':font,'__CSS__':css,'__JS__':(ROOT/'assets/app.js').read_text(encoding='utf8'),'__DATA__':json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</',r'<\/')}.items():html=html.replace(key,value)
assert not re.search(r'__(LOGO|FONT|CSS|JS|DATA|TEXTURE)__',html)
(ROOT/'index.html').write_text(html,encoding='utf8')
print('HTML gerado:',ROOT/'index.html',len(html),'caracteres')
