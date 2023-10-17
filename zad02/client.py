import os
import time
import errno


# Wygenerowanie unikalnej nazwy pliku dla klienta
client_filename = f"client_{os.getpid()}.txt"

# Tworzenie pliku zamkowego
while True:
    try:
        # Otwarcie pliku wyłącznie (exclusively)
        fd = os.open("lockfile", os.O_CREAT | os.O_EXCL | os.O_RDWR)
        break
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
        else:
            print("Serwer zajęty, zaczekaj chwilę...")
            time.sleep(1)

print("Lockfile utworzony")

# Wprowadzanie tekstu przez klienta
while True:
    user_input = input("Wprowadź tekst (Esc, aby zakończyć): ")
    if user_input.lower() == "esc":
        print("Zakończono wprowadzanie tekstu")
        break
    with open("client_buffer.txt", "a") as buffer_file:
        buffer_file.write(user_input + "\n")

# zapisanie nazwy pliku klienta w buforze serwera
with open("bufor_serwera.txt","w") as buffer_file:
    buffer_file.write(client_filename + "\n")

while not os.path.exists(client_filename):
    print("Czekam na odpowiedź od serwera")
    time.sleep(2)

with open(client_filename,"r") as response_file:
    response = response_file.read()
    print("odpowiedź od serwera: \n", response)

os.unlink("lockfile")
os.remove(client_filename)
os.remove("client_buffer.txt")
os.remove("lockfile")