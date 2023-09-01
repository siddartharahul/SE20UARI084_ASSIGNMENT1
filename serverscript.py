import socket
import threading


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 12345)  # Change the address and port if needed

server_socket.bind(server_address)
server_socket.listen(5)
print("Server is listening on", server_address)

clients = []

def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message)
            except:
                
                clients.remove(client)

# Function to handle client connections
def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            broadcast(message, client_socket)
        except:
        
            clients.remove(client_socket)
            client_socket.close()
            break


while True:
    client_socket, client_address = server_socket.accept()
    clients.append(client_socket)
    print(f"Connection from {client_address} established.")
    
    # Start a thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
