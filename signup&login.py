#MISTAKES + FIXES
# Unique Aadhar ID needed for new registrations, must show pop up if the same ID is used more than once.
#   -> 'UNIQUE' constraint in SQL
#   -> To solve the MySQL error, update the py. code; LINE 130 
# Same for Dr ID 
 
#Connection Code:
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="doctor_db"
)
cursor = conn.cursor()

#START

import tkinter as tk
from tkinter import messagebox
import mysql.connector

#DATABASE CONNECTION
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin",
        database="doctor_db"
    )

#MAIN WINDOW
root = tk.Tk()
root.title("Doctor Database System")
root.geometry("700x500")
root.configure(bg="#1e3d59")


#DECOR
#FRAMES
home_frame = tk.Frame(root, bg="#1e3d59")
signup_frame = tk.Frame(root, bg="#f5f0e1")
login_frame = tk.Frame(root, bg="#f5f0e1")

for frame in (home_frame, signup_frame, login_frame):
    frame.place(relwidth=1, relheight=1)

#SCREEN SWITCH FUNCTION
def show_frame(frame):
    frame.tkraise()#what????
    #tkraise() is used to being a specific frame to the front in tkinter, so that multiple screens can be managed in a single window.
    #All screens are created as frames inside one window. The function tkraise() brings the required frame to the front, making it visible while hiding the others behind it.
'''SO ESSENTIALLY,
show_frame(home_frame)   # shows Home screen
show_frame(login_frame)  # switches to Login screen
show_frame(signup_frame) # switches to Sign Up screen'''

#HOME SCREEN : LOGIN/SIGNUP
tk.Label(home_frame, text="Doctor Database System",
         font=("Arial", 20, "bold"),
         bg="#1e3d59", fg="white").pack(pady=40)
                #tk.Label creates label, same with tk.Button
tk.Button(home_frame, text="Sign Up",
          width=20, bg="#ff6e40", fg="white",
          command=lambda: show_frame(signup_frame)).pack(pady=10)

tk.Button(home_frame, text="Login",
          width=20, bg="#4caf50", fg="white",
          command=lambda: show_frame(login_frame)).pack(pady=10)

#SIGNUP SCREEN
tk.Label(signup_frame, text="SIGN UP",
         font=("Arial", 16, "bold"),
         bg="#f5f0e1").pack(pady=10)

e_name = tk.Entry(signup_frame)
e_age = tk.Entry(signup_frame)
e_aadhar = tk.Entry(signup_frame)
e_locality = tk.Entry(signup_frame)
e_docid = tk.Entry(signup_frame)
e_password = tk.Entry(signup_frame, show="*")

for i, text in enumerate(["Name", "Age", "Aadhar", "Locality", "Doctor ID", "Password"]):
    tk.Label(signup_frame, text=text, bg="#f5f0e1").pack()
    [e_name, e_age, e_aadhar, e_locality, e_docid, e_password][i].pack()

