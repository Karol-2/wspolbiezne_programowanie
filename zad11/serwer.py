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

    print("Serwer UDP jest uruchomiony")
    print(f"Oczekiwanie na graczy")

    while True:
        try:
            data, address = server_socket.recvfrom(BUF_SIZE)

            mess = data.decode('utf-8')

            if mess == "connect":
                print(f"Połączył się nowy gracz: {address}")

                can_start = add_player_to_rooms(address)

                server_socket.sendto("connect".encode('utf-8'), address)

                if can_start and find_room(address):
                    found_room, _ = find_room(address)
                    if not found_room.gameStarted:
                        print("Pokój", found_room.id, "| GRA ZACZYNA SIĘ")
                        update_game_started(found_room.id, True)

                        first_address = found_room.player1
                        second_address = found_room.player2

                        message = "start;" + found_room.id

                        if random.randint(0, 1):  # losowanie kto zaczyna
                            print("Pokój", found_room.id, "|Gracz zaczyna", first_address)
                            server_socket.sendto((message + ";strzelasz").encode('utf-8'), first_address)
                            server_socket.sendto((message + ";czekasz").encode('utf-8'), second_address)
                        else:
                            print("Pokój", found_room.id, "|Gracz zaczyna", second_address)
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
                    remove_room_by_id(room.id)

            elif mess.lower() == "koniec":
                room, player_number = find_room(address)
                other_address = find_other_player_address(room, player_number)
                if other_address:
                    server_socket.sendto("koniec".encode('utf-8'), other_address)

                print(f"Pokój", room.id, "|Gra zakończona przez gracza {address}.")
                remove_room_by_id(room.id)

        except socket.error as e:
            print(f"Socket error: {e}")
            exit()


def remove_room_by_id(room_id):
    global rooms
    rooms = [room for room in rooms if room.id != room_id]
    print(f"Rozgrywka w pokoju ${room_id} zakończona")


def add_player_to_rooms(player):
    can_start = False
    for room in rooms:
        if not room.gameStarted:
            if not room.player1:
                room.player1 = player
                print(f"Dodano {player} jako player 1 do pokoju {room.id}")
                return can_start

            elif not room.player2:
                room.player2 = player
                can_start = True
                print(f"Dodano {player} jako player 2 do pokoju {room.id}")
                return can_start

    new_room = GameRoom()
    new_room.player1 = player
    rooms.append(new_room)
    print(f"Stworzono nowy pokój ({new_room.id}) i dodano {player} jako player 1")
    return can_start


def update_game_started(room_id, new_value):
    global rooms
    for room in rooms:
        if room.id == room_id:
            room.gameStarted = new_value
            break


def find_other_player_address(room, player_number):
    if room and player_number == 1:
        return room.player2
    elif room and player_number == 2:
        return room.player1
    else:
        print("Error, nie można znaleźć pasującego pokoju!")
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
