import os
import os.path
import time

liczba = input("Podaj liczbę do podniesienia do kwadratu: ")

f = open("dane.txt","w")
f.write(liczba)
f.close()

while True:
    path = "./wynik.txt"

    file_exists = os.path.isfile(path)
    number = 0
    if file_exists:
        time.sleep(1)
        # Wczytanie danych z pliku
        f = open('wynik.txt', 'r')
        for line in f.readlines():
            number = line
            print("Wynik: ", number)
        # Zamknięcie pliku
        f.close()
        os.remove(path)
        break

