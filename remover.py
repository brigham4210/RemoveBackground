from rembg import remove
from PIL import Image, UnidentifiedImageError
import io
import os


def remove_background(input_path, output_path):
    """
    Removes the background from an image.

    :param input_path: Path to the input image file.
    :param output_path: Path to save the output image with background removed.
    """
    try:
        # Check if the input file exists
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")

        # Open the input image file
        with open(input_path, 'rb') as input_file:
            input_image = input_file.read()

        # Remove the background
        output_image = remove(input_image)

        # Convert the output to a PIL Image and save it
        output = Image.open(io.BytesIO(output_image))
        output = output.convert("RGBA")  # Ensure transparency support
        output.save(output_path, format='PNG', optimize=True)
        print(f"Background removed successfully. Saved to: {output_path}")

    except FileNotFoundError as fnf_error:
        print(f"Error: {fnf_error}")
    except UnidentifiedImageError:
        print(f"Error: Unable to identify the input file as a valid image: {input_path}")
    except Exception as e:
        print(f"Unexpected error: {e}")


# Example usage
if __name__ == '__main__':
    input_image_path = "input.jpg"  # Replace with your image file
    output_image_path = "output.png"  # The output will be saved as a PNG file
    remove_background(input_image_path, output_image_path)
