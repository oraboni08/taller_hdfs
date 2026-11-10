import sys

current_key = None
current_count = 0

for line in sys.stdin:
    parts = line.strip().split('\t')
    if len(parts) != 2:
        continue
    key, count = parts
    
    if current_key == key:
        current_count += int(count)
    else:
        if current_key:
            print("%s\t%d" % (current_key, current_count))
        current_key = key
        current_count = int(count)

if current_key:
    print("%s\t%d" % (current_key, current_count))