import time
import os.path

path = "./dane.txt"

while True:
    file_exists = os.path.isfile(path)

    if file_exists:
        time.sleep(1)
        number = 0
        print("Znaleziono plik dane.txt")

        # Wczytanie danych z pliku
        f = open('dane.txt', 'r')
        for line in f.readlines():
            number = line
            print("Wczytano: ", number)
        # Zamknięcie pliku
        f.close()
        print("Zamknięto dane.txt")

        result = int(number) * int(number)
        # Zapis do nowego pliku
        f = open("wynik.txt", "w")
        f.write(str(result))
        f.close()
        print("Wpisano do wynik.txt")
        os.remove(path)
        print("Usunięto dane.txt")
