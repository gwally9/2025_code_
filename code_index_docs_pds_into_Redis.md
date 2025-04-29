Here’s how to modify the program to use Redis instead of PostgreSQL or Elasticsearch for storing the indexed data. Redis can store data in various structures like hashes, and we’ll use it to map filenames to their contents.

### Prerequisites
- **Install the Redis Python library:**
  ```bash
  pip install redis
  ```

### Code

```python
import os
import redis
from docx import Document
from PyPDF2 import PdfReader

# Configuration
SEARCH_DIR = "path/to/your/files"  # Replace with the directory containing your files
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

# Function to extract content from .docx files
def extract_docx(file_path):
    doc = Document(file_path)
    return "\n".join(paragraph.text for paragraph in doc.paragraphs)

# Function to extract content from .pdf files
def extract_pdf(file_path):
    reader = PdfReader(file_path)
    return "\n".join(page.extract_text() for page in reader.pages)

# Function to store data in Redis
def store_to_redis(file_data):
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    for file in file_data:
        # Store each file's content in a Redis hash
        r.hset("files", file["filename"], file["content"])
    print("Data stored in Redis successfully.")

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

    store_to_redis(file_data)

if __name__ == "__main__":
    main()
```

### Key Points
1. **File Search**:
   - The program recursively searches for `.docx` and `.pdf` files in the specified directory (`SEARCH_DIR`).

2. **Content Extraction**:
   - `python-docx` for `.docx` files and `PyPDF2` for `.pdf` files.

3. **Indexing in Redis**:
   - Data is stored in a Redis hash named `files`, where:
     - The **key** is the filename.
     - The **value** is the content of the file.

### Redis Setup
- Make sure Redis is installed and running on your system. If Redis is on a remote server, update `REDIS_HOST` and `REDIS_PORT` accordingly.
- You can verify the data using the Redis CLI:
  ```bash
  redis-cli
  HGETALL files
  ```

### Advantages of Redis
- Redis is fast and lightweight, making it ideal for temporary or rapidly accessed data.
- The hash structure allows efficient storage and retrieval by filename.

### Further Enhancements
- Add error handling for Redis connectivity issues.
- Use TTL (Time-To-Live) on the keys if the data should expire after some time.
- Use additional Redis data structures like sets or sorted sets if needed for advanced indexing or querying.