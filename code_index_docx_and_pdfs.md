Below is a Python program that performs the following tasks:

1. **Search for Word Documents (`.docx`) and PDFs (`.pdf`) locally.**  
2. **Extract content from these files.**  
   - For `.docx` files: Uses the `python-docx` library.  
   - For `.pdf` files: Uses the `PyPDF2` library.  
3. **Index the extracted content** by filename and contents.  
4. **Store the indexed data** in PostgreSQL or Elasticsearch based on your configuration.  

### Prerequisites
- **Install the necessary Python libraries:**
  ```bash
  pip install python-docx PyPDF2 psycopg2 elasticsearch
  ```

### Code

```python
import os
import psycopg2
from docx import Document
from PyPDF2 import PdfReader
from elasticsearch import Elasticsearch

# Configuration
SEARCH_DIR = "path/to/your/files"  # Replace with the directory containing your files
USE_ELASTICSEARCH = True  # Set to False if using PostgreSQL
ES_HOST = "http://localhost:9200"  # Elasticsearch URL
POSTGRES_CONFIG = {
    "dbname": "your_dbname",
    "user": "your_username",
    "password": "your_password",
    "host": "localhost",
    "port": 5432
}

# Function to extract content from .docx files
def extract_docx(file_path):
    doc = Document(file_path)
    return "\n".join(paragraph.text for paragraph in doc.paragraphs)

# Function to extract content from .pdf files
def extract_pdf(file_path):
    reader = PdfReader(file_path)
    return "\n".join(page.extract_text() for page in reader.pages)

# Function to index data into Elasticsearch
def index_to_elasticsearch(file_data):
    es = Elasticsearch([ES_HOST])
    for file in file_data:
        es.index(index="file_index", document=file)

# Function to store data in PostgreSQL
def store_to_postgresql(file_data):
    conn = psycopg2.connect(**POSTGRES_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id SERIAL PRIMARY KEY,
            filename TEXT NOT NULL,
            content TEXT
        );
    """)
    conn.commit()

    for file in file_data:
        cursor.execute(
            "INSERT INTO files (filename, content) VALUES (%s, %s)",
            (file["filename"], file["content"])
        )
    conn.commit()
    cursor.close()
    conn.close()

# Main function to search files and process content
def main():
    file_data = []
    for root, _, files in os.walk(SEARCH_DIR):
        for file in files:
            if file.endswith(".docx") or file.endswith(".pdf"):
                file_path = os.path.join(root, file)
                try:
                    if file.endswith(".docx"):
                        content = extract_docx(file_path)
                    elif file.endswith(".pdf"):
                        content = extract_pdf(file_path)
                    else:
                        continue
                    
                    file_data.append({"filename": file, "content": content})
                    print(f"Processed: {file}")
                except Exception as e:
                    print(f"Error processing {file}: {e}")

    if USE_ELASTICSEARCH:
        index_to_elasticsearch(file_data)
    else:
        store_to_postgresql(file_data)

if __name__ == "__main__":
    main()
```

### Key Points
1. **File Search**:
   - The program recursively searches for `.docx` and `.pdf` files in the specified directory (`SEARCH_DIR`).  
2. **Content Extraction**:
   - `python-docx` for `.docx` files and `PyPDF2` for `.pdf` files are used.  
3. **Indexing**:
   - Depending on the `USE_ELASTICSEARCH` flag, data is stored in Elasticsearch or PostgreSQL.  

### Elasticsearch Setup
Ensure Elasticsearch is running locally and has the appropriate index (`file_index`). Modify the configuration (`ES_HOST`) as needed.

### PostgreSQL Setup
Provide correct PostgreSQL connection details (`POSTGRES_CONFIG`). The script will create a `files` table if it doesn't already exist.

You can customize the code further to suit your requirements, such as adding error handling or supporting additional file formats.