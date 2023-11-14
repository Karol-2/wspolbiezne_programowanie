import os
import sys
import errno
import time

SERVER_FIFO = "server_fifo"


def odczytaj_dane(fifo):
    # Odczytuje dane do momentu napotkania (\n).
    dane = b""
    while not dane.endswith(b"\n"):
        dane += os.read(fifo, 128)

    return dane.decode()


def zapisz_do_kolejki_serwera(id, sciezka_klienta):
    # Zapisuje id i ścieżkę klienta do pliku FIFO serwera.
    fifo_baza_plik = os.open(SERVER_FIFO, os.O_WRONLY)
    os.write(fifo_baza_plik, f"{id},{sciezka_klienta}\n".encode())  # Forma: id, ścieżka klienta znak nowej linii
    os.close(fifo_baza_plik)


def odczytaj_z_kolejki_klienta(sciezka_klienta):
    # Odczytuje odpowiedź z serwera, korzystając z podanej ścieżki klienta.
    fifo_plik_klient = os.open(sciezka_klienta, os.O_RDONLY)
    dane = odczytaj_dane(fifo_plik_klient)
    os.close(fifo_plik_klient)
    return dane


def main():
    # Tworzenie unikalnej ścieżki klienta na podstawie identyfikatora procesu
    sciezka_klienta = "klient" + str(os.getpid())

    # Tworzenie kolejki fifo dla kienta
    try:
        os.mkfifo(sciezka_klienta)
    except OSError as oe:
        if oe.errno != errno.EEXIST:
            raise

    id = input("Podaj szukane id: ")

    # Oczekiwanie na istnienie pliku FIFO bazy danych
    while not os.path.exists(SERVER_FIFO):
        time.sleep(1)

    # Zapisanie id do bazy danych i odczytanie odpowiedzi
    zapisz_do_kolejki_serwera(id, sciezka_klienta)
    odpowiedz = odczytaj_z_kolejki_klienta(sciezka_klienta)
    print("Odpowiedź:", odpowiedz)

    os.remove(sciezka_klienta)  # Usunięcie pliku FIFO klienta


if __name__ == "__main__":
    main()
