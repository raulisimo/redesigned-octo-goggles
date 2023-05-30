# Chat Application

This is a simple chat application consisting of a client and server component. The client allows users to connect to the server and exchange messages in a chat room.

## Prerequisites

Make sure you have the following dependencies installed on your machine:

- Docker
- docker compose

## Getting Started

1. Clone this repository to your local machine:

  ```
   git clone <repository-url>
  ```

2. Build the Docker images for the client and server:

```
docker compose build
```

3. Start the chat application by running the following command:

```
docker compose up
```

This command will start the client and server containers. You will see the output from both the client and server in the terminal.

4. When prompted, enter a nickname for the client.

5. The client will connect to the server, and you can start sending and receiving messages in the chat room.

6. To exit the chat application, type !q in the client's input prompt.