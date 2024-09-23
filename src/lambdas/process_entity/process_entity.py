import boto3
from faker import Faker
import openpyxl
from openpyxl import Workbook
from io import BytesIO
import os

fake = Faker()
s3 = boto3.client('s3')
bucket_name = os.environ['BUCKET_NAME']

def handler(event, context):
    entity = event['entity']
    total_count = event['totalCount']
    columns = event['columns']

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = entity

    for _ in range(total_count):
        row = [getattr(fake, key)() for key in keys]
        sheet.append(row)

    file_stream = BytesIO()
    workbook.save(file_stream)
    file_stream.seek(0)

    s3_key = f"{entity}.xlsx"
    
    s3.put_object(Bucket=bucket_name, Key=s3_key, Body=file_stream)
    
    # Generate a presigned URL
    presigned_url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': s3_key},
        ExpiresIn=3600
    )
    
    return {
        "presigned_url": presigned_url
    }
