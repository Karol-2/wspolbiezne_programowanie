import os
import time
import errno


# Wygenerowanie unikalnej nazwy pliku dla klienta
client_filename = f"client_{os.getpid()}.txt"
print("Nazwa pliku klienta: ", client_filename)

# Tworzenie pliku zamkowego
while True:
    try:
        # Otwarcie pliku wyłącznie (exclusively)
        fd = os.open("lockfile", os.O_CREAT | os.O_EXCL | os.O_RDWR)
        print("Lockfile utworzony")
        break
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
        else:
            print("Serwer zajęty, zaczekaj chwilę...")
            time.sleep(1)


# Wprowadzanie tekstu przez klienta
with open("bufor_serwera.txt","a") as bs:
    bs.write(client_filename + "\n")
    while True:
        user_input = input("Wprowadź tekst (Esc, aby zakończyć): ")
        if user_input.lower() == "esc":
            print("Zakończono wprowadzanie tekstu")
            break

        bs.write(user_input + "\n")


while not os.path.exists(client_filename):
    print("Czekam na odpowiedź od serwera")
    time.sleep(2)

with open(client_filename, "r") as response_file:
    response = response_file.read()
    print("Odpowiedź od serwera: \n", response)

os.close(fd)
os.unlink("lockfile")
os.remove(client_filename)
# os.remove("client_buffer.txt")