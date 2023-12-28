import ast
import random
import socket


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

            elif mess.lower().startswith("strzal"):

                array = mess.lower().split(';')
                sender_address = array[1]
                coords = array[0].replace(" ", "").removeprefix("strzal").replace("(", "").replace(")", "").split(",")
                tuple_sender = ast.literal_eval(sender_address)

                other_address = [addr for addr in players if addr != tuple_sender]
                if other_address:
                    print("klient", tuple_sender, "strzela na koordynaty: ", coords)
                    print("wysylam weryfikacje do", other_address[0])
    
                    mes = "check" + str(coords)
                    server_socket.sendto(mes.encode('utf-8'), other_address[0])

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

                server_socket.sendto(mes.encode('utf-8'), other_address)
                if result == "False":
                    server_socket.sendto("czekasz".encode('utf-8'), other_address)
                    server_socket.sendto("strzelasz".encode('utf-8'), tuple_sender)
                else:
                    server_socket.sendto("czekasz".encode('utf-8'), tuple_sender)
                    server_socket.sendto("strzelasz".encode('utf-8'), other_address)

            elif mess.lower() == "koniec_wygrales":
                other_address = [addr for addr in players if addr != address]
                if other_address:
                    server_socket.sendto("wygrana".encode('utf-8'), other_address[0])
                    players = {}

            elif mess.lower() == "koniec":
                other_address = [addr for addr in players if addr != address]
                if other_address:
                    server_socket.sendto("koniec".encode('utf-8'), other_address[0])

                players.pop(address, None)
                print(f"Gra zakończona przez gracza {address}.")
                players = {}

            else:
                print("Czekam na połączenia...")

        except socket.error as e:
            print(f"Socket error: {e}")
            # other_address = [addr for addr in players]
            # if other_address:
            #     message = "koniec".encode('utf-8')
            #     for addr in other_address:
            #         server_socket.sendto(message, addr)

            players = {}
            exit()


if __name__ == "__main__":
    main()
