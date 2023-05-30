import os
import random
import socket
import threading


class ChatClient:
    def __init__(self, server_host='localhost', server_port=9999):
        # Create a UDP socket for the client
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind the client socket to a random port
        self.client.bind(('localhost', random.randint(8000, 9000)))
        # Get the user's nickname or set a default nickname
        self.name = input('Nickname: ') if os.isatty(0) else 'Anonymous'

    def start(self):
        # Start a thread to receive messages from the server
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        # Send a signup message to the server with the user's nickname
        self.client.sendto(f'SIGNUP_TAG:{self.name}'.encode(), ('localhost', 9999))

        # Main loop to send messages to the server
        while True:
            message = input('')
            if message == '!q':
                exit()
            else:
                self.client.sendto(f'{self.name}: {message}'.encode(), ('localhost', 9999))

    def receive(self):
        # Loop to receive messages from the server
        while True:
            try:
                message, _ = self.client.recvfrom(1024)
                # Print the received message
                print(message.decode())
            except Exception as e:
                print(f"Error receiving message: {str(e)}")
                break


if __name__ == '__main__':
    client = ChatClient()
    try:
        client.start()
    except KeyboardInterrupt:
        pass
