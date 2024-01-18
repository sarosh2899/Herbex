from datetime import datetime, timedelta

def generate_presigned_url(s3, bucket_name, object_key, expiration_minutes=25):
    # Generate a pre-signed URL with an expiry of specified minutes
    expiration_time = datetime.now() + timedelta(minutes=expiration_minutes)
    presigned_url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': object_key},
        ExpiresIn=expiration_minutes * 30,  # Convert minutes to seconds
    )
    return presigned_url
