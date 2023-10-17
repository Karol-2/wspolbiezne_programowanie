import os
import time
import errno

class FileLockException(Exception):
    pass

# Tworzenie pliku zamkowego
while True:
    try:
        # Otwarcie pliku wyłącznie (exclusively)
        fd = os.open("../lockfile", os.O_CREAT | os.O_EXCL | os.O_RDWR)
        break
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
        time.sleep(0.05)
print("Lockfile created")

# Operacje zabezpieczone plikiem zamkowym
while True:
    try:
        with open("server_buffer.txt", "r") as buffer_file:
            client_filename = buffer_file.readline().strip()
            client_message = buffer_file.read()
        os.remove("server_buffer.txt")

        # Generowanie odpowiedzi (tutaj uproszczone)
        response = "Serwer: Odpowiedź na Twoją wiadomość."

        with open(client_filename, "w") as response_file:
            response_file.write(response)

        print(f"Odpowiedź wysłana do klienta: {client_filename}")
        break
    except FileNotFoundError:
        time.sleep(2)

# Usuwanie pliku zamkowego
os.close(fd)
os.unlink("lockfile")
print("Koniec, plik zamkowy zlikwidowany")
