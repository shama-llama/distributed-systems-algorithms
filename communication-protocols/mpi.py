from mpi4py import MPI

def mpi_program():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    initial = 1

    if rank == 0:
        initial = initial * 2
        print(f"Value at Worker {rank}: {initial}")
        comm.send(initial, dest = rank + 1)
    elif rank == size - 1:
        recv = comm.recv(source = rank - 1)
        initial = recv * 2
        print(f"Value at Worker {rank}: {initial}")
    else:
        recv = comm.recv(source = rank - 1)
        initial = recv * 2
        print(f"Value at Worker {rank}: {initial}")
        comm.send(initial, dest = rank + 1)


if __name__ == "__main__":
    mpi_program()
