import ast
import os
import socket

import klient_boardsets as boards


def main():
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
                print("Mój adres to: ",client_address)
            elif response == "start":
                print("GRA ROZPOCZĘTA")
                shots_board = generate_shots_board(10, 10)
                show_rules()
                board = choose_board()
                print_board(board, shots_board)

            elif response == "czekasz":
                print("Teraz jest kolej twojego przeciwnika, czekamy na ruch...")

            elif response == "strzelasz":
                print("Twoja kolej")
                x_coord, y_coord = get_shot()
                message = "strzal " + "(" + str(x_coord) + "," + str(y_coord) + ");" + str(client_address)
                client_socket.sendto(message.encode('utf-8'), server_address)

            elif response.startswith("check"):
                coords = response.removeprefix("check").replace('[', '').replace(']', '').replace("'", "").split(",")
                x_coord = coords[0]
                y_coords = coords[1]
                print("Przeciwnik strzela na:", x_coord, ',', y_coords)

                if is_ship_hit(board, int(x_coord), int(y_coords)):
                    is_successful = True
                    print("PRZECIWNIK TRAFIŁ W STATEK")
                    update_board(board, int(x_coord), int(y_coords),"H")
                    print_board(board, shots_board)
                else:
                    is_successful = False
                    print("PRZECIWNIK UDERZYŁ W WODĘ")
                    print_board(board, shots_board)

                msg = "result;" + str(is_successful) + ';from;' + str(client_address) + ";coord;" + str(coords)
                client_socket.sendto(msg.encode('utf-8'), server_address)

                if has_game_ended(board):
                    print("GRA ZAKOŃCZONA, PORAŻKA")
                    client_socket.sendto("koniec_wygrales".encode('utf-8'),server_address)
                    exit()

            elif response.lower().startswith("update"):
                array = response.split(";")
                coords = array[1]
                result = array[2]

                coords_array = ast.literal_eval(coords)

                if result == "True":
                    print("Strzał na", coords_array, "jest TRAFNY!")
                    sign = "H"
                else:
                    print("Strzał na", coords_array, "jest NIETRAFIONY!")
                    sign = "M"
                input("Naciśnij ENTER by kontynuować")
                update_board(shots_board, int(coords_array[0]), int(coords_array[1]), sign)
                print_board(board, shots_board)
            elif response.lower() == "wygrana":
                print("WYGRAŁEŚ!!!")
                exit()
            elif response == "koniec":
                exit()
    except socket.error as e:
        print(f"Wystąpił błąd: {e}")
    finally:
        client_socket.close()


def has_game_ended(board):
    h_counter = 0
   # MAX_NUMBER_OF_X = 20 TODO: uncomment this
    MAX_NUMBER_OF_X = 3
    for row in board:
        for place in row:
            if place == "H":
                h_counter += 1

    return h_counter == MAX_NUMBER_OF_X


def update_board(board, shot_x, shot_y, result):
    board[shot_y - 1][shot_x - 1] = result
    return board


def is_ship_hit(board, x_coord, y_coord):
    if board[y_coord - 1][x_coord - 1] == "X":
        return True
    return False


def get_shot():
    try:
        print("Podaj swój strzał")
        x_coord = int(input("Podaj koordynat x: "))
        y_coord = int(input("Podaj koordynat y: "))
        if 1 <= x_coord <= 10 and 1 <= y_coord <= 10:
            return x_coord, y_coord
        print("Podaj wartość z przedziału 1-10!")
        get_shot()
    except ValueError:
        print("Podaj wartość liczbową z przedziału 1-10!")
        get_shot()


def choose_board():
    board_number = input("Wybierz jeden z gotowych rozkładów, napisz 1 albo 2: ")
    try:
        board_number = int(board_number)
        if board_number == 1:
            board = boards.board1
        else:
            board = boards.board2

        return board
    except ValueError:
        print("Podaj 1 albo 2");
        choose_board()


def generate_shots_board(rows, cols):
    board = [['-' for _ in range(cols)] for _ in range(rows)]
    return board


def print_board(board, shot_board):
    clear_console()
    separator = "=" * 100
    print(separator, "\n")
    print("Twoja plansza", "\t" * 4, "Twoje strzały")
    for rowB, rowS in zip(board, shot_board):
        print(" ".join(rowB), "\t" * 3, " ".join(rowS))
    print(separator, "\n")


def show_rules():
    print("ROZPOCZYNAMY GRĘ")
    print("ZASADY")
    print("\tNapisz 'koniec' aby zakończyć grę")
    print("Twoja plansza")
    print("\tZnak 'X' oznacza fragment twojego statku")
    print("\tZnak 'H' oznacza fragment statku został trafiony")
    print("\tZnak 'M' oznacza że pocisk trafił w wodę")
    print("Plansza twoich strzałów")
    print("\tZnak 'H' oznacza celny strzał")
    print("\tZnak 'M' oznacza niecelny strzał")


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":
    main()