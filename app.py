import os
import json
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads'
TAGS_FILE = 'tags.json'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load tags from JSON or initialize empty dict
if os.path.exists(TAGS_FILE):
    with open(TAGS_FILE, 'r') as f:
        tags_data = json.load(f)
else:
    tags_data = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    images = [img for img in os.listdir(app.config['UPLOAD_FOLDER']) if allowed_file(img)]
    return render_template('index.html', images=images, tags=tags_data)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(url_for('upload_file'))
        file = request.files['image']
        tags = request.form.get('tags', '').split(',')
        tags = [tag.strip() for tag in tags if tag.strip()]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            tags_data[filename] = tags
            with open(TAGS_FILE, 'w') as f:
                json.dump(tags_data, f)
        return redirect(url_for('index'))
    return render_template('upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
