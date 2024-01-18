from PIL import Image
from typing import List
from io import BytesIO

def crop_quadrants_from_bytes(image_bytes: bytes) -> List[bytes]:
    """
    Crop an image (provided as bytes) into four equal quadrants and return them as a list of bytes.

    Args:
    - image_bytes (bytes): Image data in bytes.

    Returns:
    - List[bytes]: List of bytes representing the four quadrants (top-left, top-right, bottom-left, bottom-right).
    """
    try:
        img = Image.open(BytesIO(image_bytes))
        width, height = img.size

        if width != height or width % 2 != 0:
            raise ValueError("Image dimensions should be equal and even.")

        half_width = width // 2
        half_height = height // 2

        quadrant_bytes_list = []
        for i in range(4):
            left = half_width * (i % 2)
            upper = half_height * (i // 2)
            right = left + half_width
            lower = upper + half_height

            quadrant = img.crop((left, upper, right, lower))

            # Convert the cropped quadrant to bytes
            with BytesIO() as output_bytes:
                quadrant.save(output_bytes, format="JPEG")  # You can specify the desired format (JPEG, PNG, etc.)
                quadrant_bytes_list.append(output_bytes.getvalue())

        return quadrant_bytes_list
    except ValueError as ve:
        print(f"Error: {ve}")
        return []
    except Exception as e:
        print("Error cropping quadrants:", e)
        return []
    
    
    
