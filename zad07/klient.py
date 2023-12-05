import socket


def main():
    IP = "127.0.0.1"
    PORT = 5001
    BUF_SIZE = 1024
    game = False

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (IP, PORT)

    try:
        client_socket.connect(server_address)

        client_socket.sendto("connect".encode('utf-8'), server_address)

        while True:
            response, _ = client_socket.recvfrom(BUF_SIZE)
            response = response.decode('utf-8')

            if response == "connect":
                print("Polaczono z serwerem, czekamy na przeciwnika")
            elif response == "Start":
                game = True
                print("ROZPOCZYNAMY GRĘ")
                print("Napisz odpowiednią literę aby wykonać ruch:")
                print("'p' - Papier")
                print("'k' - Kamień")
                print("'n' - Nożyce")
                print("'koniec' - Zakończenie gry")
            elif response == "Gra zakończona przez przeciwnika":
                print(response)
                client_socket.close()
                break

            if response in ["Wygrałeś rundę!", "Przegrałeś rundę.", "Remis!"]:
                print(response)
                response, _ = client_socket.recvfrom(BUF_SIZE)
                response = response.decode('utf-8')
                print(response)
            if game:
                choice = get_input()
                client_socket.sendto(choice.encode('utf-8'), server_address)

                if choice.lower() == 'koniec':
                    client_socket.close()
                    print("Zakończyłeś grę.")
                    break

                print("Czekanie na odpowiedź przeciwnika...")

    except socket.error as e:
        print(f"Wystąpił błąd: {e}")
    finally:
        client_socket.close()


def get_input():
    while True:
        choice = input("Twój wybór: ")
        if choice.lower() in ["p", "k", "n", "koniec"]:
            return choice
        else:
            print("Nieprawidłowa odpowiedź, napisz jeszcze raz")


if __name__ == "__main__":
    main()
