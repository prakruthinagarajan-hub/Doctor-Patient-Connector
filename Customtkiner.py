import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# DATABASE CONNECTION

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin",
        database="doctor_db"
    )
root = ctk.CTk()
root.title("Doctor Database System")
root.geometry("700x500")

# FRAMES
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
