import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    parts = line.split(',')
    if len(parts) == 2:
        categoria, valor = parts
        print("%s\t%s\t1" % (categoria, valor))