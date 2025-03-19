# Distributed Systems Algorithms

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)](https://docs.python.org/3.12/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repo contains projects for the Distributed Systems (CoSc 6003) course. It has Python code for some of the fundamental ideas in distributed systems: inter-process communication, mutual exclusion, and clock synchrnoization.

## Algorithms

### 1. Communication Protocols

#### 1.1. MPI (Message Passing Interface)

MPI is a standard method to handle message passing for parallel computing. The script here sets up processes in a ring. One root process sets it off by sending an integer. Each process gets the number, doubles it, and passes it to the next one in the ring. This continues until the number makes it all the way back to the start.

![MPI](/assets/mpi.png)

#### 1.2. Socket Communication

This script uses the Berkeley socket API to build a simple client-server message transfer system over TCP/IP. The server waits for clients to connect on a specific port, listens to what they send, and replies. The clients start the conversation by connecting, sending a message, and waiting for the server's response.

![Berkeley Socket](/assets/berkeley-socket.png)

### 2. Mutex Algorithms

#### 2.1. Centralized Mutex Algorithm

One process acts as the coordinator for granting access to a critical section. Any other process that wants the resource has to send a 'REQUEST' to the coordinator and wait for an 'OK' back. Although, this is a straightforward approach, it has single point of failure, which can get bottlenecked when the coordinator is busy.

![Centralized Mutex](/assets/centralized-mutex.png)

#### 2.2. Decentralized Mutex Algorithm

This is an adaptation of the Lin et al. (2004) algorithm. To enter a critical section, a process has to ask every other process for permission and get an 'OK' from more than half of them for a majority vote. This gets rid of the single-point-of-failure problem but means a lot more messages over the network.

![Decentralized Mutex](/assets/decentralized-mutex.png)

#### 2.3. Distributed Mutex Algorithm

In the Ricart-Agrawala algorithm, a process that wants access to the critical section sends a timestamped request to every other process. It can only proceed once it gets a reply from everyone. If another process has a conflicting request with an earlier timestamp, it holds off on replying until it's done. This approach is more efficient because it gets rid of separate 'RELEASE' messages. The reply serves as both a confirmation and a go-ahead.

![Distributed Mutex](/assets/distributed-mutex.png)

### 3. Synchronization Algorithms

#### 3.1. Berkeley Algorithm

One machine is picked as the master. It asks all the "slave" nodes for their time. Then, it figures out a system-wide average and tells each machine how much to adjust its clock. This is a good way to sync a cluster of machines there is no external, accurate time source. It relies on the master node to coordinate everyone. Here, there is a thin client and a thick server.

![Berkeley Algorithm](/assets/berkeley-clock.png)

#### 3.2. Cristian's Algorithm

This is in a way an inverse of Berkeley, where there is a thick client and a thin server. Clients ping a time server to get the official time. To account for the time it takes for the message to travel, they measure the round-trip time (RTT), cut it in half, and add that to the server's time before setting their own clocks. It leans on a single, trusted time server and makes a practical adjustment for network lag to get a reasonably close sync.

![Cristian Algorithm](/assets/cristian-clock.png)

## Required Packages

The following system-level dependencies need to be installed before running the projects for `mpi` support:

```bash
sudo dnf install openmpi openmpi-devel
```

## Project Setup

This project uses `uv` for package management. `uv` is an extremely fast Python package and project manager, written in Rust that can be used as a drop-in replacement for `pip`, `pip-tools`, `pipx`, `poetry`, `pyenv`, `twine`, `virtualenv`.

- **`uv` Installation**

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

- **Clone the Repository:**

    ```bash
    git clone https://github.com/shama-llama/distributed-systems-algorithms.git
    cd distributed-systems-algorithms
    ```

- **Create a Virtual Environment and Install Dependencies with `uv`:**

    ```bash
    uv venv
    uv pip install -e .
    ```

- **Activate the Virtual Environment:**

    ```bash
    source .venv/bin/activate
    ```

## References

> A. S. Tanenbaum and M. van Steen, *Distributed Systems: Principles and Paradigms*, 2nd ed. Enschede, The Netherlands: Maarten van Steen, 2016.
>
> G. Ricart and A. K. Agrawala, “An Optimal Algorithm for Mutual Exclusion in Computer Networks,” Commun. ACM, vol. 24, no. 1, pp. 9–17, Jan. 1981, doi: [10.1145/358527.358537](https://doi.org/10.1145/358527.358537).
>
> S.-D. Lin, Q. Lian, M. Chen, and Z. Zhang, “A Practical Distributed Mutual Exclusion Protocol in Dynamic Peer-to-Peer Systems,” in Peer-to-Peer Systems III, vol. 3279, G. M. Voelker and S. Shenker, Eds., in Lecture Notes in Computer Science, vol. 3279. , Berlin, Heidelberg: Springer Berlin Heidelberg, 2005, pp. 11–21. doi: [10.1007/978-3-540-30183-7_2](https://doi,org/10.1007/978-3-540-30183-7_2).
>
> F. Cristian, “Probabilistic Clock Synchronization,” Distrib Comput, vol. 3, no. 3, pp. 146–158, Sept. 1989, doi: [10.1007/BF01784024](https://doi.org/10.1007/BF01784024).
>
> R. Gusella and S. Zatti, “The Accuracy of the Clock Synchronization achieved by TEMPO in Berkeley UNIX 4.3BSD,” in IEEE Transactions on Software Engineering, vol. 15, no. 7, pp. 847-853, July 1989, doi: [10.1109/32.29484](https://doi.org/10.1109/32.29484).
>
> L. Lamport, “Time, Clocks, and the Ordering of Events in a Distributed System,” vol. 21, no. 7, 1978.

## License

This project is licensed under the terms of the [MIT](LICENSE) open source license.
