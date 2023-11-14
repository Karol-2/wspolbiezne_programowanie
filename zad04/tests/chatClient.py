import os
import signal
import struct
import sys

def handle_sigusr1(signum, frame):
    print("Received SIGUSR1 signal. Exiting...")
    sys.exit(0)

def write_message(fd, message):
    # Zapisz długość komunikatu
    length = len(message)
    os.write(fd, struct.pack("!I", length))

    # Zapisz resztę komunikatu
    os.write(fd, message.encode("utf-8"))

def read_message(fd):
    # Czytaj długość komunikatu
    length_data = os.read(fd, 4)
    if not length_data:
        return None
    length = struct.unpack("!I", length_data)[0]

    # Czytaj resztę komunikatu
    data = os.read(fd, length)
    return data.decode("utf-8")

def usun_fifo(sciezka_fifo):
    try:
        os.remove(sciezka_fifo)
        print(f"Plik FIFO {sciezka_fifo} został usunięty.")
    except FileNotFoundError:
        print(f"Plik FIFO {sciezka_fifo} nie istnieje.")
    except Exception as e:
        print(f"Wystąpił błąd podczas usuwania pliku FIFO: {str(e)}")


def client(id, server_queue_path):
    # Utwórz kolejkę FIFO dla klienta
    client_queue_path = f"/tmp/client_queue_{id}"
    usun_fifo(client_queue_path)

    os.mkfifo(client_queue_path)
    print("Utworzono kolejke klienta ",id)

    # Otwórz kolejkę serwera do zapisu
    server_queue = os.open(server_queue_path, os.O_WRONLY)
    print("Utworzono kolejkę serwera do zapisu")

    # Zarejestruj obsługę sygnału SIGUSR1
    signal.signal(signal.SIGUSR1, handle_sigusr1)
    print("Zarejestrowano obsługę sygnału SIGUUSR1")

    try:
        # Zarejestruj kolejkę klienta w serwerze
        write_message(server_queue, str(id))
        write_message(server_queue, client_queue_path)

        # Otwórz kolejkę klienta do odczytu
        client_queue = os.open(client_queue_path, os.O_RDONLY)

        # Wyslij żądanie do serwera
        request = input("Podaj ID: ")
        write_message(server_queue, request)

        # Odczytaj odpowiedź od serwera
        response = read_message(client_queue)
        print("Odpowiedź:", response)

        # Zamknij kolejkę klienta
        os.close(client_queue)
    finally:
        # Zamknij kolejkę serwera
        os.close(server_queue)
        # Usuń kolejkę klienta
        os.unlink(client_queue_path)

if __name__ == "__main__":
    client_id = int(sys.argv[1]) # ID klienta
    server_queue_path = "/tmp/server_queue" # Ścieżka do kolejki serwera
    client(client_id, server_queue_path)
