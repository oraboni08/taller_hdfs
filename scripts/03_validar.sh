#!/usr/bin/env bash
# Paso 3: validación manual. Compara cada salida en HDFS con el resultado
# esperado que calculó generar_datos.py sin usar Hadoop.
source /workspace/scripts/comun.sh
mkdir -p resultados
for job in promedio wordcount logs; do
  titulo "Validando $job"
  hdfs dfs -ls $OUT/$job
  hdfs dfs -cat $OUT/$job/part-* > resultados/$job.tsv
  python3 scripts/validar.py resultados/$job.tsv datasets/esperado/$job.tsv
done
