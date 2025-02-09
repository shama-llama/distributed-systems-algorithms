import socket
import datetime

HOST = "127.0.0.1"
PORT = 8080


def initiateClockServer():
    server_socket = socket.socket()
    print("Socket successfully created")
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print("Socket is listening...")

    while True:
        connection, address = server_socket.accept()
        print("Server connected to", address)
        connection.send(str(datetime.datetime.now()).encode())

        connection.close()


if __name__ == "__main__":
    initiateClockServer()
