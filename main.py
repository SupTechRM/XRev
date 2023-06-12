import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials, db, storage
import numpy as np
from datetime import datetime


class AttendanceSystem:
		def __init__(self):
				# Initialize Firebase
				credentials_path = "serviceAccountKey.json"
				firebase_database_url = "https://xrev-75906-default-rtdb.firebaseio.com/"
				storage_bucket = "xrev-75906.appspot.com"

				cred = credentials.Certificate(credentials_path)
				firebase_admin.initialize_app(cred, {
						'databaseURL': firebase_database_url,
						'storageBucket': storage_bucket
				})
				self.bucket = storage.bucket()

				self.video_capture = cv2.VideoCapture(0)
				self.video_capture.set(3, 640)
				self.video_capture.set(4, 480)

				self.background_image = cv2.imread('resources/background.png')

				# Load mode images into a list
				modes_folder_path = 'resources/Modes'
				mode_paths = os.listdir(modes_folder_path)
				self.mode_images = [cv2.imread(os.path.join(modes_folder_path, path)) for path in mode_paths]

				# Load the encoding file
				print("Loading Encoding File ...")
				with open('EncodeFile.p', 'rb') as file:
						encoding_data = pickle.load(file)
				self.encodings, self.student_ids = encoding_data
				print("Encoding File Loaded")

				self.mode_type = 0
				self.counter = 0
				self.current_id = -1
				self.student_image = []

		def run(self):
				while True:
						success, frame = self.video_capture.read()

						frame_resized = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
						frame_resized_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)

						face_locations = face_recognition.face_locations(frame_resized_rgb)
						face_encodings = face_recognition.face_encodings(frame_resized_rgb, face_locations)

						self.background_image[162:162 + 480, 55:55 + 640] = frame
						self.background_image[44:44 + 633, 808:808 + 414] = self.mode_images[self.mode_type]

						if face_locations:
								for encoding_face, location in zip(face_encodings, face_locations):
										face_matches = face_recognition.compare_faces(self.encodings, encoding_face)
										face_distances = face_recognition.face_distance(self.encodings, encoding_face)

										closest_match_index = np.argmin(face_distances)

										if face_matches[closest_match_index]:
												y1, x2, y2, x1 = location
												y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
												bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
												self.background_image = cvzone.cornerRect(self.background_image, bbox, rt=0)
												self.current_id = self.student_ids[closest_match_index]
												if self.counter == 0:
														cvzone.putTextRect(self.background_image, "Loading", (275, 400))
														cv2.imshow("Face Attendance", self.background_image)
														cv2.waitKey(1)
														self.counter = 1
														self.mode_type = 1

								if self.counter != 0:
										if self.counter == 1:
												student_info = db.reference(f'Students/{self.current_id}').get()
												blob = self.bucket.get_blob(f'images/{self.current_id}.png')
												image_data = np.frombuffer(blob.download_as_string(), np.uint8)
												self.student_image = cv2.imdecode(image_data, cv2.COLOR_BGRA2BGR)

												datetime_object = datetime.strptime(student_info['last_attendance_time'], "%Y-%m-%d %H:%M:%S.%f")
												seconds_elapsed = (datetime.now() - datetime_object).total_seconds()
												if seconds_elapsed > 86400:
														ref = db.reference(f'Students/{self.current_id}')
														student_info['total_attendance'] += 1
														ref.child('total_attendance').set(student_info['total_attendance'])
														ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
												else:
														self.mode_type = 3
														self.name = student_info['name']
														print(f'You have already been marked {self.name}')
														self.counter = 0
														self.background_image[44:44 + 633, 808:808 + 414] = self.mode_images[self.mode_type]

										if self.mode_type != 3:
												if 10 < self.counter < 20:
														self.mode_type = 2

												self.background_image[44:44 + 633, 808:808 + 414] = self.mode_images[self.mode_type]

												if self.counter <= 10:
														cv2.putText(self.background_image, str(student_info['total_attendance']), (861, 125),
																				cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
														cv2.putText(self.background_image, str(student_info['roll_no']), (1006, 550),
																				cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
														cv2.putText(self.background_image, str(self.current_id), (1006, 493),
																				cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
														cv2.putText(self.background_image, str(student_info['grade']), (910, 625),
																				cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

														(w, h), _ = cv2.getTextSize(student_info['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
														offset = (414 - w) // 2
														cv2.putText(self.background_image, str(student_info['name']), (808 + offset, 445),
																				cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

														self.background_image[175:175 + 216, 909:909 + 216] = self.student_image

												self.counter += 1

												if self.counter >= 20:
														self.counter = 0
														self.mode_type = 0
														student_info = []
														self.student_image = []
														self.background_image[44:44 + 633, 808:808 + 414] = self.mode_images[self.mode_type]
						else:
								self.mode_type = 0
								self.counter = 0

						cv2.imshow("Face Attendance", self.background_image)
						cv2.waitKey(1)


attendance_system = AttendanceSystem()
attendance_system.run()
