from flask import Flask, request, render_template, send_from_directory
from rembg import remove
from PIL import Image, UnidentifiedImageError
import io
import os

app = Flask(__name__)

# Folder to save uploaded and output images
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def remove_background(input_path, output_path):
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
        print(f"Error: Unable to identify the input file as a valid image.")
    except Exception as e:
        print(f"Unexpected error: {e}")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    if file:
        # Save the uploaded file
        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(input_path)

        # Prepare the output path
        output_filename = 'output_' + file.filename
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        # Call the remove_background function
        remove_background(input_path, output_path)

        # Return the output image path to render in the template
        return render_template('index.html', output_image=output_filename)


@app.route('/output/<filename>')
def output_image(filename):
    # Serve the output image file
    return send_from_directory(OUTPUT_FOLDER, filename)


if __name__ == '__main__':
    app.run(debug=True)
