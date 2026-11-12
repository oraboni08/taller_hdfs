#!/usr/bin/env python3
# JOB 3 - Análisis de logs: horas pico y errores (MAP)
# Entrada: 2026-11-08 14:23:11 INFO GET /api/productos 200 123ms
# Salida:  hora<TAB>1<TAB>es_error   (es_error = 1 si nivel ERROR o código HTTP >= 500)
import io, sys

entrada = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8", errors="replace")
salida = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

for linea in entrada:
    partes = linea.split()
    if len(partes) < 6:
        continue
    hora = partes[1][:2]
    try:
        es_error = 1 if (partes[2] == "ERROR" or int(partes[5]) >= 500) else 0
    except ValueError:
        continue
    salida.write("%s\t1\t%d\n" % (hora, es_error))
salida.flush()
