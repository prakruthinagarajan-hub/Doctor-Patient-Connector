from PIL import Image
import customtkinter as ctk
from tkinter import messagebox,ttk
import mysql.connector

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ---------------- DATABASE ---------------- #
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="doctor_agency"
)
cursor = con.cursor()

# ---------------- VALIDATION ---------------- #
def validate_aadhar(a):
    return a.isdigit() and len(a) == 12

def validate_phone(p):
    return p.isdigit() and len(p) == 10

# ---------------- SIGNUP ---------------- #
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

    if not all([name, age, gender, area, aadhar, password,phone]):
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


def show_doctors():
    global current_patient

    area = current_patient[4]

    doc_win = ctk.CTkToplevel()
    doc_win.geometry("650x600")
    doc_win.title("Available Doctors")

    doc_win.lift()
    doc_win.focus_force()
    doc_win.grab_set()

    ctk.CTkLabel(
        doc_win,
        text=f"Doctors in {area}",
        font=("Segoe UI", 22, "bold")
    ).pack(pady=10)

    scroll_frame = ctk.CTkScrollableFrame(doc_win, width=600, height=300)
    scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)

    cursor.execute(
        "SELECT name, specialization, area, patients_count FROM doctors WHERE area=%s",
        (area,)
    )

    doctors = cursor.fetchall()

    if not doctors:
        ctk.CTkLabel(scroll_frame, text="No doctors available").pack(pady=20)
        return

    #  Selected doctor variable
    selected_doctor = ctk.StringVar(value="")

    #  Display doctors with radio button
    for doc in doctors:
        name, spec, area, count = doc

        card = ctk.CTkFrame(scroll_frame, corner_radius=15)
        card.pack(fill="x", pady=8, padx=10)

        ctk.CTkRadioButton(
            card,
            text=f"Dr. {name}",
            variable=selected_doctor,
            value=name
        ).pack(anchor="w", padx=10, pady=5)

        ctk.CTkLabel(
            card,
            text=f"Patients handled: {count}"
        ).pack(anchor="w", padx=10)

        ctk.CTkLabel(
            card,
            text=f"Specialization: {spec}"
        ).pack(anchor="w", padx=10)

        ctk.CTkLabel(
            card,
            text=f"Area: {area}"
        ).pack(anchor="w", padx=10)

    # Slot selection
    ctk.CTkLabel(doc_win, text="Select Time Slot").pack(pady=5)

    slot_box = ctk.CTkComboBox(
        doc_win,
        values=["9:00 - 10:00 am", "10:00 - 11:00 am", "2:00 - 3:00 pm","3:00 - 4:00 pm", "5:00 - 6:00 pm","6:00 - 7:00 pm"],
        width=250
    )
    slot_box.set("Choose Slot")
    slot_box.pack(pady=5)

    # Problem textbox
    ctk.CTkLabel(doc_win, text="Describe your problem").pack(pady=5)

    problem_box = ctk.CTkTextbox(doc_win, height=80, width=400)
    problem_box.pack(pady=5)

    #Submit function
    def submit_appointment():
        doctor = selected_doctor.get()
        slot = slot_box.get()
        problem = problem_box.get("1.0", "end").strip()

        if not doctor:
            messagebox.showerror("Error", "Select a doctor")
            return

        if slot == "Choose Slot":
            messagebox.showerror("Error", "Select a time slot")
            return

        if not problem:
            messagebox.showerror("Error", "Enter your problem")
            return

        try:
            cursor.execute(
                "INSERT INTO appointments(patient_aadhar, doctor_name, slot, problem) VALUES (%s,%s,%s,%s)",
                (current_patient[5], doctor, slot, problem)
            )
            con.commit()

            messagebox.showinfo("Success", "Appointment booked successfully")

            # Clear fields
            problem_box.delete("1.0", "end")
            slot_box.set("Choose Slot")
            selected_doctor.set("")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Submit button for appointment
    ctk.CTkButton(
        doc_win,
        text="Book Appointment",
        command=submit_appointment
    ).pack(pady=15)

# ---------------- LOGIN CHECK ---------------- #
def check_patient_login():
    global current_patient

    aadhar = p_login_aadhar.get()
    password = p_login_password.get()

    if not aadhar or not password:
        messagebox.showerror("Error", "All fields required")
        return

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

