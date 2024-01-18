from PIL import Image
import boto3
from io import BytesIO
from datetime import datetime, timedelta
import uuid

# def upload_user_image_to_s3(s3, image, bucket_name, user_id):
    # if image.mode == 'RGBA':
    #     image = image.convert('RGB')


#     # Create a unique identifier for the image based on user ID, timestamp, and UUID
#     unique_identifier = f"{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex}"

#     object_key = f"{unique_identifier}.jpg"  # Adjust the file extension as needed

#     image_bytes = BytesIO()
#     image.save(image_bytes, format='JPEG')  # Change format as needed

#     # Upload the image bytes to S3
#     try:
#         image_bytes.seek(0)  # Reset the stream position
#         s3.upload_fileobj(image_bytes, bucket_name, object_key)
#         print(f"Image uploaded to {bucket_name}/{object_key}")
#     except Exception as e:
#         print(f"Error uploading image to S3: {e}")

#     return object_key
def upload_user_image_to_s3(s3, image_bytes, bucket_name, user_id):
    # Upload the image bytes to S3
    try:
        
        # Create a unique identifier for the image based on user ID, timestamp, and UUID
        unique_identifier = f"{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex}"

        object_key = f"{unique_identifier}.jpg"  # Adjust the file extension as needed
        print("object key -----", object_key)
        s3.upload_fileobj(BytesIO(image_bytes), bucket_name, object_key)
        print(f"Image uploaded to {bucket_name}/{object_key}")
        return object_key
    except Exception as e:
        print(f"Error uploading image to S3: {e}")
        return ''