from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
import pandas as pd
from datetime import datetime
import csv
import pickle
import numpy as np
import subprocess
import os
from django.contrib.auth.models import User
from .models import PredictionResult
import matplotlib.pyplot as plt
from io import BytesIO
import base64


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
    fs = FileSystemStorage()
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
    print("weight_result : ", weight_result.shape)

    predicted_length = length_result[0][-1][-1]
    predicted_weight = weight_result[0][-1][-1]
    print("7일 후 길이 : ", predicted_length)
    print("7일 후 무게 : ", predicted_weight)

    # DataFrame 생성
    date_range = range(length_result.shape[1])
    length_values = length_result[0, :, 0]
    weight_values = weight_result[0, :, 0]
    food_values = [0] * length_result.shape[1]

    data = {
        'date': date_range,
        'length': length_values,
        'weight': weight_values,
        'food': food_values
    }

    df = pd.DataFrame(data)

    # 결과 CSV 파일로 저장
    result_filename = f'result_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    result_file_path = os.path.join(fs.location, result_filename)
    df.to_csv(result_file_path, index=False)

    PredictionResult.objects.create(
        user=request.user,
        csv_file_path=file_path,
        result_csv_file_path=result_file_path,
    )

     # DB에서 해당 유저의 최근 예측 결과 가져오기
    prediction_result = PredictionResult.objects.filter(user=request.user).latest('created_at')

    input_csv_path = prediction_result.csv_file_path
    result_csv_path = prediction_result.result_csv_file_path

    # Load input CSV data (last 10 rows)
    input_df = pd.read_csv(input_csv_path).tail(10)
    input_length = input_df['length'].values
    input_weight = input_df['weight'].values

    # Load output CSV data (all 7 rows)
    output_df = pd.read_csv(result_csv_path)
    output_length = output_df['length'].values
    length_output = []
    length_output.append(input_length[-1])
    for item in output_length : 
        length_output.append(item)

    output_weight = output_df['weight'].values
    weight_output = []
    weight_output.append(input_weight[-1])
    for item in output_weight :
        weight_output.append(item)

    # Create plot
    plt.figure(figsize=(10, 6))
    plt.rcParams['font.family'] ='Malgun Gothic'
    plt.rcParams['axes.unicode_minus'] =False

    # Plot input data (lighter)
    plt.plot(range(1, 11), input_length, 'b-', alpha=0.5, label='과거 길이')
    plt.plot(range(1, 11), input_weight, 'r-', alpha=0.5, label='과거 무게')

    # Plot output data (darker)
    plt.plot(range(10, 18), length_output, 'b--', label='예측 길이')
    plt.plot(range(10, 18), weight_output, 'r--', label='예측 무게')

    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.legend()
    plt.title('성장 그래프')

    # Save plot to a bytes buffer
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    graph_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    context = {
        'length': predicted_length,
        'weight': predicted_weight,
        'graph' : graph_base64
    }
    return render(request, 'prediction/result.html', context)