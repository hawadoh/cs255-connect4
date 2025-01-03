import numpy as np

# In classic Connect 4, these are the parameters
ROW_COUNT = 6
COLUMN_COUNT = 7
WINNING_CHAIN_LENGTH = 4

def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT))

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return 0 <= col < COLUMN_COUNT and board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    limit = WINNING_CHAIN_LENGTH - 1
    # Check horizontal locations for a win
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT - limit):
            if all(board[r][c + i] == piece for i in range(WINNING_CHAIN_LENGTH)):
                return True

    # Check vertical locations for a win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - limit):
            if all(board[r + i][c] == piece for i in range(WINNING_CHAIN_LENGTH)):
                return True

    # Check positively sloped diagonals
    for r in range(ROW_COUNT - limit):
        for c in range(COLUMN_COUNT - limit):
            if all(board[r + i][c + i] == piece for i in range(WINNING_CHAIN_LENGTH)):
                return True

    # Check negatively sloped diagonals
    for r in range(WINNING_CHAIN_LENGTH - 1, ROW_COUNT):
        for c in range(COLUMN_COUNT - limit):
            if all(board[r - i][c + i] == piece for i in range(WINNING_CHAIN_LENGTH)):
                return True

    return False

board = create_board()
print_board(board)
game_over = False
turn = 0

while not game_over:
    try:
        if turn == 0:
            selection = int(input("Player 1 Make your selection (0-6): "))
        else:
            selection = int(input("Player 2 Make your selection (0-6): "))

        if is_valid_location(board, selection):
            row = get_next_open_row(board, selection)
            piece = 1 if turn == 0 else 2
            drop_piece(board, row, selection, piece)
            print_board(board)

            if winning_move(board, piece):
                print(f"PLAYER {piece} WINS!")
                game_over = True
            else:
                turn = (turn + 1) % 2
        else:
            print("Invalid selection. Column is full or out of range. Try again.")
    except ValueError:
        print("Invalid input. Please enter an integer between 0 and 6.")
