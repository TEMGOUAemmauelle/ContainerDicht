#!/bin/bash

# === CONFIGURATION ===
IMAGE_NAME="mon-image-mlperf"
RUNTIMES=("docker" "podman" "crio")  # Adapter CRI-O si besoin
ITERATIONS=10
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
OUTPUT_DIR="./output_AI_${TIMESTAMP}"
mkdir -p "$OUTPUT_DIR"

# Fichier CSV général
CSV_FILE="${OUTPUT_DIR}/benchmark_summary.csv"
echo "iteration,runtime,type,duration_ms,avg_pkg_watt,avg_cor_watt,avg_gfx_watt,avg_cpu_c6,avg_latency_ms,throughput,power_file" > "$CSV_FILE"

# Fonction pour exécuter avec CRI-O
run_crio_once() {
  local POD_UID=$(uuidgen)
  local TMPDIR="/tmp/crio_run_$$"
  mkdir -p "$TMPDIR"
  local POD_JSON="$TMPDIR/pod.json"
  local CONTAINER_JSON="$TMPDIR/container.json"
  
  cat > "$POD_JSON" <<EOF
{
  "metadata": {
    "name": "test-pod",
    "namespace": "default",
    "uid": "$POD_UID"
  },
  "log_directory": "/tmp",
  "linux": {}
}
EOF

  cat > "$CONTAINER_JSON" <<EOF
{
  "metadata": {
    "name": "mlperf-container"
  },
  "image": {
    "image": "localhost:5000/mon-image-mlperf"
  },
  "command": [
    "python",
    "/app/run_inference.py"
  ],
  "log_path": "mlperf-container.log",
  "mounts": [
    {
      "container_path": "/app/results",
      "host_path": "$TMPDIR/results",
      "readonly": false
    }
  ]
}
EOF

  # Créer le pod
  POD_ID=$(sudo crictl runp "$POD_JSON" 2>/dev/null)
  if [ -z "$POD_ID" ]; then
    echo "[✘] Erreur : échec création pod"
    rm -rf "$TMPDIR"
    return 1
  fi

  # Créer le conteneur
  CONTAINER_ID=$(sudo crictl create "$POD_ID" "$CONTAINER_JSON" "$POD_JSON" 2>/dev/null)
  if [ -z "$CONTAINER_ID" ]; then
    echo "[✘] Erreur : échec création conteneur"
    sudo crictl stop "$POD_ID" >/dev/null 2>&1
    sudo crictl rmp "$POD_ID" >/dev/null 2>&1
    rm -rf "$TMPDIR"
    return 1
  fi

  # Démarrer le conteneur
  if ! sudo crictl start "$CONTAINER_ID"; then
    echo "[✘] Erreur : démarrage conteneur échoué"
    sudo crictl rm "$CONTAINER_ID" >/dev/null 2>&1
    sudo crictl stopp "$POD_ID" >/dev/null 2>&1
    sudo crictl rmp "$POD_ID" >/dev/null 2>&1
    rm -rf "$TMPDIR"
    return 1
  fi

  # Attendre la fin (polling max 30s)
  for i in {1..30}; do
    STATUS=$(sudo crictl inspect "$CONTAINER_ID" | grep '"state"' | awk -F'"' '{print $4}')
    if [[ "$STATUS" == "CONTAINER_EXITED" ]]; then
      break
    fi
    sleep 1
  done

  # Extraire les résultats
  if [ -f "$TMPDIR/results/mlperf_resnet50_result.csv" ]; then
    awk -F, 'NR==2 {print $1 "," $2}' "$TMPDIR/results/mlperf_resnet50_result.csv"
  else
    echo "NA,NA"
  fi

  # Nettoyage
  sudo crictl rm "$CONTAINER_ID" >/dev/null 2>&1
  sudo crictl stopp "$POD_ID" >/dev/null 2>&1
  sudo crictl rmp "$POD_ID" >/dev/null 2>&1
  rm -rf "$TMPDIR"
  return 0
}

