#!/usr/bin/env python3
# Mapper DEFECTUOSO a propósito (prueba de tolerancia a fallos).
# Falla al leer la primera línea: YARN reintenta cada tarea map
# (4 intentos por defecto) y al final el job queda en estado FAILED.
import sys

for linea in sys.stdin:
    raise RuntimeError("Error simulado en el mapper: %s" % linea[:40])
