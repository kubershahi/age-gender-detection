# importing the necessary packages
import socket
import random
import py7zr
import os
import sys

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

    N = p*q                                 # computing N
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


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # creating a socket of ipv4 supporting TCP

client_socket.connect(('127.0.0.1', 6624))                          # connecting to the server
incoming1 = client_socket.recv(1024).decode()                       # getting confirmation of connection
print(incoming1)

option = input("\nEnter your opiton: ")                             # taking the option number as input

while option not in {"1","2","3"}:
        print("Invalid option selected")
        option = input("\nEnter your opiton: ")  

client_socket.send(option.encode())                                 # sending the option number to the server

if int(option) == 1:                                                # if option is 1 login process begins
    id = input("Enter your id: ")                                   # getting id from user
    client_socket.send(id.encode())                                 # sending user id to the server
    SignedUp = client_socket.recv(1024).decode()                    # getting login record status, if the login record exists or not

    if SignedUp == "True":                                          # if the login record exists
        password = input("Enter your password: ")                   # getting password from user
        zipfile = id + '.zip'
        textfile = id + ".txt"

        correct = False                             # variable that shows whether the password is right or not  
        i = 0
        try:                                                
            with py7zr.SevenZipFile(zipfile, 'r', password=password) as archive:
                archive.extractall()                # extract the secret password(w) if password matches
            correct = True                          # changes status to true             
        except:
            i +=1
            # os.remove(textfile)
            print('Invalid password.\n')

        while not correct:                          # give three tries to user to input correct password
            if i == 3:
                client_socket.close()
                sys.exit("Too many incorrect attempts. Try again later.\n")
            password = input("Enter your password: ")
            try:
                with py7zr.SevenZipFile(zipfile, 'r', password=password) as archive:
                    archive.extractall()
                correct = True
            except:
                i +=1
                print('Invalid password.\n')

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
        elif access == 'False':
            print("Access denied.\n")               # else access denied
    elif SignedUp == "False": 
        print("User id not found.\n")

elif int(option)==2:                                        # if option is 2, begin signup process
    id = input("Enter your id eg. john : ")                 # getting user id     
    client_socket.send(id.encode())

    SignedUp = client_socket.recv(1024).decode()            # checking if the user record already exists or not
    print(SignedUp)

    if SignedUp == 'True':                                  # if login record exists, output already signed up
        print("You have already signed up.\n")
    elif SignedUp == 'False':                               # else go forward with sign up process
        password = input("Enter your password: ")           # getting user password

        w, v, N = signup()                                  # getting login record for the user
        user_record = id + " " + str(v) + " " + str(N)      # sending v and N to the server
        client_socket.send(user_record.encode())

        textfile = id + ".txt"
        file = open(textfile, "w+")
        file.write(str(w) + " " + str(N))                   # saving secret password(w) and N in local device
        file.close()

        zipfile = id + ".zip"
        with py7zr.SevenZipFile(zipfile, 'w', password=password) as archive:    # creating password protect zip that contains textfile with w and N
            archive.write(textfile)
        os.remove(textfile)                                 # removing the textfile

        print("You have signed up with id: " + id)          # ending the signup process
else:
    print("You have exited. Thank you for visiting.\n")

client_socket.close()                                               # close the client socket