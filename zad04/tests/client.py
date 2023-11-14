import os
import signal
import struct
import sys

FIFO_REQUEST = 'server_request_fifo'
FIFO_RESPONSE_PREFIX = 'client_response_fifo_'


def handle_sigusr1(signum, frame):
    print("Received SIGUSR1 signal")
    sys.exit(0)


def main():
    signal.signal(signal.SIGUSR1, handle_sigusr1)

    # Przykładowe zapytanie od klienta
    request = struct.pack('ii', 2, os.getpid())

    # Wysłanie zapytania do serwera
    with open(FIFO_REQUEST, "wb") as fifo:
        fifo.write(request)

    # Odczytanie odpowiedzi od serwera
    response_fifo = FIFO_RESPONSE_PREFIX + str(2)

    try:
        with open(response_fifo, "rb") as fifo:
            response = fifo.read()
        # Wypisanie odpowiedzi
        print(response.decode('utf-8'))
    except FileNotFoundError:
        print("File not found. Server response may not be ready yet.")


if __name__ == "__main__":
    main()
