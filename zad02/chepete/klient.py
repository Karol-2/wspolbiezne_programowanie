import os
import time
import errno


# Wygenerowanie unikalnej nazwy pliku dla klienta
client_filename = f"client_{os.getpid()}.txt"

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

# Wprowadzanie tekstu przez klienta
while True:
    user_input = input("Wprowadź tekst (Esc, aby zakończyć): ")
    if user_input.lower() == "esc":
        print("Zakończono wprowadzanie tekstu")
        break
    with open("client_buffer.txt", "a") as buffer_file:
        buffer_file.write(user_input + "\n")

# Zapisanie nazwy pliku klienta w buforze serwera
with open("server_buffer.txt", "w") as buffer_file:
    buffer_file.write(client_filename + "\n")

# Oczekiwanie na odpowiedź od serwera
while not os.path.exists(client_filename):
    print("Serwer zajęty, proszę czekać...")
    time.sleep(2)

# Odczytanie i wyświetlenie odpowiedzi od serwera
with open(client_filename, "r") as response_file:
    response = response_file.read()
    print(f"Odpowiedź od serwera: {response}")

# Usuwanie pliku klienta i pliku zamkowego
os.remove(client_filename)
os.close(fd)
os.unlink("lockfile")
print("Koniec, plik zamkowy zlikwidowany")
