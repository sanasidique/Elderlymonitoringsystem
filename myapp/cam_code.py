import cv2
import numpy as np

# --- 1. Load Model & Config ---
weights_path = r"C:\Users\user\PycharmProjects\monitoringsystem\myapp\yolo-coco/yolov3.weights"
config_path = r"C:\Users\user\PycharmProjects\monitoringsystem\myapp\yolo-coco/yolov3"
names_path = r"C:\Users\user\PycharmProjects\monitoringsystem\myapp\yolo-coco/coco.names"

net = cv2.dnn.readNetFromDarknet(config_path, weights_path)
# Optionally set CUDA backend for GPU acceleration
# net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
# net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# --- 2. Load Class Names ---
with open(names_path, 'r') as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
# Get output layer names (YOLOv3 uses three scales)
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# --- 3. Preprocess Image ---
image = cv2.imread(r"D:\elderlycaremonitori ng\media\WIN_20230925_19_51_29_Pro.jpg")
height, width, channels = image.shape
blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False) # 416x416 is common

# --- 4. Forward Pass ---
net.setInput(blob)
outs = net.forward(output_layers)

# --- 5. Process Detections ---
boxes = []
confidences = []
class_ids = []
for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.5: # Confidence Threshold
            # Scale coordinates back to original image size
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)
            x = int(center_x - w / 2)
            y = int(center_y - h / 2)
            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)

# Apply Non-Maximum Suppression (NMS)
indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4) # 0.5 conf, 0.4 IoU threshold

# --- 6. Draw Results ---
font = cv2.FONT_HERSHEY_PLAIN
colors = np.random.uniform(0, 255, size=(len(classes), 3))
# --- 6. Draw Results ---
if len(indexes) > 0:
    for i in indexes.flatten():
        x, y, w, h = boxes[i]
        label = str(classes[class_ids[i]])
        confidence = str(round(confidences[i], 2))
        color = colors[class_ids[i]]

        # Draw bounding box
        cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)

        # Add label and confidence score
        text = f"{label} {confidence}"
        cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 2, color, 2)

# --- 7. Display/Save Image ---
cv2.imshow("YOLOv3 Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
# Optional: cv2.imwrite("output.jpg", image)
