import random

def init_board():
    board = [['-' for _ in range(10)] for _ in range(10)]
    return board

def print_board(board):
    for row in board:
        print(' '.join(row))
    print()

def place_ship(board, ship_size):
    while True:
        orientation = random.choice(['horizontal', 'vertical'])
        if orientation == 'horizontal':
            start_row = random.randint(0, 9)
            start_col = random.randint(0, 10 - ship_size)
            end_col = start_col + ship_size
            if all(board[start_row][c] == '-' for c in range(start_col, end_col)):
                for c in range(start_col, end_col):
                    board[start_row][c] = 'x'
                break
        else:
            start_row = random.randint(0, 10 - ship_size)
            start_col = random.randint(0, 9)
            end_row = start_row + ship_size
            if all(board[r][start_col] == '-' for r in range(start_row, end_row)):
                for r in range(start_row, end_row):
                    board[r][start_col] = 'x'
                break

def place_all_ships(board):
    ship_sizes = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    for size in ship_sizes:
        place_ship(board, size)

def generate_ship_board():
    board = init_board()
    place_all_ships(board)
    return board

# Przykład użycia:
ship_board = generate_ship_board()
print_board(ship_board)
