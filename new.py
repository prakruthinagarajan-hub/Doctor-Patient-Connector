import tkinter
import customtkinter as ctk
from tkinter import messagebox, ttk
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ================= ROOT =================
root = ctk.CTk()
root.geometry("900x600")
root.title("Hospital System")

# ================= DB =================
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin",
        database="doctor_db"
    )

# ================= PATIENT DB =================
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="doctor_agency"
)
cursor = con.cursor()

# ================= PATIENT FUNCTIONS =================
def validate_aadhar(a):
    return a.isdigit() and len(a) == 12

def validate_phone(p):
    return p.isdigit() and len(p) == 10

def patient_signup():
    name = p_name.get()
    age = p_age.get()
    gender = p_gender.get()
    area = p_area.get()
    aadhar = p_aadhar.get()
    password = p_password.get()
    phone = p_phone.get()

    if not validate_aadhar(aadhar):
        messagebox.showerror("Error", "Invalid Aadhaar")
        return

    if not validate_phone(phone):
        messagebox.showerror("Error", "Invalid Phone Number")
        return

    if not all([name, age, gender, area, aadhar, password, phone]):
        messagebox.showerror("Error", "All fields required")
        return

    try:
        cursor.execute(
            "INSERT INTO patients(name,age,gender,area,aadhar,password,phone) VALUES(%s,%s,%s,%s,%s,%s,%s)",
            (name, age, gender, area, aadhar, password, phone)
        )
        con.commit()
        messagebox.showinfo("Success", "Patient Registered")
    except:
        messagebox.showerror("Error", "Aadhaar already exists")

def check_patient_login():
    global current_patient
    aadhar = p_login_aadhar.get()
    password = p_login_password.get()

    cursor.execute(
        "SELECT * FROM patients WHERE aadhar=%s AND password=%s",
        (aadhar, password)
    )
    user = cursor.fetchone()

    if user:
        current_patient = user
        messagebox.showinfo("Success", "Logged in Successfully")
        show_doctors()
    else:
        messagebox.showerror("Error", "Invalid login")

def show_doctors():
    global current_patient

    area = current_patient[4]

    doc_win = ctk.CTkToplevel()
    doc_win.geometry("650x600")
    doc_win.title("Available Doctors")

    ctk.CTkLabel(doc_win, text=f"Doctors in {area}", font=("Segoe UI", 22, "bold")).pack(pady=10)

    scroll_frame = ctk.CTkScrollableFrame(doc_win, width=600, height=300)
    scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)

    cursor.execute(
        "SELECT name, specialization, area, patients_count FROM doctors WHERE area=%s",
        (area,)
    )
    doctors = cursor.fetchall()

    selected_doctor = ctk.StringVar(value="")

    for doc in doctors:
        name, spec, area, count = doc

        card = ctk.CTkFrame(scroll_frame)
        card.pack(fill="x", pady=8)

        ctk.CTkRadioButton(card, text=f"Dr. {name}", variable=selected_doctor, value=name).pack(anchor="w")
        ctk.CTkLabel(card, text=f"Patients handled: {count}").pack(anchor="w")
        ctk.CTkLabel(card, text=f"Specialization: {spec}").pack(anchor="w")

    slot_box = ctk.CTkComboBox(doc_win, values=["morning", "afternoon", "evening"])
    slot_box.pack(pady=10)

    problem_box = ctk.CTkTextbox(doc_win, height=80)
    problem_box.pack(pady=10)

    def submit():
        doctor = selected_doctor.get()
        slot = slot_box.get()
        problem = problem_box.get("1.0", "end").strip()

        cursor.execute(
            "INSERT INTO appointments(patient_aadhar, doctor_name, slot, problem) VALUES (%s,%s,%s,%s)",
            (current_patient[5], doctor, slot, problem)
        )
        con.commit()
        messagebox.showinfo("Success", "Appointment booked")

    ctk.CTkButton(doc_win, text="Book Appointment", command=submit).pack(pady=10)

