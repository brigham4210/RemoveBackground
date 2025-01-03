from flask import Flask, request, render_template, send_file, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
from remover import remove_background

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.secret_key = 'your_secret_key'

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)

        output_path = os.path.join(app.config['PROCESSED_FOLDER'], f"processed_{filename}")
        try:
            remove_background(input_path, output_path)
            return redirect(url_for('download', filename=f"processed_{filename}"))
        except Exception as e:
            flash(f"Error processing image: {e}")
            return redirect(url_for('index'))
    else:
        flash('Invalid file type. Only PNG, JPG, and JPEG are allowed.')
        return redirect(url_for('index'))


@app.route('/download/<filename>')
def download(filename):
    path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
    return send_file(path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