def signup():
    name = e_name.get()
    age = e_age.get()
    aadhar = e_aadhar.get()
    locality = e_locality.get()
    docid = e_docid.get()
    password = e_password.get()

    if not all([name, age, aadhar, locality, docid, password]):
        messagebox.showerror("Error", "All fields required!")
        return

    try:
        conn = connect_db()
        cursor = conn.cursor()

        sql = """
        INSERT INTO doctors (name, age, aadhar_id, locality, tn_doctor_id, password)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
#MADE ERROR HERE, MUST ALWAYS USE GLOBAL VARIABLES, OR ITS BASICALLY USELESS!!!!
        cursor.execute(sql, (name, age, aadhar, locality, docid, password))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Registered Successfully!")

        # clear fields
        e_name.delete(0, tk.END)
        e_age.delete(0, tk.END)
        e_aadhar.delete(0, tk.END)
        e_locality.delete(0, tk.END)
        e_docid.delete(0, tk.END)
        e_password.delete(0, tk.END)

        # go back to home screen
        show_frame(home_frame)


    except mysql.connector.IntegrityError:
        # THIS TC OF DUPLICATE AADHAR
        messagebox.showerror("Error", "Aadhar ID already registered!")
    except Exception as e:
        messagebox.showerror("DB Error", str(e))

tk.Button(signup_frame, text="Submit",
          bg="#ff6e40", fg="white",
          command=signup).pack(pady=10)

tk.Button(signup_frame, text="Back",
          command=lambda: show_frame(home_frame)).pack()

# ---------------- LOGIN SCREEN ---------------- #
tk.Label(login_frame, text="LOGIN",
         font=("Arial", 16, "bold"),
         bg="#f5f0e1").pack(pady=10)

login_aadhar = tk.Entry(login_frame)
login_password = tk.Entry(login_frame, show="*")

tk.Label(login_frame, text="Aadhar", bg="#f5f0e1").pack()
login_aadhar.pack()

tk.Label(login_frame, text="Password", bg="#f5f0e1").pack()
login_password.pack()

def login():
    aadhar = login_aadhar.get()
    password = login_password.get()

    if not aadhar or not password:
        messagebox.showerror("Error", "All fields required!")
        return

    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT name FROM doctors WHERE aadhar_id=%s AND password=%s",
            (aadhar, password)
        )

        result = cursor.fetchone()
        conn.close()

        if result:
            messagebox.showinfo("Welcome", f"Welcome Dr. {result[0]}!")
        else:
            messagebox.showerror("Error", "Invalid credentials")

    except Exception as e:
        messagebox.showerror("DB Error", str(e))

tk.Button(login_frame, text="Login",
          bg="#4caf50", fg="white",
          command=login).pack(pady=10)

tk.Button(login_frame, text="Back",
          command=lambda: show_frame(home_frame)).pack()

# ---------------- START APP ---------------- #
show_frame(home_frame)
root.mainloop()


#SIGN UP:
#CODE FIXING:
#mistakes made------> not using aadhar, name, etc as a global variable, not using giu variables as global variables, cannot be used again nor called outside function, makes it pointless.
#make the aadhar unique, shld show error, so add table in sql (varchar12)
'''def signup():
    name = e_name.get()
    age = e_age.get()
    aadhar = e_aadhar.get()
    locality = e_locality.get()
    doctor_id = e_docid.get()
    password = e_password.get()

    if not all([name, age, aadhar, locality, doctor_id, password]):
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        import mysql.connector

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin",
            database="doctor_db"
        )

        cursor = conn.cursor()

        sql = """
        INSERT INTO doctors (name, age, aadhar_id, locality, tn_doctor_id, password)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (name, age, aadhar, locality, doctor_id, password)

        cursor.execute(sql, values)
        conn.commit()

        messagebox.showinfo("Success", "Registration Successful!")

        conn.close()

    except Exception as e:
        messagebox.showerror("Database Error", str(e))


#LOGIN CHECK:
def login():
    aadhar = login_aadhar.get()
    password = login_password.get()

    if not aadhar or not password:
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        import mysql.connector

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin",
            database="doctor_db"
        )

        cursor = conn.cursor()

        sql = "SELECT * FROM doctors WHERE aadhar_id=%s AND password=%s"
        values = (aadhar, password)

        cursor.execute(sql, values)
        result = cursor.fetchone()

        if result:
            messagebox.showinfo("Success", f"Welcome Doctor {result[1]}!")
        else:
            messagebox.showerror("Login Failed", "Invalid Aadhar or Password")

        conn.close()

    except Exception as e:
        messagebox.showerror("Database Error", str(e))

#MAIN CODE (god help me)
import tkinter as tk
from tkinter import messagebox
import json
import os

DB_FILE = "doctors.json"

#DATABASE FUNCTIONS

def load_data():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

#SIGNUP FUNCTION

