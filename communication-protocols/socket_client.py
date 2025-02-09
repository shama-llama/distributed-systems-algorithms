import socket

HOST = "127.0.0.1"
PORT = 65432


def client_program():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    print("Connected to the server. Type 'exit' to disconnect.")
    while True:
        message = input("Enter message to send: ")
        if message.lower() == "exit":
            print("Disconnecting from the server.")
            break
        client_socket.send(message.encode("utf-8"))

        data = client_socket.recv(1024).decode("utf-8")
        print(f"Received from server: {data}")

    client_socket.close()


if __name__ == "__main__":
    client_program()
