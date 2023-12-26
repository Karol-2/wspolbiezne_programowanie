import socket

import klient_boardsets as boards


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
                shots_board = generate_shots_board(10, 10)
                show_rules()
                board = choose_board()
                print_board(board, shots_board)

                # x, y = get_shot()
                # if(is_ship_hit(board,x,y)):
                #     update_board(board,x,y,"H")
                #     update_board(shots_board,x,y,"H")
                #     print_board(board,shots_board)

            if game:
                choice = "koniec"
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


def has_game_ended(board):
    h_counter = 0
    MAX_NUMBER_OF_X = 20
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
        return x_coord, y_coord
    except ValueError:
        print("Podaj wartość z przedziału 1-10!")
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
    print("=" * 100, "\n")
    print("Twoja plansza", "\t" * 12, "Twoje strzały")
    for rowB, rowS in zip(board, shot_board):
        print(rowB, "\t" * 3, rowS)
    print("=" * 100, "\n")

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


if __name__ == "__main__":
    main()
