import datetime
import os
import queue
import socket
import threading


class ChatServer:
    def __init__(self, host='localhost', port=9999):
        # Initialize the server with the given host and port
        self.messages = queue.Queue()  # Queue to store received messages
        self.clients = set()  # Set to store connected clients
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create UDP socket
        self.server.bind((host, port))  # Bind socket to the host and port
        self.log_file = os.path.join(os.path.dirname(__file__), 'chat_log.txt')  # Path to the log file

    def start(self):
        # Start the server and the necessary threads
        self.log_startup()
        receive_thread = threading.Thread(target=self.receive)
        broadcast_thread = threading.Thread(target=self.broadcast)

        receive_thread.start()
        broadcast_thread.start()

    def receive(self):
        # Loop to receive messages from clients
        while True:
            try:
                message, addr = self.server.recvfrom(1024)  # Receive message from a client
                self.messages.put((message, addr))  # Put the message in the message queue
                self.log_message(message)  # Log the received message
            except Exception as e:
                print(f"Error receiving message: {str(e)}")
                break

    def broadcast(self):
        # Loop to broadcast messages to clients
        while True:
            while not self.messages.empty():
                message, addr = self.messages.get()  # Get a message from the message queue
                print(message.decode())  # Print the message
                if addr not in self.clients:
                    self.clients.add(addr)  # Add the client address to the connected clients set
                    self.send_join_message(addr)  # Send a join message to the client
                for client in self.clients:
                    try:
                        self.server.sendto(message, client)  # Send the message to all connected clients
                    except Exception as e:
                        print(f"Error sending message: {str(e)}")
                        self.clients.remove(client)
                        print(f'{client} removed')

    def send_join_message(self, addr):
        # Send a join message to a client
        name = self.extract_name(addr)
        join_message = f'{name} joined the chat room'.encode()
        self.server.sendto(join_message, addr)

    @staticmethod
    def extract_name(addr):
        # Extract the name from the client's address
        return addr[0] if addr else ''

    def log_message(self, message):
        # Write the message to the log file
        with open(self.log_file, 'a') as f:
            try:
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f'[{timestamp}] {message.decode()}\n')
            except Exception as e:
                print(f"Error writing to log file: {str(e)}")
            finally:
                f.close()

    def log_startup(self):
        # Print the server's address and log file path when it starts
        host, port = self.server.getsockname()
        print(f'Server started at {host}:{port}')
        print(f'Log file path: {self.log_file}')

    def stop(self):
        # Close the server socket
        self.server.close()


if __name__ == '__main__':
    server = ChatServer()
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
