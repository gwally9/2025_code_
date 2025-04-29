To create a program that searches for Word documents (.docx) and PDF files (.pdf) locally, extracts their content, and indexes the content by filename and the actual content, you can break down the task into these main steps:

1. **Search for .docx and .pdf files locally**.
2. **Extract the text content from these files**.
3. **Create an index of filenames and contents**.
4. **Store the index (e.g., in a dictionary or a database)** for future querying.

Here's a basic Python program that does this using the `os` module to search for files, the `python-docx` library for reading Word documents, and the `PyPDF2` library for reading PDF files.

### Prerequisites:
1. **Install the required libraries**:
   ```bash
   pip install python-docx PyPDF2
   ```

2. **Python program**:

```python
import os
from docx import Document
import PyPDF2

# Function to extract text from a .docx file
def extract_text_from_docx(file_path):
    doc = Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

# Function to extract text from a .pdf file
def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in range(len(reader.pages)):
            text += reader.pages[page].extract_text() + "\n"
    return text

# Function to search files and index contents
def index_files(directory):
    index = {}
    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            if filename.endswith(".docx"):
                content = extract_text_from_docx(file_path)
            elif filename.endswith(".pdf"):
                content = extract_text_from_pdf(file_path)
            else:
                continue  # Skip non-Word and non-PDF files
            
            index[filename] = content
    return index

# Function to display indexed contents (for demonstration purposes)
def display_index(index):
    for filename, content in index.items():
        print(f"Filename: {filename}")
        print(f"Content: {content[:200]}...")  # Display the first 200 chars
        print("-" * 50)

# Main execution
if __name__ == "__main__":
    directory_to_search = "C:/path/to/your/directory"  # Replace with your directory path
    index = index_files(directory_to_search)
    display_index(index)
```

### Explanation:
1. **Extracting text from `.docx`**:
   - The `python-docx` library is used to extract text from `.docx` files. We iterate through paragraphs in the document and concatenate the text.

2. **Extracting text from `.pdf`**:
   - The `PyPDF2` library is used to extract text from PDFs. It reads the pages and extracts their text.

3. **Directory search**:
   - The `os.walk()` function recursively searches the given directory for files. It looks for `.docx` and `.pdf` files specifically and calls the appropriate extraction function.

4. **Indexing**:
   - The `index` dictionary stores the filename as the key and the extracted content as the value. You can expand this further to store more metadata (e.g., file size, date modified, etc.).

5. **Displaying the index**:
   - The `display_index` function prints the indexed files along with the first 200 characters of their content.

### Improvements:
- **Advanced Text Indexing**: You could integrate a more sophisticated indexing mechanism, such as storing the extracted content in a full-text search database like Elasticsearch.
- **Handling Large Files**: For large files, it may be more efficient to extract and index the text in chunks, or store the indexed content in a file or database.
- **Error Handling**: Add error handling in case of corrupted or unreadable files.

### Running the Program:
1. Replace `C:/path/to/your/directory` with the actual directory where your `.docx` and `.pdf` files are located.
2. The program will then scan this directory, extract content from Word and PDF files, and print the indexed filenames and their content.

This is a basic implementation, but it can be extended with features like search, better error handling, or storage in a database for persistent indexing.
