# disease/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
import csv
import pickle
import numpy as np
import subprocess
import os
from .forms import CsvUploadForm
from .models import CsvData, ModelResult

current_dir = os.path.dirname(os.path.abspath(__file__))
disease_prediction_path = os.path.join(current_dir, '..', 'DLinear', 'PatchTST', 'PatchTST_supervised', 'disease_prediction.py')

def normalize(value, zero, one):
    return (value - zero) / (one - zero) 

@login_required
def main_view(request):
    if request.method == 'POST' and 'csv_file' in request.FILES:
        form = CsvUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            fs = FileSystemStorage()
            filename = fs.save(csv_file.name, csv_file)
            file_path = fs.path(filename)
            
            CsvData.objects.create(
            user=request.user,
            file_path=file_path
            )

            # 세션에 파일 경로와 이름 저장
            request.session['csv_file_path'] = file_path
            request.session['csv_file_name'] = filename

            # 세션 저장 확인
            if request.session.get('csv_file_path') and request.session.get('csv_file_name'):
                print("File path and name stored in session.")
            else:
                print("Failed to store file path and name in session.")
            
            return redirect('disease:result')
    else:
        form = CsvUploadForm()
    return render(request, 'disease/main.html', {'form': form})

@login_required
def result_view(request):
    file_path = request.session.get('csv_file_path')
    csv_file_name = request.session.get('csv_file_name')

    if not file_path or not csv_file_name:
        print("Missing file path or file name in session.")
        return redirect('disease:main')

    # CSV 파일 경로를 subprocess에 전달하여 예측 수행
    subprocess.run(['python', disease_prediction_path, file_path], capture_output=True, text=True)

    # 예측 결과 파일 불러오기
    disease_result = np.load(os.path.join(current_dir, '..', 'result', 'disease', 'real_prediction.npy'))
    disease_list = [disease_result[0][i][0] for i in range(24)]
    
    one = 0.51808286
    zero = -1.9301933
    pred_list = [normalize(value, zero, one) for value in disease_list]
    
    probability = sum(pred_list) / len(pred_list)
    label = "질병 발생 고위험" if abs(probability - 1) < abs(probability) else "질병 발생 저위험"
    probability = probability * 100

    # 모델 결과 데이터베이스에 저장
    ModelResult.objects.create(
        user=request.user,
        label=label,
        probability=probability,
        file_name=csv_file_name
    )

    context = {
        'label': label,
        'probability': probability
    }
    return render(request, 'disease/result.html', context)
