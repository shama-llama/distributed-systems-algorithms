import socket

def server_program():
    host = '127.0.0.1'
    port = 65432

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server started at {host}:{port}")

    while True:
        conn, address = server_socket.accept()
        print(f"Connection from {address}")
        
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                print("Client disconnected.")
                break
            print(f"Received from client: {data}")
            
            response = f"Server received: {data}"
            conn.send(response.encode('utf-8'))
        
        conn.close()

if __name__ == "__main__":
    server_program()
