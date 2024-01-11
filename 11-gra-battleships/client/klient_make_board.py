def print_board(board):
    print("Twoja plansza")
    print("  0 1 2 3 4 5 6 7 8 9")
    for i, rowB in enumerate(board):
        print(i, " ".join(rowB))


def is_valid_position(board, x, y, ship_size, orientation):
    if orientation.lower() == "h":
        if y + ship_size > 10:
            return False
        for i in range(ship_size):
            if board[x][y + i] != "-" or (x > 0 and board[x - 1][y + i] != "-") or (
                    x < 9 and board[x + 1][y + i] != "-"):
                return False
    elif orientation.lower() == "v":
        if x + ship_size > 10:
            return False
        for i in range(ship_size):
            if board[x + i][y] != "-" or (y > 0 and board[x + i][y - 1] != "-") or (
                    y < 9 and board[x + i][y + 1] != "-"):
                return False
    return True


def place_ship(board, ship_size):
    while True:
        try:
            coordinates = input(f"Podaj współrzędne dla statku o rozmiarze {ship_size} (x,y): ").split(",")
            y, x = int(coordinates[0]), int(coordinates[1])

            if x < 0 or x >= 10 or y < 0 or y >= 10:
                print("Podane współrzędne są poza zakresem planszy. Spróbuj ponownie.")
                continue

            orientation = input("Podaj orientację statku (h - poziomo, v - pionowo): ")

            if is_valid_position(board, x, y, ship_size, orientation):
                if orientation.lower() == "h":
                    for i in range(ship_size):
                        board[x][y + i] = str(ship_size)
                elif orientation.lower() == "v":
                    for i in range(ship_size):
                        board[x + i][y] = str(ship_size)
                break
            else:
                print("Statki nie mogą się dotykać ani wychodzić poza planszę. Spróbuj ponownie.")
        except (ValueError, IndexError):
            print("Niepoprawne dane. Spróbuj ponownie.")


def convert_to_x(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j].isdigit():
                board[i][j] = "X"
    return board


def make_user_board():
    board = [["-" for _ in range(10)] for _ in range(10)]

    ship_sizes = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

    for ship_size in ship_sizes:
        print_board(board)
        place_ship(board, ship_size)

    board = convert_to_x(board)

    print("Twoja plansza statków:")
    print_board(board)
    return board

