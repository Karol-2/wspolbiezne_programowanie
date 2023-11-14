import os
import signal
import sys
import errno

BAZA_DANYCH = {0: "Krawczykiewicz", 1: "Radecka", 2: "Majcher"}
SERVER_FIFO = "server_fifo"


def przyjmij_requesty():  # obsługa zadań z kolejki
    content = ""

    try:
        os.mkfifo(SERVER_FIFO)
    except OSError as oe:
        if oe.errno != errno.EEXIST:
            raise

    fifo = os.open(SERVER_FIFO, os.O_RDONLY)

    while input_str := os.read(fifo, 128).decode():
        content += input_str

    os.close(fifo)

    requesty = []
    for r in content.strip().split("\n"):
        id, sciezka_klienta = r.split(",")
        requesty.append((int(id), sciezka_klienta))

    print("Tablica requestów: ", requesty)
    return requesty


def SIGTERM_handler(signum, frame):
    print("SIGTERM")
    pass


def SIGHUP_handler(signum, frame):
    print("SIGHUP")
    pass


def SIGUSR1_handler(signum, frame):
    print("SIGUSR1")
    os.remove(SERVER_FIFO)
    sys.exit(0)


def main():
    signal.signal(signal.SIGHUP, SIGHUP_handler)
    signal.signal(signal.SIGTERM, SIGTERM_handler)
    signal.signal(signal.SIGUSR1, SIGUSR1_handler)
    print("Serwer oczekuje na requesty, pid:", os.getpid())

    while True:
        requesty = przyjmij_requesty()
        for id, sciezka_klienta in requesty:
            wynik_zapytania = BAZA_DANYCH.get(id, "Nie ma!")
            print(f"Odpowiedz: id-{id} sciezka-{sciezka_klienta} wynik-{wynik_zapytania}")

            fifo = os.open(sciezka_klienta, os.O_WRONLY)
            os.write(fifo, f"{wynik_zapytania}\n".encode())
            os.close(fifo)


if __name__ == "__main__":
    main()
