from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import io
from image_generation import create_barbie_image, fetch_image_from_task
from send_email import send_email
from create_mongodb_connection import create_connection_to_mongodb
from add_data_to_mongodb import add_data_to_collection
import logging
from remove_image_background import remove_background
from add_data_to_s3 import upload_user_image_to_s3
from create_s3_connection import create_s3_connection
from create_presigned_url import generate_presigned_url
import datetime
from crop_images import crop_quadrants_from_bytes
from post_image_operations import add_text_and_logo_to_image_bytes
import base64

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

class Config:
    # Set your OpenAI API key
    MIDJOURNEY_KEY = os.getenv("MIDJOURNEY_API_KEY")

    MONGODB_CONNECTION_STRING = os.getenv("connection_string")
    DATABASE_NAME = os.getenv("database_name")
    COLLECTION_NAME = os.getenv("collection_name")

    SENDER_EMAIL = os.getenv('sender_email')
    RECEIVER_EMAIL = os.getenv('receiver_email')
    SUBJECT = os.getenv('subject')
    SENDER_PASSWORD = os.getenv('sender_password')

    REMOVE_BACKGROUND_KEY = os.getenv('remove_background_key')
    API_URL = os.getenv('api_url')
    
    DEFAULT_FONT_PATH = os.getenv("DEFAULT_FONT")
    FONT_SIZE = os.getenv("FONT_SIZE")
    DEFAULT_LOGO_SIZE = os.getenv("DEFAULT_LOGO_SIZE")
    PADDING = os.getenv("PADDING")
    aws_access_key_id = os.getenv("aws_access_key_id")
    aws_secret_access_key = os.getenv("aws_secret_access_key")
    region = os.getenv("region")
    bucket_name = os.getenv("bucket_name")
    
    font_path = os.getenv("font_path")
    text_to_add = os.getenv("text_to_add")
    logo_path = os.getenv("logo_path")
    prefix = os.getenv("prefix")
    
    barbie_image_path_beach = os.getenv("barbie_image_path_beach")
    barbie_image_path_gym = os.getenv("barbie_image_path_gym")
    ken_image_path_beach = os.getenv("ken_image_path_beach")
    ken_image_path_gym = os.getenv("ken_image_path_gym")
    # email_message = os.getenv("message")
    

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_image():

    base64_list = []
    try:
        
        gender = request.form['gender']

        if gender == 'male':
            beach_image = Config.ken_image_path_beach
            gym_image = Config.ken_image_path_gym
        else:
            beach_image = Config.barbie_image_path_beach
            gym_image = Config.barbie_image_path_gym
            
        logger.info("Generating using Midjourney")

                # Extract data from the request
        name = request.form ['name']
        surname = request.form['surname']
        age = request.form['age']
        email = request.form['email']
        city = request.form['city']

        if not all([name, surname, age, email, city]):
            raise ValueError("Incomplete form data")

        user_image = request.files.get('image')
        if not user_image:
            raise ValueError("No image file provided")

        image_data = user_image.read()

        # Now you can use BytesIO to work with the image as bytes
        user_image = BytesIO(image_data)
        user_image = Image.open(user_image)

        # Remove background from an image
        background_removed_image = remove_background(Config.REMOVE_BACKGROUND_KEY, user_image, Config.API_URL)

        s3_client = create_s3_connection(Config.aws_access_key_id, Config.aws_secret_access_key, Config.region)

        object_name = upload_user_image_to_s3(s3_client, background_removed_image, Config.bucket_name, name)

        presigned_url = generate_presigned_url(s3_client, Config.bucket_name, object_name)
        quadrant_image_list = []
        
        presigned_image_list = []
        

        for character_image in [beach_image, gym_image]:
            barbie_image_urls = [presigned_url, character_image]
            
            
            # Generate an image using Midjourney
            barbie_response = create_barbie_image(Config.MIDJOURNEY_KEY, barbie_image_urls)
            print(barbie_response)
            task_id_barbie = barbie_response['task_id']
            generated_image, response = fetch_image_from_task(task_id_barbie)

            print(response)
            
            quadrants = crop_quadrants_from_bytes(generated_image)

            with open(Config.logo_path, 'rb') as logo_file:
                logo_bytes = logo_file.read()

            for quadrant_image_number in range(1):
                result_bytes = add_text_and_logo_to_image_bytes(quadrants[quadrant_image_number], Config.text_to_add, Config.font_path, logo_bytes)
                
                base_64_data = base64.b64encode(result_bytes)
                
                base64_list.append(base_64_data.decode('utf-8'))
                image_path = str(upload_user_image_to_s3(s3_client, result_bytes, Config.bucket_name, name))
                
                # image_path = Config.prefix + image_path
                
                quadrant_image_list.append(image_path)
                
                presigned_image_list.append(generate_presigned_url(s3_client, Config.bucket_name, image_path))


        current_datetime = datetime.datetime.now().isoformat()
        data = {
            "name": name,
            "age": age,
            "city": city,
            "datetime_str": current_datetime,
            "email": email,
            "surname": surname,
            "user_image": Config.prefix + object_name,
            "generated_images": {
                "gym1": quadrant_image_list[0],
                # "gym2": quadrant_image_list[1],
                "beach1": quadrant_image_list[1],
                # "beach2": quadrant_image_list[3]
            }
        }

        final_list = base64_list + presigned_image_list
        # print(final_list)
        print(presigned_image_list)
        # Connect to MongoDB
        client = create_connection_to_mongodb(Config.MONGODB_CONNECTION_STRING)
        logger.info('MongoDB connection done')

        # Add data to MongoDB collection
        result = add_data_to_collection(client, Config.DATABASE_NAME, Config.COLLECTION_NAME, data)

        email_message = """
            <html>
            <head>
                <style>
                body {
                    font-family: 'Arial', sans-serif;
                    margin: 0;
                    padding: 0;
                }
                .container {
                    background-color: #f8f8f8;
                    max-width: 600px;
                    margin: 0 auto;
                }
                .header {
                    background-color: #f03ab9;
                    color: #ffffff;
                    padding: 20px;
                    text-align: center;
                }
                .content {
                    padding: 30px;
                    text-align: center;
                }
                .button {
                    display: inline-block;
                    font-size: 16px;
                    font-weight: bold;
                    padding: 15px 30px;
                    margin-top: 20px;
                    text-decoration: none;
                    background-color: #3498db;
                    color: #ffffff;
                    border-radius: 5px;
                }
                .footer {
                    background-color: #f03ab9;
                    color: #ffffff;
                    text-align: center;
                    padding: 10px;
                }
                </style>
            </head>
            <body>
                <div class='container'>
                <div class='header'>
                    <h2>Download Your Images</h2>
                </div>
                <div class='content'>
                    <p>Thank you for having some fun with us!</p>
                    <p>We hope that you enjoyed igniting your hottest shape with our AI-image generator!</p>
                    <p>Please click <a href='https://google.com'>here</a> to download your FREE RESOURCES to ignite your hottest shape in 2024!
                    We have included exercise routines, eating plans, and more!</p>
                    <p>Our Herbex Team is on standby, should you need any information on products or advice on how to shed those extra kilos!</p>
                    <p>All the best, <br/>THE HERBEX TEAM</p>
                </div>
                <div class='footer'>
                    <p>Thank you for using our service.</p>
                </div>
                </div>
            </body>
            </html>
            """
        image_paths = ['image1.png', 'image2.png']
        # Send an email with the generated image
        email_status = send_email(Config.SENDER_EMAIL, email, Config.SUBJECT, email_message,base64_list, image_paths, Config.SENDER_PASSWORD)
        logger.info("Email status == %s", email_status)

        return jsonify({'success': True, 'data':final_list})

    except ValueError as value_error:

        logger.error("Value error: %s", value_error)
        return jsonify({'success': False, 'error': str(value_error)}), 400

    except FileNotFoundError as file_not_found_error:

        logger.exception("File not found error: %s", file_not_found_error)
        return jsonify({'success': False, 'error': 'File not found'}), 404

    except Exception as e:

        logger.exception("An error occurred during image generation: %s", e)
        return jsonify({'success': False, 'error': str(e)}), 500
    

if __name__ == '__main__':
    app.run(debug=True, port=5001)
