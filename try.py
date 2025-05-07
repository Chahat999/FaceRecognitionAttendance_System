import cv2
import os
import numpy as np
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import csv
from datetime import datetime
from tap import *

# Directories
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

    existing_ids = set()
    if os.path.exists("StudentDetails.csv"):
        with open("StudentDetails.csv", 'r', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 2:
                    existing_ids.add(row[0].strip())

    if Id in existing_ids:
        messagebox.showerror("Duplicate Entry", f"ID {Id} already exists. Please use a different ID.")
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

def mark_attendance():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    try:
        recognizer.read("Trainer.yml")
    except:
        messagebox.showerror("Error", "Trainer file not found. Train the model first.")
        return

    # Load existing student details
    student_dict = {}
    with open("StudentDetails.csv", 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:
                student_dict[row[0]] = row[1]

    today = datetime.now().strftime('%d-%m-%Y')
    already_marked = set()

    # Load today's attendance
    attendance_file = "Attendance/Attendance.csv"
    if os.path.exists(attendance_file):
        with open(attendance_file, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 3 and row[2] == today:
                    already_marked.add(row[0])

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    new_attendance = set()

    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in faces:
            Id, conf = recognizer.predict(gray[y:y+h, x:x+w])
            if conf < 50 and str(Id) in student_dict:
                if str(Id) not in already_marked and str(Id) not in new_attendance:
                    name = student_dict[str(Id)]
                    time_now = datetime.now().strftime('%H:%M:%S')
                    with open(attendance_file, 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([Id, name, today, time_now])
                    new_attendance.add(str(Id))
                    print(f"Marked: {Id}, {name}")
                name = student_dict.get(str(Id), "Unknown")
                cv2.putText(img, f"{name}", (x+5, y-5), font, 1, (0, 255, 0), 2)
            else:
                cv2.putText(img, "Unknown", (x+5, y-5), font, 1, (0, 0, 255), 2)

            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 0), 2)

        cv2.imshow('Recognizing Faces - Press Q to Exit', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
    update_treeview(new_attendance, student_dict)
    
def check_student_attendance():
    student_id = entry_check_id.get().strip()
    if not student_id:
        messagebox.showwarning("Input Error", "Please enter a student ID.")
        return

    if not os.path.exists("Attendance/Attendance.csv"):
        messagebox.showinfo("No Records", "No attendance records found.")
        return

    count = 0
    with open("Attendance/Attendance.csv", 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == student_id:
                count += 1

    if count > 0:
        messagebox.showinfo("Attendance Count", f"Student ID {student_id} has been marked present {count} times.")
    else:
        messagebox.showinfo("No Attendance", f"No attendance found for Student ID {student_id}.")
        
def load_existing_attendance():
    tree.delete(*tree.get_children())  # clear previous rows
    if not os.path.exists("Attendance/Attendance.csv"):
        return
    with open("Attendance/Attendance.csv", 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 4:
                tree.insert('', 'end', values=(row[0], row[1], row[2], row[3]))



def update_treeview(attendance_list, student_dict):
    attendance_file = "Attendance/Attendance.csv"

    # Read entire attendance history
    all_attendance = []
    if os.path.exists(attendance_file):
        with open(attendance_file, 'r') as f:
            reader = csv.reader(f)
            all_attendance = list(reader)

    # Clear existing TreeView
    for item in tree.get_children():
        tree.delete(item)

    for Id in attendance_list:
        name = student_dict.get(str(Id), "Unknown")
        date = datetime.now().strftime('%d-%m-%Y')
        time = datetime.now().strftime('%H:%M:%S')

        # Count how many times this student was marked present
        student_attendance_count = sum(1 for row in all_attendance if row[0] == str(Id))

        tree.insert('', 'end', values=[Id, name, date, time, student_attendance_count])


# GUI Layout
title = tk.Label(window, text="Face Recognition Based Attendance System", font=('Times New Roman', 20, 'bold'), fg='white', bg='black')
window.state('zoomed')
# window.state('zoomed')  # Windows only
# window.attributes('-fullscreen', True)




title.pack(pady=10)

time_label = tk.Label(window, text=datetime.now().strftime('%d-%b-%Y  |  %H:%M:%S'), font=('Times New Roman', 16), fg='orange', bg='black')
time_label.pack()

frame_left = tk.Frame(window, bg='deepskyblue', bd=2)
frame_left.place(x=20, y=130, width=1000, height=600)

frame_right = tk.Frame(window, bg='deepskyblue', bd=2)
frame_right.place(x=1030, y=130, width=500, height=600)

# # Left Section
tk.Label(frame_left, text="For Already Registered", font=('Times New Roman', 16, 'bold'), bg='limegreen' ,relief=tk.RIDGE).pack(fill='x')
tk.Button(frame_left, text="Take Attendance", font=('Times New Roman', 14, 'bold'), bg='yellow', command=mark_attendance).pack(pady=10)

tree = ttk.Treeview(frame_left, columns=("ID", "NAME", "DATE", "TIME"), show='headings')
tree.heading("ID", text="ID")
tree.heading("NAME", text="NAME")
tree.heading("DATE", text="DATE")
tree.heading("TIME", text="TIME")
# tree.heading("COUNT", text="TOTAL ATTENDANCE")


# # Frame for Already Registered (left side)
# left_frame = tk.Frame(window, bg="deepskyblue", bd=10, relief=tk.RIDGE)
# left_frame.place(x=20, y=100, width=250, height=300)

# # Label
# tk.Label(left_frame, text="Attendance", font=("Arial", 16, "bold"), bg="deepskyblue").pack()

# # Treeview widget
# columns = ('ID', 'Name', 'Date', 'Time')
# tree = ttk.Treeview(left_frame, columns=columns, show='headings')
# for col in columns:
#     tree.heading(col, text=col)
#     tree.column(col, width=100)
tree.pack(expand=True, fill=tk.BOTH)


# Label and Entry to check attendance count for specific student
tk.Label(frame_left, text="Check Attendance Count for (Enter ID):", font=('Times New roman', 14, 'bold'), bg='deepskyblue').pack(pady=5)
entry_check_id = tk.Entry(frame_left, font=('Times New Roman', 14))
entry_check_id.pack()
tk.Button(frame_left, text="Check Count", font=('Times New Roman', 13, 'bold'), bg='blue', fg='white', command=check_student_attendance).pack(pady=5)

update_treeview([], {})  # Initialize with empty attendance list

tk.Button(frame_left, text="Quit", font=('Times New Roman', 14, 'bold'), bg='red', fg='white', command=window.quit).pack(fill='x', pady=5)



# Right Section
tk.Label(frame_right, text="For New Registrations", font=('Times New Roman', 16, 'bold'), bg='limegreen',relief=tk.RIDGE).pack(fill='x')

tk.Label(frame_right, text="Enter ID", font=('Times New Roman', 15, 'bold'), bg='deepskyblue').pack(pady=10)
txt_id = tk.Entry(frame_right, font=('Times New Roman', 15))
txt_id.pack()
tk.Button(frame_right, text="Clear", command=clear_id, bg='red', fg='white').pack(pady=10)

tk.Label(frame_right, text="Enter Name", font=('Times New Roman', 15, 'bold'), bg='deepskyblue').pack(pady=15)
txt_name = tk.Entry(frame_right, font=('Times New Roman', 15))
txt_name.pack()
tk.Button(frame_right, text="Clear", command=clear_name, bg='red', fg='white').pack(pady=10)

tk.Label(frame_right, text="1)Take Images  >>>  2)Save Profile", font=('Times New Roman', 14, 'bold'), bg='deepskyblue').pack(pady=10)
tk.Button(frame_right, text="Take Images", font=('Times New Roman', 15, 'bold'), bg='blue', fg='white', command=capture_images).pack(pady=10)
tk.Button(frame_right, text="Save Profile", font=('Times New Roman', 15, 'bold'), bg='blue', fg='white', command=save_profile).pack(pady=10)

lbl_count = tk.Label(frame_right, text="Total Registrations till now  : 0", font=('Arial', 12), bg='deepskyblue')
lbl_count.pack(pady=10)

update_registration_count()
load_existing_attendance()

# Main loop
window.mainloop()



# import tkinter as tk
# from tkinter import ttk
# from datetime import datetime

# window = tk.Tk()
# window.title("Face Recognition Based Attendance System")
# window.state('zoomed')  # Fullscreen for Windows

# # Title
# tk.Label(window, text="Face Recognition Based Attendance System",
#          font=('Arial', 26, 'bold'), fg='black', bg='black').pack(fill='x', pady=5)

# # Clock
# time_label = tk.Label(window, text=datetime.now().strftime('%d-%b-%Y  |  %H:%M:%S'),
#                       font=('Arial', 18), fg='orange', bg='black')
# time_label.pack(fill='x')

# # Frame for left (Already Registered)
# frame_left = tk.Frame(window, bg='deepskyblue', bd=2)
# frame_left.place(relx=0.05, rely=0.2, relwidth=0.4, relheight=0.7)

# tk.Label(frame_left, text="For Already Registered", font=('Arial', 16, 'bold'), bg='limegreen').pack(fill='x', pady=5)
# tk.Button(frame_left, text="Take Attendance", font=('Arial', 14, 'bold'),
#           bg='yellow', command=lambda: print("Attendance")).pack(pady=5)

# tree = ttk.Treeview(frame_left, columns=("ID", "NAME", "DATE", "TIME", "COUNT"), show='headings')
# for col in ("ID", "NAME", "DATE", "TIME", "COUNT"):
#     tree.heading(col, text=col)
#     tree.column(col, width=80)
# tree.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

# tk.Label(frame_left, text="Check Attendance Count (Enter ID):",
#          font=('Arial', 12, 'bold'), bg='deepskyblue').pack(pady=5)
# entry_check_id = tk.Entry(frame_left, font=('Arial', 12))
# entry_check_id.pack()
# tk.Button(frame_left, text="Check Count", font=('Arial', 12, 'bold'),
#           bg='blue', fg='white', command=lambda: print("Check")).pack(pady=5)

# tk.Button(frame_left, text="Quit", font=('Arial', 14, 'bold'),
#           bg='red', fg='white', command=window.quit).pack(fill='x', pady=5)


# # Frame for right (New Registrations)
# frame_right = tk.Frame(window, bg='deepskyblue', bd=2)
# frame_right.place(relx=0.55, rely=0.2, relwidth=0.4, relheight=0.7)

# tk.Label(frame_right, text="For New Registrations", font=('Arial', 16, 'bold'), bg='limegreen').pack(fill='x', pady=5)

# tk.Label(frame_right, text="Enter ID", font=('Arial', 12, 'bold'), bg='deepskyblue').pack(pady=5)
# txt_id = tk.Entry(frame_right, font=('Arial', 12))
# txt_id.pack()
# tk.Button(frame_right, text="Clear", command=lambda: txt_id.delete(0, 'end'),
#           bg='red', fg='white').pack()

# tk.Label(frame_right, text="Enter Name", font=('Arial', 12, 'bold'), bg='deepskyblue').pack(pady=5)
# txt_name = tk.Entry(frame_right, font=('Arial', 12))
# txt_name.pack()
# tk.Button(frame_right, text="Clear", command=lambda: txt_name.delete(0, 'end'),
#           bg='red', fg='white').pack()

# tk.Label(frame_right, text="1)Take Images  >>>  2)Save Profile",
#          font=('Arial', 10, 'bold'), bg='deepskyblue').pack(pady=10)

# tk.Button(frame_right, text="Take Images", font=('Arial', 12, 'bold'),
#           bg='blue', fg='white', command=lambda: print("Take")).pack(pady=5)
# tk.Button(frame_right, text="Save Profile", font=('Arial', 12, 'bold'),
#           bg='blue', fg='white', command=lambda: print("Save")).pack(pady=5)

# lbl_count = tk.Label(frame_right, text="Total Registrations till now  : 1",
#                      font=('Arial', 12), bg='deepskyblue')
# lbl_count.pack(pady=10)

# load_existing_attendance()
# update_treeview([], {})  # Initialize with empty attendance list

# window.mainloop()
