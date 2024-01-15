import os
import logging
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view

import json
from .utils import system_prompt
import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv
import requests
from urllib.parse import unquote, urlencode, urlparse, urlunparse

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
# AWS S3 Configuration
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
INVOICE_UPLOAD_BUCKET = "amazon-textract-bucket-174039713486"
EXCEL_REPORT_BUCKET = "textract-raw-result"
AWS_REGION = "ap-south-1"
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)

import pandas as pd 
import tempfile 
import os 

def generate_excel_file(data, filename):
    df = pd.DataFrame(data)
    temp_dir = tempfile.mkdtemp()
    # Save the Excel file in the temporary directory
    excel_file_path = os.path.join(temp_dir, f"{filename}.xlsx")
    df.to_excel(excel_file_path, index=False)
    return excel_file_path

@api_view(["POST", "GET"])
def upload_invoice(request):
    if request.method == "POST" and request.FILES.get("pdfFile"):
        pdf_file = request.FILES["pdfFile"]

        # Perform S3 upload using your S3 client
        s3_client.upload_fileobj(pdf_file, INVOICE_UPLOAD_BUCKET, pdf_file.name)

        return HttpResponse("File uploaded successfully!")
    return render(request, "invoice_upload.html")


def call_gpt(csv):
    user_prompt = f"""
    understand the invoice data given and give out the expected dictionary
    Input :- 
    {csv}

    """
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    content_data = response.choices[0].message.content
    return content_data


# textract output from lambda
@api_view(["POST"])
def handle_csv_upload(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            csv_data = data.get("csv_data", "")
            filename = data.get("file_name", "output")
            # print(filename)
            # print(csv_data)
            desired_dict = call_gpt(csv_data)
            # print(desired_dict)
            excel_file_path = generate_excel_file(desired_dict, filename)
            # print(excel_file_path)
            try:
                s3_client.upload_fileobj(excel_file_path, EXCEL_REPORT_BUCKET, f"{filename}.xlsx")
                print("Upload successful")
            except Exception as e:
                print(f"Error uploading to S3: {str(e)}")
               

            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
