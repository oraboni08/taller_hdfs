#!/usr/bin/env python3
# JOB 1 - Promedio de ventas por categoría (REDUCE)
# Hadoop entrega las líneas ORDENADAS por clave: todas las de una categoría llegan juntas.
# Salida: categoria<TAB>promedio<TAB>cantidad_ventas<TAB>total
import io, sys

entrada = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8", errors="replace")
salida = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

actual, suma, cantidad = None, 0.0, 0


def emitir():
    salida.write("%s\t%.2f\t%d\t%.2f\n" % (actual, suma / cantidad, cantidad, suma))


for linea in entrada:
    partes = linea.rstrip("\n").split("\t")
    if len(partes) != 2:
        continue
    categoria, valor = partes
    if categoria != actual:
        if actual is not None:
            emitir()
        actual, suma, cantidad = categoria, 0.0, 0
    suma += float(valor)
    cantidad += 1

if actual is not None:
    emitir()
salida.flush()
