import os
import base64
from django.conf import settings
def save_images_to_media(image_data):
    if image_data is None:
        return ""  # Return an empty string if image data is None
    
    try:
        # Decode the base64 encoded image data
        image_binary = base64.b64decode(image_data)
    except Exception as e:
        print("Error decoding base64 image:", e)
        return ""  # Return an empty string if decoding fails
    
    # Generate a unique filename
    filename = 'image.jpg'  # You can use any desired image format
    
    # Construct the file path where the image will be saved
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    
    # Save the image to the media directory
    try:
        with open(file_path, 'wb') as file:
            file.write(image_binary)
    except Exception as e:
        print("Error saving image to media directory:", e)
        return ""  # Return an empty string if saving fails
    
    return file_path
