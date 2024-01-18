from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

def add_text_and_logo_to_image_bytes(image_bytes, text, font_path, logo_bytes):
    """
    Add text and a logo to an image.

    Args:
        - image_bytes (bytes): Image data in bytes.
        - text (str): The text to be added to the image.
        - font_path (str): The path to the font file.
        - logo_bytes (bytes): Logo image data in bytes.

    Returns:
        - bytes: The modified image data with text and logo in bytes, or the original image data on error.
    """
    try:
        image = Image.open(BytesIO(image_bytes))
        draw = ImageDraw.Draw(image)

        try:
            font = ImageFont.truetype(font_path, 30)  # You can adjust the font size here
        except IOError:
            font = ImageFont.load_default()

        text_color = (255, 255, 255)

        # Get the bounding box of the text
        text_bbox = draw.textbbox((0, 0), text, font=font)

        # Calculate text position
        text_position = (
            (image.width - (text_bbox[2] - text_bbox[0])) // 2,
            (image.height - (text_bbox[3] - text_bbox[1])) // 2
        )

        draw.text(text_position, text, font=font, fill=text_color)

        logo = Image.open(BytesIO(logo_bytes)).resize((55, 55))  # Resize the logo
        padding = 10
        img_width, img_height = image.size
        logo_width, logo_height = logo.size
        position = (img_width - logo_width - padding, img_height - logo_height - padding)

        image.paste(logo, position, logo)

        with BytesIO() as output_bytes:
            image.save(output_bytes, format="JPEG")  # You can specify the desired format (JPEG, PNG, etc.)
            return output_bytes.getvalue()

    except Exception as e:
        print(f"An error occurred during image modification: {e}")
        return image_bytes  # Return the original image data on error
