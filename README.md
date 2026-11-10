# Clúster de Hadoop en Docker & Trabajos MapReduce con Python

Este proyecto implementa un entorno de desarrollo distribuido Big Data para Apache Hadoop 3.2.1 (HDFS + YARN) contenedorizado con Docker Compose. Está optimizado para ejecutarse sin conflictos de arquitectura tanto en **macOS (Apple Silicon M1/M2/M3)** mediante la emulación `linux/amd64` (Rosetta 2), como en **Windows (WSL2 / Docker Desktop)**.

---

## 🏛️ Arquitectura del Clúster

El clúster está integrado por 6 contenedores interconectados bajo una red privada dedicada (`hdfs-net`):

- **NameNode**: Administrador del sistema de archivos distribuido (HDFS), encargado de gestionar la metainformación y bloques de datos.
- **DataNode 1 & DataNode 2**: Nodos de almacenamiento físico en HDFS donde se replican y guardan los bloques de archivos.
- **ResourceManager (YARN)**: Orquestador central encargado de la gestión de recursos del clúster y asignación de tareas de cómputo.
- **NodeManager (YARN)**: Agente ejecutor de contenedores de tareas MapReduce en los nodos de trabajo.
- **Client**: Contenedor cliente de administración interactiva con Python 3 instalado, utilizado para ejecutar comandos HDFS y enviar los trabajos de Hadoop Streaming al clúster sin afectar los servicios núcleo.

---

## 🛠️ Requisitos e Infraestructura

- **Host Compatible:** macOS (Apple Silicon M1/M2/M3) o Windows (WSL2 / Docker Desktop).
- **Runtime:** Docker Engine & Docker Compose.
- **Imágenes Base:** Suite oficial `bde2020` (versión Hadoop 3.2.1 / Java 8 / Debian Stretch).
- **Intérprete en Contenedor Client:** Python 3 (instalado en el contenedor cliente vía repositorios históricos de Debian).

---

## 📂 Estructura del Proyecto

    taller_hdfs/
    ├── docker-compose.yml       # Configuración del clúster (NameNode, DataNodes, YARN, Client)
    ├── hadoop.env               # Variables de entorno compartidas del clúster HDFS
    ├── .gitattributes          # Normalización de saltos de línea (LF) para compatibilidad Windows/Linux
    ├── datasets/
    │   └── data.csv             # Dataset de prueba con transacciones y logs
    ├── jobs/
    │   ├── mapper_avg.py        # Mapper: Promedio por categoría
    │   ├── reducer_avg.py       # Reducer: Promedio por categoría
    │   ├── mapper_wc.py         # Mapper: Conteo de palabras (WordCount)
    │   ├── reducer_wc.py        # Reducer: Conteo de palabras (WordCount)
    │   ├── mapper_filter.py     # Mapper: Filtrado de logs de error
    │   └── reducer_filter.py    # Reducer: Filtrado de logs de error
    └── README.md                # Documentación del proyecto

---

## ⚙️ Descripción de los Trabajos MapReduce

### 1. Trabajo 1: Promedio por Categoría (/output_avg)
- **Mapper:** Procesa registros CSV emitiendo pares de la categoría con su respectivo valor numérico.
- **Reducer:** Agrupa las claves, calcula la suma acumulada de valores, el total de registros por categoría y emite el promedio final formateado.

### 2. Trabajo 2: Conteo de Palabras / WordCount (/output_wc)
- **Mapper:** Descompone las líneas del dataset en palabras individuales, las normaliza en minúsculas y emite pares (palabra, 1).
- **Reducer:** Suma y agrupa la frecuencia total de aparición de cada token único.

### 3. Trabajo 3: Filtro de Logs de Error (/output_filter)
- **Mapper:** Examina las entradas y filtra únicamente las líneas asociadas a eventos con severidad ERROR o CRITICAL.
- **Reducer:** Contabiliza y estructura los eventos de error encontrados.

