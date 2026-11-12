#!/usr/bin/env python3
# JOB 3 - Análisis de logs (REDUCE)
# Salida: hora<TAB>peticiones<TAB>errores<TAB>porcentaje_error
import io, sys

entrada = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8", errors="replace")
salida = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

actual, total, errores = None, 0, 0


def emitir():
    salida.write("%s\t%d\t%d\t%.2f\n" % (actual, total, errores, 100.0 * errores / total))


for linea in entrada:
    partes = linea.rstrip("\n").split("\t")
    if len(partes) != 3:
        continue
    hora, uno, es_error = partes
    if hora != actual:
        if actual is not None:
            emitir()
        actual, total, errores = hora, 0, 0
    total += int(uno)
    errores += int(es_error)

if actual is not None:
    emitir()
salida.flush()
