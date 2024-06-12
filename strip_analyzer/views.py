from django.shortcuts import render
import cv2
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage

def process_image(image_path):
    # Read the image using OpenCV
    img = cv2.imread(image_path)
    
    # Convert to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Assuming the strips are vertically aligned and have consistent spacing
    height, width, _ = img_rgb.shape
    strip_height = height // 10
    
    colors = {}
    labels = ['URO', 'BIL', 'KET', 'BLD', 'PRO', 'NIT', 'LEU', 'GLU', 'SG', 'PH']
    
    for i, label in enumerate(labels):
        strip_section = img_rgb[i * strip_height: (i + 1) * strip_height, :]
        mean_color = strip_section.mean(axis=(0, 1)).astype(int).tolist()
        colors[label] = mean_color
    
    return colors

@csrf_exempt
def analyze_strip(request):
    try:
        if request.method == 'POST' and 'image' in request.FILES:
            # Save uploaded image
            image = request.FILES['image']
            file_name = default_storage.save(image.name, image)
            file_path = default_storage.path(file_name)
            
            # Process the image
            result = process_image(file_path)
            
            # Clean up
            default_storage.delete(file_name)
            
            return JsonResponse(result)
        else:
            return JsonResponse({'error': 'Strip Image not selected'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
def home(request):
    return render(request, 'home.html')