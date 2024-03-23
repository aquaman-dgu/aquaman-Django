from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.urls import reverse

# Create your views here.

def recognition_view(request):
    photo_name = request.session.get('photo')
    if photo_name:
        photo_path = default_storage.save(photo_name, ContentFile(request.FILES['photo'].read()))
        # 이미지 처리 로직, 예: 모델 예측 등
        
        # 예: recognition_result = recognition_model.predict(image)
        recognition_result = "넙치 객체 인식 결과"
        
        # 결과를 세션에 저장
        request.session['recognition_result'] = recognition_result
    return redirect(reverse('disease:disease_view'))
