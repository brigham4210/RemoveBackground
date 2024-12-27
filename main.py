from rembg import remove
from PIL import Image
import io


def remove_background(input_path, output_path):
    """
    Removes the background from an image.

    :param input_path: Path to the input image file.
    :param output_path: Path to save the output image with background removed.
    """
    try:
        # Open the input image file
        with open(input_path, 'rb') as input_file:
            input_image = input_file.read()

        # Remove the background
        output_image = remove(input_image)

        # Convert the output to a PIL Image and save it
        output = Image.open(io.BytesIO(output_image))
        output.save(output_path, format='PNG')
        print(f"Background removed successfully. Saved to: {output_path}")

    except Exception as e:
        print(f"Error: {e}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    input_image_path = "input.jpeg"  # Replace with your image file
    output_image_path = "output.png"  # The output will be saved as a PNG file
    remove_background(input_image_path, output_image_path)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
