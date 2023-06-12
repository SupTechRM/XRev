import os
import json
from PIL import Image


class ImageDataProcessor:
    def __init__(self, image_directory, json_file):
        self.image_directory = image_directory
        self.json_file = json_file
        self.data = {}

    def process_images(self):
        self.load_json_data()
        for filename in os.listdir(self.image_directory):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                image_path = os.path.join(self.image_directory, filename)
                self.process_image(image_path)
        self.save_json_data()

    def process_image(self, image_path):
        # Extract the image title from the file name
        title = os.path.splitext(os.path.basename(image_path))[0]

        # Check if data already exists for the image
        if title in self.data:
            print(f"Data already exists for image '{title}'. Skipping.")
            return

        # Prompt user for information
        name = self.get_attribute(title, "name", "Enter name: ")
        roll_no = self.get_attribute(title, "roll_no", "Enter roll no: ")
        grade = self.get_attribute(title, "grade", "Enter grade: ")
        total_attendance = self.get_attribute(title, "total_attendance", "Enter total attendance: ")
        last_attendance_time = self.get_attribute(title, "last_attendance_time", "Enter last attendance time: ")

        # Update the JSON data
        self.data[title] = {
            "name": name,
            "roll_no": roll_no,
            "grade": grade,
            "total_attendance": total_attendance,
            "last_attendance_time": last_attendance_time
        }

        print(f"Data added for image '{title}'.")

    def get_attribute(self, title, attribute, prompt):
        if title in self.data and attribute in self.data[title]:
            if attribute == 'total_attendance':
                return int(self.data[title][attribute])  # Convert to int if attribute is total_attendance
            else:
                return self.data[title][attribute]
        else:
            if attribute == 'total_attendance':
                return int(input(prompt))  # Convert user input to int if attribute is total_attendance
            else:
                return input(prompt)

    def load_json_data(self):
        if os.path.isfile(self.json_file):
            with open(self.json_file, "r") as file:
                self.data = json.load(file)

    def save_json_data(self):
        with open(self.json_file, "w") as file:
            json.dump(self.data, file, indent=4)

    def run(self):
        self.process_images()
        print("Program completed.")


# Usage Example:
if __name__ == '__main__':
    image_directory = "images"
    json_file = "data.json"

    processor = ImageDataProcessor(image_directory, json_file)
    processor.run()
