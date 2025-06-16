import os
import json
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from werkzeug.utils import secure_filename

# Config
UPLOAD_FOLDER = 'static/uploads'
TAGS_FILE = 'tags.json'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# App setup
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'your_secret_key'

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load/save tags
def load_tags():
    if os.path.exists(TAGS_FILE):
        with open(TAGS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_tags(tags_data):
    with open(TAGS_FILE, 'w') as f:
        json.dump(tags_data, f)

# Allowed file checker
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Routes
@app.route('/')
def index():
    tags_data = load_tags()
    images = [img for img in os.listdir(app.config['UPLOAD_FOLDER']) if allowed_file(img)]
    return render_template('index.html', images=images, tags=tags_data)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('image')
        if not file or file.filename == '':
            flash("No file selected.")
            return redirect(url_for('upload_file'))

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # Handle filename collision
            counter = 1
            base, ext = os.path.splitext(filename)
            while os.path.exists(filepath):
                filename = f"{base}_{counter}{ext}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                counter += 1

            file.save(filepath)

            # Handle tags
            tags = request.form.get('tags', '')
            tags_list = [t.strip() for t in tags.split(',') if t.strip()]
            tags_data = load_tags()
            tags_data[filename] = tags_list
            save_tags(tags_data)

            return redirect(url_for('index'))
    return render_template('upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)