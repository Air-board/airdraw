import pyrebase


class FilestoCloud:

    def __init__(self,predicted_text='None'):
        self.predicted_text = predicted_text
        self.config = {
            "apiKey": "AIzaSyB6gdW-cTtKJTp0hPvdIUt6jR5AeNRJl38",
            "authDomain": "air-board-897a0.firebaseapp.com",
            "databaseURL": "",
            "projectId": "air-board-897a0",
            "storageBucket": "air-board-897a0.appspot.com",
            "serviceAccount": "serviceAccountKey.json"
        }

    def upload_file(self):
        firebase_storage = pyrebase.initialize_app(self.config)
        storage = firebase_storage.storage()

        textobject = open("predicted_text.txt","w")
        textobject.writelines(self.predicted_text)
        textobject.close()
        storage.child("predicted_text.txt").put("predicted_text.txt")
        print("File uploaded")