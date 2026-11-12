#!/usr/bin/env python3
# JOB 2 - WordCount sobre reseñas de clientes (MAP)
# Entrada: una reseña por línea      Salida: palabra<TAB>1
import io, re, sys

entrada = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8", errors="replace")
salida = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
PALABRA = re.compile(r"[a-záéíóúüñ]+")

for linea in entrada:
    for palabra in PALABRA.findall(linea.lower()):
        salida.write("%s\t1\n" % palabra)
salida.flush()
