# FaceID-Attendance

This repository contains a **Face Recognition Attendance System** implemented in Python, leveraging computer vision techniques to identify individuals and track attendance efficiently. The system provides two options for attendance storage: **MySQL database** and **Excel file**.

## Features
- Real-time face recognition using a webcam.
- Attendance logging with two storage options:
  - **MySQL database** for robust and scalable storage.
  - **Excel file** for simple and quick setup.
- Optimized video feed processing for faster detection.
- Displays bounding boxes and labels for recognized faces.

## Requirements
Install the required Python libraries before running the project:
```bash
pip install face_recognition opencv-python numpy mysql-connector-python openpyxl
```

## Setup Instructions
### MySQL Attendance Storage
1. **Prepare Images:**
   - Add images of individuals to the `/Images` folder.
   - Image filenames should correspond to individual names (e.g., `JohnDoe.jpg`).
2. **Database Configuration:**
   - Set up a MySQL database and table:
     ```sql
     CREATE DATABASE attendance_db;
     USE attendance_db;
     CREATE TABLE attendance (
         id INT AUTO_INCREMENT PRIMARY KEY,
         name VARCHAR(255),
         date DATETIME
     );
     ```
   - Update database credentials in `Face_Recognition_Mysql.py`.
3. **Run the Script:**
   ```bash
   python Face_Recognition_Mysql.py
   ```
4. **View Attendance:**
   - Attendance records will be stored in the MySQL table.

### Excel Attendance Storage
1. **Prepare Images:**
   - Add images of individuals to the `/Images` folder.
   - Image filenames should correspond to individual names (e.g., `JohnDoe.jpg`).
2. **Run the Script:**
   ```bash
   python Face_Recognition_Excel.py
   ```
3. **View Attendance:**
   - Attendance will be logged in `Attendance.xlsx`.

## How It Works
1. Encodes known faces from the `/Images` folder.
2. Detects faces in real-time using a webcam feed.
3. Matches detected faces with encoded images.
4. Logs attendance for recognized faces in the specified storage.

## Folder Structure
```plaintext
FaceID-Attendance/
    Attendance.csv
    Face_Recognition_Excel.py
    Face_Recognition_Mysql.py
    Images/
        - Image1.jpg
        - Image2.jpg
    README.md
```

## Disclaimer
- Ensure compliance with privacy laws and obtain consent before collecting face data.
- Optimize the dataset for better recognition performance.
- It has accuracy of 90-95 percent.
- Provide images of good clarity and clear background for better performance.
- Face_Recognition_Mysql.py stores the data in MySql server with name along date and time where as in Face_Recognition_Excel.py it stores name and current time.
- Refer Attendance.csv as example of what data will be stored in the excel.


---
Feel free to fork this repository and customize it to suit your needs.




