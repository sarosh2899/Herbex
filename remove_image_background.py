from PIL import Image
from io import BytesIO
import requests
from typing import Optional

def remove_background(api_key: str, image: Image.Image, api_url='https://api.remove.bg/v1.0/removebg') -> Optional[bytes]:
    """
    Remove the background from an image using the remove.bg API.

    Args:
        api_key (str): The API key for remove.bg.
        image (Image.Image): The PIL Image object.

    Returns:
        bytes or None: The image content with removed background, or the original image on error.

    Raises:
        Exception: If an error occurs during the API request.
    """
    try:
        image_bytes = BytesIO()
        image.save(image_bytes, format='PNG')  # Assuming remove.bg API expects PNG format

        response = requests.post(
            api_url,
            files={'image_file': image_bytes.getvalue()},
            data={'size': 'auto'},
            headers={'X-Api-Key': api_key},
        )

        if response.status_code == requests.codes.ok:
            return response.content
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return image_bytes.getvalue()  # Return the original image on error
    except Exception as e:
        print(f"An error occurred: {e}")
        return image_bytes.getvalue()  # Return the original image on error
    finally:
        image_bytes.close()  # Ensure the BytesIO object is closed regardless of success or failure
