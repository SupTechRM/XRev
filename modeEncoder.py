import cv2
import os

# Set the path to the folder containing the modes
folder_mode_path = 'resources/modes'

# Get the list of mode paths in the folder
mode_path_list = os.listdir(folder_mode_path)

# Create an empty list to store the mode images
img_mode_list = []

# Iterate over each mode path
for path in mode_path_list:
    # Load the mode image and append it to the list
    img_mode_list.append(cv2.imread(os.path.join(folder_mode_path, path)))

# Print the number of mode images
print(f"Number of mode images: {len(img_mode_list)}")