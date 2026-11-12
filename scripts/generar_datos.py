#!/usr/bin/env python3
"""Genera los 3 datasets del taller y sus resultados esperados (para validar a mano).

  datasets/ventas.csv         ~11 MB  -> Job 1 (promedio por categoría)
  datasets/resenas.txt        ~10 MB  -> Job 2 (WordCount)
  datasets/logs_servidor.log  ~15 MB  -> Job 3 (horas pico y errores)
  datasets/esperado/*.tsv     resultados calculados SIN Hadoop, para comparar

Compatible con Python 3.5 (el de las imágenes bde2020). Semilla fija: siempre
genera exactamente los mismos datos.
"""
import bisect
import io
import os
import random
import re
from collections import Counter, defaultdict

random.seed(2026)
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "datasets")
ESPERADO = os.path.join(BASE, "esperado")
if not os.path.isdir(ESPERADO):
    os.makedirs(ESPERADO)


def elegir(opciones, pesos):
    acumulado, total = [], 0
    for p in pesos:
        total += p
        acumulado.append(total)
    return opciones[bisect.bisect_right(acumulado, random.random() * total)]


def abrir(nombre):
    return io.open(os.path.join(BASE, nombre), "w", encoding="utf-8", newline="\n")


# ---------------- Dataset 1: ventas ----------------
CATEGORIAS = {  # categoria: (peso, precio mínimo, precio máximo) en pesos colombianos
    "electronica": (12, 300000, 2500000),
    "ropa": (25, 30000, 250000),
    "hogar": (18, 20000, 400000),
    "alimentos": (30, 5000, 80000),
    "deportes": (9, 40000, 600000),
    "libros": (6, 15000, 120000),
}
CIUDADES = ["Cali", "Bogota", "Medellin", "Barranquilla", "Cartagena"]
nombres = list(CATEGORIAS)
pesos = [CATEGORIAS[c][0] for c in nombres]
suma, cuenta = defaultdict(int), defaultdict(int)
with abrir("ventas.csv") as f:
    f.write("fecha,categoria,ciudad,valor\n")
    for _ in range(260000):
        cat = elegir(nombres, pesos)
        _, lo, hi = CATEGORIAS[cat]
        valor = random.randint(lo // 100, hi // 100) * 100
        fecha = "2026-%02d-%02d" % (random.randint(1, 12), random.randint(1, 28))
        f.write("%s,%s,%s,%d\n" % (fecha, cat, random.choice(CIUDADES), valor))
        suma[cat] += valor
        cuenta[cat] += 1
with io.open(os.path.join(ESPERADO, "promedio.tsv"), "w", encoding="utf-8", newline="\n") as f:
    for cat in sorted(suma):
        f.write("%s\t%.2f\t%d\t%.2f\n" % (cat, suma[cat] / cuenta[cat], cuenta[cat], suma[cat]))

# ---------------- Dataset 2: reseñas ----------------
SUJETOS = ["El pedido", "La comida", "El domicilio", "El producto", "La atención", "El empaque",
           "La panadería", "El servicio", "La app", "El precio"]
POSITIVO = ["llegó rápido y caliente", "estuvo excelente", "superó lo que esperaba", "es muy buena calidad",
            "fue amable y rápida", "vale cada peso", "me encantó", "estaba fresco y delicioso"]
NEGATIVO = ["llegó frío y tarde", "fue muy malo", "no era lo que pedí", "estaba en mal estado",
            "fue lenta y grosera", "es demasiado caro", "me decepcionó", "llegó incompleto"]
CIERRES = ["Volvería a comprar.", "No vuelvo a pedir.", "Lo recomiendo.", "Gracias Cali.",
           "Cinco estrellas.", "Una estrella.", "Mejoren por favor.", ""]
PALABRA = re.compile(r"[a-záéíóúüñ]+")
conteo = Counter()
with abrir("resenas.txt") as f:
    for _ in range(150000):
        bueno = random.random() < 0.62
        frase = "%s %s, %s %s. %s" % (
            random.choice(SUJETOS), random.choice(POSITIVO if bueno else NEGATIVO),
            random.choice(SUJETOS).lower(), random.choice(POSITIVO if bueno else NEGATIVO),
            random.choice(CIERRES))
        frase = frase.strip()
        f.write(frase + "\n")
        conteo.update(PALABRA.findall(frase.lower()))
with io.open(os.path.join(ESPERADO, "wordcount.tsv"), "w", encoding="utf-8", newline="\n") as f:
    for palabra in sorted(conteo):
        f.write("%s\t%d\n" % (palabra, conteo[palabra]))

# ---------------- Dataset 3: logs de servidor web ----------------
HORAS = ["%02d" % h for h in range(24)]
PESO_HORA = [1, 1, 1, 1, 1, 2, 4, 6, 8, 8, 9, 11, 16, 15, 9, 8, 8, 9, 12, 18, 20, 14, 7, 3]
URLS = ["/", "/api/productos", "/api/carrito", "/api/pagos", "/api/login", "/img/logo.png", "/api/pedidos"]
METODOS = ["GET", "GET", "GET", "POST"]
total_h, error_h = Counter(), Counter()
with abrir("logs_servidor.log") as f:
    for _ in range(280000):
        hora = elegir(HORAS, PESO_HORA)
        pico = hora in ("12", "13", "19", "20")
        r = random.random()
        prob_error = 0.09 if pico else 0.03
        if r < prob_error:
            nivel, codigo = "ERROR", random.choice([500, 502, 503])
        elif r < prob_error + 0.05:
            nivel, codigo = "WARN", random.choice([404, 401, 429])
        else:
            nivel, codigo = "INFO", random.choice([200, 200, 200, 201, 304])
        f.write("2026-11-%02d %s:%02d:%02d %s %s %s %d %dms\n" % (
            random.randint(1, 30), hora, random.randint(0, 59), random.randint(0, 59),
            nivel, random.choice(METODOS), random.choice(URLS), codigo, random.randint(5, 2500)))
        total_h[hora] += 1
        if nivel == "ERROR" or codigo >= 500:
            error_h[hora] += 1
with io.open(os.path.join(ESPERADO, "logs.tsv"), "w", encoding="utf-8", newline="\n") as f:
    for h in sorted(total_h):
        f.write("%s\t%d\t%d\t%.2f\n" % (h, total_h[h], error_h[h], 100.0 * error_h[h] / total_h[h]))

for nombre in ("ventas.csv", "resenas.txt", "logs_servidor.log"):
    print("%-20s %6.1f MB" % (nombre, os.path.getsize(os.path.join(BASE, nombre)) / 1048576.0))
print("Resultados esperados en datasets/esperado/")
