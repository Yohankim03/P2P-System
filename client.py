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
                # Assuming the message format is "username: message"
                message_content = data.decode('utf-8')
                print(f"Received message from {message_content}")

    def send_message(self, target_ip, target_port, message):
        # Include the username in the message
        full_message = f"{self.username}: {message}"
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((target_ip, int(target_port)))
            s.send(full_message.encode('utf-8'))
            
            
    def lookup_user(self, username):
        """
        Request the IP and port for a given username from the discovery server.
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(self.server_address)
                request_message = f'LOOKUP {username}'
                s.send(request_message.encode('utf-8'))
                response = s.recv(1024).decode('utf-8')
                if response != 'User not found':
                    target_ip, target_port = eval(response)  # Safe here because we trust the server
                    print(f"User {username} is at {target_ip}:{target_port}")
                    return target_ip, target_port
                else:
                    print(f"User {username} not found.")
                    return None, None
        except Exception as e:
            print(f"Failed to lookup user {username}: {e}")
            return None, None


    def run_cli(self):
        username = input("Enter your username: ").strip()
        self.register_with_server(username)
        threading.Thread(target=self.handle_incoming_connections, daemon=True).start()
        
        while True:
            command = input("Enter command (lookup <username>, send <username> <message>, exit): ").strip()
            if command.startswith("lookup"):
                _, lookup_username = command.split()
                self.lookup_user(lookup_username)
            elif command.startswith("send"):
                _, target_username, *message = command.split()
                message = " ".join(message)
                target_ip, target_port = self.lookup_user(target_username)
                if target_ip:
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

