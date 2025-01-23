import face_recognition
from datetime import datetime
import cv2
import numpy as np
import os
import mysql.connector


path = r'/Images' # Path to your dataset of images
images = []  # List containing all the images
className = []  # List containing all the corresponding class names
myList = os.listdir(path)
print("Total Classes Detected:", len(myList))

# Load images and their names
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    className.append(os.path.splitext(cl)[0])

# Function to find encodings of images
def findEncodings(images):
    encodeList = []
    for img in images:
        try:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        except IndexError:
            print("Warning: No face detected in one of the images. Skipping...")
    return encodeList

# Function to mark attendance in MySQL database
def markAttendance(name):
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host="Local Host",  # MySQL server host
            user="Username",  # MySQL username
            password="Password",  # MySQL password
            database="Database"  # Database name
        )

        cursor = connection.cursor()

        # Check if the name already exists in the attendance table
        cursor.execute("SELECT name FROM attendance WHERE name = %s", (name,))
        result = cursor.fetchone()

        if result is None:  # If name is not found in the table, insert the attendance
            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("INSERT INTO attendance (name, date) VALUES (%s, %s)", (name, dt_string))
            connection.commit()
            print(f"Attendance marked for {name} at {dt_string}")
        else:
            print(f"Attendance already marked for {name}")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Generate face encodings for the known images
encodeListKnown = findEncodings(images)
print('Encodings Complete')

# Start the webcam
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    success, img = cap.read()
    if not success:
        print("Failed to grab frame")
        break

    imgS = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)  # Reduce size for faster processing
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # Detect faces and find encodings in the current frame
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    # Compare faces in the current frame with known faces
    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex] and faceDis[matchIndex] < 0.50:
            name = className[matchIndex].upper()
            markAttendance(name)
        else:
            name = 'Unknown'

        # Draw a rectangle and label on the detected face
        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4  # Scale back to the original size
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    # Show the webcam feed
    cv2.imshow('Webcam', img)

    # Exit condition: press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
