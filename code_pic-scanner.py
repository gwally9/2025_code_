import os
from PIL import Image

# Set the input directory containing PNG and JPEG files
input_dir = '/Users/gwallace/Desktop/PIC_Archive'

# Set the output directory for thumbnails
output_dir = '/Users/gwallace/Desktop/PIC_Archive/thumbnails'

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
