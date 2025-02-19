from dateutil import parser
import threading
import datetime
import socket
import time

HOST = '127.0.0.1'
PORT = 65423

client_data = {}

def receive_clock(connector, address):
    while True:
        clock_time_string = connector.recv(1024).decode()
        clock_time = parser.parse(clock_time_string)
        clock_time_diff = datetime.datetime.now() - clock_time

        client_data[address] = {
            "clock_time": clock_time,
            "time_difference": clock_time_diff,
            "connector": connector
        }

        print("Client Data updated with: " + str(address), end="\n\n")
        time.sleep(5)

def start_connection(master_server):
    while True:
        master_slave_connector, addr = master_server.accept()
        slave_address = str(addr[0]) + ":" + str(addr[1])

        print(slave_address + " got connected successfully")

        current_thread = threading.Thread(
            target=receive_clock,
            args=(master_slave_connector,
                  slave_address, ))
        current_thread.start()

def get_average_diff():
    current_client_data = client_data.copy()
    time_difference_list = list(client['time_difference']
                                for client_addr, client
                                in client_data.items())
    sum_of_clock_difference = sum(time_difference_list, datetime.timedelta(0, 0))
    average_clock_difference = sum_of_clock_difference / len(client_data)

    return average_clock_difference

def sync_clocks():
    while True:
        print("New synchronization cycle started.")
        print("Number of clients to be synchronized: " + str(len(client_data)))

        if len(client_data) > 0:
            average_clock_difference = get_average_diff()
            if average_clock_difference < datetime.timedelta(0):
                print("Average clock difference is negative. Skipping synchronization.")
                continue

            for client_addr, client in client_data.items():
                try:
                    synchronized_time = datetime.datetime.now() + average_clock_difference
                    client['connector'].send(str(synchronized_time).encode())
                except Exception as e:
                    print("Something went wrong while sending synchronized time through " + str(client_addr))
        else:
            print("No client data." + " Synchronization not applicable.")

        print("\n\n")

        time.sleep(5)

def initiate_server():
    master_server = socket.socket()
    master_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    print("Socket at master node created successfully\n")

    master_server.bind((HOST, PORT))

    master_server.listen(10)
    print("Clock server started...\n")

    print("Starting to make connections...\n")
    master_thread = threading.Thread(
        target=start_connection,
        args=(master_server, ))
    master_thread.start()

    print("Starting synchronization parallelly...\n")
    sync_thread = threading.Thread(
        target=sync_clocks,
        args=())
    sync_thread.start()

if __name__ == '__main__':
    initiate_server()
