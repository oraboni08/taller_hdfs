import sys

for line in sys.stdin:
    if "ERROR" in line:
        parts = line.strip().split()
        if parts:
            print("%s\t1" % parts[0])