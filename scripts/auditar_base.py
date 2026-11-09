"""Confere cobertura e equações sem substituir os totais impressos na fonte."""
from collections import Counter
from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]
data = json.loads((root / 'dados/bases.json').read_text(encoding='utf8'))
issues = []
conversion = data['conversion']
forecast = data['forecast']
key = lambda r: tuple(r.get(k) for k in ('year','month','area','dimension','clinic','person'))
issues += [('duplicate', k, n) for k,n in Counter(map(key, conversion)).items() if n != 1]
for year, last_month in ((2025,12),(2026,10)):
    for area in ('novos','readesao'):
        for dimension in ('consultor','medico'):
            for month in range(1,last_month+1):
                for clinic in ('BH','CAMPINAS','CURITIBA','POA'):
                    rows = [r for r in conversion if (r['year'],r['month'],r['area'],r['dimension'],r['clinic']) == (year,month,area,dimension,clinic)]
                    if not rows: issues.append(('missing',year,month,area,dimension,clinic))
for r in conversion:
    if r['patients'] != r['closed'] + r['notConverted']: issues.append(('patients equation',key(r)))
for year,las