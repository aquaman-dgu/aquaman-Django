# prediction/models.py
from django.db import models
from django.contrib.auth.models import User

class PredictionResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    csv_file_path = models.CharField(max_length=255)
    result_csv_file_path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PredictionResult by {self.user.username} on {self.created_at}"
