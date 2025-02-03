# Centralized Mutual Exclusion Algorithm

import time
from collections import deque


class Coordinator:
    def __init__(self):
        self.currently_accessing = None
        self.queue = deque()

    def request_access(self, process_id):
        print(f"[Coordinator]: Received access request from Process {process_id}.")
        if self.currently_accessing is None:
            self.currently_accessing = process_id
            print(f"[Coordinator]: Resource granted to Process {process_id}.\n")
            return True
        else:
            print(f"[Coordinator]: Resource busy. Process {process_id} added to the queue.\n")
            self.queue.append(process_id)
            return False

    def release_resource(self, process_id):
        print(f"[Coordinator]: Process {process_id} has released the resource.")
        if self.queue:
            next_process = self.queue.popleft()
            self.currently_accessing = next_process
            print(f"[Coordinator]: Resource granted to Process {next_process}.\n")
        else:
            self.currently_accessing = None
            print(f"[Coordinator]: Resource is now free.\n")


class Process:
    def __init__(self, process_id, coordinator):
        self.process_id = process_id
        self.coordinator = coordinator

    def request_resource(self):
        print(
            f"[Process {self.process_id}]: Requesting access to the resource.")
        granted = self.coordinator.request_access(self.process_id)
        if granted:
            self.use_resource()
        else:
            print(f"[Process {self.process_id}]: Waiting for resource.\n")

    def use_resource(self):
        print(f"[Process {self.process_id}]: Using the resource...\n")
        time.sleep(2)  # Simulate resource usage
        self.release_resource()

    def release_resource(self):
        print(f"[Process {self.process_id}]: Releasing the resource.\n")
        self.coordinator.release_resource(self.process_id)


if __name__ == "__main__":
    # Instantiate the coordinator
    coordinator = Coordinator()

    # Create processes
    process1 = Process(1, coordinator)
    process2 = Process(2, coordinator)
    process3 = Process(3, coordinator)

    # Simulate resource requests
    print("--- Simulation Start ---\n")
    process1.request_resource()
    time.sleep(1)  # Simulate a slight delay before the next request
    process2.request_resource()
    time.sleep(1)  # Simulate a slight delay before the next request
    process3.request_resource()

    # Allow time for the processes to use and release the resource
    time.sleep(5)
    print("--- Simulation End ---")
