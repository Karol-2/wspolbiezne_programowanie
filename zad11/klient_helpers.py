import os
import klient_boardsets as boards


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
        x_coord = input("Podaj koordynat x: ")
        y_coord = input("Podaj koordynat y: ")
        if x_coord == "koniec" or y_coord == "koniec":
            return -1, -1, True

        x_coord = int(x_coord)
        y_coord = int(y_coord)

        if 1 <= x_coord <= 10 and 1 <= y_coord <= 10:
            return x_coord, y_coord, False

        print("Podaj wartość z przedziału 1-10!")
        return get_shot()
    except ValueError:
        print("Podaj wartość liczbową z przedziału 1-10!")
        return get_shot()


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
        print("Podaj 1 albo 2")
        choose_board()


def generate_shots_board(rows, cols):
    board = [['-' for _ in range(cols)] for _ in range(rows)]
    return board


def print_board(board, shot_board):
    separator = "=" * 80
    print(separator, "\n")
    print("Twoja plansza", "\t" * 4, "Twoje strzały")
    print("  1 2 3 4 5 6 7 8 9 10 			   1 2 3 4 5 6 7 8 9 10")
    for rowB, rowS in zip(board, shot_board):
        print(board.index(rowB) + 1, " ".join(rowB), "\t" * 3, board.index(rowB) + 1, " ".join(rowS))
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
