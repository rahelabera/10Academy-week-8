import os
import csv
import pandas as pd
from ultralytics import YOLO

# Load YOLOv8 nano model
model = YOLO('yolov8n.pt')  # Downloads if not present

# Classification logic
def classify_detections(detections):
    has_person = any(d == 'person' for d in detections)
    has_product = any(d in ['bottle', 'cup', 'bowl'] for d in detections)  # Approximate medical products
    if has_person and has_product:
        return 'promotional'
    elif has_product:
        return 'product_display'
    elif has_person:
        return 'lifestyle'
    else:
        return 'other'

# Scan images and detect
results = []
for root, dirs, files in os.walk('data/raw/images'):
    for file in files:
        if file.endswith('.jpg'):
            img_path = os.path.join(root, file)
            channel_name = os.path.basename(root)
            message_id = os.path.splitext(file)[0]
            
            # Run detection
            detection = model(img_path)[0]
            detected_objects = [model.names[int(cls)] for cls in detection.boxes.cls] if detection.boxes else []
            confidences = detection.boxes.conf.tolist() if detection.boxes else []
            
            category = classify_detections(detected_objects)
            
            results.append({
                'message_id': message_id,
                'channel_name': channel_name,
                'img_path': img_path,
                'detected_objects': ','.join(detected_objects),
                'confidence_scores': ','.join(map(str, confidences)),
                'image_category': category
            })

# Save to CSV
os.makedirs('data', exist_ok=True)
csv_path = 'data/yolo_results.csv'
pd.DataFrame(results).to_csv(csv_path, index=False)
print(f'Results saved to {csv_path}')