import ast
import random
import socket


# jako drugi musi być koniec
def main():
    IP = "127.0.0.1"
    PORT = 5001
    BUF_SIZE = 1024

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((IP, PORT))

    players = {}

    print("Serwer UDP jest uruchomiony")
    print(f"Oczekiwanie na graczy")

    while True:
        try:
            data, address = server_socket.recvfrom(BUF_SIZE)

            mess = data.decode('utf-8')

            if mess == "connect" and len(players) != 2:
                players[address] = mess

                print(f"Połączył się nowy gracz: {address} ({len(players)}/2)")

                server_socket.sendto("connect".encode('utf-8'), address)
                if len(players) == 2:
                    print("GRA ZACZYNA SIĘ")

                    for addr in players:
                        server_socket.sendto("start".encode('utf-8'), addr)

                    first_address = list(players.keys())[0]
                    second_address = list(players.keys())[1]
                    print(first_address, second_address)

                    if random.randint(0, 1):  # losowanie kto zaczyna
                        print("Gracz zaczyna", first_address)
                        server_socket.sendto("strzelasz".encode('utf-8'), first_address)
                        server_socket.sendto("czekasz".encode('utf-8'), second_address)
                    else:
                        print("Gracz zaczyna", second_address)
                        server_socket.sendto("strzelasz".encode('utf-8'), second_address)
                        server_socket.sendto("czekasz".encode('utf-8'), first_address)

                    # oczekiwanie na wiadomość zaczynającą się na 'strzal'

            elif mess.lower().startswith("strzal"):

                array = mess.lower().split(';')
                sender_address = array[1]
                coords = array[0].replace(" ", "").removeprefix("strzal").replace("(", "").replace(")", "").split(",")
                tuple_sender = ast.literal_eval(sender_address)

                other_address = [addr for addr in players if addr != tuple_sender][0]
                print("klient", tuple_sender, "strzela na koordynaty: ", coords)
                print("wysylam weryfikacje do", other_address)

                mes = "check" + str(coords)
                server_socket.sendto(mes.encode('utf-8'), other_address)

            elif mess.lower().startswith("result"):
                array = mess.split(';')
                result = array[1]
                sender_address = array[3]
                coords = array[5]

                tuple_sender = ast.literal_eval(sender_address)

                print("klient", tuple_sender, "weryfikuje sukces strzału jako: ", result)
                other_address = [addr for addr in players if addr != tuple_sender][0]
                print("Aktualizuję u ", other_address)
                mes = "update;" + coords + ";" + str(result)

                print("this",tuple_sender)
                print("other",other_address)

                server_socket.sendto(mes.encode('utf-8'), other_address)
                server_socket.sendto("czekasz".encode('utf-8'), other_address)
                server_socket.sendto("strzelasz".encode('utf-8'), tuple_sender)

            elif mess.lower() == "koniec":

                other_address = [addr for addr in players if addr != address]
                if other_address:
                    server_socket.sendto("Gra zakończona przez przeciwnika".encode('utf-8'), other_address[0])

                players.pop(address, None)
                print(f"Gra zakończona przez gracza {address}. Oczekiwanie na nowych graczy...")
                players = {}

        except socket.error as e:
            print(f"Socket error: {e}")
            players = {}


if __name__ == "__main__":
    main()
