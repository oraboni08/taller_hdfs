#!/usr/bin/env bash
# Estado del clúster: DataNodes vivos/muertos, NodeManagers y aplicaciones YARN.
source /workspace/scripts/comun.sh
titulo "HDFS: DataNodes"
hdfs dfsadmin -report 2>/dev/null | grep -E "^Live datanodes|^Dead datanodes|^Name:|^Hostname:|^DFS Used:|Under replicated blocks|Missing blocks"
titulo "HDFS: salud del sistema de archivos"
hdfs fsck /taller 2>/dev/null | grep -E "Average block replication|Under-replicated|Missing blocks|is HEALTHY|is CORRUPT"
titulo "YARN: NodeManagers"
yarn node -list -all 2>/dev/null
titulo "YARN: aplicaciones"
yarn application -list -appStates ALL 2>/dev/null | grep -E "Application-Id|taller-"
