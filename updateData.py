import os
import json
from firebase_admin import credentials, db, initialize_app

class FirebaseDataProcessor:
    def __init__(self, service_account_file, database_url, json_file):
        self.service_account_file = service_account_file
        self.database_url = database_url
        self.json_file = json_file

    def process_data(self):
        self.initialize_firebase()
        data = self.retrieve_data()
        self.save_json_data(data)

    def initialize_firebase(self):
        cred = credentials.Certificate(self.service_account_file)
        initialize_app(cred, {'databaseURL': self.database_url})

    def retrieve_data(self):
        ref = db.reference('Students')
        return ref.get()

    def save_json_data(self, data):
        with open(self.json_file, "w") as file:
            json.dump(data, file, indent=4)

    def run(self):
        self.process_data()
        print("Program completed.")


# Usage Example:
if __name__ == '__main__':
    service_account_file = "serviceAccountKey.json"
    database_url = "https://xrev-75906-default-rtdb.firebaseio.com/"
    if os.path.exists('data.json'):
        os.remove('data.json')
    json_file = "data.json"

    processor = FirebaseDataProcessor(service_account_file, database_url, json_file)
    processor.run()
