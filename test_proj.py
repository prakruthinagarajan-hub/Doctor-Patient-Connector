


import tkinter
import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image

root = ctk.CTk()
root.geometry("900x600")
root.title("Doctor System")
home_frame = ctk.CTkFrame(root)
login_frame = ctk.CTkFrame(root)
signup_frame = ctk.CTkFrame(root)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ---------------- DATABASE ---------------- #
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="main_db"
)
cursor = con.cursor()

# ---------------- VALIDATION ---------------- #
def validate_aadhar_id(a):
    return a.isdigit() and len(a) == 12

def validate_phone(p):
    return p.isdigit() and len(p) == 10

# ---------------- SIGNUP ---------------- #
def patient_signup():
    name = p_name.get()
    age = p_age.get()
    gender = p_gender.get()
    locality = p_locality.get()
    aadhar_id = p_aadhar_id.get()
    phone = p_phone.get()
    password = p_password.get()

    
    if not validate_aadhar_id(aadhar_id):
        messagebox.showerror("Error", "Invalid Aadhaar")
        return

    if not validate_phone(phone):
        messagebox.showerror("Error", "Invalid Phone Number")
        return

    if not all([name, age, gender, locality, aadhar_id, phone,password]):
        messagebox.showerror("Error", "All fields required")
        return

    try:
        cursor.execute(
            "INSERT INTO patient(name,age,gender,locality,aadhar_id,phone,password) VALUES(%s,%s,%s,%s,%s,%s,%s)",
            (name, age, gender, locality, aadhar_id, phone,password)
        )
        con.commit()
        messagebox.showinfo("Success", "Patient Registered")
    except mysql.connector.IntegrityError as e:
        if "aadhar_id" in str(e):
         messagebox.showerror("Error", "Aadhaar ID already exists")
        elif "phone" in str(e):
            messagebox.showerror("Error", "Phone number already exists")
        else:
            messagebox.showerror("Database Error", str(e))

    except Exception as e:
        messagebox.showerror("Error", str(e))


