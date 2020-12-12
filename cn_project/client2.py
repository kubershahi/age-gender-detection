# importing the necessary packages
import socket
import random
import py7zr
import os
import sys
import tkinter as tk

from Crypto.Util import number

# signup function that lets a user signup
def signup():
    def get_primes():                       # function that gets two primes
        p = number.getPrime(50)             # geting a prime p
        q = number.getPrime(50)             # geting a prime q
        while p == q:                       # if both prime are equal get another q
            q = number.getPrime(50)
        return p, q

    p, q = get_primes()                     # getting two primes p and q
    print("p: " + str(p))
    print("q: " + str(q))

    N = p * q                                 # computing N
    print("N: " + str(N))

    w = int(random.uniform(1, 2**20))       # computing w
    print("w: " + str(w))

    v = (w**2) % N                          # computing v
    print("v: " + str(v))
    return w, v, N

# function that lets a user login
def login(w, N):

    x = int(random.uniform(1, 2**20))       # getting a random x uniformly
    while number.GCD(x, N) != 1:
        x = int(random.uniform(1, 2**20))   # if gcd(x,N) is not 1, get anothe x

    y = (x**2) % N                          # computing y

    print("x: " + str(x))
    print("y: " + str(y))

    client_socket.send(str(y).encode())     # sending y

    b = client_socket.recv(1024).decode()   # receiving b
    print("b: " + b)

    z = 0

    if int(b) == 0:                         # computing z
        z = x
    elif int(b) == 1:
        z = w * x

    print("z: " + str(z))
    client_socket.send(str(z).encode())     # sending z

    access = client_socket.recv(1024).decode()  # getting access status
    return access


def login_user(start,log_in,frame, entry_user, entry_password):
    id = entry_user                                      # getting id from user
    client_socket.send(id.encode())                                 # sending user id to the server
    SignedUp = client_socket.recv(1024).decode()                    # getting login record status, if the login record exists or not

    if SignedUp == "True":                                          # if the login record exists
        password = entry_password               # getting password from user
        zipfile = id + '.zip'
        textfile = id + ".txt"

        correct = True
        try:
            with py7zr.SevenZipFile(zipfile, 'r', password=entry_password) as archive:
                archive.extractall()                # extract the secret password(w) if password matches
        except:
            os.remove(textfile)
            correct=False
            client_socket.send(str(correct).encode())
            print('Invalid password.\n')
            frame=tk.Frame(log_in, bg="#c2d8e5")
            frame.place(relx=0, rely=0, relheight=1, relwidth=1)
            log_in.after(1700, log_in.destroy)
            submit_label = tk.Label(frame, bg="red", font=20, text="Invalid Password.\n")
            submit_label.place(relx=0.5, rely=0.35, anchor='n')
            submit_label = tk.Label(frame, font=20, text="This window will close now.\n")
            submit_label.place(relx=0.5, rely=0.65, anchor='n')
            log_in.wait_window()
            return start.deiconify()


        client_socket.send(str(correct).encode())
        file = open(textfile, "r")                  # open the file that contains the secret password(w)
        line = file.read()
        file.close()
        os.remove(textfile)

        w, N = line.split()                         # getting w and N from the file
        print("w: " + w)
        print("N: " + N)

        access = login(int(w), int(N))              # trying to login with the w and N
        print("Access: " + access)

        if access == 'True':                        # if the login record (w, N) matches access granted
            print("You have logged in.\n")
            frame=tk.Frame(log_in, bg="#c2d8e5")
            frame.place(relx=0, rely=0, relheight=1, relwidth=1)
            log_in.after(1700, log_in.destroy)
            submit_label = tk.Label(frame,bg="green", font=20, text="You have logged in.\n")
            submit_label.place(relx=0.5, rely=0.35, anchor='n')
            submit_label = tk.Label(frame, font=20, text="This window will close now.\n")
            submit_label.place(relx=0.5, rely=0.65, anchor='n')
        elif access == 'False':
            print("Access denied.\n")               # else access denied
            frame=tk.Frame(log_in, bg="#c2d8e5")
            frame.place(relx=0, rely=0, relheight=1, relwidth=1)
            log_in.after(1700, log_in.destroy)
            submit_label = tk.Label(frame, bg="red", font=20, text="Access Denied.\n")
            submit_label.place(relx=0.5, rely=0.35, anchor='n')
            submit_label = tk.Label(frame, font=20, text="This window will close now.\n")
            submit_label.place(relx=0.5, rely=0.65, anchor='n')

    elif SignedUp == "False":
        print("User id not found.\n")
        frame=tk.Frame(log_in, bg="#c2d8e5")
        frame.place(relx=0, rely=0, relheight=1, relwidth=1)
        log_in.after(1700, log_in.destroy)
        submit_label = tk.Label(frame,bg="red", font=20, text="User ID not found.\n")
        submit_label.place(relx=0.5, rely=0.35, anchor='n')
        submit_label = tk.Label(frame, font=20, text="This window will close now.\n")
        submit_label.place(relx=0.5, rely=0.65, anchor='n')

    log_in.wait_window()
    return start.deiconify()


