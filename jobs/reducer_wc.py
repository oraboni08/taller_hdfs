import sys

current_word = None
current_count = 0

for line in sys.stdin:
    parts = line.strip().split('\t')
    if len(parts) != 2:
        continue
    word, count = parts
    
    if current_word == word:
        current_count += int(count)
    else:
        if current_word:
            print("%s\t%d" % (current_word, current_count))
        current_word = word
        current_count = int(count)

if current_word:
    print("%s\t%d" % (current_word, current_count))