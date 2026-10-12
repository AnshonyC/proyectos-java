import json, re, subprocess, sys
txt = subprocess.run(['pdftotext', sys.argv[1], '-'], capture_output=True, text=True).stdout.split('\f')
pags = {}
for i, p in enumerate(txt):
    if i < 6:
        continue
    for m in re.finditer(r'^CAPÍTULO (\d+)$', p, re.M):
        pags.setdefault(str(int(m.group(1))), i + 1)
    for m in re.finditer(r'^APÉNDICE ([A-E])$', p, re.M):
        pags.setdefault(m.group(1), i + 1)
json.dump(pags, open(sys.argv[2], 'w'))
print(len(pags), 'entradas;', 'faltan', [str(n) for n in range(1, 70) if str(n) not in pags])
