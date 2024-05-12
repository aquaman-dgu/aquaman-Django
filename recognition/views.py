import os
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from PIL import Image
from ultralytics import YOLO

recognition_model = YOLO('recognition/model/recognition.pt')
disease_model = YOLO('recognition/model/disease.pt')

def main_view(request):
    if request.method == 'POST' and request.FILES['image']:
        image_file = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image_file.name, image_file)
        
        # 파일의 실제 시스템 경로를 가져옵니다
        image_path = fs.path(filename)

        # Recognition 모델을 사용하여 이미지에서 객체를 인식
        result = recognition_model.predict(image_path, save = True, retina_masks=True, imgsz = 640, 
                               conf=0.2, save_crop=True, project=os.getcwd())
        
        image_directory = 'predict/crops/넙치'
        
        for filename in os.listdir(image_directory):
            if filename.endswith('.jpg') or filename.endswith('.png'):  # 이미지 파일 확인
                file_path = os.path.join(image_directory, filename)  # 파일의 전체 경로
                
                result = disease_model.predict(file_path, save = True, retina_masks=True, imgsz = 640, 
                               conf=0.3, project=os.getcwd() + '/results')
        return redirect('recognition:result')
    return render(request, 'recognition/main.html')

def result_view(request):
    return render(request, 'recognition/result.html')
