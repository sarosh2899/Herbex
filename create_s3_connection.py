import boto3
from botocore.client import Config


def create_s3_connection(aws_access_key_id, aws_secret_access_key,region ):
    
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,region_name = region, config=Config(signature_version='s3v4'), endpoint_url='https://user-details-herbex.s3.eu-north-1.amazonaws.com')
    return s3