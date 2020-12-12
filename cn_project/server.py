# importing the necessary packages
import socket
import random


def check_id(id):
    if id in user.keys():
        return True
    else:
        return False


user = {}                  # dictionary that stores responses of quiz

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # ccreating a server socket
server_socket.bind(('127.0.0.2', 6624))                             # binding socket to predefined port
server_socket.listen()                                              # listening for incoming connction

print('Server is running! (IP Address: %s, Port: %s)' % ('127.0.0.1', 5545))

while True:
    (client_socket, address) = server_socket.accept()   # accepting connections

    ip = address[0]                                     # IP addresses of client
    port = address[1]                                   # port of client

    print("Connected client is:(%s, %s)" % (ip, port))

    while True:
        option = client_socket.recv(1024).decode()             # receiving mac of client
        print("Chosen option: " + option)

        if int(option) == 1:                                    # login process
            id = client_socket.recv(1024).decode()
            print(id)

            SignedUp = check_id(id)
            client_socket.send(str(SignedUp).encode())
            print(SignedUp)

            if SignedUp:
                reset = client_socket.recv(1024).decode()
                print("Reset status: " + reset)

                if reset == 'True':
                    y = client_socket.recv(1024).decode()
                    y = int(y)
                    print("y: " + str(y))

                    b = random.choice([0, 1])
                    print("b: " + str(b))
                    client_socket.send(str(b).encode())

                    z = client_socket.recv(1024).decode()
                    z = int(z)
                    print("z: " + str(z))

                    record = user[id]
                    print(record)
                    v = int(record[0])
                    N = int(record[1])

                    print("v: " + str(v))
                    print("N: " + str(N))

                    access = False
                    if b == 0 and (z**2) % N == y % N:
                        access = True
                    elif b == 1 and (z**2) % N == (v * y) % N:
                        access = True

                    print('Acccess: ' + str(access))
                    client_socket.send(str(access).encode())

        elif int(option) == 2:                                  # sign up process
            id = client_socket.recv(1024).decode()
            print(id)

            SignedUp = check_id(id)
            client_socket.send(str(SignedUp).encode())
            print(SignedUp)

            if not SignedUp:
                id, v, N = client_socket.recv(1024).decode().split(" ")
                user[id] = [int(v), int(N)]
                print(user)
        elif int(option) == 3:
            break
    print("Closing client is:(%s, %s)" % (ip, port))
    client_socket.close()                               # close the client connection
