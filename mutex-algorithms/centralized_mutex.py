import threading
import time
import random

class Coordinator:
    def __init__(self):
        self.lock = threading.Lock()
        self.resource_busy = False
        self.waiting_queue = []

    def request_access(self, process_id, event):
        with self.lock:
            if not self.resource_busy:
                print(f"Coordinator: Granting access to Process {process_id}.")
                self.resource_busy = True
                event.set()
            else:
                print(f"Coordinator: Process {process_id} must wait. Adding to queue.")
                self.waiting_queue.append((process_id, event))

    def release_access(self, process_id):
        with self.lock:
            print(f"Coordinator: Process {process_id} released the resource.")
            if self.waiting_queue:
                next_process_id, next_event = self.waiting_queue.pop(0)
                print(f"Coordinator: Granting access to waiting Process {next_process_id}.")
                next_event.set()
            else:
                self.resource_busy = False

def process_task(process_id, coordinator):
    print(f"Process {process_id}: Requesting access.")

    event = threading.Event()
    coordinator.request_access(process_id, event)
    event.wait()
    
    print(f"Process {process_id}: Access granted. Using resource...")
    time.sleep(random.uniform(1, 3))
    
    print(f"Process {process_id}: Finished using resource. Releasing it.")
    coordinator.release_access(process_id)

if __name__ == '__main__':
    coordinator = Coordinator()
    threads = []

    for i in range(1, 4):
        t = threading.Thread(target=process_task, args=(i, coordinator))
        threads.append(t)
        t.start()
        time.sleep(random.uniform(0.1, 1))

    for t in threads:
        t.join()

    print("All processes completed.")
