
from django.db import models
from django.contrib.auth.models import User

class CsvData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_path = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class ModelResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    label = models.CharField(max_length=255)
    probability = models.FloatField()
    file_name = models.CharField(max_length=255)  # 추가된 필드
