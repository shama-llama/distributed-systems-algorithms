import socket

def server_program():
    host = '127.0.0.1'  # localhost
    port = 65432        # Port to listen on

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))  # Bind to the address and port
    server_socket.listen(5)          # Listen for up to 5 connections
    print(f"Server started at {host}:{port}")

    while True:
        conn, address = server_socket.accept()  # Accept a new connection
        print(f"Connection from {address}")
        
        while True:
            data = conn.recv(1024).decode('utf-8')  # Receive data from client
            if not data:
                print("Client disconnected.")
                break
            print(f"Received from client: {data}")
            
            response = f"Server received: {data}"
            conn.send(response.encode('utf-8'))  # Send response back to client
        
        conn.close()  # Close the connection

if __name__ == "__main__":
    server_program()