def signup_user(start,sign_up,frame, entry_user, entry_password):
    id = str(entry_user)                # getting user id
    client_socket.send(id.encode())

    SignedUp = client_socket.recv(1024).decode()            # checking if the user record already exists or not
    print(SignedUp)

    if SignedUp == 'True':                                  # if login record exists, output already signed up
        print("You have already signed up.\n")
        frame=tk.Frame(sign_up, bg="#c2d8e5")
        frame.place(relx=0, rely=0, relheight=1, relwidth=1)
        sign_up.after(2000, sign_up.destroy)
        submit_label = tk.Label(frame,bg="red", font=20, text="You have already signed up.\n")
        submit_label.place(relx=0.5, rely=0.35, anchor='n')
        submit_label = tk.Label(frame,font=20, text="This window will now close.\n")
        submit_label.place(relx=0.5, rely=0.65, anchor='n')

    elif SignedUp == 'False':                               # else go forward with sign up process

        password = str(entry_password)
        w, v, N = signup()                               # getting login record for the user
        user_record = id + " " + str(v) + " " + str(N)
        print(user_record)      # sending v and N to the server
        client_socket.send(user_record.encode())

        textfile=id + ".txt"
        file=open(textfile, "w+")
        file.write(str(w) + " " + str(N))                   # saving secret password(w) and N in local device
        file.close()

        zipfile=id + ".zip"
        with py7zr.SevenZipFile(zipfile, 'w', password=entry_password) as archive:    # creating password protect zip that contains textfile with w and N
            archive.write(textfile)
        os.remove(textfile)                                 # removing the textfile

        frame=tk.Frame(sign_up, bg="#c2d8e5")
        frame.place(relx=0, rely=0, relheight=1, relwidth=1)
        sign_up.after(2000, sign_up.destroy)
        submit_label = tk.Label(frame, bg="green", font=20, text="You have signed up with: " + id )
        submit_label.place(relx=0.5, rely=0.35, anchor='n')
        submit_label = tk.Label(frame, font=20, text="This window will close now.\n")
        submit_label.place(relx=0.5, rely=0.65, anchor='n')

    sign_up.wait_window()
    return start.deiconify()

def tk_login():
    option=1
    print(option)
    client_socket.send(str(option).encode())

    log_in=tk.Toplevel()
    start.withdraw()
    backgroung=tk.Canvas(log_in, height=300, width=400)
    backgroung.pack()

    frame=tk.Frame(log_in, bg="#c2d8e5")
    frame.place(relx=0, rely=0, relheight=1, relwidth=1)

    log_in_lable=tk.Label(frame, font=25, text="Login")
    log_in_lable.place(relx=0.5, rely=0.10, anchor='n')

    user_name=tk.Label(frame, text="User ID*:")
    user_name.place(relx=0.35, rely=0.30, anchor='n')

    entry_user=tk.Entry(frame)
    entry_user.place(relx=0.65, rely=0.30, anchor='n')

    password=tk.Label(frame, text="Password*:")
    password.place(relx=0.35, rely=0.40, anchor='n')

    entry_password=tk.Entry(frame, show="*")
    entry_password.place(relx=0.65, rely=0.40, anchor='n')

    button=tk.Button(frame, text="Login", bg="grey", command=lambda: login_user(start,log_in,frame, entry_user.get(), entry_password.get()))
    button.place(relx=0.5, rely=0.55, anchor='n')

    log_in.mainloop()


def tk_signup(start):
    option=2
    print(option)
    client_socket.send(str(option).encode())

    sign_up=tk.Toplevel()
    start.withdraw()
    backgroung=tk.Canvas(sign_up, height=300, width=400)
    backgroung.pack()

    frame=tk.Frame(sign_up, bg="#c2d8e5")
    frame.place(relx=0, rely=0, relheight=1, relwidth=1)

    sign_up_label=tk.Label(frame, font=20, text="Sign Up")
    sign_up_label.place(relx=0.5, rely=0.10, anchor='n')

    user_name=tk.Label(frame, text="User ID*:")
    user_name.place(relx=0.35, rely=0.30, anchor='n')

    entry_user=tk.Entry(frame)
    entry_user.place(relx=0.65, rely=0.30, anchor='n')

    password=tk.Label(frame, text="Password*:")
    password.place(relx=0.35, rely=0.40, anchor='n')

    entry_password=tk.Entry(frame, show="*")
    entry_password.place(relx=0.65, rely=0.40, anchor='n')

    button=tk.Button(frame, text="Sign Up", bg="grey", command=lambda: signup_user(start,sign_up,frame, entry_user.get(), entry_password.get()))
    button.place(relx=0.5, rely=0.55, anchor='n')

    sign_up.mainloop()



# creating a socket of ipv4 supporting TCP
                         # connecting to the server

client_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.2', 6624))

start=tk.Tk()
start.title("User: B")

backgroung=tk.Canvas(start, height=300, width=400)
backgroung.pack()

frame=tk.Frame(start,bg="#c2d8e5")
frame.place(relx=0, rely=0, relheight=1, relwidth=1)

welcome=tk.Label(frame, font=30, text="Welcome To Santos Server !")
welcome.place(relx=0.5, rely=0.20, anchor='n')

login_button=tk.Button(frame, font=25, text="Login", bg="grey", command=lambda: tk_login())
login_button.place(relx=0.4, rely=0.40, anchor='n')

signup_button=tk.Button(frame, font=25, text="Sign up", bg="grey", command=lambda: tk_signup(start))
signup_button.place(relx=0.6, rely=0.40, anchor='n')

start.mainloop()                   # getting confirmation of connection

option = 3
client_socket.send(str(option).encode())

client_socket.close()