# ---------------- LOGIN WINDOW ---------------- #
def patient_login():
    pat = ctk.CTkToplevel()
    pat.geometry("400x400")
    pat.title("Patient Login")

    pat.lift()
    pat.focus_force()
    pat.grab_set()

    # Glass style frame
    frame = ctk.CTkFrame(pat, corner_radius=20)
    frame.pack(expand=True, fill="both", padx=30, pady=30)

    ctk.CTkLabel(
        frame,
        text="LOGIN",
        font=("Century Gothic", 26, "bold")
    ).pack(pady=20)

    global p_login_aadhar, p_login_password

    p_login_aadhar = ctk.CTkEntry(
        frame,
        placeholder_text="Aadhaar ID",
        width=260
    )
    p_login_aadhar.pack(pady=10)

    p_login_password = ctk.CTkEntry(
        frame,
        placeholder_text="Password",
        show="*",
        width=260
    )
    p_login_password.pack(pady=10)

    ctk.CTkButton(
        frame,
        text="Login",
        width=200,
        fg_color="green",
        hover_color="darkgreen",
        command=check_patient_login
    ).pack(pady=20)

# ---------------- SIGNUP WINDOW ---------------- #
def patient_window():
    root.withdraw()

    win = ctk.CTkToplevel()
    win.geometry("450x600")
    win.title("Patient Signup")

    frame = ctk.CTkFrame(win, corner_radius=25)
    frame.pack(expand=True, fill="both", padx=30, pady=30)

    ctk.CTkLabel(
        frame,
        text="SIGN UP",
        font=("Century Gothic", 26, "bold")
    ).pack(pady=20)

    global p_name, p_age, p_gender, p_area, p_aadhar,p_phone, p_password

    def create_entry(placeholder):
        entry = ctk.CTkEntry(frame, placeholder_text=placeholder, width=280)
        entry.pack(pady=8)
        return entry

    p_name = create_entry("Name")
    p_age = create_entry("Age")
    p_gender = ctk.CTkComboBox(frame,values=["Male", "Female", "Other"],width=280,state="readonly"  # user cannot type random text
    )
    p_gender.set("Select Gender")
    p_gender.pack(pady=8)
    p_area = create_entry("Area")
    p_aadhar = create_entry("Aadhaar ID")
    p_phone = create_entry("Phone Number")
    p_password = ctk.CTkEntry(frame, placeholder_text="Password", show="*", width=280)
    p_password.pack(pady=8)

    ctk.CTkButton(
        frame,
        text="Submit",
        width=220,
        command=patient_signup
    ).pack(pady=15)

    ctk.CTkButton(
        frame,
        text="Back",
        width=220,
        fg_color="green",
        command=lambda: win.destroy() or root.deiconify()
    ).pack(pady=5)

    ctk.CTkLabel(frame, text="Already have an account?").pack(pady=10)

    ctk.CTkButton(
        frame,
        text="Login",
        command=patient_login
    ).pack()

# ---------------- MAIN WINDOW ---------------- #
root = ctk.CTk()
root.geometry("500x350")
root.title("Hospital System")

# Background Image
bg_img = ctk.CTkImage(
    light_image=Image.open(r"C:\Users\ramya\Downloads\Medical.png"),
    dark_image=Image.open(r"C:\Users\ramya\Downloads\Medical.png"),
    size=(500, 350)
)

bg_label = ctk.CTkLabel(root, image=bg_img, text="")
bg_label.place(relwidth=1, relheight=1)

# Glass Card
main_frame = ctk.CTkFrame(root, corner_radius=25)
main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.85, relheight=0.8)

ctk.CTkLabel(
    main_frame,
    text="SP Hospitals & Health Care",
    font=("Arial", 22, "bold")
).pack(pady=20)

ctk.CTkLabel(
    main_frame,
    text="Welcome",
    font=("Arial", 16)
).pack()

btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
btn_frame.pack(pady=30)

ctk.CTkButton(
    btn_frame,
    text="Patient",
    width=140,
    command=patient_window
).pack(side="left", padx=10)

ctk.CTkButton(
    btn_frame,
    text="Doctor",
    width=140
).pack(side="left", padx=10)

root.mainloop()