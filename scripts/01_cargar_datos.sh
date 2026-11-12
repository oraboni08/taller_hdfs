#!/usr/bin/env bash
# Paso 1: generar los datasets (si no existen) y subirlos a HDFS.
set -e
source /workspace/scripts/comun.sh

if [ ! -f datasets/ventas.csv ]; then
  titulo "Generando datasets"
  python3 scripts/generar_datos.py
fi

esperar_hdfs
titulo "Creando estructura en HDFS"
hdfs dfs -mkdir -p $IN/ventas $IN/resenas $IN/logs $OUT
hdfs dfs -put -f datasets/ventas.csv        $IN/ventas/
hdfs dfs -put -f datasets/resenas.txt       $IN/resenas/
hdfs dfs -put -f datasets/logs_servidor.log $IN/logs/
hdfs dfs -ls -R /taller

titulo "Bloques y réplicas (hdfs fsck)"
hdfs fsck $IN -files -blocks -locations 2>/dev/null \
  | grep -E "^/taller/input/.+ bytes|^[0-9]+\. BP|Total blocks|Average block replication|Under-replicated|Missing blocks|is HEALTHY|is CORRUPT" \
  | sed -E 's/BP-[^:]+:(blk_[0-9]+)_[0-9]+/\1/; s/DatanodeInfoWithStorage\[([0-9.]+):9866,[^]]+\]/\1/g'
