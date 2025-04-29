Building a localized search engine that indexes and allows searching of all files on your local hard drive, while storing the contents in a PostgreSQL database, involves several steps. Here's a complete roadmap along with the code to get you started:

---

### 1. **Plan the Features**
- **Indexing**: Traverse the file system to identify and extract contents from supported files (e.g., `.txt`, `.docx`, `.pdf`, etc.).
- **Storage**: Store file metadata and contents in a PostgreSQL database for easy querying.
- **Search**: Implement a search interface (command-line or web-based) that queries the database.

---

### 2. **Setup Prerequisites**
#### Install Necessary Tools:
1. **PostgreSQL Database**: Install and set up PostgreSQL.
2. **Python Libraries**:
   ```bash
   pip install psycopg2 python-docx PyPDF2
   ```

#### Create a PostgreSQL Table:
Run the following SQL command in your PostgreSQL database:
```sql
CREATE TABLE file_index (
    id SERIAL PRIMARY KEY,
    filepath TEXT NOT NULL,
    filename TEXT NOT NULL,
    content TEXT,
    indexed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### 3. **Python Code for Indexing and Storage**

```python
import os
import psycopg2
from docx import Document
from PyPDF2 import PdfReader
from datetime import datetime

# Configuration
SEARCH_DIR = "/"  # Root directory to start indexing
POSTGRES_CONFIG = {
    "dbname": "your_dbname",
    "user": "your_username",
    "password": "your_password",
    "host": "localhost",
    "port": 5432
}
SUPPORTED_EXTENSIONS = {".txt", ".docx", ".pdf"}

# Function to extract content from .txt files
def extract_txt(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

# Function to extract content from .docx files
def extract_docx(file_path):
    doc = Document(file_path)
    return "\n".join(paragraph.text for paragraph in doc.paragraphs)

# Function to extract content from .pdf files
def extract_pdf(file_path):
    reader = PdfReader(file_path)
    return "\n".join(page.extract_text() for page in reader.pages)

# Function to store data in PostgreSQL
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

# Main function to search files, extract content, and index them
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

### 4. **Search Functionality**

Add a simple search feature to query the database for files matching a keyword:

```python
def search_files(keyword):
    conn = psycopg2.connect(**POSTGRES_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT filename, filepath, content
        FROM file_index
        WHERE content ILIKE %s
        LIMIT 10;
    """, (f"%{keyword}%",))
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    if results:
        print("Search Results:")
        for filename, filepath, content in results:
            print(f"\nFilename: {filename}\nPath: {filepath}\n---\nSnippet: {content[:200]}...\n")
    else:
        print("No results found.")

if __name__ == "__main__":
    keyword = input("Enter search keyword: ")
    search_files(keyword)
```

---

### 5. **Enhancements**
1. **Add More File Types**: Extend support to `.html`, `.csv`, `.json`, etc., using relevant Python libraries.
2. **Optimize Indexing**:
   - Use a hashing mechanism to skip files that haven't changed since the last index.
   - Store file modification times in the database.
3. **Full-Text Search**:
   - Use PostgreSQL's full-text search capabilities with the `tsvector` column type for faster and more powerful searching.
4. **Web Interface**:
   - Use frameworks like Flask or Django to create a web-based search interface.

---

### 6. **Run the Code**
1. Modify `SEARCH_DIR` to the root directory you want to index (e.g., `/home/user/`).
2. Run the indexing script:
   ```bash
   python index_files.py
   ```
3. Search for keywords using:
   ```bash
   python search_files.py
   ```

---

With this setup, you’ll have a localized search engine that indexes and searches files efficiently while storing their contents in PostgreSQL.
