import socket

def client_program():
    host = '127.0.0.1'  # Server's hostname or IP address
    port = 65432        # Port used by the server

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))  # Connect to the server

    print("Connected to the server. Type 'exit' to disconnect.")
    while True:
        message = input("Enter message to send: ")  # Input from user
        if message.lower() == 'exit':
            print("Disconnecting from the server.")
            break
        client_socket.send(message.encode('utf-8'))  # Send message to server

        data = client_socket.recv(1024).decode('utf-8')  # Receive response
        print(f"Received from server: {data}")

    client_socket.close()  # Close the connection

if __name__ == "__main__":
    client_program()
