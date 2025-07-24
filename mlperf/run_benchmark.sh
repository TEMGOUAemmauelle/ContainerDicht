import onnxruntime as ort
import numpy as np

sess = ort.InferenceSession("resnet50/model.onnx")
input_name = sess.get_inputs()[0].name
x = np.random.rand(1, 3, 224, 224).astype(np.float32)
pred = sess.run(None, {input_name: x})
print("Output shape:", np.array(pred).shape)

