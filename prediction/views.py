from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
import csv
import pickle
import numpy as np
import subprocess
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

length_prediction_path = os.path.join(current_dir, '..', 'DLinear', 'PatchTST', 'PatchTST_supervised', 'length_prediction.py')
weight_prediction_path = os.path.join(current_dir, '..', 'DLinear', 'PatchTST', 'PatchTST_supervised', 'weight_prediction.py')


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
        
        return redirect('prediction:result')
    return render(request, 'prediction/main.html')

@login_required
def result_view(request):
    file_path = request.session.get('csv_file_path')
    csv_file_name = file_path.split()[-1]

    if not file_path or not csv_file_name:
        print("Missing file path or file name in session.")
        return redirect('prediction:main')

    # CSV 파일 경로를 subprocess에 전달하여 예측 수행
    length_result = subprocess.run(['python', length_prediction_path, file_path], capture_output=True, text=True)
    print("Length Prediction Result:", length_result.stdout)
    print("Length Prediction Error:", length_result.stderr)
    weight_result = subprocess.run(['python', weight_prediction_path, file_path], capture_output=True, text=True)
    print("Weight Prediction Result:", weight_result.stdout)
    print("Weight Prediction Error:", weight_result.stderr)

    # 예측 결과 파일 불러오기
    length_result = np.load(os.path.join(current_dir, '..', 'result', 'length', 'real_prediction.npy'))
    weight_result = np.load(os.path.join(current_dir, '..', 'result', 'weight', 'real_prediction.npy'))

    predicted_length = length_result[0][0][0]
    predicted_weight = weight_result[0][0][0]
    print("7일 후 길이 : ", predicted_length)
    print("7일 후 무게 : ", predicted_weight)

    context = {
        'length': predicted_length,
        'weight': predicted_weight,
    }
    return render(request, 'prediction/result.html', context)