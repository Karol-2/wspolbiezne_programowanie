import os
import sys
import time


def licz_wystapienia_slowa(tekst, szukane):
    czysty_tekst = tekst.replace('.', "").replace(',', "").lower()
    tablica_slow = czysty_tekst.split(" ")

    ilosc = 0
    for slowo in tablica_slow:
        if slowo.lower() == szukane.lower():
            ilosc += 1

    return ilosc


def znajdz_dyrektywy_input(text):
    dyrektywy = []
    pozycja = 0

    while True:
        pozycja_start = text.find('\\input{', pozycja)
        if pozycja_start == -1:
            break
        pozycja_koniec = text.find('}', pozycja_start)
        if pozycja_koniec == -1:
            break

        nazwa_pliku = text[pozycja_start + 7:pozycja_koniec]
        dyrektywy.append(nazwa_pliku)
        pozycja = pozycja_koniec + 1

    return dyrektywy


def main(nazwa_pliku, slowo):
    with open(nazwa_pliku, 'r') as plik:
        tekst = plik.read()

    calkowita_liczba_slow = licz_wystapienia_slowa(tekst, slowo)  # Najpierw sprawdza wystąpienia w swoim pliku
    print("w pliku:", "\"" + nazwa_pliku + "\"", "znaleziono", calkowita_liczba_slow, "słów")
    dyrektywy_input = znajdz_dyrektywy_input(tekst)  # Potem szuka dyrektyw

    for plik_input in dyrektywy_input:  # iteracja po nazwach plików
        pid = os.fork()
        print("Utworzono proces", pid, ',z pliku', nazwa_pliku, 'do pliku', plik_input)
        if pid == 0:  # proces potomny
            liczba_slow_dziecka = main(plik_input, slowo)  # odpalenie main dla kolejnego procesu
            time.sleep(5)
            sys.exit(liczba_slow_dziecka)

        else:  # proces macierzysty

            _, status_dziecka = os.waitpid(pid, 0)  # czekanie na zakończenie procesu potomnego
            liczba_slow_dziecka = os.WEXITSTATUS(status_dziecka)
            print("Proces", pid, "dostał wartość -", liczba_slow_dziecka)
            calkowita_liczba_slow += liczba_slow_dziecka

    return calkowita_liczba_slow


p = 'plikA.txt'
s = "i"

word_count = main(p, s)
print(f"\nIlość wystąpień słowa '{s}': {word_count}")
