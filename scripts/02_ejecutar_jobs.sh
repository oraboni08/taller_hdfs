#!/usr/bin/env bash
# Paso 2: ejecutar los 3 jobs MapReduce en YARN con Hadoop Streaming.
# Uso: bash scripts/02_ejecutar_jobs.sh            (los 3)
#      bash scripts/02_ejecutar_jobs.sh wordcount  (solo uno: promedio | wordcount | logs)
set -e
source /workspace/scripts/comun.sh
esperar_hdfs
JOB=${1:-todos}

if [ "$JOB" = todos ] || [ "$JOB" = promedio ]; then
  correr_job promedio mapper_promedio.py reducer_promedio.py $IN/ventas $OUT/promedio
  hdfs dfs -cat $OUT/promedio/part-00000
fi
if [ "$JOB" = todos ] || [ "$JOB" = wordcount ]; then
  # El reducer también se usa como combiner (suma parcial en cada map)
  correr_job wordcount mapper_wordcount.py reducer_wordcount.py $IN/resenas $OUT/wordcount \
    -combiner "python3 reducer_wordcount.py"
  echo "Top 10 palabras:"
  hdfs dfs -cat $OUT/wordcount/part-00000 | sort -t$'\t' -k2,2nr | head -10
fi
if [ "$JOB" = todos ] || [ "$JOB" = logs ]; then
  correr_job logs mapper_logs.py reducer_logs.py $IN/logs $OUT/logs
  echo "hora  peticiones  errores  %error"
  hdfs dfs -cat $OUT/logs/part-00000
fi

titulo "Aplicaciones en YARN"
yarn application -list -appStates ALL 2>/dev/null | grep -E "Application-Id|taller-"
