import os
import json
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from werkzeug.utils import secure_filename
import datetime
import humanize
from collections import Counter

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

# Calculate storage used
def calculate_storage_used():
    total_size = 0
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.isfile(filepath):
            total_size += os.path.getsize(filepath)
    return humanize.naturalsize(total_size)

# Get newest upload year
def get_newest_upload():
    newest = 0
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.isfile(filepath):
            mod_time = os.path.getmtime(filepath)
            file_year = datetime.datetime.fromtimestamp(mod_time).year
            if file_year > newest:
                newest = file_year
    return newest if newest > 0 else datetime.datetime.now().year

# Count tags
def count_tags(tags_data):
    count = 0
    for tags in tags_data.values():
        count += len(tags)
    return count

# Allowed file checker
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Routes
@app.route('/')
def index():
    tags_data = load_tags()
    images = [img for img in os.listdir(app.config['UPLOAD_FOLDER']) if allowed_file(img)]
    
    return render_template('index.html', 
                           images=images, 
                           tags=tags_data,
                           tag_count=count_tags(tags_data),
                           storage_used=calculate_storage_used(),
                           newest_upload=get_newest_upload())

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('image')
        if not file or file.filename == '':
            flash("No file selected.", "error")
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
            tags_list = [t.strip().lower() for t in tags.split(',') if t.strip()]
            tags_data = load_tags()
            tags_data[filename] = tags_list
            save_tags(tags_data)

            flash(f"Image '{filename}' uploaded successfully!", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid file type. Allowed types: PNG, JPG, JPEG, GIF, WEBP", "error")
    return render_template('upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete', methods=['POST'])
def delete_image():
    filename = request.form.get('filename')
    if not filename:
        flash("No filename provided", "error")
        return redirect(url_for('index'))
    
    # Secure filename check
    safe_filename = secure_filename(filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
    
    # Check if file exists
    if not os.path.exists(filepath):
        flash("File not found", "error")
        return redirect(url_for('index'))
    
    try:
        # Delete file
        os.remove(filepath)
        
        # Remove from tags
        tags_data = load_tags()
        if safe_filename in tags_data:
            del tags_data[safe_filename]
            save_tags(tags_data)
            
        flash(f"Image '{safe_filename}' deleted successfully", "success")
    except Exception as e:
        flash(f"Error deleting image: {str(e)}", "error")
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)