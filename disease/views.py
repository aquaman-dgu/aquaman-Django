from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
import csv
import pickle
import numpy as np
import subprocess
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

disease_prediction_path = os.path.join(current_dir, '..', 'DLinear', 'PatchTST', 'PatchTST_supervised', 'disease_prediction.py')

def normalize(value, zero, one) :
    return (value - zero) / (one - zero) 


@login_required
def main_view(request):
    if request.method == 'POST' and 'csv_file' in request.FILES:
        csv_file = request.FILES['csv_file']
        print(csv_file)
        fs = FileSystemStorage()
        filename = fs.save(csv_file.name, csv_file)
        file_path = fs.path(filename)
        
        # 세션에 파일 경로와 이름 저장
        request.session['csv_file_path'] = file_path
        request.session['csv_file_name'] = filename

        # 세션 저장 확인
        if request.session.get('csv_file_path') and request.session.get('csv_file_name'):
            print("File path and name stored in session.")
        else:
            print("Failed to store file path and name in session.")
        
        return redirect('disease:result')
    return render(request, 'disease/main.html')

@login_required
def result_view(request):
    file_path = request.session.get('csv_file_path')
    csv_file_name = file_path.split()[-1]

    if not file_path or not csv_file_name:
        print("Missing file path or file name in session.")
        return redirect('disease:main')

    # CSV 파일 경로를 subprocess에 전달하여 예측 수행
    disease_result = subprocess.run(['python', disease_prediction_path, file_path], capture_output=True, text=True)

    # 예측 결과 파일 불러오기
    disease_result = np.load(os.path.join(current_dir, '..', 'result', 'disease', 'real_prediction.npy'))
    disease_list = []

    for i in range(24) :
        disease_list.append(disease_result[0][i][0])
    
    one = 0.51808286
    zero = -1.9301933

    pred_list = [normalize(value, zero, one) for value in disease_list]

    probability = sum(pred_list) / len(pred_list)
    if abs(probability - 1) < abs(probability) :
        label = "질병 발생 고위험"
    else :
        label = "질병 발생 저위험"
    probability = probability * 100

    context = {
        'label': label,
        'probability' : probability
    }
    return render(request, 'disease/result.html', context)