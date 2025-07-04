# 🖼️ Local Image Host

Welcome to **Local Image Host** — a clean, modern, and minimalist image gallery built with Flask. It's perfect for self-hosting your personal image album locally with tags and a dark aesthetic.




## ✨ Features

* 🌌 **Dark Mode**: Sleek, modern UI with a stylish dark theme.
* 🖼️ **Gallery Page** (`/`): Browse all uploaded images in a smooth, animated grid layout.
* 📤 **Upload Page** (`/upload`): Upload images with optional comma-separated tags.
* 🏷️ **Tagging Support**: Add, store, and display custom tags per image.
* 💾 **Local File Storage**: Images are saved to your disk — no cloud required.



## Screenshots

## Preview
[![Watch the video](https://img.youtube.com/vi/DlvrjOVjZ1Y/0.jpg)](https://youtu.be/DlvrjOVjZ1Y)



## 📁 Project Structure

```
minimalist_image_host/
├── app.py              # Flask application logic
├── tags.json           # Tags data in JSON format
├── static/
│   └── uploads/        # Uploaded image files
└── templates/
    ├── index.html      # Main gallery UI
    └── upload.html     # Upload form UI
```

## 🚀 Getting Started

1. 🔽 Clone the repository:

   ```bash
   git clone https://github.com/Laszlobeer/localalbum/
   cd localalbum
   ```
2. 📦 Install dependencies:

   ```bash
   pip install flask Werkzeug
   ```
3. ▶️ Run the app:

   ```bash
   python app.py
   ```
4. 🌐 Open in browser:

   * Gallery: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
   * Upload: [http://127.0.0.1:5000/upload](http://127.0.0.1:5000/upload)

## ❤️ Support Me

If you enjoy using this project, consider buying me a coffee:

☕ [https://ko-fi.com/laszlobeer](https://ko-fi.com/laszlobeer)
