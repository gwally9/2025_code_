```python
import os
from PIL import Image

# Set the input directory containing PNG and JPEG files
input_dir = 'path/to/input/directory'

# Set the output directory for thumbnails
output_dir = 'path/to/output/thumbnails'

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Loop through all files in the input directory
for filename in os.listdir(input_dir):
    # Check if the file is a PNG or JPEG image
    if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
        # Open the image using PIL
        img = Image.open(os.path.join(input_dir, filename))
        
        # Resize the image to a thumbnail size (e.g. 100x100 pixels)
        thumb_width = 100
        thumb_height = int((img.size[1] / img.size[0]) * thumb_width)
        img.thumbnail((thumb_width, thumb_height), Image.ANTIALIAS)
        
        # Save the thumbnail to the output directory
        thumbnail_filename = os.path.join(output_dir, filename + '_thumb.png')
        img.save(thumbnail_filename)

print(f"Thumbnails saved to {output_dir}")
```
Here's how the code works:

1. The first section sets the input directory containing PNG and JPEG files, as well as the output directory for thumbnails.
2. The code creates the output directory if it doesn't exist.
3. The loop iterates through all files in the input directory using `os.listdir()`.
4. For each file, the code checks if the file is a PNG or JPEG image by checking its extension (e.g. `.png`, `.jpg`, or `.jpeg`).
5. If the file is an image, the code opens it using PIL's `Image.open()` function.
6. The code resizes the image to a thumbnail size (in this example, 100x100 pixels) using PIL's `thumbnail()` method with the `ANTIALIAS` filter for smooth scaling.
7. Finally, the code saves the thumbnail to the output directory using PIL's `save()` method.

Note that you'll need to install the PIL library if it's not already installed. You can do this by running `pip install pillow` in your terminal.