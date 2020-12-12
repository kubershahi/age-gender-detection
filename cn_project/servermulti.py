# server that can host multiple client processses

# importing th necessary packages
import socket
import random
import threading
from threading import Thread

# function that checks whether a user has a login record or not in that user dictionary


def check_id(id):
    if id in user.keys():                               # iterate over keys to find key that is equal to user id
        return True                                     # if id key exists, th record exists, return true
    else:                                               # else return false
        return False

# client class: a thread
class clientThread(Thread):

    def __init__(self, client_socket, address):         # init definition
        Thread.__init__(self)
        self.client_socket = client_socket              # class properties are client socket, ip and address
        self.ip = address[0]
        self.port = address[1]

    def run(self):

        print("Connected client is:(%s, %s)" % (self.ip, self.port))

        while True:
            option = self.client_socket.recv(1024).decode()             # receiving mac of client
            print("Chosen option: " + option)

            if int(option) == 1:                                    # if option is 1, login process starts
                id = self.client_socket.recv(1024).decode()         # getting user id
                print(id)

                SignedUp = check_id(id)
                self.client_socket.send(str(SignedUp).encode())     # sending true if there is a record, else false
                print(SignedUp)

                if SignedUp:
                    reset = self.client_socket.recv(1024).decode()
                    print("Reset status: " + reset)                                       # if there is a record

                    if reset == 'True':
                        y = self.client_socket.recv(1024).decode()      # receive y
                        y = int(y)
                        print("y: " + str(y))

                        b = random.choice([0, 1])                        # choose b
                        print("b: " + str(b))
                        self.client_socket.send(str(b).encode())        # send b

                        z = self.client_socket.recv(1024).decode()      # receive z
                        z = int(z)
                        print("z: " + str(z))

                        record = user[id]                               # getting login record of the user
                        print(record)
                        v = int(record[0])
                        N = int(record[1])

                        print("v: " + str(v))
                        print("N: " + str(N))

                        access = False                                  # default access set to denied
                        if b == 0 and (z**2) % N == y % N:              # if the computation matches, give access
                            access = True
                        elif b == 1 and (z**2) % N == (v * y) % N:
                            access = True

                        print('Acccess: ' + str(access))
                        self.client_socket.send(str(access).encode())   # sending access status

            elif int(option) == 2:                                  # if option is 2, sign-up process starts
                id = self.client_socket.recv(1024).decode()
                print(id)

                user_lock.acquire()                                 # lock the sign up process to eliminate duplicate records
                SignedUp = check_id(id)                             # checking if user has a login record or not#

                self.client_socket.send(str(SignedUp).encode())     # sending true if record exists else false
                print(SignedUp)

                if not SignedUp:                                    # if there is no record
                    id, v, N = client_socket.recv(1024).decode().split()  # get user record, id, v , N

                    user[id] = [int(v), int(N)]                    # append the user record into dictionary
                    print(user)
                user_lock.release()                                 # release the lock

            elif int(option) == 3:
                break
        print("Closing client is:(%s, %s)" % (self.ip, self.port))
        self.client_socket.close()                              # close the client connection


user = {}                                                       # dictionary that stores responses of quiz
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # creating a server socket
server_socket.bind(('127.0.0.2', 6624))                             # binding socket to predefined port

user_lock = threading.Lock()                                        # creating a lock

server_socket.listen(4)                                              # listening for incoming connection

print('Server is running! (IP Address: %s, Port: %s)' % ('127.0.0.2', 6624))

while True:
    (client_socket, address) = server_socket.accept()   # accepting connections with ip and port

    newThread = clientThread(client_socket, address)    # creating a thread per connection
    newThread.start()                                   # starting the thread
