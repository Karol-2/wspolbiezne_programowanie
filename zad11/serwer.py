import socket


# jako drugi musi być koniec
def main():
    IP = "127.0.0.1"
    PORT = 5001
    BUF_SIZE = 1024

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((IP, PORT))

    players = {}
    scores = {}

    print("Serwer UDP jest uruchomiony")
    print(f"Oczekiwanie na graczy")

    while True:
        try:
            data, address = server_socket.recvfrom(BUF_SIZE)

            choice = data.decode('utf-8')

            if choice == "connect" and len(players) != 2:
                players[address] = choice
                scores[address] = 0
                print(f"Połączył się nowy gracz: {address} ({len(players)}/2)")

                server_socket.sendto("connect".encode('utf-8'), address)
                # if len(players) == 2:
                print("GRA ZACZYNA SIĘ")
                for addr in players:
                    server_socket.sendto("Start".encode('utf-8'), addr)
            elif choice.lower() == "koniec":

                other_address = [addr for addr in players if addr != address]
                if other_address:
                    server_socket.sendto("Gra zakończona przez przeciwnika".encode('utf-8'), other_address[0])

                scores.pop(address, None)
                players.pop(address, None)
                print(f"Gra zakończona przez gracza {address}. Oczekiwanie na nowych graczy...")
                players = {}
                scores = {}
            else:

               exit()

        except socket.error as e:
            print(f"Socket error: {e}")
            players = {}
            scores = {}


def choose_winner(choice1, choice2):
    if choice1 == choice2:
        print("REMIS")
        return 0
    elif (choice1 == 'K' and choice2 == 'N') or \
            (choice1 == 'P' and choice2 == 'K') or \
            (choice1 == 'N' and choice2 == 'P'):
        print(choice1 + " WYGRYWA")
        return 1
    else:
        return -1


if __name__ == "__main__":
    main()
