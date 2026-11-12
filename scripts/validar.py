#!/usr/bin/env python3
"""Compara la salida de Hadoop con el resultado esperado calculado sin Hadoop.

Uso: python3 validar.py <salida_hadoop.tsv> <esperado.tsv>
"""
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def leer(ruta):
    filas = {}
    with io.open(ruta, encoding="utf-8") as f:
        for linea in f:
            partes = linea.rstrip("\n").split("\t")
            if len(partes) >= 2:
                filas[partes[0]] = partes[1:]
    return filas


def igual(a, b):
    try:
        return abs(float(a) - float(b)) < 0.011
    except ValueError:
        return a == b


hadoop, esperado = leer(sys.argv[1]), leer(sys.argv[2])
errores = []
for clave in sorted(set(hadoop) | set(esperado)):
    if clave not in hadoop:
        errores.append("falta en Hadoop: %s" % clave)
    elif clave not in esperado:
        errores.append("sobra en Hadoop: %s" % clave)
    elif len(hadoop[clave]) != len(esperado[clave]) or not all(map(igual, hadoop[clave], esperado[clave])):
        errores.append("%s -> Hadoop %s / esperado %s" % (clave, hadoop[clave], esperado[clave]))

print("  claves comparadas: %d" % len(esperado))
if errores:
    print("  RESULTADO: NO COINCIDE (%d diferencias)" % len(errores))
    for e in errores[:10]:
        print("   - " + e)
    sys.exit(1)
print("  RESULTADO: OK, la salida de Hadoop coincide 100 % con el cálculo esperado")
