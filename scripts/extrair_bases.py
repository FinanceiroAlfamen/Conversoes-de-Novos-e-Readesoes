"""Extrai as tabelas mensais dos dois PDFs e preserva os totais impressos para auditoria."""
from pathlib import Path
import json, re, hashlib, logging
import pdfplumber

logging.getLogger('pdfminer').setLevel(logging.ERROR)
ROOT = Path(__file__).resolve().parents[1]
MONTHS = ['janeiro','fevereiro','março','abril','maio','junho','julho','agosto','setembro','outubro','novembro','dezembro']
CLINICS = ['BH','CAMPINAS','CURITIBA','POA']

def number(s):
    s = s.replace('R$', '').replace('%','').replace(' ','').replace('.','').replace(',','.').strip()
    return float(s) if s else None

def grouped(words):
    lines = {}
    for w in words:
        lines.setdefault(round(w['top']), []).append(w)
    return [sorted(v, key=lambda w:w['x0']) for k,v in sorted(lines.items())]

def cells(words, centers):
    bounds = [(a+b)/2 for a,b in zip(centers,centers[1:])]
    result = [[] for _ in centers]
    for w in words:
        x = (w['x0']+w['x1'])/2
        i = sum(x>b for b in bounds)
        result[i].append(w['text'])
    return [' '.join(v) for v in result]

def conversion(page, year, area, dimension):
    words = page.extract_words()
    header = next(w['top'] for w in words if w['text']=='PACIENTES' and w['top']>100)
    lower = sorted([w for w in words if abs(w['top']-header)<1],key=lambda w:w['x0'])
    numeric = [w for w in lower if w['text'] in ['PACIENTES','FECHAMENTOS','APROVEITAMENTO','CONVERTIDOS','(ATEND.','TRATAMENTO','TRATAMENTOS']]
    centers = [(w['x0']+w['x1'])/2 for w in numeric]
    assert len(centers)==9,(year,area,dimension,lower)
    numeric_left = numeric[0]['x0']-8
    keys = ['patients','closed','rate','notConverted','perClosing','treatments','average','value','treatmentRate'] if area=='novos' else ['patients','closed','notConverted','rate','perClosing','treatments','average','value','treatmentRate']
    rows=[]
    printed={}
    for line in grouped([w for w in words if w['top']>header+15]):
        first=line[0]['text']
        if first not in [str(year),'TOTAL']:
            if rows and all(w['x0']<numeric_left for w in line) and first in ['CONSULTOR','MÉDICO']:
                rows[-1]['person']+=' '+' '.join(w['text'] for w in line)
            continue
        ns=cells([w for w in line if w['x0']>=numeric_left],centers)
        values=dict(zip(keys,[number(x) for x in ns]))
        if first=='TOTAL':
            printed=values;continue
        assert line[1]['text'] in MONTHS and line[2]['text'] in CLINICS,line
        name=' '.join(w['text'] for w in line[3:] if w['x0']<numeric_left)
        assert name and values['patients'] is not None,line
        # Blank counts in these Power BI tables represent no event; preserve raw cells separately.
        raw=values.copy()
        for key in ['closed','notConverted','treatments','value']:values[key]=values[key] or 0
        if values['patients'] != values['closed']+values['notConverted']:
            raise ValueError(('Pacientes não conciliam',year,area,dimension,line))
        values.update(year=year,month=MONTHS.index(line[1]['text'])+1,clinic=line[2]['text'],person=name,area=area,dimension=dimension,sourcePage=(1 if area=='novos' else 3)+(dimension=='medico'),raw=raw)
        rows.append(values)
    return rows,printed

def forecast(page,year):
    words=page.extract_words()
    # Numeric column centers from the first monthly subtotal, whose five cells are populated.
    first=next(line for line in grouped(words) if line[0]['text']=='janeiro')
    centers=[(w['x0']+w['x1'])/2 for w in first[1:]]
    assert len(centers)==5,first
    keys=['released','notRejoined','absent','rejoined','total']
    rows=[]; monthly=[];printed={};month=None
    for line in grouped(words):
        label=line[0]['text']
        if label not in MONTHS+CLINICS+['TOTAL']:continue
        values=dict(zip(keys,[number(x) or 0 for x in cells([w for w in line[1:] if w['x0']>120],centers)]))
        if label in MONTHS:
            month=MONTHS.index(label)+1;monthly.append(dict(year=year,month=month,**values))
        elif label=='TOTAL':printed=values
        else:
            assert month is not None
            rows.append(dict(year=year,month=month,clinic=label,sourcePage=5,**values))
    assert len(rows)==4*len(monthly),(year,len(rows),len(monthly))
    return rows,monthly,printed

def main():
    out=ROOT/'dados';out.mkdir(exist_ok=True)
    cache=ROOT/'tmp';cache.mkdir(exist_ok=True)
    result={'conversion':[],'forecast':[],'sources':[],'audits':[]}
    for path in sorted((ROOT/'Base de Dados').glob('BADE DE DADOS - *.pdf')):
        year=int(re.search(r'(20\d\d)',path.name)[0])
        digest=hashlib.sha256(path.read_bytes()).hexdigest()
        cached=cache/f'extracao-v2-{digest}.json'
        if cached.exists():part=json.loads(cached.read_text(encoding='utf8'))
        else:
            part={'conversion':[],'forecast':[],'audits':[]}
            with pdfplumber.open(path) as pdf:
                assert len(pdf.pages)==5, 'A base deve conter as quatro tabelas de conversão e a tabela mensal.'
                for i,(area,dimension) in enumerate([('novos','consultor'),('novos','medico'),('readesao','consultor'),('readesao','medico')]):
                    rows,printed=conversion(pdf.pages[i],year,area,dimension)
                    summed={k:round(sum(r[k] for r in rows),2) for k in ['patients','closed','notConverted','treatments','value']}
                    part['conversion']+=rows
                    part['audits'].append(dict(year=year,area=area,dimension=dimension,page=i+1,rows=len(rows),printed=printed,summed=summed))
                rows,monthly,printed=forecast(pdf.pages[4],year)
                part['forecast']=rows
                part['audits'].append(dict(year=year,area='previsao',dimension='clinica',page=5,rows=len(rows),printed=printed,summed={k:sum(r[k] for r in rows) for k in printed},monthlyPrinted=monthly))
            cached.write_text(json.dumps(part,ensure_ascii=False),encoding='utf8')
        result['conversion']+=part['conversion'];result['forecast']+=part['forecast'];result['audits']+=part['audits']
        result['sources'].append(dict(year=year,file=path.name,sha256=digest,lastMonth=max(r['month'] for r in part['conversion']+part['forecast'])))
    assert {s['year'] for s in result['sources']}>={2025,2026}
    (out/'bases.json').write_text(json.dumps(result,ensure_ascii=False,separators=(',',':')),encoding='utf8')
    print(json.dumps({'conversionRows':len(result['conversion']),'forecastRows':len(result['forecast']),'audits':result['audits']},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
