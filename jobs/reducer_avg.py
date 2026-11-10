import sys

current_category = None
total_sum = 0.0
total_count = 0

for line in sys.stdin:
    parts = line.strip().split('\t')
    if len(parts) != 3:
        continue
    category, value, count = parts
    
    if current_category == category:
        total_sum += float(value)
        total_count += int(count)
    else:
        if current_category:
            print("%s\t%.2f" % (current_category, total_sum / total_count))
        current_category = category
        total_sum = float(value)
        total_count = int(count)

if current_category:
    print("%s\t%.2f" % (current_category, total_sum / total_count))