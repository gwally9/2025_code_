To add support for **YAML**, **Markdown** (`.md`), and `.webloc` files in the localized search engine, you'll need to extend the functionality to handle these file formats. Here's how you can implement it:

---

### 1. **Understand the File Types**
- **YAML**: Structured data format often used for configuration files.
- **Markdown (`.md`)**: Text-based file format with optional lightweight markup for formatting.
- **`.webloc`**: macOS-specific URL bookmark files in XML format.

### 2. **Add Dependencies**
Install libraries for parsing YAML and XML files:
```bash
pip install pyyaml lxml markdown
```

---

### 3. **Functions to Extract Content**

#### YAML Files
Extract key-value pairs and represent them as text:
```python
import yaml

def extract_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return yaml.dump(data, default_flow_style=False)
```

#### Markdown Files
Extract plain text, optionally converting to HTML for indexing:
```python
from markdown import markdown

def extract_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    # Convert Markdown to plain text or HTML
    return markdown_content  # Or markdown(markdown_content) for HTML
```

#### `.webloc` Files
Extract the URL from the `.webloc` XML structure:
```python
from lxml import etree

def extract_webloc(file_path):
    try:
        tree = etree.parse(file_path)
        url = tree.xpath('//string')[0].text  # Extract the <string> tag containing the URL
        return f"URL: {url}"
    except Exception as e:
        return f"Error extracting .webloc: {e}"
```

---

### 4. **Update the Supported Extensions**
Extend the `SUPPORTED_EXTENSIONS` set:
```python
SUPPORTED_EXTENSIONS = {".txt", ".docx", ".pdf", ".yaml", ".yml", ".md", ".webloc"}
```

---

### 5. **Update Main Function**
In the `main()` function, add cases for the new formats:
```python
if file.endswith(".yaml") or file.endswith(".yml"):
    content = extract_yaml(file_path)
elif file.endswith(".md"):
    content = extract_markdown(file_path)
elif file.endswith(".webloc"):
    content = extract_webloc(file_path)
```

---

### 6. **Complete Updated Code**

Here’s the updated code snippet incorporating the new file types:

```python
import os
import psycopg2
from docx import Document
from PyPDF2 import PdfReader
from datetime import datetime
import yaml
from markdown import markdown
from lxml import etree

# Configuration
SEARCH_DIR = "/"  # Root directory to start indexing
POSTGRES_CONFIG = {
    "dbname": "your_dbname",
    "user": "your_username",
    "password": "your_password",
    "host": "localhost",
    "port": 5432
}
SUPPORTED_EXTENSIONS = {".txt", ".docx", ".pdf", ".yaml", ".yml", ".md", ".webloc"}

def extract_txt(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def extract_docx(file_path):
    doc = Document(file_path)
    return "\n".join(paragraph.text for paragraph in doc.paragraphs)

def extract_pdf(file_path):
    reader = PdfReader(file_path)
    return "\n".join(page.extract_text() for page in reader.pages)

def extract_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return yaml.dump(data, default_flow_style=False)

def extract_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    return markdown_content  # Or markdown(markdown_content) for HTML

def extract_webloc(file_path):
    try:
        tree = etree.parse(file_path)
        url = tree.xpath('//string')[0].text
        return f"URL: {url}"
    except Exception as e:
        return f"Error extracting .webloc: {e}"

def store_to_postgresql(file_data):
    conn = psycopg2.connect(**POSTGRES_CONFIG)
    cursor = conn.cursor()
    for file in file_data:
        cursor.execute("""
            INSERT INTO file_index (filepath, filename, content, indexed_at)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (filepath) DO NOTHING;
        """, (file["filepath"], file["filename"], file["content"], datetime.now()))
    conn.commit()
    cursor.close()
    conn.close()
    print("Data stored in PostgreSQL successfully.")

def main():
    file_data = []
    for root, _, files in os.walk(SEARCH_DIR):
        for file in files:
            if any(file.endswith(ext) for ext in SUPPORTED_EXTENSIONS):
                file_path = os.path.join(root, file)
                try:
                    if file.endswith(".txt"):
                        content = extract_txt(file_path)
                    elif file.endswith(".docx"):
                        content = extract_docx(file_path)
                    elif file.endswith(".pdf"):
                        content = extract_pdf(file_path)
                    elif file.endswith(".yaml") or file.endswith(".yml"):
                        content = extract_yaml(file_path)
                    elif file.endswith(".md"):
                        content = extract_markdown(file_path)
                    elif file.endswith(".webloc"):
                        content = extract_webloc(file_path)
                    else:
                        continue

                    file_data.append({"filepath": file_path, "filename": file, "content": content})
                    print(f"Indexed: {file_path}")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

    store_to_postgresql(file_data)

if __name__ == "__main__":
    main()
```

---

### 7. **Test the Functionality**
1. Place some `.yaml`, `.md`, and `.webloc` files in the `SEARCH_DIR` and run the script:
   ```bash
   python index_files.py
   ```

2. Query the PostgreSQL database to verify the indexed data:
   ```sql
   SELECT * FROM file_index WHERE content ILIKE '%keyword%';
   ```

---

### 8. **Enhancements**
- Add logging for better tracking of indexed files and errors.
- Use a unified framework (like Flask or Django) to build a web interface for indexing and searching.
- Consider adding advanced file formats like `.html`, `.csv`, and `.json`.

This enhanced script now supports YAML, Markdown, and `.webloc` files in addition to the previously supported formats.
