import os
import signal
import struct
import sys
import threading

FIFO_REQUEST = 'server_request_fifo'
FIFO_RESPONSE_PREFIX = 'client_response_fifo_'


def handle_sighup(signum, frame):
    print("Received SIGHUP signal")


def handle_sigterm(signum, frame):
    print("Received SIGTERM signal")
    sys.exit(0)


def handle_sigusr1(signum, frame):
    print("Received SIGUSR1 signal")
    sys.exit(0)


def handle_client(request_fifo, client_id, data):
    response_fifo = FIFO_RESPONSE_PREFIX + str(client_id)

    try:
        # Odczytanie zapytania
        request = os.read(request_fifo, 8)
        client_id, _ = struct.unpack('ii', request)

        # Przeszukanie bazy danych
        response = "Nie ma"
        for record_id, name in data:
            if record_id == client_id:
                response = name.encode('utf-8')
                break

        # Wysłanie odpowiedzi do klienta
        with open(response_fifo, "wb") as fifo:
            fifo.write(response)
    except Exception as e:
        print(f"Error handling client {client_id}: {e}")


def main():
    data = [(1, "Kowalski"), (2, "Nowak"), (3, "Doe")]

    # Inicjalizacja kolejki
    try:
        os.mkfifo(FIFO_REQUEST)
    except FileExistsError:
        pass

    # Inicjalizacja sygnałów
    signal.signal(signal.SIGHUP, handle_sighup)
    signal.signal(signal.SIGTERM, handle_sigterm)
    signal.signal(signal.SIGUSR1, handle_sigusr1)

    while True:
        try:
            # Odczytanie zapytania od klienta
            request_fifo = os.open(FIFO_REQUEST, os.O_RDONLY)
            request = os.read(request_fifo, 8)
            os.close(request_fifo)

            client_id, _ = struct.unpack('ii', request)

            # Tworzenie kolejki odpowiedzi dla klienta
            response_fifo = FIFO_RESPONSE_PREFIX + str(client_id)
            try:
                os.mkfifo(response_fifo)
            except FileExistsError:
                pass

            # Uruchomienie wątku obsługującego klienta
            handle_client_thread = threading.Thread(
                target=handle_client, args=(response_fifo, client_id, data)
            )
            handle_client_thread.start()

        except KeyboardInterrupt:
            sys.exit(0)


if __name__ == "__main__":
    main()