def signup():
    name = e_name.get()
    age = e_age.get()
    aadhar = e_aadhar.get()
    locality = e_locality.get()
    doctor_id = e_docid.get()
    password = e_password.get()

    data = load_data()

    # Validations
    if not all([name, age, aadhar, locality, doctor_id, password]):
        messagebox.showerror("Error", "All fields are required!")
        return

    if aadhar in data:
        messagebox.showerror("Error", "Aadhar ID already registered!")
        return

    if len(password) < 5:
        messagebox.showerror("Error", "Password must be at least 5 characters!")
        return

    # Save user
    data[aadhar] = {
        "name": name,
        "age": age,
        "locality": locality,
        "doctor_id": doctor_id,
        "password": password
    }

    save_data(data)
    messagebox.showinfo("Success", "Registration Successful!")

    clear_signup()

def clear_signup():
    e_name.delete(0, tk.END)
    e_age.delete(0, tk.END)
    e_aadhar.delete(0, tk.END)
    e_locality.delete(0, tk.END)
    e_docid.delete(0, tk.END)
    e_password.delete(0, tk.END)

#LOGIN FUNCTION

def login():
    aadhar = login_aadhar.get()
    password = login_password.get()

    data = load_data()

    if aadhar not in data:
        messagebox.showerror("Login Failed", "Aadhar ID not found!")
        return

    if data[aadhar]["password"] != password:
        messagebox.showerror("Login Failed", "Incorrect Password!")
        return

    messagebox.showinfo("Welcome", f"Welcome Dr. {data[aadhar]['name']}!")

#UI SETUP

root = tk.Tk()
root.title("Doctor Database System")
root.geometry("750x500")
root.configure(bg="#1e3d59")  

#TITLE

title = tk.Label(root, text="Doctor Database System",
                 font=("Arial", 20, "bold"),
                 bg="#1e3d59", fg="white")
title.pack(pady=10)

#SIGNUP FRAME

frame_signup = tk.LabelFrame(root, text="Sign Up",
                              font=("Arial", 12, "bold"),
                              bg="#f5f0e1", padx=10, pady=10)
frame_signup.place(x=30, y=60, width=320, height=400)

#Labels & Entries
tk.Label(frame_signup, text="Name").grid(row=0, column=0, sticky="w")
e_name = tk.Entry(frame_signup)
e_name.grid(row=0, column=1)

tk.Label(frame_signup, text="Age").grid(row=1, column=0, sticky="w")
e_age = tk.Entry(frame_signup)
e_age.grid(row=1, column=1)

tk.Label(frame_signup, text="Aadhar ID").grid(row=2, column=0, sticky="w")
e_aadhar = tk.Entry(frame_signup)
e_aadhar.grid(row=2, column=1)

tk.Label(frame_signup, text="Locality").grid(row=3, column=0, sticky="w")
e_locality = tk.Entry(frame_signup)
e_locality.grid(row=3, column=1)

tk.Label(frame_signup, text="TN Doctor ID").grid(row=4, column=0, sticky="w")
e_docid = tk.Entry(frame_signup)
e_docid.grid(row=4, column=1)

tk.Label(frame_signup, text="Password").grid(row=5, column=0, sticky="w")
e_password = tk.Entry(frame_signup, show="*")
e_password.grid(row=5, column=1)

tk.Button(frame_signup, text="Sign Up",
          bg="#ff6e40", fg="white",
          command=signup).grid(row=6, column=1, pady=10)

#LOGIN FRAME

frame_login = tk.LabelFrame(root, text="Login",
                            font=("Arial", 12, "bold"),
                            bg="#f5f0e1", padx=10, pady=10)
frame_login.place(x=400, y=120, width=300, height=250)

tk.Label(frame_login, text="Aadhar ID").grid(row=0, column=0, sticky="w")
login_aadhar = tk.Entry(frame_login)
login_aadhar.grid(row=0, column=1)

tk.Label(frame_login, text="Password").grid(row=1, column=0, sticky="w")
login_password = tk.Entry(frame_login, show="*")
login_password.grid(row=1, column=1)

tk.Button(frame_login, text="Login",
          bg="#4caf50", fg="white",
          command=login).grid(row=2, column=1, pady=20)

root.mainloop()'''
