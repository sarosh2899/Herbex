from flask import Flask, render_template, request, jsonify
from PIL import Image
import openai
from io import BytesIO
import requests
import time


# # Get the list of available models
# models = openai.Model.list()
# for model in models['data']:
#     print(model)
# @app.route('/generate', methods=['POST'])
def generate():
    
    try:
        print('Generating using Dalle')
        # Get the uploaded image file
        image_file = request.files['image']

        # # Read image file content
        # image_content = image_file.read()

        # # Encode image content as base64
        # encoded_image = base64.b64encode(image_content).decode('utf-8')

        # Set up the data payload with the API key
        data = {
            "image": image_file,
            "n": 2,
            "model": "dall-e-2",
            "size": "1024x1024",
        }

        # Make the API request to create image variations
        print('started_generating respo')
        response = openai.Image.create_variation(**data)
        print('done')
        # Extract the URL of the generated image
        generated_image_urls = [variation.url for variation in response.data]

        return jsonify({'success': True, 'data': generated_image_urls})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# @app.route('/generate-edit', methods=['POST'])
def generate_edit():
    try:
        # Get the uploaded image file
        image_file = request.files['image']
        image_file1 = request.files['image1']
        
        # Prompt for image editing (customize as needed)
        prompt = "Perfect fit body image"
        
        # Read the image content and convert to 'RGBA'
        image_content = Image.open(image_file)
        image_content = image_content.convert('RGBA')
        image_io = BytesIO()
        image_content.save(image_io, 'PNG')
        image_io.seek(0)

        # Read the mask content and convert to 'RGBA'
        mask_content = Image.open(image_file1)
        mask_content = mask_content.convert('RGBA')
        mask_io = BytesIO()
        mask_content.save(mask_io, 'PNG')
        mask_io.seek(0)

        # Set up the data payload with the API key
        data = {
            "image": image_io,
            # "mask": mask_io,
            "prompt": prompt,
            "n": 1,
            "model": "dall-e-2",
            "size": "1024x1024",
        }

        # Make the API request to create image variations
        response = openai.Image.create_edit(**data)

        # Extract the URL of the generated image
        generated_image_edit_urls = [variation.url for variation in response.data]

        return jsonify({'success': True, 'data': generated_image_edit_urls})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
