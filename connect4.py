import numpy as np
import pygame
import sys
import math

# In classic Connect 4, these are the parameters
ROW_COUNT = 6
COLUMN_COUNT = 7
WINNING_CHAIN_LENGTH = 4

SQUARE_SIZE = 100
RADIUS = int(SQUARE_SIZE / 2 - 5)
OFFSET = int(SQUARE_SIZE / 2)
width = SQUARE_SIZE * COLUMN_COUNT
height = SQUARE_SIZE * (ROW_COUNT + 1) # For the insertion row
size = (width, height)

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (50, 205, 50)

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
                return True, [(r, c + i) for i in range(WINNING_CHAIN_LENGTH)]

    # Check vertical locations for a win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - limit):
            if all(board[r + i][c] == piece for i in range(WINNING_CHAIN_LENGTH)):
                return True, [(r + i, c) for i in range(WINNING_CHAIN_LENGTH)]

    # Check positively sloped diagonals
    for r in range(ROW_COUNT - limit):
        for c in range(COLUMN_COUNT - limit):
            if all(board[r + i][c + i] == piece for i in range(WINNING_CHAIN_LENGTH)):
                return True, [(r + i, c + i) for i in range(WINNING_CHAIN_LENGTH)]

    # Check negatively sloped diagonals
    for r in range(WINNING_CHAIN_LENGTH - 1, ROW_COUNT):
        for c in range(COLUMN_COUNT - limit):
            if all(board[r - i][c + i] == piece for i in range(WINNING_CHAIN_LENGTH)):
                return True, [(r - i, c + i) for i in range(WINNING_CHAIN_LENGTH)]

    return False, []

board = create_board()
print_board(board)
game_over = False
turn = 0

def draw_board(board, screen):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK, (c * SQUARE_SIZE + OFFSET, r * SQUARE_SIZE + SQUARE_SIZE + OFFSET), RADIUS)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (c * SQUARE_SIZE + OFFSET, height - r * SQUARE_SIZE - SQUARE_SIZE + OFFSET), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (c * SQUARE_SIZE + OFFSET, height - r * SQUARE_SIZE - SQUARE_SIZE + OFFSET), RADIUS)
    pygame.display.update()

pygame.init()

screen = pygame.display.set_mode(size)
draw_board(board, screen)

while True: # Keep running until the user closes the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if not game_over: # Only process hover and click events during gameplay
            if event.type == pygame.MOUSEMOTION:
                # Clear the hover area and draw the hover circle
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
                colour = RED if turn == 0 else YELLOW        
                pygame.draw.circle(screen, colour, (event.pos[0], OFFSET), RADIUS)    
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                player = 1 if turn == 0 else 2
                # selection = int(input(f"Player {player} Make your selection (0-{COLUMN_COUNT-1}): ")) # CLI-based
                selection = math.floor(event.pos[0] / SQUARE_SIZE) # GUI-based column selection

                if is_valid_location(board, selection):
                    row = get_next_open_row(board, selection)
                    piece = 1 if turn == 0 else 2
                    drop_piece(board, row, selection, piece)
                    print_board(board)
                    draw_board(board, screen)

                    has_won, win_coords = winning_move(board, piece)
                    if has_won:
                        print(f"PLAYER {piece} WINS!")
                        font = pygame.font.SysFont("monospace", 75)
                        label = font.render(f"Player {piece} wins!", 1, RED if piece == 1 else YELLOW)
                        pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE)) # Reset insertion column
                        screen.blit(label, (40, 10))
                        pygame.display.update()

                        # Draw the winning line
                        start = (win_coords[0][1] * SQUARE_SIZE + OFFSET, height - win_coords[0][0] * SQUARE_SIZE - OFFSET)
                        end = (win_coords[-1][1] * SQUARE_SIZE + OFFSET, height - win_coords[-1][0] * SQUARE_SIZE - OFFSET)
                        pygame.draw.line(screen, GREEN, start, end, 10)
                        pygame.display.update()

                        game_over = True
                        print("Press SPACEBAR to start a new game.")
                    else:
                        # Check for a draw
                        if not any(board[ROW_COUNT - 1][c] == 0 for c in range(COLUMN_COUNT)):
                            print("Draw!")
                            font = pygame.font.SysFont("monospace", 75)
                            label = font.render("Draw!", 1, GREEN)
                            # Calculate the centre position for the text
                            text_width, text_height = font.size("Draw!")
                            text_x = (width - text_width) // 2
                            text_y = (SQUARE_SIZE - text_height) // 2 # Centre it in the top row
                            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE)) # Clear the top row
                            screen.blit(label, (text_x, text_y)) # Blit the text at the centred position
                            pygame.display.update()
                            game_over = True
                            print("Press SPACEBAR to start a new game.")
                        else:
                            turn = (turn + 1) % 2
                else:
                    print("Invalid selection. Column is full or out of range. Try again.")
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Reset game state
                board = create_board()
                draw_board(board, screen)
                game_over = False
                turn = 0
                print("Game restarted!")
