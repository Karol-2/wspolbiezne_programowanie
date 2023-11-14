import os
import signal
import sys
import errno

BAZA_DANYCH = {0: "Krawczykiewicz", 1: "Radecka", 2: "Majcher"}
SERVER_FIFO = "server_fifo"


def przyjmij_requesty():  # obsługa zadań z kolejki
    zawartosc_requesta = ""

    try:
        os.mkfifo(SERVER_FIFO)
    except OSError as oe:
        if oe.errno != errno.EEXIST:
            raise

    fifo = os.open(SERVER_FIFO, os.O_RDONLY)

    while input_str := os.read(fifo, 128).decode():
        zawartosc_requesta += input_str

    os.close(fifo)

    requesty = []
    for r in zawartosc_requesta.strip().split("\n"):
        id, sciezka_klienta = r.split(",")
        requesty.append((int(id), sciezka_klienta))

    print("Tablica requesów: ", requesty)
    return requesty


def signal_ignore(signum, frame):
    pass


def sigusr1_handler(signum, frame):
    os.remove(SERVER_FIFO)
    sys.exit(0)


def main():
    signal.signal(signal.SIGHUP, signal_ignore)
    signal.signal(signal.SIGTERM, signal_ignore)
    signal.signal(signal.SIGUSR1, sigusr1_handler)
    print("PID:", os.getpid())

    while True:
        requesty = przyjmij_requesty()
        for id, sciezka_klienta in requesty:
            wynik_zapytania = BAZA_DANYCH.get(id, "Nie ma!")
            print(f"{id} {sciezka_klienta}: {wynik_zapytania}")

            fifo = os.open(sciezka_klienta, os.O_WRONLY)
            os.write(fifo, f"{wynik_zapytania}\n".encode())
            os.close(fifo)


if __name__ == "__main__":
    main()
