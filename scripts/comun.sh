# Variables y funciones compartidas por los scripts (se cargan con "source").
STREAMING=/opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar
IN=/taller/input
OUT=/taller/output
cd /workspace

titulo() { printf '\n==================== %s ====================\n' "$*"; }

esperar_hdfs() {
  until hdfs dfsadmin -safemode get 2>/dev/null | grep -q "OFF"; do
    echo "Esperando a que HDFS salga de safe mode..."; sleep 3
  done
}

# correr_job <nombre> <mapper> <reducer> <entrada HDFS> <salida HDFS> [opciones extra de streaming]
correr_job() {
  local nombre=$1 mapper=$2 reducer=$3 entrada=$4 salida=$5; shift 5
  titulo "JOB: $nombre"
  hdfs dfs -rm -r -f -skipTrash "$salida" >/dev/null 2>&1 || true
  hadoop jar "$STREAMING" \
    -D mapreduce.job.name="taller-$nombre" \
    -D mapreduce.job.reduces=1 \
    -files "jobs/$mapper,jobs/$reducer" \
    -mapper "python3 $mapper" \
    -reducer "python3 $reducer" \
    -input "$entrada" \
    -output "$salida" "$@"
}
