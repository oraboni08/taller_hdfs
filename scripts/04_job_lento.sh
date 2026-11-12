#!/usr/bin/env bash
# Prueba de fallos: job de promedio a propósito LENTO (~2-3 min) para tener
# tiempo de detener un NodeManager o un DataNode mientras corre.
source /workspace/scripts/comun.sh
esperar_hdfs
correr_job promedio-lento mapper_promedio.py reducer_promedio.py $IN/ventas $OUT/promedio_lento \
  -cmdenv RETARDO_MS=${RETARDO_MS:-1500}
echo "Resultado:"
hdfs dfs -cat $OUT/promedio_lento/part-00000
