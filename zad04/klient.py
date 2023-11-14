import os
import sys
import errno
import time


DB_FIFO = "db_fifo"


def create_fifo(fifo_path):
    try:
        os.mkfifo(fifo_path)
    except OSError as oe:
        if oe.errno != errno.EEXIST:
            raise


def wait_file(path):
    while not os.path.exists(path):
        time.sleep(0.5)


def read_data(fifo):
    data = b""
    while not data.endswith(b"\n"):
        data += os.read(fifo, 128)

    return data.decode()


def write_to_db(id, client_path):
    write_fifo = os.open(DB_FIFO, os.O_WRONLY)
    os.write(write_fifo, f"{id},{client_path}\n".encode())
    os.close(write_fifo)


def read_from_db():
    read_fifo = os.open(client_path, os.O_RDONLY)
    data = read_data(read_fifo)
    os.close(read_fifo)
    return data


client_path = sys.argv[-1]
if len(sys.argv) != 2:
    print("Nieprawidłowa ilość argumentów")
    sys.exit(1)

create_fifo(client_path)

id = input("Podaj ID: ")
wait_file(DB_FIFO)
write_to_db(id, client_path)
print("Wynik:", read_from_db())

os.remove(client_path)
