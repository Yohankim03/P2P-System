# import socket
# import threading
# import time

# class Client:
#     def __init__(self, discovery_server_ip, discovery_server_port, my_ip, my_port):
#         self.server_address = (discovery_server_ip, discovery_server_port)
#         self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.my_address = (my_ip, my_port)
#         self.client_socket.bind(self.my_address)
#         self.client_socket.listen()
#         self.keep_running = True

#     def register_with_server(self):
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#             s.connect(self.server_address)
#             s.send('REGISTER'.encode('utf-8'))

#     def send_keep_alive(self):
#         while self.keep_running:
#             try:
#                 with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#                     s.connect(self.server_address)
#                     s.send('KEEPALIVE'.encode('utf-8'))
#                 time.sleep(60)  # send a keep-alive packet every 60 seconds
#             except ConnectionError:
#                 # Handle the connection error (e.g., retry connection or exit)
#                 pass

#     def look_up_user(self, username):
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#             s.connect(self.server_address)
#             s.send(f'LOOKUP {username}'.encode('utf-8'))
#             response = s.recv(1024).decode('utf-8')
#             return response

#     def handle_incoming_connections(self):
#         while self.keep_running:
#             conn, addr = self.client_socket.accept()
#             threading.Thread(target=self.handle_client, args=(conn, addr)).start()

#     def handle_client(self, conn, addr):
#         with conn:
#             while True:
#                 data = conn.recv(1024)
#                 if not data:
#                     break
#                 # Here, you would handle the incoming data/message.
#                 print(f"Received message from {addr}: {data.decode('utf-8')}")

#     def send_message(self, target_ip, target_port, message):
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#             s.connect((target_ip, target_port))
#             s.send(message.encode('utf-8'))


#     def start(self):
#         self.register_with_server()
#         threading.Thread(target=self.send_keep_alive).start()
#         threading.Thread(target=self.handle_incoming_connections).start()

# # Inside your Client class
# if __name__ == '__main__':
#     # Prompt user to enter a unique port for this client instance
#     my_port = int(input("Enter a unique port number for this client: "))
#     client = Client('127.0.0.1', 5000, '127.0.0.1', my_port)
#     client.start()
    
#     # Test sending a message to another client (you'll need to know the port number)
#     target_port = int(input("Enter the target client's port to send a message: "))
#     client.send_message('127.0.0.1', target_port, 'Hello from client on port ' + str(my_port))

import socket
import threading
import time

class Client:
    def __init__(self, discovery_server_ip, discovery_server_port, my_ip, my_port):
        self.server_address = (discovery_server_ip, discovery_server_port)
        self.my_address = (my_ip, my_port)
        self.client_socket = None
        self.keep_running = True
        self.username = None

    def register_with_server(self, username):
        message = f'REGISTER {username} {self.my_address[1]}'  # Include the listening port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(self.server_address)
            s.send(message.encode('utf-8'))
        self.username = username
        print(f"Registered as {username} with server for listening on port {self.my_address[1]}.")

    def handle_incoming_connections(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.bind(self.my_address)
        self.client_socket.listen()
        print(f"Listening for incoming connections on {self.my_address}")
        
        while self.keep_running:
            conn, addr = self.client_socket.accept()
            threading.Thread(target=self.handle_client, args=(conn, addr)).start()

    def handle_client(self, conn, addr):
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(f"Received message from {addr}: {data.decode('utf-8')}")

    def send_message(self, target_ip, target_port, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((target_ip, int(target_port)))
            s.send(message.encode('utf-8'))

    def run_cli(self):
        username = input("Enter your username: ").strip()
        self.register_with_server(username)
        threading.Thread(target=self.handle_incoming_connections, daemon=True).start()
        
        while True:
            command = input("Enter command (send <ip> <port> <message>, exit): ").strip()
            if command.startswith("send"):
                _, target_ip, target_port, *message = command.split()
                message = " ".join(message)
                self.send_message(target_ip, target_port, message)
            elif command == "exit":
                print("Shutting down client.")
                self.keep_running = False
                self.client_socket.close()
                break

if __name__ == '__main__':
    my_port = int(input("Enter your client's listening port: "))
    client = Client('127.0.0.1', 5000, '127.0.0.1', my_port)
    client.run_cli()
