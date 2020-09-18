import threading
import socket

host = '127.0.0.1' #localhost
port = 55555

#SOCK_STREAM for TCP connection
#AF_INET is about IPv4 address family
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = [] #to store the connected clients
nicknames = [] #to store there nicknames

def broadcast(message):  #to broadcast the message to other clients
    for client in clients: #for every client
        client.send(message) #send the message

def handle(client): #to handle a client
    while True:
        try:
            message = client.recv(1024) #store received msg in a variable
            broadcast(message) #then broadcast the message to other clients
        except:
            index = clients.index(client) #find and store the index of the client
            clients.remove(client) # remove the client from the list
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('ascii')) #notify other clients about the client leaving
            nicknames.remove(nickname)
            break

def receive():  #to accept multiple clients
    while True:
        client, address = server.accept() #to get the client and its address
        print(f'Connected with {str(address)}')

        client.send('NICK'.encode('ascii')) # to ask user to send nickname
        nickname = client.recv(1024).decode('ascii') #to receive nickname from client
        nicknames.append(nickname) #add the nickname of the client to the list
        clients.append(client) #add the client to clients list

        print(f'Nickname of the client is {nickname}!')
        broadcast(f'{nickname} joined the chat'.encode('ascii')) #Notify other clients about other client joining the chat

        #create thread to handle multiple clients
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is listening")
receive()
        
