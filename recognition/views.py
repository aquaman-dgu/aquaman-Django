from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from ultralytics import YOLO
from PIL import Image
import os
import shutil

recognition_model = YOLO('recognition/model/recognition.pt')
disease_model = YOLO('recognition/model/disease.pt')

@login_required
def main_view(request):
    #이미지 입력 응답이 들어오면
    if request.method == 'POST' and request.FILES['image']:
        
        #기존 disease 결과 이미지 제거
        static_dir = os.path.join(os.getcwd(), 'static')
        image_files = [f for f in os.listdir(static_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
        for file_name in image_files:
            file_path = os.path.join(static_dir, file_name)
            os.remove(file_path)
        
        image_file = request.FILES['image']
        fs = FileSystemStorage()
        rfilename = fs.save(image_file.name, image_file)
        image_path = fs.path(rfilename)
        source = Image.open(image_path)
        
        #recognition 모델
        results = recognition_model(source)
        
        recognition_directory = '넙치'
        
        #recognition 모델 결과 저장
        for result in results:
            result.save_crop(save_dir = os.getcwd())
        
        for filename in os.listdir(recognition_directory):
            if filename.endswith('.jpg') or filename.endswith('.png'):  # 이미지 파일 확인
                image_path = os.path.join(recognition_directory, filename)  # 파일의 전체 경로
                source = Image.open(image_path)
                
                #disease 모델
                results = disease_model(source)
                
                #diease 모델 결과 저장
                for result in results:
                    result.save()
                    
        #recognition 모델 결과 폴더 제거
        shutil.rmtree(recognition_directory)
        
        # 결과 이미지 파일을 static 폴더로 이동
        image_files = [f for f in os.listdir(os.getcwd()) if f.endswith(('.png', '.jpg', '.jpeg'))]
        for file_name in image_files:
            source_path = os.path.join(os.getcwd(), file_name)
            target_path = os.path.join(os.getcwd(), 'static', file_name)
            shutil.move(source_path, target_path)
        
        return redirect('recognition:result')
    return render(request, 'recognition/main.html')

@login_required
def result_view(request):
    static_dir = os.path.join(os.getcwd(), 'static')
    
    # static 디렉토리 내의 모든 이미지 파일 리스트
    image_files = [f for f in os.listdir(static_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]

    # 이미지 파일의 URL 리스트 생성
    image_urls = [os.path.join('/static', file_name) for file_name in image_files]

    return render(request, 'recognition/result.html', {'image_urls': image_urls})
