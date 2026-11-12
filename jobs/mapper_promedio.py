#!/usr/bin/env python3
# JOB 1 - Promedio de ventas por categoría (MAP)
# Entrada: fecha,categoria,ciudad,valor      Salida: categoria<TAB>valor
import io, os, sys, time

entrada = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8", errors="replace")
salida = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Solo para las pruebas de tolerancia a fallos: hace el job más lento a propósito
retardo_ms = float(os.environ.get("RETARDO_MS", "0"))

for n, linea in enumerate(entrada, 1):
    if retardo_ms and n % 1000 == 0:
        time.sleep(retardo_ms / 1000.0)
    partes = linea.strip().split(",")
    if len(partes) != 4 or partes[0] == "fecha":   # línea vacía o encabezado
        continue
    categoria, valor = partes[1], partes[3]
    try:
        float(valor)
    except ValueError:
        continue
    salida.write("%s\t%s\n" % (categoria, valor))
salida.flush()
