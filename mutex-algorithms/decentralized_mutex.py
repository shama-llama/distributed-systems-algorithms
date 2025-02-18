# Quorum-Based Mutual Exclusion Algorithm

import time
from collections import deque


class LamportClock:
    def __init__(self):
        self.timestamp = 0

    def increment(self):
        self.timestamp += 1

    def update(self, received_timestamp):
        self.timestamp = max(self.timestamp, received_timestamp) + 1


class Process:
    def __init__(self, process_id, quorum):
        self.process_id = process_id
        self.clock = LamportClock()
        self.queue = deque()
        self.resource_in_use = False
        self.waiting_for_resource = False
        self.quorum = quorum  # Define quorum for this process

    def send_request(self):
        self.clock.increment()
        self.waiting_for_resource = True
        message = (self.clock.timestamp, self.process_id)
        print(f"[Process {self.process_id}]: Sending resource request with timestamp {self.clock.timestamp} to quorum {self.quorum}.")
        for process in self.quorum:
            if process.process_id != self.process_id:
                process.receive_request(message)

    def receive_request(self, message):
        incoming_timestamp, sender_id = message
        self.clock.update(incoming_timestamp)
        print(f"[Process {self.process_id}]: Received request from Process {sender_id} with timestamp {incoming_timestamp}.")

        if not self.resource_in_use and not self.waiting_for_resource:
            print(f"[Process {self.process_id}]: Sending OK to Process {sender_id}.")
            self.send_ok(sender_id)
        elif self.resource_in_use:
            print(f"[Process {self.process_id}]: Resource in use. Queuing request from Process {sender_id}.")
            self.queue.append(message)
        elif self.waiting_for_resource:
            if (incoming_timestamp, sender_id) < (self.clock.timestamp, self.process_id):
                print(f"[Process {self.process_id}]: Sending OK to Process {sender_id} (lower timestamp).")
                self.send_ok(sender_id)
            else:
                print(f"[Process {self.process_id}]: Queuing request from Process {sender_id} (higher timestamp).")
                self.queue.append(message)

    def send_ok(self, receiver_id):
        print(f"[Process {self.process_id}]: OK sent to Process {receiver_id}.")

    def release_resource(self):
        self.resource_in_use = False
        self.waiting_for_resource = False
        print(f"[Process {self.process_id}]: Releasing the resource.")
        while self.queue:
            queued_message = self.queue.popleft()
            _, sender_id = queued_message
            print(f"[Process {self.process_id}]: Sending OK to queued Process {sender_id}.")
            self.send_ok(sender_id)

    def access_resource(self):
        print(f"[Process {self.process_id}]: Accessing the resource.")
        self.resource_in_use = True
        time.sleep(2)
        self.release_resource()


if __name__ == "__main__":
    # Define quorums
    total_processes = 4
    processes = [Process(i, []) for i in range(1, total_processes + 1)]

    # Assign quorums (example with overlapping quorums)
    processes[0].quorum = [processes[0], processes[1], processes[2]]
    processes[1].quorum = [processes[1], processes[2], processes[3]]
    processes[2].quorum = [processes[2], processes[3], processes[0]]
    processes[3].quorum = [processes[3], processes[0], processes[1]]

    # Simulate resource requests
    print("--- Simulation Start ---\n")
    processes[0].send_request()
    time.sleep(1)
    processes[1].send_request()
    time.sleep(1)
    processes[2].send_request()
    # Allow time for the processes to use and release the resource
    time.sleep(5)
    print("--- Simulation End ---")