def show_doctors():
    global current_patient

    locality = current_patient[4]

    doc_win = ctk.CTkToplevel()
    doc_win.geometry("650x600")
    doc_win.title("Available Doctors")

    doc_win.lift()
    doc_win.focus_force()
    doc_win.grab_set()

    ctk.CTkLabel(
        doc_win,
        text=f"Doctors in {locality}",
        font=("Segoe UI", 22, "bold")
    ).pack(pady=10)

    scroll_frame = ctk.CTkScrollableFrame(doc_win, width=600, height=300)
    scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)

    cursor.execute(
        "SELECT name, specialization, locality, patients_count FROM doctors WHERE locality=%s",
        (locality,)
    )

    doctors = cursor.fetchall()

    if not doctors:
        ctk.CTkLabel(scroll_frame, text="No doctors available").pack(pady=20)
        return

    #  Selected doctor variable
    selected_doctor = ctk.StringVar(value="")

    #  Display doctors with radio button
    for doc in doctors:
        name, spec, locality, count = doc

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
            text=f"Locality: {locality}"
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
                "INSERT INTO appointments(patient_aadhar_id, doctor_name, slot, problem) VALUES (%s,%s,%s,%s)",
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

    aadhar_id = p_login_aadhar_id.get()
    password = p_login_password.get()

    if not aadhar_id or not password:
        messagebox.showerror("Error", "All fields required")
        return

    cursor.execute(
        "SELECT * FROM patient WHERE aadhar_id=%s AND password=%s",
        (aadhar_id, password)
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

    global p_login_aadhar_id, p_login_password

    p_login_aadhar_id = ctk.CTkEntry(
        frame,
        placeholder_text="Aadhaar ID",
        width=260
    )
    p_login_aadhar_id.pack(pady=10)

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

    global p_name, p_age, p_gender, p_locality, p_aadhar_id,p_phone, p_password

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
    p_locality = create_entry("Locality")
    p_aadhar_id = create_entry("Aadhaar ID")
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


#--------------------doctors page-----------------------#

def doctor_window():



    def connect_db():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin",
            database="doctor_agency")

    def open_dashboard(doctor_name):

        dash = ctk.CTkToplevel()
        dash.title("Doctor Dashboard")
        dash.geometry("1200x700")

        dash.grid_columnconfigure(0, weight=1)
        dash.grid_columnconfigure(1, weight=1)
        dash.grid_rowconfigure(0, weight=1)
        dash.grid_rowconfigure(1, weight=1)

        # =====================================================
        # 🔵 TOP LEFT - PATIENTS
        # =====================================================
        frame_patients = ctk.CTkFrame(dash)
        frame_patients.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        ctk.CTkLabel(frame_patients, text="Patients", font=("Arial", 20, "bold")).pack(pady=10)

        listbox = ctk.CTkTextbox(frame_patients)
        listbox.pack(fill="both", expand=True)

        # =====================================================
        def load_patients():

            conn = connect_db()
            cur = conn.cursor()

            cur.execute("""
                SELECT r.patient_id, p.name, r.ailment, r.time_slot, r.status
                FROM request r
                JOIN patient p ON p.patient_id = r.patient_id
            """)

            rows = cur.fetchall()
            conn.close()

            listbox.delete("1.0", "end")

            for r in rows:
                listbox.insert("end", f"{r[0]} - {r[1]} | {r[3]} | {r[4]}\n")

        # =====================================================
        def show_patient(pid):

            conn = connect_db()
            cur = conn.cursor()

            cur.execute("SELECT name, age, gender FROM patient WHERE patient_id=%s", (pid,))
            p = cur.fetchone()

            cur.execute("SELECT ailment, time_slot FROM request WHERE patient_id=%s", (pid,))
            r = cur.fetchone()

            conn.close()

            popup = ctk.CTkToplevel(dash)
            popup.geometry("350x300")

            ctk.CTkLabel(popup, text="Patient Details", font=("Arial", 18, "bold")).pack(pady=10)

            ctk.CTkLabel(popup, text=f"Name: {p[0]}").pack()
            ctk.CTkLabel(popup, text=f"Age: {p[1]}").pack()
            ctk.CTkLabel(popup, text=f"Gender: {p[2]}").pack()

            ctk.CTkLabel(popup, text=f"Ailment: {r[0]}").pack()
            ctk.CTkLabel(popup, text=f"Time Slot: {r[1]}").pack()

        # ---------------- ACCEPT / REJECT ----------------
        def update(status):

            conn = connect_db()
            cur = conn.cursor()

            cur.execute("""
                UPDATE request
                SET status=%s
                WHERE patient_id=%s
            """, (status, pid))

            conn.commit()
            conn.close()

            popup.destroy()

            # 🔥 THIS REMOVES REJECTED PATIENT FROM LIST
            load_patients()

            ctk.CTkButton(
                popup,
                text="Accept",
                fg_color="green",
                command=lambda: update("accepted")
            ).pack(pady=10)

            ctk.CTkButton(
                popup,
                text="Reject",
                fg_color="red",
                command=lambda: update("rejected")
            ).pack(pady=5)

        # click handler
        def on_click(event):
            text = listbox.get("1.0", "end").strip().split("\n")[0]
            if text:
                pid = text.split(" - ")[0]
                show_patient(pid)

        listbox.bind("<Double-Button-1>", on_click)

        load_patients()

        # =====================================================
        # 🔵 TOP RIGHT - CALENDAR
        # =====================================================
        calendar = ctk.CTkFrame(dash)
        calendar.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        ctk.CTkLabel(calendar, text="Appointments", font=("Arial", 20, "bold")).pack(pady=10)

        slots = ["morning", "afternoon", "evening"]

        def load_calendar():

            for widget in calendar.winfo_children()[1:]:
                widget.destroy()

            for slot in slots:

                box = ctk.CTkFrame(calendar)
                box.pack(fill="x", pady=5)

                ctk.CTkLabel(box, text=slot.upper(), font=("Arial", 16, "bold")).pack()

                conn = connect_db()
                cur = conn.cursor()

                cur.execute("""
                    SELECT p.name
                    FROM request r
                    JOIN patient p ON p.patient_id = r.patient_id
                    WHERE r.time_slot=%s AND r.status='accepted'
                """, (slot,))

                patients = cur.fetchall()
                conn.close()

                for p in patients:
                    ctk.CTkLabel(box, text=p[0]).pack()

        load_calendar()

        # =====================================================
        # 🔵 BOTTOM LEFT - ANALYTICS
        # =====================================================
        analytics = ctk.CTkFrame(dash)
        analytics.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        ctk.CTkLabel(analytics, text="Analytics", font=("Arial", 20, "bold")).pack()

        def load_graph():

            conn = connect_db()
            cur = conn.cursor()

            cur.execute("""
                SELECT status, COUNT(*)
                FROM request
                GROUP BY status
            """)

            data = cur.fetchall()
            conn.close()

            if not data:
                return

            labels = [d[0] for d in data]
            values = [d[1] for d in data]

            fig = plt.Figure(figsize=(4,3))
            ax = fig.add_subplot(111)
            ax.bar(labels, values, color=["green", "red", "orange"])
            ax.set_title("Request Status")

            canvas = FigureCanvasTkAgg(fig, analytics)
            canvas.get_tk_widget().pack()
            canvas.draw()

        load_graph()

        # =====================================================
        # 🔵 BOTTOM RIGHT - USER INFO + LOGOUT
        # =====================================================
        bottom = ctk.CTkFrame(dash)
        bottom.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        ctk.CTkLabel(bottom, text=f"Dr. {doctor_name}", font=("Arial", 18)).pack(pady=20)

        def logout():
            dash.destroy()

        ctk.CTkButton(bottom, text="Logout", fg_color="red", command=logout).pack(pady=20)# FRAMES
    home_frame = ctk.CTkFrame(root)
    signup_frame = ctk.CTkFrame(root)
    login_frame = ctk.CTkFrame(root)

    for frame in (home_frame, signup_frame, login_frame):
        frame.place(relwidth=1, relheight=1)

    # FRAME SWITCH FUNCTION
    #All screens are created as frames inside one window. The function tkraise() brings the required frame to the front, making it visible while hiding the others behind it.
    def show_frame(frame):
        frame.tkraise()


    #HOME
    title = ctk.CTkLabel(
        home_frame,
        text="Doctor Database System",
        font=("Century Gothic", 30, "bold")
    )
    title.pack(pady=50)
    signup_btn = ctk.CTkButton(
        home_frame,
        text="Sign Up",
        width=250,
        height=45,
        font=("Century Gothic", 18, "bold"),
        command=lambda: show_frame(signup_frame)
    )
    signup_btn.pack(pady=20)

    login_btn = ctk.CTkButton(
        home_frame,
        text="Login",
        width=250,
        height=45,
        font=("Century Gothic", 18, "bold"),
        fg_color="green",
        hover_color="darkgreen",
        command=lambda: show_frame(login_frame)
    )
    login_btn.pack(pady=20)

    # SIGNUP PAGE
    signup_title = ctk.CTkLabel(
        signup_frame,
        text="SIGN UP",
        font=("Century Gothic", 28, "bold")
    )
    signup_title.pack(pady=20)

    # Entries
    e_name = ctk.CTkEntry(signup_frame, placeholder_text="Name", width=300)
    e_age = ctk.CTkEntry(signup_frame, placeholder_text="Age", width=300)
    e_aadhar_id = ctk.CTkEntry(signup_frame, placeholder_text="Aadhar ID", width=300)
    e_specialization = ctk.CTkEntry(signup_frame, placeholder_text="Specialization", width=300)
    e_locality = ctk.CTkEntry(signup_frame, placeholder_text="Locality", width=300)
    e_tn_doctor_id = ctk.CTkEntry(signup_frame, placeholder_text="Doctor ID", width=300)
    e_password = ctk.CTkEntry(signup_frame, placeholder_text="Password", show="*", width=300)

    entries = [e_name, e_age, e_aadhar_id, e_specialization, e_locality, e_tn_doctor_id, e_password]

    for entry in entries:
        entry.pack(pady=8)


    # SIGNUP

    def signup():
        name = e_name.get()
        age = e_age.get()
        aadhar = e_aadhar_id.get()
        specialization = e_specialization.get()
        locality = e_locality.get()
        docid = e_tn_doctor_id.get()
        password = e_password.get()

        if not all([name, age, aadhar, specialization, locality, docid, password]):
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()

            # Insert doctor
            sql = """
            INSERT INTO doctor
            (name, age, aadhar_id, specialization, locality, tn_doctor_id, password)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(sql, (
                name,
                age,
                aadhar,
                specialization,
                locality,
                docid,
                password
            ))

            # Insert locality if not exists
            locality_sql = """
            INSERT IGNORE INTO doctor(locality)
            VALUES (%s)
            """

            cursor.execute(locality_sql, (locality,))

            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo("Success", "Registered Successfully!")

            # Clear fields
            for entry in entries:
                entry.delete(0, "end")

            show_frame(home_frame)

        except mysql.connector.IntegrityError as e:

            # Duplicate Aadhar / Doctor ID
            if "aadhar_id" in str(e):
                messagebox.showerror(
                    "Duplicate Error",
                    "Aadhar ID already registered!"
                )

            elif "tn_doctor_id" in str(e):
                messagebox.showerror(
                    "Duplicate Error",
                    "Doctor ID already exists!"
                )

            else:
                messagebox.showerror("Database Error", str(e))

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    # Buttons
    submit_btn = ctk.CTkButton(
        signup_frame,
        text="Submit",
        width=200,
        command=signup
    )
    submit_btn.pack(pady=15)

    back_btn1 = ctk.CTkButton(
        signup_frame,
        text="Back",
        width=200,
        fg_color="gray",
        command=lambda: show_frame(home_frame)
    )
    back_btn1.pack()


    # LOGIN
    login_title = ctk.CTkLabel(
        login_frame,
        text="LOGIN",
        font=("Century Gothic", 28, "bold")
    )
    login_title.pack(pady=30)

    login_aadhar = ctk.CTkEntry(
        login_frame,
        placeholder_text="Aadhar ID",
        width=300
    )
    login_aadhar.pack(pady=10)

    login_password = ctk.CTkEntry(
        login_frame,
        placeholder_text="Password",
        show="*",
        width=300
    )
    login_password.pack(pady=10)


    # LOGIN FUNCTION
    def login():

        aadhar = login_aadhar.get()
        password = login_password.get()

        if not aadhar or not password:
            messagebox.showerror("Error", "All fields required!")
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()

            query = """
            SELECT name
            FROM doctor
            WHERE aadhar_id=%s AND password=%s
            """

            cursor.execute(query, (aadhar, password))

            result = cursor.fetchone()

            cursor.close()
            conn.close()

            if result:
                messagebox.showinfo(
                    "Welcome",
                    f"Welcome Dr. {result[0]}!"
                )
                open_dashboard(result[0])
            else:
                messagebox.showerror(
                    "Login Failed",
                    "Invalid credentials!"
                )

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    # Buttons
    login_btn2 = ctk.CTkButton(
        login_frame,
        text="Login",
        width=200,
        fg_color="green",
        hover_color="darkgreen",
        command=login
    )
    login_btn2.pack(pady=20)

    back_btn2 = ctk.CTkButton(
        login_frame,
        text="Back",
        width=200,
        fg_color="gray",
        command=lambda: show_frame(home_frame)
    )
    back_btn2.pack()


    #START

    show_frame(home_frame)


# ---------------- MAIN WINDOW ---------------- #


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
    width=140,
    command=doctor_window
).pack(side="left", padx=10)

root.mainloop()