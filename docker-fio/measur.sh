#!/bin/bash

# === CONFIGURATION ===
IMAGE_NAME="mon-image-fio"
RUNTIMES=("docker" "podman" "crio")
ITERATIONS=10
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
OUTPUT_DIR="./output_RUN_${TIMESTAMP}"
mkdir -p "$OUTPUT_DIR"

CSV_FILE="${OUTPUT_DIR}/benchmark_startup.csv"
echo "iteration,runtime,startup_duration_ms,time_file" > "$CSV_FILE"

# Fonction pour lancer un conteneur avec CRI-O et mesurer le temps de démarrage
run_crio_once() {
  local POD_UID=$(uuidgen)
  local TMPDIR="/tmp/crio_run_$$"
  mkdir -p "$TMPDIR"
  local POD_JSON="$TMPDIR/pod.json"
  local CONTAINER_JSON="$TMPDIR/container.json"
  local power_file="$1"
  local time_file="$2"

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
    "name": "fio-container"
  },
  "image": {
    "image": "localhost:5000/${IMAGE_NAME}"
  },
  "log_path": "fio-container.log"
}
EOF

  START=$(date +%s%3N)

  POD_ID=$(sudo crictl runp "$POD_JSON" 2>/dev/null)
  if [ -z "$POD_ID" ]; then
    echo "[✘] Erreur : création pod CRI-O"
    rm -rf "$TMPDIR"
    return 1
  fi

  CONTAINER_ID=$(sudo crictl create "$POD_ID" "$CONTAINER_JSON" "$POD_JSON" 2>/dev/null)
  if [ -z "$CONTAINER_ID" ]; then
    echo "[✘] Erreur : création conteneur CRI-O"
    sudo crictl stopp "$POD_ID" >/dev/null 2>&1
    sudo crictl rmp "$POD_ID" >/dev/null 2>&1
    rm -rf "$TMPDIR"
    return 1
  fi

  sudo crictl start "$CONTAINER_ID" >/dev/null 2>&1

  for i in {1..100}; do
    STATUS=$(sudo crictl inspect "$CONTAINER_ID" | grep '"state"' | awk -F'"' '{print $4}')
    if [[ "$STATUS" == "CONTAINER_RUNNING" ]]; then
      break
    fi
    sleep 0.0001
  done

  END=$(date +%s%3N)
  DURATION=$((END - START))
  echo "$DURATION" > "$time_file"

  sudo crictl logs "$CONTAINER_ID"

  sudo crictl rm "$CONTAINER_ID" >/dev/null 2>&1
  sudo crictl stopp "$POD_ID" >/dev/null 2>&1
  sudo crictl rmp "$POD_ID" >/dev/null 2>&1
  rm -rf "$TMPDIR"

  return 0
}

# Fonction principale par runtime
run_with_runtime() {
  local runtime=$1
  local iteration=$2

  local iteration_dir="${OUTPUT_DIR}/run${iteration}_${runtime}"
  mkdir -p "$iteration_dir"

  local time_file="${iteration_dir}/time.txt"

  echo ""
  echo "==============================="
  echo "[🚀] Runtime : $runtime - Itération : $iteration"
  echo "==============================="

  case $runtime in
    docker)
      START=$(date +%s%3N)
      CONTAINER_ID=$(docker run -d --runtime=runc "$IMAGE_NAME")
      for i in {1..100}; do
        STATUS=$(docker inspect -f '{{.State.Status}}' "$CONTAINER_ID")
        if [[ "$STATUS" == "running" ]]; then
          break
        fi
        sleep 0.01
      done
      END=$(date +%s%3N)
      DURATION=$((END - START))
      echo "$DURATION" > "$time_file"
      docker stop "$CONTAINER_ID" >/dev/null
      docker rm "$CONTAINER_ID" >/dev/null
      ;;

    podman)
      START=$(date +%s%3N)
      CONTAINER_ID=$(podman run -d --runtime=crun "$IMAGE_NAME")
      for i in {1..100}; do
        STATUS=$(podman inspect -f '{{.State.Status}}' "$CONTAINER_ID")
        if [[ "$STATUS" == "running" ]]; then
          break
        fi
        sleep 0.0001
      done
      END=$(date +%s%3N)
      DURATION=$((END - START))
      echo "$DURATION" > "$time_file"
      podman stop "$CONTAINER_ID" >/dev/null
      podman rm "$CONTAINER_ID" >/dev/null
      ;;

    crio)
      run_crio_once "$power_file" "$time_file"
      DURATION=$(cat "$time_file")
      ;;

    *)
      echo "[!] Runtime inconnu : $runtime"
      return 1
      ;;
  esac

  echo "Temps de démarrage : ${DURATION} ms"
  echo "$iteration,$runtime,$DURATION,$time_file" >> "$CSV_FILE"

  echo "[✔] Itération $iteration terminée ($runtime)."
}

# Boucle principale
for runtime in "${RUNTIMES[@]}"; do
  for i in $(seq 1 $ITERATIONS); do
    run_with_runtime "$runtime" "$i"
  done
done

echo ""
echo "✅ Tous les benchmarks sont terminés."
echo "📁 Résultats disponibles dans : $OUTPUT_DIR"
