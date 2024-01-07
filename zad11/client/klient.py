import ast
import socket

from klient_helpers import *

global my_room_id
my_room_id = ""


def main():
    global my_room_id
    IP = "127.0.0.1"
    PORT = 5001
    BUF_SIZE = 1024

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (IP, PORT)

    try:
        client_socket.connect(server_address)
        client_address = client_socket.getsockname()

        client_socket.sendto("connect".encode('utf-8'), server_address)

        while True:
            response, _ = client_socket.recvfrom(BUF_SIZE)
            response = response.decode('utf-8')

            if response == "connect":
                print("Polaczono z serwerem, czekamy na przeciwnika")
                print("Mój adres to: ", client_address)
            elif response.startswith("start"):
                my_room_id = response.split(";")[1]
                action = response.split(';')[2]

                print("Room id:", my_room_id)
                print("GRA ROZPOCZĘTA")

                shots_board = generate_shots_board(10, 10)
                show_rules()
                board = choose_board()
                clear_console()
                print_board(board, shots_board)

                if action == "wait":
                    print("Teraz jest kolej twojego przeciwnika, czekamy na ruch...")
                elif action == "shoot":
                    print("Twoja kolej")
                    x_coord, y_coord, end_game = get_shot(shots_board)
                    if end_game:
                        print("end, PODDAJESZ SIĘ")
                        client_socket.sendto("end_you_won".encode('utf-8'), server_address)
                        play_again()

                    message = "strzal " + "(" + str(x_coord) + "," + str(y_coord) + ");" + str(
                        client_address) + ";" + my_room_id
                    client_socket.sendto(message.encode('utf-8'), server_address)
                else:
                    print("error podczas pobierania wiadomości")

            elif response == "wait":
                print("Teraz jest kolej twojego przeciwnika, czekamy na ruch...")

            elif response == "shoot":
                print("Twoja kolej")
                if not has_game_ended(shots_board):
                    x_coord, y_coord, end_game = get_shot(shots_board)

                    if end_game:
                        print("end, PODDAJESZ SIĘ")
                        client_socket.sendto("end_you_won".encode('utf-8'), server_address)
                        play_again()

                    message = "strzal " + "(" + str(x_coord) + "," + str(y_coord) + ");" + str(client_address) + ";" + my_room_id
                    client_socket.sendto(message.encode('utf-8'), server_address)

            elif response.startswith("check"):
                try:
                    coords = response.split(';')[0].removeprefix("check").replace('[', '').replace(']', '').replace("'", "").split(",")
                    x_coord = coords[0]
                    y_coords = coords[1]

                    print("=" * 80)
                    if is_ship_hit(board, int(x_coord), int(y_coords)):
                        clear_console()
                        is_successful = True
                        print("PRZECIWNIK TRAFIŁ W STATEK")
                        update_board(board, int(x_coord), int(y_coords), "H")
                        print_board(board, shots_board)
                    else:
                        clear_console()
                        is_successful = False
                        print("PRZECIWNIK UDERZYŁ W WODĘ")
                        update_board(board, int(x_coord), int(y_coords), "M")
                        print_board(board, shots_board)

                    print("Przeciwnik strzelił na:", x_coord, ',', y_coords)
                    msg = "result;" + str(is_successful) + ';from;' + str(client_address) + ";coord;" + str(coords)
                    client_socket.sendto(msg.encode('utf-8'), server_address)

                    if has_game_ended(board):
                        print("GRA ZAKOŃCZONA, PORAŻKA")
                        client_socket.sendto("end_you_won".encode('utf-8'), server_address)
                        play_again()
                except UnboundLocalError:
                    continue
            elif response.lower().startswith("update"):
                array = response.split(";")
                coords = array[1]
                result = array[2]

                coords_array = ast.literal_eval(coords)
                clear_console()
                print("=" * 80)
                if result == "True":
                    print("Strzał na", coords_array, "jest TRAFNY!")
                    sign = "H"
                else:
                    print("Strzał na", coords_array, "jest NIETRAFIONY!")
                    sign = "M"

                update_board(shots_board, int(coords_array[0]), int(coords_array[1]), sign)
                print_board(board, shots_board)
            elif response.lower() == "wygrana":
                print("WYGRAŁEŚ!!!")
                play_again()
            elif response == "end":
                play_again()
            else:
                print("Oczekiwanie na ruch...")
    except socket.error as e:
        print(f"Wystąpił błąd: {e}")
    finally:
        client_socket.close()


def play_again():
    print("Czy chcesz zagrać jeszcze raz?")
    res = input("Wpisz T lub N: ")

    if res.lower() in ['t', 'tak', 'y', 'yes', 'continue']:
        main()
    elif res.lower() in ['n', 'nie', 'no', 'dont', 'exit', 'e', 'q']:
        exit()
    else:
        print("Niewłaściwe dane")
        play_again()


if __name__ == "__main__":
    main()
