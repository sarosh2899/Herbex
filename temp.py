import openai
# from flask import Flask, render_template, request, jsonify
import base64
import openai
from dotenv import load_dotenv
import os
from PIL import Image
from io import BytesIO

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate():
        # Get the uploaded image file
        image_file = open('/home/unthinkable/Pictures/elon_musk_resized.png', 'rb')
        
        # # Read image file content
        # image_content = image_file.read()
        # image_content = Image.open(image_file)
        # image_content = image_content.resize((256,256))
        # image_content.save('/home/unthinkable/Pictures/image_edit_mask_resized.png') 
        # image_io = BytesIO()
        # # Encode image content as base64
        # encoded_image = base64.b64encode(image_content).decode('utf-8')

        # Set up the data payload with the API key
        data = {
            "image": image_file,
            "n": 1,
            "model": "dall-e-2",
            "size": "256x256",
            "prompt":'Create a barbie image'
            
        }

        # Make the API request to create image variations
        print('started_generating respo')
        response = openai.Image.create_variation(**data)
        print('done')
        # Extract the URL of the generated image
        generated_image_urls = [variation.url for variation in response.data]
        
        print(generated_image_urls)
        
(generate())

def generate_edit():
        # Get the uploaded image file
        
        image_file = open('/home/unthinkable/Pictures/image_edit_mask.png', 'rb')
        image_file1 = open('/home/unthinkable/Pictures/image_edit_original.png', 'rb')
        
        # Prompt for image editing (customize as needed)
        prompt = "Create a barbie image out of it"
        
        # Read the image content and convert to 'RGBA'
        image_content = Image.open(image_file)
        image_content = image_content.resize((256,256))
        image_content = image_content.convert('RGBA')
        image_io = BytesIO()
        image_content.save(image_io, 'PNG')
        image_data = image_io.getvalue()

        # Read the mask content and convert to 'RGBA'
        mask_content = Image.open(image_file1)
        mask_content = mask_content.resize((256,256))
        
        mask_content = mask_content.convert('RGBA')
        mask_io = BytesIO()
        mask_content.save(mask_io, 'PNG')
        mask_data = mask_io.getvalue()

        # Set up the data payload with the API key
        data = {
            "image": image_data,
            "mask": mask_data,
            "prompt": prompt,
            "n": 1,
            "model": "dall-e-2",
            "size": "256x256",
            # 'api_key':''

        }

        # Make the API request to create image variations
        response = openai.Image.create_edit(**data)

        # Extract the URL of the generated image
        generated_image_edit_urls = [variation.url for variation in response.data]
        print(generated_image_edit_urls)
        
        
# generate_edit() 
