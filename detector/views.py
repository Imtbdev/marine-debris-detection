import os
import json
from django.shortcuts import render
from .forms import ImageUploadForm
from ultralytics import YOLO
from django.conf import settings

MODEL_PATH = '../model_pt/best_robo.pt'

model = YOLO(MODEL_PATH)


def upload_and_detect(request):
    result_image_url = None
    json_file_url = None
    total_objects_detected = 0

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save()
            image_path = uploaded_image.image.path

            results = model(image_path)

            detections = []
            for result in results[0].boxes:
                bbox = result.xyxy[0].tolist()
                cls = result.cls.tolist()
                conf = result.conf.tolist()
                detections.append({
                    'bbox': bbox,
                    'class': cls,
                    'confidence': conf
                })

            total_objects_detected = len(detections)

            detection_data = {
                'image_name': os.path.basename(image_path),
                'total_objects_detected': total_objects_detected,
                'detections': detections
            }

            results_dir = os.path.join(settings.MEDIA_ROOT, 'results')
            os.makedirs(results_dir, exist_ok=True)

            json_filename = f"{os.path.splitext(os.path.basename(image_path))[0]}_results.json"
            json_path = os.path.join(results_dir, json_filename)
            with open(json_path, 'w') as json_file:
                json.dump(detection_data, json_file, indent=4)

            json_file_url = settings.MEDIA_URL + 'results/' + json_filename

            result_image_path = os.path.join(results_dir, os.path.basename(image_path))
            results[0].save(result_image_path)

            result_image_url = settings.MEDIA_URL + 'results/' + os.path.basename(image_path)

    else:
        form = ImageUploadForm()

    return render(request, 'upload_and_detect.html', {
        'form': form,
        'result_image_url': result_image_url,
        'json_file_url': json_file_url,
        'total_objects_detected': total_objects_detected
    })
