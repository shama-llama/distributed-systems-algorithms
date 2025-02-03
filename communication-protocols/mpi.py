from mpi4py import MPI

def mpi_program():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if rank == 0:
        print(f"Server (rank {rank}) waiting for messages from clients...")
        for i in range(1, size):
            data = comm.recv(source=i, tag=100)
            print(f"Server received from client {i}: {data}")
            response = f"Hello, Client {i}. Server acknowledges your message."
            comm.send(response, dest=i, tag=200)
    else:
        message = f"Hello from Client {rank}"
        comm.send(message, dest=0, tag=100)
        print(f"Client {rank} sent message: {message}")
        
        response = comm.recv(source=0, tag=200)
        print(f"Client {rank} received response: {response}")

if __name__ == "__main__":
    mpi_program()
