import time
import csv
import onnxruntime as ort
import numpy as np
import os

def run_benchmark():
    # Modifier ce chemin pour correspondre à l'emplacement dans le Dockerfile
    model_path = "/app/resnet50/model.onnx"
    
    # Créer le dossier results si inexistant
    os.makedirs("/app/results", exist_ok=True)
    
    session = ort.InferenceSession(model_path)
    input_name = session.get_inputs()[0].name

    dummy_input = np.random.rand(1, 3, 224, 224).astype(np.float32)

    iterations = 100
    latencies = []

    start_time = time.time()
    for _ in range(iterations):
        start = time.time()
        session.run(None, {input_name: dummy_input})
        end = time.time()
        latencies.append((end - start) * 1000)  # en ms

    end_time = time.time()

    total_duration = (end_time - start_time) * 1000  # en ms
    avg_latency = sum(latencies) / len(latencies)
    throughput = iterations / (total_duration / 1000)

    with open("/app/results/mlperf_resnet50_result.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["latency_ms", "throughput", "iterations", "duration_ms"])
        writer.writerow([round(avg_latency, 2), round(throughput, 2), iterations, round(total_duration, 2)])

    print(f"Latence moyenne: {avg_latency:.2f} ms")
    print(f"Throughput: {throughput:.2f} inférences/sec")

if __name__ == "__main__":
    run_benchmark()
