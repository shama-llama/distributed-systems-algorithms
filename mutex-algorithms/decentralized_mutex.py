import random
import time

class Coordinator:
    """
    Represents one replica's coordinator.
    Each coordinator can grant its vote if it is available.
    Once granted to a process, it denies further requests until it resets.
    """
    def __init__(self, id):
        self.id = id
        self.granted_to = None  # Vote is available when None

    def request_vote(self, process_id):
        if self.granted_to is None:
            self.granted_to = process_id
            print(f"Coordinator {self.id} grants vote to process {process_id}")
            return True
        else:
            print(f"Coordinator {self.id} denies vote to process {process_id} (already granted to {self.granted_to})")
            return False

    def reset(self):
        if self.granted_to is not None:
            print(f"Coordinator {self.id} resets (forgot vote granted to {self.granted_to})")
        self.granted_to = None

class Resource:
    """
    Represents a resource replicated N times.
    Each replica has its own coordinator. To access the resource, a process needs a majority
    vote, i.e. at least m = (N//2 + 1) coordinators must grant permission.
    """
    def __init__(self, name, num_replicas):
        self.name = name
        self.num_replicas = num_replicas
        self.coordinators = [Coordinator(i) for i in range(num_replicas)]
        self.m = (num_replicas // 2) + 1

    def request_access(self, process_id):
        votes = 0
        for coord in self.coordinators:
            if coord.request_vote(process_id):
                votes += 1
        return votes

    def check_access_granted(self, votes):
        return votes >= self.m

    def reset_coordinators(self, reset_probability):
        """
        Each coordinator resets with the given probability, simulating a crash/recovery.
        """
        for coord in self.coordinators:
            if random.random() < reset_probability:
                coord.reset()

class Process:
    """
    Dummy process that tries to acquire access to the resource.
    If not enough votes are gathered, it backs off for a random interval and retries.
    """
    def __init__(self, process_id, resource, delta_t, reset_probability):
        self.process_id = process_id
        self.resource = resource
        self.delta_t = delta_t
        self.reset_probability = reset_probability

    def request_resource(self):
        attempt = 0
        while True:
            attempt += 1
            print(f"\nProcess {self.process_id} attempt {attempt} to access resource '{self.resource.name}'")
            votes = self.resource.request_access(self.process_id)
            print(f"Process {self.process_id} received {votes} votes (needs at least {self.resource.m})")
            if self.resource.check_access_granted(votes):
                print(f"Process {self.process_id} is granted access to resource '{self.resource.name}'!")
                # Simulate resource usage for 1 second
                time.sleep(1)
                break
            else:
                print(f"Process {self.process_id} not granted access; backing off.")
                # Backoff for a random time between 0.5 and 2.0 seconds
                backoff_time = random.uniform(0.5, 2.0)
                time.sleep(backoff_time)
                # Simulate potential resets during the backoff period
                self.resource.reset_coordinators(self.reset_probability)
        print(f"Process {self.process_id} finished using resource '{self.resource.name}'.")

if __name__ == "__main__":
    resource_name = "example_resource"
    num_replicas = 32  # N = 32 replicas
    resource = Resource(resource_name, num_replicas)
    
    # Define simulation parameters:
    # Assuming a process holds the resource for a short period (delta_t = 10 seconds) 
    # over a 3-hour (10800 seconds) session, the probability of a coordinator resetting is:
    delta_t = 10
    reset_probability = delta_t / 10800.0
    
    # Create 3 dummy processes that share the same resource.
    process1 = Process(1, resource, delta_t, reset_probability)
    process2 = Process(2, resource, delta_t, reset_probability)
    process3 = Process(3, resource, delta_t, reset_probability)
    
    print("--- Simulation Start ---\n")
    
    process1.request_resource()
    time.sleep(1)
    process2.request_resource()
    time.sleep(1)
    process3.request_resource()
    
    time.sleep(5)
    print("\n--- Simulation End ---")
