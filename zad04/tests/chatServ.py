import os
import signal
import struct
import sys
import errno
import time

def handle_sighup(signum, frame):
    print("Received SIGHUP signal")

def handle_sigterm(signum, frame):
    print("Received SIGTERM signal")
    sys.exit(0)

def handle_sigusr1(signum, frame):
    print("Received SIGUSR1 signal. Exiting...")
    sys.exit(0)

def read_message(fd):
    # Czytaj długość komunikatu
    length_data = os.read(fd, 4)
    if not length_data:
        return None
    length = struct.unpack("!I", length_data)[0]

    # Czytaj resztę komunikatu
    data = os.read(fd, length)
    return data.decode("utf-8")

def write_message(fd, message):
    # Zapisz długość komunikatu
    length = len(message)
    os.write(fd, struct.pack("!I", length))

    # Zapisz resztę komunikatu
    os.write(fd, message.encode("utf-8"))

def process_request(request, database):
    id = int(request)
    response = database.get(id, "Nie ma")
    return response

def usun_fifo(sciezka_fifo):
    try:
        os.remove(sciezka_fifo)
        print(f"Plik FIFO {sciezka_fifo} został usunięty.")
    except FileNotFoundError:
        print(f"Plik FIFO {sciezka_fifo} nie istnieje.")
    except Exception as e:
        print(f"Wystąpił błąd podczas usuwania pliku FIFO: {str(e)}")

def server():

    # Utwórz kolejkę FIFO dla serwera
    server_queue_path = "/tmp/server_queue"

    usun_fifo(server_queue_path)

    os.mkfifo(server_queue_path)
    print("Utworzono kolejke")

    # Zarejestruj obsługę sygnałów
    signal.signal(signal.SIGHUP, handle_sighup)
    signal.signal(signal.SIGTERM, handle_sigterm)
    signal.signal(signal.SIGUSR1, handle_sigusr1)
    print("Dodano sygnały")

    # Twórz bazę danych (ID, nazwisko)
    database = {1: "Kowalski", 2: "Nowak", 3: "Doe"}
    print("Dodano bazę danych")

    # Otwórz kolejkę serwera do zapisu
    server_queue = os.open(server_queue_path, os.O_WRONLY)
    print("Otwarto kolejke")

    while True:
        try:
            # Odczytaj zapytanie od klienta
            request = read_message(server_queue)
            if request is None:
                break
            print("request: ",request)

            # Przetwórz zapytanie
            response = process_request(request, database)
            print("response: ",response)

            # Odczytaj ścieżkę do kolejki klienta
            client_queue_path = read_message(server_queue)
            print("client queue path: ", client_queue_path)

            # Otwórz kolejkę klienta do zapisu
            client_queue = os.open(client_queue_path, os.O_WRONLY)

            # Wyślij odpowiedź do klienta
            write_message(client_queue, response)

            # Zamknij kolejkę klienta
            os.close(client_queue)
        except OSError as e:
            if e.errno != errno.EINTR:
                raise

if __name__ == "__main__":
    server()
