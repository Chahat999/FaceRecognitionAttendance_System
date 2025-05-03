import cv2
import os
import numpy as np
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import csv
from datetime import datetime

# # Directories
# os.makedirs("TrainingImages", exist_ok=True)
# os.makedirs("Attendance", exist_ok=True)
# if not os.path.exists("StudentDetails.csv"):
#     open("StudentDetails.csv", 'a').close()

# # Initialize GUI window
# window = tk.Tk()
# window.title("Face Recognition Based Attendance System")
# window.geometry('900x550')
# window.configure(bg='black')

# # Functions
# def clear_id():
#     txt_id.delete(0, 'end')

# def clear_name():
#     txt_name.delete(0, 'end')

# def capture_images():
#     Id = txt_id.get().strip()
#     name = txt_name.get().strip()

#     if not Id or not name:
#         messagebox.showwarning("Input Error", "Please enter both ID and Name.")
#         return

#     cam = cv2.VideoCapture(0)
#     face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
#     sample_num = 0

#     while True:
#         ret, img = cam.read()
#         if not ret:
#             break
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         faces = face_detector.detectMultiScale(gray, 1.3, 5)

#         for (x, y, w, h) in faces:
#             sample_num += 1
#             cv2.imwrite(f"TrainingImages/{name}.{Id}.{sample_num}.jpg", gray[y:y+h, x:x+w])
#             cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
#             cv2.imshow('Capturing Images', img)

#         if cv2.waitKey(100) & 0xFF == ord('q'):
#             break
#         elif sample_num >= 30:
#             break

#     cam.release()
#     cv2.destroyAllWindows()
#     messagebox.showinfo("Success", f"Images Saved for ID: {Id}, Name: {name}")

# def save_profile():
#     Id = txt_id.get().strip()
#     name = txt_name.get().strip()

#     if not Id or not name:
#         messagebox.showwarning("Input Error", "Please enter both ID and Name.")
#         return

#     existing_ids = set()
#     if os.path.exists("StudentDetails.csv"):
#         with open("StudentDetails.csv", 'r', newline='') as f:
#             reader = csv.reader(f)
#             for row in reader:
#                 if len(row) >= 2:
#                     existing_ids.add(row[0].strip())

#     if Id in existing_ids:
#         messagebox.showerror("Duplicate Entry", f"ID {Id} already exists. Please use a different ID.")
#         return

#     with open("StudentDetails.csv", 'a', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow([Id, name])

#     update_registration_count()
#     messagebox.showinfo("Success", f"Profile Saved for ID: {Id}, Name: {name}")

# def update_registration_count():
#     if os.path.exists("StudentDetails.csv"):
#         with open("StudentDetails.csv", 'r') as f:
#             lines = f.readlines()
#             total = len(lines)
#             lbl_count.config(text=f"Total Registrations till now: {total}")

# def mark_attendance():
#     recognizer = cv2.face.LBPHFaceRecognizer_create()
#     detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

#     recognizer.read("Trainer.yml")
#     cam = cv2.VideoCapture(0)
#     font = cv2.FONT_HERSHEY_SIMPLEX

#     student_dict = {}  

#     with open("StudentDetails.csv", 'r') as f:
#         reader = csv.reader(f)
#         for row in reader:
#             if len(row) >= 2:  
#                 student_dict[row[0]] = row[1]

#     attendance_list = set()  

#     while True:
#         ret, img = cam.read()
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         faces = detector.detectMultiScale(gray, 1.2, 5)

#         for (x, y, w, h) in faces:
#             Id, conf = recognizer.predict(gray[y:y+h, x:x+w])
#             if conf < 50 and str(Id) in student_dict:  
#                 name = student_dict.get(str(Id), "Unknown")

#                 if Id not in attendance_list:
#                     attendance_list.add(Id)
#                     with open("Attendance/Attendance.csv", 'a', newline='') as f:
#                         writer = csv.writer(f)
#                         writer.writerow([Id, name, datetime.now().strftime('%d-%m-%Y'), datetime.now().strftime('%H:%M:%S')])

#                 cv2.putText(img, f"{name}", (x+5, y-5), font, 1, (0, 255, 0), 2)
#             else:
#                 cv2.putText(img, "Unknown", (x+5, y-5), font, 1, (0, 0, 255), 2)  

#             cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 0), 2)

#         cv2.imshow('Recognizing Faces - Press Q to Exit', img)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cam.release()
#     cv2.destroyAllWindows()
#     update_treeview(attendance_list, student_dict)

# def update_treeview(attendance_list, student_dict):
#     for item in tree.get_children():
#         tree.delete(item)

#     for Id in attendance_list:
#         name = student_dict.get(str(Id), "Unknown")
#         date = datetime.now().strftime('%d-%m-%Y')
#         time = datetime.now().strftime('%H:%M:%S')
#         tree.insert('', 'end', values=[Id, name, date, time])



