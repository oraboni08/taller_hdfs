# Taller HDFS + Hadoop MapReduce con Docker

Clúster Hadoop 3.2.1 (HDFS + YARN) en Docker Compose, con 3 trabajos MapReduce en Python
(Hadoop Streaming), validación de resultados y pruebas de tolerancia a fallos.

> Guía completa paso a paso (conceptos, comandos y resultados esperados):
> [`docs/guia_taller_hdfs.html`](docs/guia_taller_hdfs.html) — descargar y abrir en el navegador.

## Arquitectura

| Contenedor | Rol | Web |
|---|---|---|
| `namenode` | HDFS: guarda el "índice" (qué bloques forman cada archivo y en qué nodo están) | http://localhost:9870 |
| `datanode1`, `datanode2` | HDFS: guardan los bloques. Replicación = 2 (cada bloque vive en ambos) | — |
| `resourcemanager` | YARN: reparte memoria/CPU y decide dónde corre cada tarea | http://localhost:8088 |
| `nodemanager1`, `nodemanager2` | YARN: ejecutan las tareas map/reduce (traen Python 3) | — |
| `historyserver` | YARN Timeline: historial de aplicaciones terminadas | http://localhost:8188 |
| `client` | Desde aquí se dan los comandos `hdfs`, `yarn`, `hadoop jar` | — |

Ajustes clave en `hadoop.env`: `mapreduce.framework.name=yarn` (sin esto los jobs corren en modo
local y no aparecen en YARN), `dfs.replication=2`, bloques de 4 MB, un DataNode se marca *Dead* en
~60 s y un NodeManager *LOST* en 30 s (para poder demostrar los fallos en clase), y agregación de logs.

## Datasets y jobs

`scripts/generar_datos.py` genera (semilla fija) 3 datasets y calcula sus resultados esperados sin Hadoop:

| Job | Dataset (HDFS) | Mapper → Reducer | Salida |
|---|---|---|---|
| 1. Promedio por clave | `/taller/input/ventas/ventas.csv` (260 000 ventas, ~8,5 MB) | `categoria, valor` → promedio, cantidad y total | `/taller/output/promedio` |
| 2. WordCount (+ combiner) | `/taller/input/resenas/resenas.txt` (150 000 reseñas, ~11 MB) | `palabra, 1` → suma | `/taller/output/wordcount` |
| 3. Análisis de logs | `/taller/input/logs/logs_servidor.log` (280 000 líneas, ~14 MB) | `hora, 1, es_error` → peticiones, errores, % | `/taller/output/logs` |

## Ejecución (Windows PowerShell, macOS o Linux)

```bash
docker compose up -d --build                          # 1. levantar el clúster (la 1.ª vez tarda)
docker compose ps                                     #    todos deben estar "Up"
docker compose exec client bash scripts/01_cargar_datos.sh   # 2. generar datos y subirlos a HDFS
docker compose exec client bash scripts/02_ejecutar_jobs.sh  # 3. correr los 3 jobs en YARN
docker compose exec client bash scripts/03_validar.sh        # 4. comparar con el resultado esperado
docker compose exec client bash scripts/estado.sh            # estado de nodos y aplicaciones
```

Comandos útiles dentro del cliente (`docker compose exec client bash`):

```bash
hdfs dfs -ls -R /taller
hdfs dfs -cat /taller/output/promedio/part-00000
hdfs fsck /taller/input -files -blocks -locations
yarn application -list -appStates ALL
yarn logs -applicationId <application_id> | less
```

## Pruebas de tolerancia a fallos

| # | Prueba | Cómo | Qué se observa |
|---|---|---|---|
| 1 | Apagar un DataNode | `docker compose stop datanode2`, esperar ~60 s, `scripts/estado.sh`, leer un archivo; luego `docker compose start datanode2` | 1 Dead node, bloques *under-replicated*, pero los archivos se siguen leyendo; al volver: Healthy |
| 2 | Reiniciar un contenedor durante una operación HDFS | Mientras corre un `hdfs dfs -put` de un archivo grande: `docker compose restart datanode1` | El `put` termina igual (recuperación del pipeline de escritura) y el archivo queda completo |
| 3 | Detener un NodeManager con un job corriendo | `scripts/04_job_lento.sh` y, mientras corre, `docker compose stop nodemanager2` | El NodeManager pasa a LOST, YARN reprograma sus tareas en `nodemanager1` y el job termina SUCCEEDED |
| 4 | Fallo dentro de un Map | `scripts/05_job_con_error.sh` | Cada tarea map se reintenta 4 veces y el job queda FAILED; se lee el error con `yarn logs` |

El detalle de cada prueba, con las salidas obtenidas, está en la guía HTML.

## Apagar

```bash
docker compose down        # apaga (conserva los datos de HDFS)
docker compose down -v     # apaga y BORRA los datos de HDFS
```

Si los puertos 9870/8088/8188 están ocupados: `PUERTO_HDFS=19870 PUERTO_YARN=18088 PUERTO_HISTORY=18188 docker compose up -d`
(en PowerShell: `$env:PUERTO_HDFS=19870; ...`).
