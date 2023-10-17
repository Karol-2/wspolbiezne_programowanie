import os
import time
import errno

# Tworzenie pliku zamkowego
while True:
    try:
        lockfileExists = os.path.isfile("lockfile")
        if lockfileExists:
            break
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
        time.sleep(0.05)
print("Lockfile znaleziony")

# Operacje zabezpieczone plikiem zamkowym
while True:
    try:
        with open("bufor_serwera.txt", "r") as buffer_file:
            client_filename = buffer_file.readline().strip()

        os.remove("bufor_serwera.txt")
        # with open(client_filename, "r") as buffer_file:
        #     client_message = buffer_file.read()
        #
        # print("Wiadomość od klienta:")
        # print(client_message)

        # Generowanie odpowiedzi (wersja uproszczona)
        response = "Serwer odczytal twoją wiadomosc!"

        with open(client_filename, "w") as response_file:
            response_file.write(response)

        print(f"Odpowiedź wysłana do klienta: {client_filename}")
        break
    except FileNotFoundError:
        time.sleep(2)

# os.unlink("lockfile")
# os.remove("lockfile")
print("Plik zamkowy zlikwidowany")