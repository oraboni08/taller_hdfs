#!/usr/bin/env bash
# Prueba de fallos: job con un mapper que siempre falla.
# YARN reintenta cada tarea map hasta 4 veces (mapreduce.map.maxattempts) y el job queda FAILED.
source /workspace/scripts/comun.sh
esperar_hdfs
correr_job con-error mapper_con_error.py reducer_promedio.py $IN/ventas $OUT/con_error
echo "Código de salida del job: $? (distinto de 0 = falló)"
