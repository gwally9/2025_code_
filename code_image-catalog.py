Below is a step-by-step guide to achieve this. We'll create a Python program to scan the hard drive for images, extract metadata, store them in a PostgreSQL database, and then create a web app with Flask for display.

---

### **1. Install Required Libraries**
Run the following command to install the required libraries:
```bash
pip install psycopg2 flask flask-sqlalchemy pillow exiftool
```

---

### **2. Python Program to Index Images**
This script will:
1. Scan the file system for images.
2. Extract metadata using the `Pillow` and `exiftool` libraries.
3. Insert metadata and file paths into a PostgreSQL database.

```python
import os
import psycopg2
from PIL import Image
from PIL.ExifTags import TAGS
import subprocess

# Database connection settings
DB_CONFIG = {
    "dbname": "images_db",
    "user": "your_user",
    "password": "your_password",
    "host": "localhost",
    "port": 5432
}

# Supported image formats
SUPPORTED_FORMATS = (".png", ".jpg", ".jpeg", ".svg", ".gif", ".bmp", ".tiff", ".webp")

# Connect to PostgreSQL
def connect_db():
    return psycopg2.connect(**DB_CONFIG)

# Create the database schema
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS images (
            id SERIAL PRIMARY KEY,
            file_path TEXT NOT NULL,
            metadata JSONB,
            thumbnail BYTEA
        );
    """)
    conn.commit()
    conn.close()

# Extract metadata using Pillow
def extract_metadata(file_path):
    metadata = {}
    try:
        with Image.open(file_path) as img:
            info = img._getexif()
            if info:
                metadata = {TAGS.get(tag, tag): value for tag, value in info.items()}
    except Exception as e:
        print(f"Error reading metadata for {file_path}: {e}")
    return metadata

# Generate a thumbnail
def generate_thumbnail(file_path):
    try:
        with Image.open(file_path) as img:
            img.thumbnail((100, 100))  # Resize to a thumbnail
            thumb_io = io.BytesIO()
            img.save(thumb_io, format="JPEG")
            return thumb_io.getvalue()
    except Exception as e:
        print(f"Error generating thumbnail for {file_path}: {e}")
        return None

# Scan the disk and insert records
def index_images(base_path):
    conn = connect_db()
    cursor = conn.cursor()
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.lower().endswith(SUPPORTED_FORMATS):
                file_path = os.path.join(root, file)
                metadata = extract_metadata(file_path)
                thumbnail = generate_thumbnail(file_path)
                cursor.execute(
                    "INSERT INTO images (file_path, metadata, thumbnail) VALUES (%s, %s, %s)",
                    (file_path, metadata, thumbnail),
                )
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_table()
    index_images("/path/to/scan")  # Replace with the path to scan
```

---

### **3. Flask Web App to Display Images**
This app will:
1. Query the database for image records.
2. Serve thumbnails in a grid layout.

```python
from flask import Flask, render_template, send_file
from flask_sqlalchemy import SQLAlchemy
import io

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://your_user:your_password@localhost/images_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Define the image model
class Image(db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.Text, nullable=False)
    metadata = db.Column(db.JSON, nullable=True)
    thumbnail = db.Column(db.LargeBinary, nullable=True)

@app.route("/")
def index():
    images = Image.query.all()
    return render_template("index.html", images=images)

@app.route("/thumbnail/<int:image_id>")
def thumbnail(image_id):
    image = Image.query.get_or_404(image_id)
    return send_file(io.BytesIO(image.thumbnail), mimetype="image/jpeg")

if __name__ == "__main__":
    app.run(debug=True)
```

---

### **4. HTML Template (`templates/index.html`)**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Gallery</title>
    <style>
        .grid {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }
        .grid img {
            width: 100px;
            height: 100px;
            object-fit: cover;
        }
    </style>
</head>
<body>
    <h1>Image Gallery</h1>
    <div class="grid">
        {% for image in images %}
            <a href="{{ image.file_path }}">
                <img src="/thumbnail/{{ image.id }}" alt="Image">
            </a>
        {% endfor %}
    </div>
</body>
</html>
```

---

### **5. Setup PostgreSQL**
1. Create the database:
   ```sql
   CREATE DATABASE images_db;
   ```
2. Create a user and grant access:
   ```sql
   CREATE USER your_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE images_db TO your_user;
   ```

---

### **6. Run the Programs**
1. First, run the indexing script:
   ```bash
   python index_images.py
   ```
2. Start the web app:
   ```bash
   python app.py
   ```

Visit `http://localhost:5000` to see the image gallery.