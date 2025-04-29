To set up the project directory for this application, you need to structure it logically so that the code, templates, and other assets are easy to manage and maintain. Below is a suggested directory structure and setup process.

---

### **Project Directory Structure**

```
image_gallery/
├── app.py                  # Main Flask app
├── index_images.py         # Script to index images and populate the database
├── requirements.txt        # Python dependencies
├── config.py               # Configuration for the project (optional)
├── templates/              # HTML templates for the web app
│   └── index.html          # Main template for displaying the image gallery
├── static/                 # Static files like CSS, JS, and images
│   ├── css/
│   │   └── styles.css      # Additional custom CSS (if needed)
│   └── js/
│       └── scripts.js      # Custom JavaScript (if needed)
└── migrations/             # Database migration files (if using Flask-Migrate)
```

---

### **Step-by-Step Setup**

#### **1. Create the Project Directory**
Run the following commands in your terminal to create the project directory:
```bash
mkdir image_gallery
cd image_gallery
mkdir templates static static/css static/js migrations
```

#### **2. Install Required Python Packages**
Inside the `image_gallery` directory, create a `requirements.txt` file with the following content:
```
Flask
Flask-SQLAlchemy
psycopg2
Pillow
flask-migrate
```

Install these dependencies:
```bash
pip install -r requirements.txt
```

#### **3. Create Flask App**
In the root of the project (`image_gallery`), create `app.py` and add the main Flask application code.

#### **4. Create the Indexing Script**
In the root, create `index_images.py` and include the image scanning and indexing logic.

#### **5. Add HTML Templates**
Place the HTML template (`index.html`) inside the `templates/` directory. This will be used by Flask's `render_template()` function.

#### **6. Add Static Files (Optional)**
If you need custom CSS or JavaScript, create files inside the `static/css/` and `static/js/` directories.

For example, to customize the grid styling further, you can move the CSS from the `<style>` block in `index.html` to `static/css/styles.css`:
```css
/* static/css/styles.css */
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: #f5f5f5;
}
h1 {
    margin: 20px 0;
}
.grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 10px;
    max-width: 90%;
    margin: auto;
}
.grid img {
    width: 100%;
    height: auto;
    border-radius: 5px;
    transition: transform 0.2s;
}
.grid img:hover {
    transform: scale(1.05);
}
```

#### **7. Configure the Database**
If you want to keep your database configuration reusable, create a `config.py` file:
```python
# config.py
class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://your_user:your_password@localhost/images_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```
Then, update `app.py` to use this configuration:
```python
app.config.from_object("config.Config")
```

#### **8. Initialize the Database**
Run the following commands to set up the database (assuming PostgreSQL is installed and running):
```bash
# Create the database
psql -U postgres -c "CREATE DATABASE images_db;"

# Create tables
python index_images.py
```

---

### **Final Checklist**
1. **Run Indexing Script**: Use `python index_images.py` to populate the database with image paths and metadata.
2. **Run Flask App**: Start the web application using:
   ```bash
   python app.py
   ```
3. **Access the App**: Open [http://localhost:5000](http://localhost:5000) in your browser.

With this setup, your project directory will remain organized, scalable, and easy to maintain!