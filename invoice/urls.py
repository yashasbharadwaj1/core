# urls.py
from django.urls import path
from .views import upload_invoice,handle_csv_upload

app_name = "invoice"

urlpatterns = [
    path('upload/', upload_invoice, name='upload_invoice'), 
    path('upload/csv/output',handle_csv_upload,name='csv_upload')
    
]
