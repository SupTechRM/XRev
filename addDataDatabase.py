import firebase_admin
from firebase_admin import credentials, db
import json


class FirebaseDataUploader:
    def __init__(self, service_account_file, database_url):
        """
        Initializes the FirebaseDataUploader class.

        Args:
            service_account_file (str): Path to the Firebase service account file.
            database_url (str): URL of the Firebase Realtime Database.
        """
        self.service_account_file = service_account_file
        self.database_url = database_url

    def initialize_firebase(self):
        """
        Initializes Firebase using the provided service account file and database URL.
        """
        cred = credentials.Certificate(self.service_account_file)
        firebase_admin.initialize_app(cred, {'databaseURL': self.database_url})

    def upload_data(self, json_file, database_path):
        """
        Uploads the JSON data to the specified database path.

        Args:
            json_file (str): Path to the JSON file containing the data.
            database_path (str): Path in the database where the data will be uploaded.
        """
        ref = db.reference(database_path)

        with open(json_file, "r") as file:
            data = json.load(file)

        for key, value in data.items():
            ref.child(key).set(value)

        print("Data upload complete.")


# Usage Example:
if __name__ == '__main__':
    service_account_file = "serviceAccountKey.json"
    database_url = "https://xrev-75906-default-rtdb.firebaseio.com/"
    json_file = "data.json"
    database_path = "Students"

    uploader = FirebaseDataUploader(service_account_file, database_url)
    uploader.initialize_firebase()
    uploader.upload_data(json_file, database_path)
