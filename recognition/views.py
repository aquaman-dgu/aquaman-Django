import torch
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from PIL import Image

# YOLOv8 모델 로드 함수
def load_model(model_path):
    model = torch.load(model_path, map_location=torch.device('cpu'))  # 직접 모델 파일을 로드
    model.eval()
    return model

# 모델 인스턴스 생성
recognition_model = load_model('recognition/model/recognition.pt')
disease_model = load_model('recognition/model/disease.pt')

def main_view(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        image_path = fs.path(filename)

        # 이미지 처리 및 객체 인식
        img = Image.open(image_path)
        results = recognition_model(img)

        # 각 자른 이미지를 disease 모델로 처리
        disease_results = []
        for crop_img in results:
            result = disease_model(crop_img)
            disease_results.append(result)

        # 결과 페이지로 리다이렉트
        request.session['disease_results'] = disease_results
        return redirect('recognition:result_view')

    return render(request, 'recognition/main.html')

def result_view(request):
    disease_results = request.session.get('disease_results', [])
    return render(request, 'recognition/result.html', {'disease_results': disease_results})
