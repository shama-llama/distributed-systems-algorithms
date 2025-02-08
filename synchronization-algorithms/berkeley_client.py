from dateutil import parser
import threading
import datetime
import socket
import time

HOST = '127.0.0.1'
PORT = 65423

def send_time(client_socket):
    while True:
        client_socket.send(str(datetime.datetime.now()).encode())
        print("Recent time sent successfully", end="\n\n")
        time.sleep(5)

def startReceivingTime(client_socket):
    while True:
        Synchronized_time = parser.parse(client_socket.recv(1024).decode())
        print("Synchronized time at the client is: " +
              str(Synchronized_time),
              end="\n\n")

def initiate_client():
    client_socket = socket.socket()

    client_socket.connect((HOST, PORT))

    print("Starting to receive time from server\n")
    send_time_thread = threading.Thread(
        target=send_time,
        args=(client_socket, ))
    send_time_thread.start()

    print("Starting to receiving " +
          "synchronized time from server\n")
    receive_time_thread = threading.Thread(
        target=startReceivingTime,
        args=(client_socket, ))
    receive_time_thread.start()

if __name__ == '__main__':
    initiate_client()
