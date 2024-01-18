from PIL import Image
from typing import List

def crop_quadrants(image: Image.Image, output_paths: List[str]):
    """
    Crop an image into four equal quadrants and save them separately.

    Args:
    - image_path (str): Path to the input image file.
    - output_paths (List[str]): List of output paths to save the quadrants (top-left, top-right, bottom-left, bottom-right).

    Returns:
    - None
    """
    try:
        # img = Image.open(image_path)
        width, height = image.size

        if width != height or width % 2 != 0:
            raise ValueError("Image dimensions should be equal and even.")

        half_width = width // 2
        half_height = height // 2

        for i, output_path in enumerate(output_paths):
            left = half_width * (i % 2)
            upper = half_height * (i // 2)
            right = left + half_width
            lower = upper + half_height

            quadrant = image.crop((left, upper, right, lower))
            quadrant.save(output_path)

        print("Quadrants cropped and saved successfully!")
    except FileNotFoundError:
        print("Error: File not found. Please provide a valid image path.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print("Error cropping quadrants:", e)

# Example usage:
input_image_path = 'downloaded_imagenew.jpg'  # Replace with your image path
output_paths = ['quadrant1.jpg', 'quadrant2.jpg', 'quadrant3.jpg', 'quadrant4.jpg']
image = Image.open(input_image_path)
crop_quadrants(image, output_paths)