# Fonction pour extraire les métriques de performance
extract_perf_metrics() {
  local runtime=$1
  local iteration_dir=$2
  
  # Pour Docker/Podman
  if [ "$runtime" != "crio" ]; then
    local result_file="${iteration_dir}/results/mlperf_resnet50_result.csv"
    if [ -f "$result_file" ]; then
      awk -F, 'NR==2 {print $1 "," $2}' "$result_file"
    else
      echo "NA,NA"
    fi
  # Pour CRI-O (déjà extrait dans run_with_runtime)
  else
    if [ -f "${iteration_dir}/perf_metrics.csv" ]; then
      cat "${iteration_dir}/perf_metrics.csv"
    else
      echo "NA,NA"
    fi
  fi
}

# Fonction principale
run_with_runtime() {
    local runtime=$1
    local iteration=$2

    local iteration_dir="${OUTPUT_DIR}/run${iteration}_${runtime}"
    mkdir -p "$iteration_dir"

    local power_file="${iteration_dir}/power.txt"
    local time_file="${iteration_dir}/time.txt"
    local tmp_pid_file="${iteration_dir}/turbostat.pid"

    echo ""
    echo "==============================="
    echo "[🔥] Runtime : $runtime - Itération : $iteration"
    echo "==============================="

    rm -f "$power_file" "$time_file" "$tmp_pid_file"

    # Démarrage turbostat (en arrière-plan)
    if command -v turbostat >/dev/null 2>&1; then
      sudo turbostat --quiet --show PkgWatt,CorWatt,GFXWatt,CPU%c1,CPU%c3,CPU%c6,CPU%c7 -i 1 > "$power_file" &
      TURBO_PID=$!
      echo $TURBO_PID > "$tmp_pid_file"
      sleep 2  # stabilisation
    else
      echo "[!] turbostat non trouvé, pas de mesure énergétique"
      TURBO_PID=""
    fi

    START=$(date +%s%3N)
    case $runtime in
      docker)
        docker run --rm -v "${iteration_dir}/results:/app/results" "$IMAGE_NAME"
        ;;
      podman)
        podman run --rm -v "${iteration_dir}/results:/app/results" "$IMAGE_NAME"
        ;;
      crio)
        # Pour CRI-O, on récupère les résultats directement depuis la sortie
        crio_results=$(run_crio_once)
        if [ -n "$crio_results" ]; then
          echo "$crio_results" > "${iteration_dir}/perf_metrics.csv"
        fi
        ;;
      *)
        echo "[!] Runtime inconnu : $runtime"
        ;;
    esac
    END=$(date +%s%3N)
    DURATION=$((END - START))

    # Arrêter turbostat
    if [ -n "$TURBO_PID" ]; then
      sudo kill "$TURBO_PID" 2>/dev/null
      rm -f "$tmp_pid_file"
    fi

    echo "Durée d'exécution : ${DURATION} ms" | tee "$time_file"

    # Calcul moyenne turbostat (PkgWatt, CorWatt, GFXWatt, CPU%c6)
    if [ -f "$power_file" ]; then
      AVG_VALUES=$(awk '
        NR>1 && $1 ~ /^[0-9.]+$/ {
          sum1+=$1; sum2+=$2; sum3+=$3; sum4+=$6; count++
        }
        END {
          if(count>0)
            printf "%.2f,%.2f,%.2f,%.2f", sum1/count, sum2/count, sum3/count, sum4/count
          else
            print "NA,NA,NA,NA"
        }
      ' "$power_file")
    else
      AVG_VALUES="NA,NA,NA,NA"
    fi

    # Extraire les métriques de performance
    PERF_METRICS=$(extract_perf_metrics "$runtime" "$iteration_dir")

    # Ajout au CSV général
    echo "$iteration,$runtime,run,$DURATION,$AVG_VALUES,$PERF_METRICS,$power_file" >> "$CSV_FILE"

    echo "[✔] Fichiers générés dans $iteration_dir :"
    echo "  ↪ Énergie : $power_file"
    echo "  ↪ Temps   : $time_file"
    echo "  ↪ Métriques : $PERF_METRICS"
}

# Boucle sur runtimes et itérations
for runtime in "${RUNTIMES[@]}"; do
  for i in $(seq 1 $ITERATIONS); do
    run_with_runtime "$runtime" "$i"
  done
done

echo ""
echo "✅ Tous les tests terminés. Résultats dans : $OUTPUT_DIR"
