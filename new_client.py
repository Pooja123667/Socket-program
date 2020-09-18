import socket
import threading

nickname = input("Choose a nickname: ") #to get the nickname

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555)) #connect to server

def receive():
    while True:
        try:
            message = client.recv(1024).decode("ascii") #receive message from the server
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message) #prints the message given by the server
        except:
            print("An error occurred!")
            client.close() #close the connection
            break

def write():  # function for user to send the messages
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))

#create two threads to run the two functions simultaneously
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
