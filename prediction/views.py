from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import pickle

# Create your views here.

#로그인 필요
@login_required
def main_view(request):
    # 유저 메인 화면 렌더링
    return render(request, 'prediction/main.html')

# 모델 로드 (예를 들어 전역 변수로 사용)
model = pickle.load('model.pkl')

def main_view(request):
    if request.method == 'POST':
        length = float(request.POST['length'])
        weight = float(request.POST['weight'])
        processed_data = preprocess(length, weight)
        prediction = model.predict([processed_data])[0]
        return redirect('prediction:result_view', prediction=prediction)
    return render(request, 'prediction/main.html')

def result_view(request, prediction):
    return render(request, 'prediction/result.html', {'prediction': prediction})


def preprocess(length, weight):
    return [length, weight]