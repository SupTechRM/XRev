import os
import cv2

# Input folder path
input_folder = 'images'

# Output folder path
output_folder = 'scaled_images'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Iterate through the input folder
for filename in os.listdir(input_folder):
    # Read the image
    image_path = os.path.join(input_folder, filename)
    image = cv2.imread(image_path)

    # Resize the image to 216x216 pixels
    resized_image = cv2.resize(image, (216, 216))

    # Generate the output file path
    output_path = os.path.join(output_folder, filename)

    # Save the scaled image
    cv2.imwrite(output_path, resized_image)

    print(f"Image '{filename}' scaled and saved.")

print("Scaling complete.")
