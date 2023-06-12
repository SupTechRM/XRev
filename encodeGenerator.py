import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials, storage


class StudentImageEncoder:
    def __init__(self, service_account_file, storage_bucket, database_url):
        """
        Initializes the StudentImageEncoder class.

        Args:
            service_account_file (str): Path to the Firebase service account file.
            storage_bucket (str): Name of the Firebase Storage bucket.
        """
        self.service_account_file = service_account_file
        self.storage_bucket = storage_bucket
        self.database_url = database_url

    def initialize_firebase(self):
        """
        Initializes Firebase using the provided service account file and storage bucket.
        """
        cred = credentials.Certificate(self.service_account_file)
        firebase_admin.initialize_app(cred,
                                      {'storageBucket': self.storage_bucket,
                                       'databaseURL': self.database_url
                                       })

    def import_student_images(self, folder_path):
        """
        Imports student images from the specified folder.

        Args:
            folder_path (str): Path to the folder containing student images.

        Returns:
            tuple: A tuple containing the image list and student IDs.
        """
        path_list = os.listdir(folder_path)
        img_list = []
        student_ids = []

        for path in path_list:
            img = cv2.imread(os.path.join(folder_path, path))
            if img is not None:
                img_list.append(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                student_ids.append(os.path.splitext(path)[0])

                file_name = f'{folder_path}/{path}'
                bucket = storage.bucket()
                blob = bucket.blob(file_name)
                blob.upload_from_filename(file_name)

        return img_list, student_ids

    def find_encodings(self, img_list):
        """
        Finds face encodings for the given image list.

        Args:
            img_list (list): List of images.

        Returns:
            list: List of face encodings.
        """
        encode_list = []
        for img in img_list:
            encode = face_recognition.face_encodings(img)[0]
            encode_list.append(encode)

        return encode_list

    def save_encoding_data(self, encode_list, student_ids, file_name):
        """
        Saves the encoding data to a pickle file.

        Args:
            encode_list (list): List of face encodings.
            student_ids (list): List of student IDs.
            file_name (str): Output file to save the encoding data.
        """
        data = [encode_list, student_ids]
        with open(file_name, 'wb') as file:
            pickle.dump(data, file)

    def process_images(self, folder_path, encoding_file):
        """
        Processes the images, including importing, encoding, and saving the data.

        Args:
            folder_path (str): Path to the folder containing student images.
            encoding_file (str): Output file to save the encoding data.
        """
        self.initialize_firebase()
        img_list, student_ids = self.import_student_images(folder_path)
        encode_list = self.find_encodings(img_list)
        self.save_encoding_data(encode_list, student_ids, encoding_file)

        print("Encoding complete.")
        print("Data saved to", encoding_file)
        print("Uploaded to Cloud")


# Usage Example:
if __name__ == '__main__':
    service_account_file = "serviceAccountKey.json"
    storage_bucket = "xrev-75906.appspot.com"
    database_url = "https://xrev-75906-default-rtdb.firebaseio.com/"
    folder_path = "images"
    encoding_file = "EncodeFile.p"

    encoder = StudentImageEncoder(service_account_file, storage_bucket, database_url)
    encoder.process_images(folder_path, encoding_file)