---

## 🚀 Guía de Ejecución y Comandos Utilizados

### Despliegue y Ejecución Automatizada en un Solo Paso

Copia y pega las siguientes instrucciones secuenciales en tu terminal para ejecutar de principio a fin la limpieza del entorno, inicialización del clúster, configuración de dependencias, ingesta de datos a HDFS y corrida de los 3 trabajos MapReduce:

    docker compose down -v
    docker compose up -d
    echo "Esperando inicialización del clúster..."
    sleep 15
    docker compose exec client bash -c "echo 'deb [http://archive.debian.org/debian](http://archive.debian.org/debian) stretch main' > /etc/apt/sources.list && echo 'deb [http://archive.debian.org/debian-security](http://archive.debian.org/debian-security) stretch/updates main' >> /etc/apt/sources.list && echo 'Acquire::Check-Valid-Until \"false\";' > /etc/apt/apt.conf.d/99no-check-valid-until"
    docker compose exec client bash -c "apt-get update && apt-get install -y python3"
    docker compose exec client bash -c "until hdfs dfs -mkdir -p /input 2>/dev/null; do echo 'Esperando a HDFS en puerto 9000...'; sleep 3; done; hdfs dfs -put -f /workspace/datasets/data.csv /input/data.csv && hdfs dfs -ls /input"

    docker compose exec client hdfs dfs -rm -r /output_avg 2>/dev/null
    docker compose exec client hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar -files /workspace/jobs/mapper_avg.py,/workspace/jobs/reducer_avg.py -mapper "python3 /workspace/jobs/mapper_avg.py" -reducer "python3 /workspace/jobs/reducer_avg.py" -input /input/data.csv -output /output_avg
    echo "=== RESULTADO TRABAJO 1 (PROMEDIO) ==="
    docker compose exec client hdfs dfs -cat /output_avg/part-00000

    docker compose exec client hdfs dfs -rm -r /output_wc 2>/dev/null
    docker compose exec client hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar -files /workspace/jobs/mapper_wc.py,/workspace/jobs/reducer_wc.py -mapper "python3 /workspace/jobs/mapper_wc.py" -reducer "python3 /workspace/jobs/reducer_wc.py" -input /input/data.csv -output /output_wc
    echo "=== RESULTADO TRABAJO 2 (WORDCOUNT) ==="
    docker compose exec client hdfs dfs -cat /output_wc/part-00000

    docker compose exec client hdfs dfs -rm -r /output_filter 2>/dev/null
    docker compose exec client hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar -files /workspace/jobs/mapper_filter.py,/workspace/jobs/reducer_filter.py -mapper "python3 /workspace/jobs/mapper_filter.py" -reducer "python3 /workspace/jobs/reducer_filter.py" -input /input/data.csv -output /output_filter
    echo "=== RESULTADO TRABAJO 3 (FILTRO LOGS) ==="
    docker compose exec client hdfs dfs -cat /output_filter/part-00000

---

## 🌐 Consolas de Monitoreo Web

El clúster expone las interfaces gráficas nativas en la máquina host para validación visual:

- **HDFS NameNode Status & File System Explorer:** http://localhost:9870
- **YARN Resource Manager Status & Application Logs:** http://localhost:8088

---

## 🛡️ Evaluación de Tolerancia a Fallos

Para evaluar el comportamiento del sistema ante la caída controlada de un nodo:

1. **Simular la pérdida de un DataNode:**

       docker compose stop datanode1

2. **Validación:**
   - Consulta el estado en el navegador en http://localhost:9870 en la sección **Datanodes** para verificar el estado `Dead` de `datanode1`.
   - Consulta cualquier resultado en HDFS desde el cliente para confirmar la disponibilidad continua del servicio a través de `datanode2`:

         docker compose exec client hdfs dfs -cat /output_avg/part-00000

3. **Reintegrar el DataNode:**

       docker compose start datanode1