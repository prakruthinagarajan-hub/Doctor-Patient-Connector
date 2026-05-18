import tkinter
import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.geometry("900x600")
root.title("Doctor System")
home_frame = ctk.CTkFrame(root)
login_frame = ctk.CTkFrame(root)
signup_frame = ctk.CTkFrame(root)



# ================= DB =================
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin",
        database="doctor_db"
    )

# ================= DASHBOARD =================
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
e_aadhar = ctk.CTkEntry(signup_frame, placeholder_text="Aadhar ID", width=300)
e_locality = ctk.CTkEntry(signup_frame, placeholder_text="Locality", width=300)
e_docid = ctk.CTkEntry(signup_frame, placeholder_text="Doctor ID", width=300)
e_password = ctk.CTkEntry(signup_frame, placeholder_text="Password", show="*", width=300)

entries = [e_name, e_age, e_aadhar, e_locality, e_docid, e_password]

for entry in entries:
    entry.pack(pady=8)


# SIGNUP

def signup():
    name = e_name.get()
    age = e_age.get()
    aadhar = e_aadhar.get()
    locality = e_locality.get()
    docid = e_docid.get()
    password = e_password.get()

    if not all([name, age, aadhar, locality, docid, password]):
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Insert doctor
        sql = """
        INSERT INTO doctors
        (name, age, aadhar_id, locality, tn_doctor_id, password)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (
            name,
            age,
            aadhar,
            locality,
            docid,
            password
        ))

        # Insert locality if not exists
        locality_sql = """
        INSERT IGNORE INTO locality(locality_name)
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
        FROM doctors
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

root.mainloop()

