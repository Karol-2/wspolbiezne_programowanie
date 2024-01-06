import random
import socket
from GameRoom import GameRoom

global rooms
rooms = []


def main():
    global rooms
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

            if mess == "connect":
                players[address] = mess
                print(f"Połączył się nowy gracz: {address}")

                print(add_player_to_rooms(address))

                server_socket.sendto("connect".encode('utf-8'), address)

            if len(rooms) != 0 and rooms[0].player1 and rooms[0].player2 and not rooms[0].gameStarted:
                print("Pokój", rooms[0].id, "| GRA ZACZYNA SIĘ")
                rooms[0].gameStarted = True;

                first_address = rooms[0].player1
                second_address = rooms[0].player2

                message = "start;"+rooms[0].id

                if random.randint(0, 1):  # losowanie kto zaczyna
                    print("Pokój", rooms[0].id, "|Gracz zaczyna", first_address)
                    server_socket.sendto((message + ";strzelasz").encode('utf-8'), first_address)
                    server_socket.sendto((message + ";czekasz").encode('utf-8'), second_address)
                else:
                    print("Pokój", rooms[0].id, "|Gracz zaczyna", second_address)
                    server_socket.sendto((message + ";strzelasz").encode('utf-8'), second_address)
                    server_socket.sendto((message + ";czekasz").encode('utf-8'), first_address)

            elif mess.lower().startswith("strzal"):

                array = mess.lower().split(';')
                sender_address = address
                coords = array[0].replace(" ", "").removeprefix("strzal").replace("(", "").replace(")", "").split(",")

                room, player_number = find_room(sender_address)
                other_address = find_other_player_address(room, player_number)

                if other_address:
                    print("Pokój", room.id, "|Gracz", sender_address, "strzela na koordynaty: ", coords)
                    print("Pokój", room.id, "|Wysyłam weryfikacje strzalu do", other_address)
    
                    mes = "check" + str(coords) + ';' + room.id
                    server_socket.sendto(mes.encode('utf-8'), other_address)

            elif mess.lower().startswith("result"):
                array = mess.split(';')
                result = array[1]
                sender_address = address
                coords = array[5]

                room, player_number = find_room(sender_address)
                other_address = find_other_player_address(room, player_number)

                if other_address:
                    print("Pokój", room.id, "|Gracz", address, "weryfikuje sukces strzału jako: ", result)
                    print("Pokój", room.id, "|Aktualizuję u ", other_address)

                    mes = "update;" + coords + ";" + str(result) + ";" + room.id
                    server_socket.sendto(mes.encode('utf-8'), other_address)
                if result == "False":
                    server_socket.sendto("czekasz".encode('utf-8'), other_address)
                    server_socket.sendto("strzelasz".encode('utf-8'), sender_address)
                else:
                    server_socket.sendto("czekasz".encode('utf-8'), sender_address)
                    server_socket.sendto("strzelasz".encode('utf-8'), other_address)

            elif mess.lower() == "koniec_wygrales":

                room, player_number = find_room(address)
                other_address = find_other_player_address(room, player_number)

                if other_address:
                    print("Pokój", room.id, "|Gracz", other_address, "wygrywa!")
                    server_socket.sendto("wygrana".encode('utf-8'), other_address)
                    players = {}
                    # usun pokoj

            elif mess.lower() == "koniec":
                room, player_number = find_room(address)
                other_address = find_other_player_address(room, player_number)
                if other_address:

                    server_socket.sendto("koniec".encode('utf-8'), other_address)

                players.pop(address, None)
                print(f"Pokój", room.id, "|Gra zakończona przez gracza {address}.")
                players = {}
                # usun pokooj

        except socket.error as e:
            print(f"Socket error: {e}")
            players = {}
            exit()


def add_player_to_rooms(player):
    for room in rooms:
        if not room.gameStarted:
            if not room.player1:
                room.player1 = player
                return f"Added {player} as player 1 to existing room {room.id}"
            elif not room.player2:
                room.player2 = player
                return f"Added {player} as player 2 to existing room {room.id}"

    new_room = GameRoom()
    new_room.player1 = player
    rooms.append(new_room)
    return f"Created a new room ({new_room.id}) and added {player} as player 1"


def find_other_player_address(room, player_number):
    if room and player_number == 1:
        return room.player2
    elif room and player_number == 2:
        return room.player1
    else:
        print("Error, problem with finding matching room!")
        return None


def find_room(player):
    for room in rooms:
        if room.player1 == player:
            return room, 1
        elif room.player2 == player:
            return room, 2
    return None, -1


if __name__ == "__main__":
    main()
