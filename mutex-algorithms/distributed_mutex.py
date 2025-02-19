import threading
import time
import random

class Process:
    def __init__(self, process_id, processes):
        self.id = process_id
        self.processes = processes  # List of all processes in the system
        self.state = "RELEASED"     # Can be "RELEASED", "WANTED", or "HELD"
        self.timestamp = None       # Timestamp of our own request
        self.clock = 0              # Logical clock for this process
        self.reply_count = 0        # Count of OK replies received for current request
        self.deferred_requests = [] # Queue for deferred requests (store sender IDs)
        self.lock = threading.Lock() 
        self.condition = threading.Condition(self.lock)

    def request_cs(self):
        """Request entry into the critical section."""
        with self.lock:
            self.state = "WANTED"
            self.clock += 1
            self.timestamp = self.clock
            self.reply_count = 0
            print(f"[Process {self.id}] Requesting critical section with timestamp {self.timestamp}")

        # Send request message to all processes (including self conceptually)
        for proc in self.processes:
            if proc.id == self.id:
                # Self-granting (conceptual); count it immediately.
                with self.lock:
                    self.reply_count += 1
            else:
                # Asynchronously call the receiver's request handler.
                threading.Thread(target=proc.receive_request, args=(self.id, self.timestamp)).start()

        # Wait until replies have been received from everyone.
        with self.condition:
            while self.reply_count < len(self.processes):
                self.condition.wait()
        
        with self.lock:
            self.state = "HELD"
            print(f"[Process {self.id}] Entering critical section")

    def release_cs(self):
        """Exit the critical section and reply to any deferred requests."""
        with self.lock:
            self.state = "RELEASED"
            print(f"[Process {self.id}] Releasing critical section")
            # Process all deferred requests
            for sender_id in self.deferred_requests:
                target = self.processes[sender_id]
                # Asynchronously send the OK reply.
                threading.Thread(target=target.receive_reply, args=(self.id,)).start()
            self.deferred_requests = []

    def receive_request(self, sender_id, sender_timestamp):
        """
        Handle an incoming request from another process.
        The decision to reply immediately or defer depends on the current state.
        """
        with self.lock:
            # Update logical clock.
            self.clock = max(self.clock, sender_timestamp) + 1
            if self.state == "RELEASED":
                print(f"[Process {self.id}] Received request from {sender_id} (timestamp {sender_timestamp}). Not interested: sending reply.")
                threading.Thread(target=self.processes[sender_id].receive_reply, args=(self.id,)).start()
            elif self.state == "HELD":
                print(f"[Process {self.id}] Received request from {sender_id} (timestamp {sender_timestamp}). In CS: deferring reply.")
                self.deferred_requests.append(sender_id)
            elif self.state == "WANTED":
                # Compare timestamps; in case of tie, lower process ID wins.
                if (sender_timestamp < self.timestamp) or (sender_timestamp == self.timestamp and sender_id < self.id):
                    print(f"[Process {self.id}] Received request from {sender_id} (timestamp {sender_timestamp}). Sender wins: sending reply.")
                    threading.Thread(target=self.processes[sender_id].receive_reply, args=(self.id,)).start()
                else:
                    print(f"[Process {self.id}] Received request from {sender_id} (timestamp {sender_timestamp}). Deferring reply.")
                    self.deferred_requests.append(sender_id)

    def receive_reply(self, sender_id):
        """
        Handle an OK reply from another process.
        Once all replies are in, the process can enter its critical section.
        """
        with self.condition:
            self.reply_count += 1
            print(f"[Process {self.id}] Received reply from {sender_id} (Total replies: {self.reply_count}).")
            if self.reply_count >= len(self.processes):
                self.condition.notify_all()

    def do_critical_section(self):
        """Simulate doing some work in the critical section."""
        time_in_cs = random.uniform(1, 3)
        print(f"[Process {self.id}] In critical section for {time_in_cs:.2f} seconds.")
        time.sleep(time_in_cs)

    def run(self):
        """Simulate the process lifecycle: request, execute, and release critical section."""
        # Request critical section
        self.request_cs()
        # Critical section
        self.do_critical_section()
        # Release critical section
        self.release_cs()

if __name__ == '__main__':
    # Create 3 processes.
    num_processes = 3
    processes = [None] * num_processes  # placeholder list
    for i in range(num_processes):
        processes[i] = Process(i, processes)
    
    threads = []
    # Start each process with a staggered start to simulate concurrent requests.
    for proc in processes:
        t = threading.Thread(target=proc.run)
        threads.append(t)
        t.start()
        time.sleep(random.uniform(0.1, 1))  # Slight delay between process starts

    # Wait for all processes to complete.
    for t in threads:
        t.join()

    print("All processes have completed.")
