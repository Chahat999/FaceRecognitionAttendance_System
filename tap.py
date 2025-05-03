import cv2
import pandas as pd
import os
from datetime import datetime

# Global variables
detected_faces = []
face_marked = set()
attendance_df = None

def click_event(event, x, y, flags, param):
    global attendance_df, face_marked

    if event == cv2.EVENT_LBUTTONDOWN:
        for (x1, y1, x2, y2, id_, name) in detected_faces:
            if x1 <= x <= x2 and y1 <= y <= y2:
                if id_ in face_marked:
                    print(f"[INFO] Already marked attendance for ID {id_}")
                    return

                now = datetime.now()
                date_today = now.strftime("%d-%m-%Y")
                time_now = now.strftime("%H:%M:%S")

                # Append to DataFrame
                attendance_df = pd.concat([attendance_df, pd.DataFrame([{
                    "ID": id_,
                    "Name": name,
                    "Date": date_today,
                    "Time": time_now
                }])], ignore_index=True)

                print(f"[SUCCESS] Attendance marked for {name} at {time_now}")
                face_marked.add(id_)

def mark_attendance_to_excel():
    global detected_faces, attendance_df, face_marked

    # Load face recognizer
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("trainer/trainer.yml")

    # Load face detector
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Load student data
    student_df = pd.read_csv("StudentDetails.csv")  # Must have ID and Name

    # Prepare attendance Excel file
    date_today = datetime.now().strftime("%d-%m-%Y")
    filename = f"Attendance_{date_today}.xlsx"

    # Create or load today's attendance
    if os.path.exists(filename):
        attendance_df = pd.read_excel(filename)
    else:
        attendance_df = pd.DataFrame(columns=["ID", "Name", "Date", "Time"])

    # Start camera
    cam = cv2.VideoCapture(0)
    cv2.namedWindow('Tap Face to Mark Attendance')
    cv2.setMouseCallback('Tap Face to Mark Attendance', click_event)

    while True:
        ret, frame = cam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        detected_faces.clear()

        for (x, y, w, h) in faces:
            id_, conf = recognizer.predict(gray[y:y+h, x:x+w])
            if conf < 50:
                matched = student_df[student_df["ID"] == id_]
                if not matched.empty:
                    name = matched.iloc[0]["Name"]
                    cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
                    cv2.putText(frame, f"{id_} - {name}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
                    detected_faces.append((x, y, x+w, y+h, id_, name))
            else:
                cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 2)
                cv2.putText(frame, "Unknown", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)

        cv2.imshow('Tap Face to Mark Attendance', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

    # Drop duplicates and save
    attendance_df.drop_duplicates(subset=['ID', 'Date'], keep='first', inplace=True)
    attendance_df.to_excel(filename, index=False)
    print(f"[SAVED] Attendance saved to {filename}")