#Directories
os.makedirs("TrainingImages", exist_ok=True)
os.makedirs("Attendance", exist_ok=True)
if not os.path.exists("StudentDetails.csv"):
    open("StudentDetails.csv", 'a').close()

# Initialize GUI window
window = tk.Tk()
window.title("Face Recognition Based Attendance System")
window.geometry('900x550')
window.configure(bg='black')

# Functions
def clear_id():
    txt_id.delete(0, 'end')

def clear_name():
    txt_name.delete(0, 'end')

def capture_images():
    Id = txt_id.get().strip()
    name = txt_name.get().strip()

    if not Id or not name:
        messagebox.showwarning("Input Error", "Please enter both ID and Name.")
        return

    cam = cv2.VideoCapture(0)
    face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    sample_num = 0

    while True:
        ret, img = cam.read()
        if not ret:
            break
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            sample_num += 1
            cv2.imwrite(f"TrainingImages/{name}.{Id}.{sample_num}.jpg", gray[y:y+h, x:x+w])
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.imshow('Capturing Images', img)

        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
        elif sample_num >= 30:
            break

    cam.release()
    cv2.destroyAllWindows()
    messagebox.showinfo("Success", f"Images Saved for ID: {Id}, Name: {name}")

def save_profile():
    Id = txt_id.get().strip()
    name = txt_name.get().strip()

    if not Id or not name:
        messagebox.showwarning("Input Error", "Please enter both ID and Name.")
        return

    with open("StudentDetails.csv", 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([Id, name])
    
    update_registration_count()
    messagebox.showinfo("Success", f"Profile Saved for ID: {Id}, Name: {name}")

def update_registration_count():
    if os.path.exists("StudentDetails.csv"):
        with open("StudentDetails.csv", 'r') as f:
            lines = f.readlines()
            total = len(lines)
            lbl_count.config(text=f"Total Registrations till now: {total}")

def update_treeview():
    """ Load and display attendance records for today """
    tree.delete(*tree.get_children())  # Clear existing entries

    today_date = datetime.now().strftime('%d-%m-%Y')
    filename = f"Attendance/Attendance_{today_date}.csv"

    if os.path.exists(filename):
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 4:
                    tree.insert('', 'end', values=(row[0], row[1], row[2], row[3]))

def mark_attendance():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    recognizer.read("Trainer.yml")
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX

    student_dict = {}  

    with open("StudentDetails.csv", 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:  
                student_dict[row[0]] = row[1]

    today_date = datetime.now().strftime('%d-%m-%Y')
    attendance_file = f"Attendance/Attendance_{today_date}.csv"

    recorded_attendance = set()
    if os.path.exists(attendance_file):
        with open(attendance_file, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 3 and row[2] == today_date:
                    recorded_attendance.add(row[0])

    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in faces:
            Id, conf = recognizer.predict(gray[y:y+h, x:x+w])

            if conf < 50 and str(Id) in student_dict and str(Id) not in recorded_attendance:  
                name = student_dict[str(Id)]  
                recorded_attendance.add(str(Id))  

                with open(attendance_file, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([Id, name, today_date, datetime.now().strftime('%H:%M:%S')])

            #     cv2.putText(img, f"{name}", (x+5, y-5), font, 1, (0, 255, 0), 2)
            # else:
            #     cv2.putText(img, "Unknown", (x+5, y-5), font, 1, (0, 0, 255), 2)  

                cv2.putText(img, f"{name}", (x, y-5), font, 1, (0, 255, 0), 2, cv2.LINE_AA)  
            else:
                cv2.putText(img,"Unknown" , (x, y-5), font, 1, (0, 0, 255), 2, cv2.LINE_AA)  

            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 0), 2)

        cv2.imshow('Recognizing Faces - Press Q to Exit', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
    update_treeview()

# # GUI Layout
# title = tk.Label(window, text="Face Recognition Based Attendance System", font=('Arial', 20, 'bold'), fg='white', bg='black')
# title.pack(pady=10)

# time_label = tk.Label(window, text=datetime.now().strftime('%d-%b-%Y  |  %H:%M:%S'), font=('Arial', 16), fg='orange', bg='black')
# time_label.pack()

# frame_left = tk.Frame(window, bg='deepskyblue', bd=2)
# frame_left.place(x=20, y=100, width=400, height=400)

# frame_right = tk.Frame(window, bg='deepskyblue', bd=2)
# frame_right.place(x=460, y=100, width=400, height=400)

# # Left Section
# tk.Label(frame_left, text="For Already Registered", font=('Arial', 14, 'bold'), bg='limegreen').pack(fill='x')
# tk.Button(frame_left, text="Take Attendance", font=('Arial', 14, 'bold'), bg='yellow', command=mark_attendance).pack(pady=10)

# tree = ttk.Treeview(frame_left, columns=("ID", "NAME", "DATE", "TIME"), show='headings')
# tree.heading("ID", text="ID")
# tree.heading("NAME", text="NAME")
# tree.heading("DATE", text="DATE")
# tree.heading("TIME", text="TIME")
# tree.pack(expand=True, fill='both')

# # update_treeview()

# tk.Button(frame_left, text="Quit", font=('Arial', 14, 'bold'), bg='red', fg='white', command=window.quit).pack(fill='x', pady=5)

# # Right Section
# tk.Label(frame_right, text="For New Registrations", font=('Arial', 14, 'bold'), bg='limegreen').pack(fill='x')

# tk.Label(frame_right, text="Enter ID", font=('Arial', 12, 'bold'), bg='deepskyblue').pack(pady=5)
# txt_id = tk.Entry(frame_right, font=('Arial', 12))
# txt_id.pack()
# tk.Button(frame_right, text="Clear", command=clear_id, bg='red', fg='white').pack()

# tk.Label(frame_right, text="Enter Name", font=('Arial', 12, 'bold'), bg='deepskyblue').pack(pady=5)
# txt_name = tk.Entry(frame_right, font=('Arial', 12))
# txt_name.pack()
# tk.Button(frame_right, text="Clear", command=clear_name, bg='red', fg='white').pack()

# tk.Label(frame_right, text="1)Take Images  >>>  2)Save Profile", font=('Arial', 10, 'bold'), bg='deepskyblue').pack(pady=5)
# tk.Button(frame_right, text="Take Images", font=('Arial', 12, 'bold'), bg='blue', fg='white', command=capture_images).pack(pady=5)
# tk.Button(frame_right, text="Save Profile", font=('Arial', 12, 'bold'), bg='blue', fg='white', command=save_profile).pack(pady=5)

# lbl_count = tk.Label(frame_right, text="Total Registrations till now  : 0", font=('Arial', 12), bg='deepskyblue')
# lbl_count.pack(pady=10)

# update_registration_count()

# # Main loop
# window.mainloop()




# GUI Layout
title = tk.Label(window, text="Face Recognition Based Attendance System", font=('Arial', 20, 'bold'), fg='white', bg='black')
title.pack(pady=10)

frame_left = tk.Frame(window, bg='deepskyblue', bd=2)
frame_left.place(x=20, y=100, width=400, height=400)

frame_right = tk.Frame(window, bg='deepskyblue', bd=2)
frame_right.place(x=460, y=100, width=400, height=400)

# Left Section (Attendance Display)
tk.Label(frame_left, text="For Already Registered", font=('Arial', 14, 'bold'), bg='limegreen').pack(fill='x')
tk.Button(frame_left, text="Take Attendance", font=('Arial', 14, 'bold'), bg='yellow', command=mark_attendance).pack(pady=10)

tree = ttk.Treeview(frame_left, columns=("ID", "NAME", "DATE", "TIME"), show='headings')
tree.heading("ID", text="ID")
tree.heading("NAME", text="NAME")
tree.heading("DATE", text="DATE")
tree.heading("TIME", text="TIME")
tree.pack(expand=True, fill='both')

update_treeview()

tk.Button(frame_left, text="Quit", font=('Arial', 14, 'bold'), bg='red', fg='white', command=window.quit).pack(fill='x', pady=5)


# Right Section (New User Registration)
tk.Label(frame_right, text="For New Registrations", font=('Arial', 14, 'bold'), bg='limegreen').pack(fill='x')

tk.Label(frame_right, text="Enter ID", font=('Arial', 12, 'bold'), bg='deepskyblue').pack(pady=5)
txt_id = tk.Entry(frame_right, font=('Arial', 12))
txt_id.pack()
tk.Button(frame_right, text="Clear", command=clear_id, bg='red', fg='white').pack()

tk.Label(frame_right, text="Enter Name", font=('Arial', 12, 'bold'), bg='deepskyblue').pack(pady=5)
txt_name = tk.Entry(frame_right, font=('Arial', 12))
txt_name.pack()
tk.Button(frame_right, text="Clear", command=clear_name, bg='red', fg='white').pack()

tk.Label(frame_right, text="1) Take Images >>> 2) Save Profile", font=('Arial', 10, 'bold'), bg='deepskyblue').pack(pady=5)

tk.Button(frame_right, text="Take Images", font=('Arial', 12, 'bold'), bg='blue', fg='white', command=capture_images).pack(pady=5)
tk.Button(frame_right, text="Save Profile", font=('Arial', 12, 'bold'), bg='blue', fg='white', command=save_profile).pack(pady=5)

lbl_count = tk.Label(frame_right, text="Total Registrations till now: 0", font=('Arial', 12), bg='deepskyblue')
lbl_count.pack(pady=10)




update_registration_count()
window.mainloop()
