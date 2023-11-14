import os
import signal
import sys
import errno

database = {
    0: "Nowak",
    1: "Kowalski",
    2: "Rybak",
    3: "Wiśniewska",
    4: "Szymański"
}

FIFO_PATH = "server_fifo"


def create_fifo(fifo_path):
    try:
        os.mkfifo(fifo_path)
    except OSError as oe:
        if oe.errno != errno.EEXIST:
            raise


def get_requests():
    requests_str = ""

    create_fifo(FIFO_PATH)

    fifo = os.open(FIFO_PATH, os.O_RDONLY)

    while input_str := os.read(fifo, 128).decode():
        requests_str += input_str

    os.close(fifo)

    requests = []
    for r in requests_str.strip().split("\n"):
        id, client_path = r.split(",")
        requests.append((int(id), client_path))

    return requests


def ignore_signal(signum, frame):
    pass


def handle_sigusr1(signum, frame):
    os.remove(FIFO_PATH)
    sys.exit(0)


signal.signal(signal.SIGHUP, ignore_signal)
signal.signal(signal.SIGTERM, ignore_signal)
signal.signal(signal.SIGUSR1, handle_sigusr1)
print("PID:", os.getpid())

while True:
    for id, client_path in get_requests():
        query_result = database.get(id, "nie ma")
        print(f"{id} {client_path}: {query_result}")

        fifo = os.open(client_path, os.O_WRONLY)
        os.write(fifo, f"{query_result}\n".encode())
        os.close(fifo)
