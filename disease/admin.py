# disease/admin.py

from django.contrib import admin
from .models import CsvData, ModelResult

admin.site.register(CsvData)
admin.site.register(ModelResult)
