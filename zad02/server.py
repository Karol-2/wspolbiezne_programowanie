import os
import time
import errno


def main():
    while True:
        try:
            lockfile_esists = os.path.isfile("lockfile")
            if lockfile_esists:
                break
        except OSError as e:
            if e.errno != errno.EEXIST:
                print("Czekam na połączenie od klienta...")
                raise
            time.sleep(0.05)
    print("Nowy lockfile znaleziony!")

    while True:
        try:
            with open("bufor_serwera.txt", "r") as buffer_file:
                client_filename = buffer_file.readline().strip()
                client_message = buffer_file.read()

            os.remove("bufor_serwera.txt")

            print("\nOtrzymana wiadomośc:")
            print(client_message)

            # response = "Serwer odczytal twoją wiadomosc!"
            response = input("Podaj odpowiedź serwera: ")

            with open(client_filename, "w") as response_file:
                response_file.write(response)
            print(f"Odpowiedź wysłana do klienta: {client_filename}")
            print("\n Serwer czeka na dalsze połączenia...")
            break

        except FileNotFoundError:
            time.sleep(2)
        except PermissionError:
            time.sleep(1)
            continue


while True:
    main()
    time.sleep(2)
