import os
import io
import logging
from rembg import remove
from PIL import Image, UnidentifiedImageError, ImageFilter, ImageEnhance

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def preprocess_image(input_image):
    """
    Preprocesses the image to improve background removal quality.

    :param input_image: The input image (PIL Image).
    :return: Preprocessed PIL Image.
    """
    # Convert to RGBA for transparency support
    input_image = input_image.convert("RGBA")

    # Increase contrast to distinguish foreground from background
    enhancer = ImageEnhance.Contrast(input_image)
    input_image = enhancer.enhance(1.5)  # Adjust the contrast factor as needed

    # Apply sharpness to make the edges more distinct
    input_image = input_image.filter(ImageFilter.SHARPEN)

    # Optional: Apply resizing if the image is too large, helps improve speed
    # input_image = input_image.resize((input_image.width // 2, input_image.height // 2))

    return input_image


def postprocess_image(output_image):
    """
    Post-processes the output image to improve final quality.

    :param output_image: The output image (PIL Image) after background removal.
    :return: Processed PIL Image.
    """
    # Apply sharpness filter to improve the edges
    output_image = output_image.filter(ImageFilter.SHARPEN)

    # Optional: Edge refinement and alpha smoothing can be added here

    return output_image


def remove_background(input_path, output_path):
    """
    Removes the background from an image and saves it to the specified output path.

    :param input_path: Path to the input image file.
    :param output_path: Path to save the output image with background removed.
    :return: None
    """
    try:
        # Check if the input file exists
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")

        logger.info(f"Processing image: {input_path}")

        # Open the input image file
        with open(input_path, 'rb') as input_file:
            input_image = input_file.read()

        # Preprocess the input image to improve background removal
        input_image_pil = Image.open(io.BytesIO(input_image))
        input_image_pil = preprocess_image(input_image_pil)

        # Remove the background using rembg (which uses AI-based background removal)
        logger.info("Removing background...")
        output_image = remove(input_image)

        # Convert the output to a PIL Image and ensure transparency support
        output = Image.open(io.BytesIO(output_image))
        output = output.convert("RGBA")  # Ensure image has RGBA mode for transparency

        # Post-process the output image for better sharpness
        output = postprocess_image(output)

        # Optimize and save the output image with higher quality
        output.save(output_path, format='PNG', optimize=True, quality=95)
        logger.info(f"Background removed successfully. Image saved to: {output_path}")

    except FileNotFoundError as fnf_error:
        logger.error(f"FileNotFoundError: {fnf_error}")
    except UnidentifiedImageError:
        logger.error(f"Unable to identify the input file as a valid image: {input_path}")
    except Exception as e:
        logger.exception(f"Unexpected error occurred: {e}")


# Example usage
if __name__ == '__main__':
    input_image_path = "input.jpg"  # Replace with your image file
    output_image_path = "output.png"  # The output will be saved as a PNG file
    remove_background(input_image_path, output_image_path)
