import tkinter
from tkinter import PhotoImage
from tkinter import messagebox

root=tkinter.Tk()
root.title("doctor_agency")
root.geometry("1000x600")



image_path=PhotoImage(file=r"C:\Users\ramya\Downloads\Teal Gradient Digital Marketing Zoom Virtual Background.png")
bg_image=tkinter.Label(root,image=image_path)
bg_image.place(x=0,y=0,relheight=1,relwidth=1)



frame=tkinter.Frame(bg="#000b15")

def login():
    username="shivani"
    password="123456"
    if username_entry.get()==username and password_entry.get()==password:
        messagebox.showinfo(title="login success",message="You successfully logged in")
    else:
        messagebox.showerror(title="Error",message="Invalid login")

 #creating widgets
login_label=tkinter.Label(frame,text="Login",bg='#000b15',fg='#FF3399',font=("Georgia",26))
username_label=tkinter.Label(frame,text="Username",bg='#000b15',fg='#FFFFFF',font=("Arial",16))
username_entry=tkinter.Entry(frame,font=("Arial",16))
password_label=tkinter.Label(frame,text="Password",bg='#000b15',fg='#FFFFFF',font=("Arial",16))
password_entry=tkinter.Entry(frame,show="*",font=("Arial",16))
login_button=tkinter.Button(frame,text="Login",bg='#000b15',fg="#FFFFFF",font=("Arial",20),command=login)

#placing the widgets
login_label.grid(row=0,column=0,columnspan=2,sticky="news",pady=40)
username_label.grid(row=1,column=0)
username_entry.grid(row=1,column=1,pady=20)
password_label.grid(row=2,column=0)
password_entry.grid(row=2,column=1,pady=20)
login_button.grid(row=3,column=0,columnspan=2,pady=30)

#frame placement
frame.place(relx=0.05, rely=0.5, anchor="w") 


root.mainloop()
