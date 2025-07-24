FROM python:3.9-slim

RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*
RUN pip install onnxruntime numpy

WORKDIR /app
RUN mkdir -p resnet50 && \
    wget -O resnet50/model.onnx https://github.com/onnx/models/raw/main/validated/vision/classification/resnet/model/resnet50-v2-7.onnx

COPY run_inference.py .

# Créer le dossier results à l'avance
RUN mkdir -p /app/results

CMD ["python", "run_inference.py"]
