"""Atualiza somente a base incorporada, preservando o layout de cada relatório."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import argparse
import json
import re

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', help='Data de extração, no formato DD/MM/AAAA')
    args = parser.parse_args()
    data = json.loads((ROOT / 'dados/bases.json').read_text(encoding='utf8'))
    date = args.data or datetime.now(ZoneInfo('America/Sao_Paulo')).strftime('%d/%m/%Y')
    datetime.strptime(date, '%d/%m/%Y')
    data['extractedAt'] = date
    payload = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', r'<\/')
    pattern = re.compile(r'(<script\b[^>]*\bid="database"[^>]*>)([\s\S]*?)(</script>)')
    pending = []
    for name in ['index.html', 'painel-flutuante-branco.html']:
        path = ROOT / name
        if not path.exists():
            continue
        original = path.read_bytes().decode('utf8')
        assert len(pattern.findall(original)) == 1, f'Base ausente ou duplicada: {name}'
        updated = pattern.sub(lambd