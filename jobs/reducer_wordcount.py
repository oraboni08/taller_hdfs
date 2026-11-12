#!/usr/bin/env python3
# JOB 2 - WordCount (REDUCE). Suma los 1 de cada palabra.
# También sirve como COMBINER (suma parcial en cada map antes de enviar por la red).
import io, sys

entrada = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8", errors="replace")
salida = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

actual, total = None, 0
for linea in entrada:
    partes = linea.rstrip("\n").split("\t")
    if len(partes) != 2:
        continue
    palabra, cuenta = partes
    if palabra != actual:
        if actual is not None:
            salida.write("%s\t%d\n" % (actual, total))
        actual, total = palabra, 0
    total += int(cuenta)

if actual is not None:
    salida.write("%s\t%d\n" % (actual, total))
salida.flush()
