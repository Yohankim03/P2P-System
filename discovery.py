import socket
import threading

class DiscoveryServer:
    def __init__(self, host, port):
        self.active_clients = {}  # Stores client info
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen()

              
    def handle_client(self, client_socket, client_address):
        try:
            while True:
                message = client_socket.recv(1024).decode('utf-8')
                if message.startswith('REGISTER'):
                    _, username, listen_port = message.split()  # Split the message to extract username and listen_port
                    self.active_clients[username] = (client_address[0], int(listen_port))  # Store client's IP and specified listening port
                    print(f"{username} registered with address {self.active_clients[username]}.")                   
                elif message.startswith('LOOKUP'):
                    username_lookup = message.split(' ')[1]
                    client_info = self.active_clients.get(username_lookup)
                    if client_info:
                        client_socket.send(str(client_info).encode('utf-8'))
                    else:
                        client_socket.send('User not found'.encode('utf-8'))
                elif message == 'UNREGISTER':
                    if username and username in self.active_clients:
                        del self.active_clients[username]
                    client_socket.close()
                    break
        except ConnectionResetError:
            if username and username in self.active_clients:
                del self.active_clients[username]
            print(f"Connection lost with {username}.")
        finally:
            if username and username in self.active_clients:
                del self.active_clients[username]

    def start_server(self):
        print('Starting Discovery Server...')
        while True:
            client_socket, client_address = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_thread.start()

if __name__ == '__main__':
    server = DiscoveryServer('127.0.0.1', 5000)
    server.start_server()