def patient_login():
    pat = ctk.CTkToplevel()
    pat.geometry("400x400")

    global p_login_aadhar, p_login_password

    p_login_aadhar = ctk.CTkEntry(pat, placeholder_text="Aadhaar")
    p_login_aadhar.pack(pady=10)

    p_login_password = ctk.CTkEntry(pat, placeholder_text="Password", show="*")
    p_login_password.pack(pady=10)

    ctk.CTkButton(pat, text="Login", command=check_patient_login).pack(pady=20)

def patient_window():
    win = ctk.CTkToplevel()
    win.geometry("450x600")

    global p_name, p_age, p_gender, p_area, p_aadhar, p_phone, p_password

    def create_entry(text):
        e = ctk.CTkEntry(win, placeholder_text=text)
        e.pack(pady=8)
        return e

    p_name = create_entry("Name")
    p_age = create_entry("Age")
    p_gender = ctk.CTkComboBox(win, values=["Male", "Female", "Other"])
    p_gender.pack(pady=8)
    p_area = create_entry("Area")
    p_aadhar = create_entry("Aadhaar")
    p_phone = create_entry("Phone")
    p_password = create_entry("Password")

    ctk.CTkButton(win, text="Submit", command=patient_signup).pack(pady=10)
    ctk.CTkButton(win, text="Login", command=patient_login).pack(pady=10)

# ================= DOCTOR DASHBOARD =================
def open_dashboard(name):
    dash = ctk.CTkToplevel()
    dash.geometry("600x400")
    ctk.CTkLabel(dash, text=f"Welcome Dr. {name}").pack(pady=20)

# ================= FRAMES =================
home_frame = ctk.CTkFrame(root)
login_frame = ctk.CTkFrame(root)
signup_frame = ctk.CTkFrame(root)

for f in (home_frame, login_frame, signup_frame):
    f.place(relwidth=1, relheight=1)

def show_frame(frame):
    frame.tkraise()

# ================= HOME =================
ctk.CTkLabel(home_frame, text="Hospital System", font=("Arial", 30)).pack(pady=40)

ctk.CTkButton(home_frame, text="Doctor Login", command=lambda: show_frame(login_frame)).pack(pady=10)
ctk.CTkButton(home_frame, text="Doctor Signup", command=lambda: show_frame(signup_frame)).pack(pady=10)

# 👉 ADDED PATIENT BUTTON
ctk.CTkButton(home_frame, text="Patient", fg_color="orange", command=patient_window).pack(pady=10)

# ================= LOGIN =================
login_aadhar = ctk.CTkEntry(login_frame, placeholder_text="Aadhar")
login_aadhar.pack(pady=10)

login_password = ctk.CTkEntry(login_frame, placeholder_text="Password", show="*")
login_password.pack(pady=10)

def login():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT name FROM doctors WHERE aadhar_id=%s AND password=%s",
                (login_aadhar.get(), login_password.get()))
    res = cur.fetchone()
    conn.close()

    if res:
        open_dashboard(res[0])
    else:
        messagebox.showerror("Error", "Invalid Login")

ctk.CTkButton(login_frame, text="Login", command=login).pack(pady=10)
ctk.CTkButton(login_frame, text="Back", command=lambda: show_frame(home_frame)).pack()

# ================= SIGNUP =================
e_name = ctk.CTkEntry(signup_frame, placeholder_text="Name")
e_name.pack(pady=8)

e_aadhar = ctk.CTkEntry(signup_frame, placeholder_text="Aadhar")
e_aadhar.pack(pady=8)

e_password = ctk.CTkEntry(signup_frame, placeholder_text="Password")
e_password.pack(pady=8)

def signup():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO doctors(name,aadhar_id,password) VALUES(%s,%s,%s)",
                (e_name.get(), e_aadhar.get(), e_password.get()))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Doctor Registered")

ctk.CTkButton(signup_frame, text="Submit", command=signup).pack(pady=10)
ctk.CTkButton(signup_frame, text="Back", command=lambda: show_frame(home_frame)).pack()

# ================= START =================
show_frame(home_frame)
root.mainloop()
