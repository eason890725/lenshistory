"""Rewrite products.json fields into one house style (see the format table in design.md).

Only changes how a value is written, never what it says: units, abbreviations, word order.
Usage: python scripts/normalize_products.py            (edits src/data/products.json in place)
       python scripts/normalize_products.py --selftest
"""
import json, re, sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / 'src/data/products.json'

MOTOR = {
    'stm (stepping motor)': 'STM', 'stepping motor (stm)': 'STM', 'linear motor (lm)': 'Linear Motor',
    'vxd (linear motor)': 'VXD', 'rxd (stepping motor)': 'RXD', 'hla (high-response linear actuator)': 'HLA',
    'none (manual focus)': 'Manual focus', 'manual focus only': 'Manual focus', 'none': 'Manual focus',
    'stepper motor': 'Stepping Motor', 'stepping motor': 'Stepping Motor', 'linear motor': 'Linear Motor', 'dc motor': 'DC Motor',
}


def num(s):
    return float(s) if '.' in s else int(s)


def ratio_to_x(m):
    """'1:5.2' -> '0.19x'"""
    return f'{1 / float(m.group(1)):.2f}x'


def norm(k, v, g):
    if not isinstance(v, str):
        if k == 'maxMagnification' and isinstance(v, (int, float)):
            return f'{v:g}x'
        return v
    s = re.sub(r'\s+', ' ', v).strip()
    if k == 'closeFocus':
        s = re.sub(r'(\d)\s*m\b', r'\1m', s).replace('(Wide)', '(W)').replace('(Tele)', '(T)')
    elif k == 'maxMagnification':
        s = re.sub(r'\b1\s*:\s*(\d+(?:\.\d+)?)', ratio_to_x, s)
        s = re.sub(r'(\d)\s*x\b', r'\1x', s)
        s = re.sub(r'^(\d+(?:\.\d+)?)$', r'\1x', s)
    elif k == 'opticalDesign':
        m = re.match(r'^(\d+ elements in \d+ groups)\s*\((.+)\)$', s)
        if m:
            s = m.group(1)
            g.setdefault('specialElements', norm('specialElements', m.group(2), g))
    elif k == 'specialElements':
        s = re.sub(r'\b(ASPH|ASP|aspherical|Aspheric)\b\.?', 'Aspherical', s)
        s = re.sub(r'\s*[;/]\s*', ', ', s)
    elif k == 'burstSpeed':
        s = re.sub(r'(\d)\s*fps', r'\1fps', s, flags=re.I)
        m = re.fullmatch(r'(.+\(Elec[^)]*\)) / (.+\(Mech\))', s)
        if m:   # mechanical shutter first
            s = f'{m.group(2)} / {m.group(1)}'
    elif k == 'dimensions':
        s = re.sub(r'[øφΦ]\s*', 'Ø', s).replace('×', 'x')
        s = re.sub(r'\s*x\s*', ' x ', s)
        s = re.sub(r'(\d)\s*mm', r'\1 mm', s)
    elif k == 'ibisRating':
        if s.lower().startswith('no'):
            return None
        s = s.replace(' (CIPA)', '')
    elif k == 'evfResolution':
        if s.lower().startswith('no'):
            return None
    elif k == 'afPoints':
        s = re.sub(r'\bPoints\b', 'points', s)
        s = re.sub(r'\bAreas\b', 'areas', s)
        s = re.sub(r'\bPhase-detection\b', 'phase-detect', s, flags=re.I)
        s = re.sub(r'^(\d+)$', r'\1 points', s)
        s = re.sub(r'(\d+ (?:phase|contrast)-detect)(?! points)', r'\1 points', s)
    elif k == 'batterySpec':
        s = s.replace('Approx. ', '')
    elif k == 'cardSlots':
        s = re.sub(r'\bSD UHS-(I+(?:/I+)?)\b', r'SD (UHS-\1)', s)
        if re.match(r'^(SD|CFexpress)', s):
            s = '1x ' + s
    elif k == 'lcdSpec':
        for a, b in (('Touchscreen', 'touch'), ('touchscreen', 'touch'), ('Vari-angle', 'vari-angle'), ('Tilting', 'tilting'), ('Fixed', 'fixed')):
            s = s.replace(a, b)
        s = re.sub(r'(\d+(?:\.\d+)?)K-dot', lambda m: f'{float(m.group(1)) / 1000:.2f}M-dot', s)
    elif k == 'videoResolution':
        s = re.sub(r'\bFHD\b', 'Full HD', s).replace('2160p', '4K').replace('1080p', 'Full HD')
        s = re.sub(r'\s*/\s*\d+-bit$', '', s)   # bit depth belongs in videoColorDepth
    elif k == 'motorType':
        s = MOTOR.get(s.lower(), s)
    elif k == 'logSupport':
        s = s.replace('C-Log 2/3', 'Canon Log 2, Canon Log 3').replace('C-Log 3', 'Canon Log 3')
    elif k == 'apertureMax' and re.fullmatch(r'\d+(\.\d+)?', s):
        return num(s)
    return s


def normalize(items):
    for g in items:
        for k in list(g):
            v = norm(k, g[k], g)
            if v is None:
                g.pop(k)
            else:
                g[k] = v
    return items


def selftest():
    g = {'closeFocus': '0.18 m (Wide) / 0.38 m (Tele)', 'maxMagnification': '1:5.2 (W) / 1:6 (T)',
         'opticalDesign': '14 elements in 11 groups (2 ASPH, 1 ED)', 'dimensions': 'φ76 × 96mm',
         'ibisRating': '5.5 stops (CIPA)', 'burstSpeed': '10 fps', 'cardSlots': 'SD UHS-II',
         'apertureMax': '1.8', 'motorType': 'STM (Stepping Motor)'}
    normalize([g])
    assert g['closeFocus'] == '0.18m (W) / 0.38m (T)', g['closeFocus']
    assert g['maxMagnification'] == '0.19x (W) / 0.17x (T)', g['maxMagnification']
    assert g['opticalDesign'] == '14 elements in 11 groups' and g['specialElements'] == '2 Aspherical, 1 ED'
    assert g['dimensions'] == 'Ø76 x 96 mm', g['dimensions']
    assert g['ibisRating'] == '5.5 stops' and g['burstSpeed'] == '10fps'
    assert g['cardSlots'] == '1x SD (UHS-II)' and g['apertureMax'] == 1.8 and g['motorType'] == 'STM'
    assert normalize([{'maxMagnification': 0.25}])[0]['maxMagnification'] == '0.25x'
    h = normalize([{'burstSpeed': '30fps (Elec) / 10fps (Mech)', 'lcdSpec': '3.0-inch 1040K-dot tilting',
                    'videoResolution': '4K 30p / 8-bit', 'afPoints': '425 phase-detect'}])[0]
    assert h['burstSpeed'] == '10fps (Mech) / 30fps (Elec)', h['burstSpeed']
    assert h['lcdSpec'] == '3.0-inch 1.04M-dot tilting', h['lcdSpec']
    assert h['videoResolution'] == '4K 30p' and h['afPoints'] == '425 phase-detect points'
    print('selftest ok')


if __name__ == '__main__':
    if sys.argv[1:] == ['--selftest']:
        selftest()
    else:
        items = normalize(json.loads(DATA.read_text(encoding='utf-8')))
        DATA.write_text(json.dumps(items, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f'normalized {len(items)} items')
