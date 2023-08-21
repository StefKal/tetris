# Example file showing a basic pygame "game loop"
import random
import pygame

from board import Board
from piece import PieceType, Piece
initial_array = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

BLOCK_SIZE = 30
BOARD_WIDTH = BLOCK_SIZE * len(initial_array[0])
BOARD_HEIGHT = BLOCK_SIZE * len(initial_array)
SCREEN_WIDTH = BLOCK_SIZE * 40
SCREEN_HEIGHT = BLOCK_SIZE * 30

# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
TIMER = pygame.event.custom_type()
pygame.time.set_timer(TIMER, 1000)
clock = pygame.time.Clock()
running = True
time_elapsed_since_last_action = 0


STARTING_POINT_X = (SCREEN_WIDTH // 2) - (BOARD_WIDTH // 2)
STARTING_POINT_Y = SCREEN_HEIGHT - BOARD_HEIGHT
board = Board(board_array=initial_array,
              window=screen,
              )
# get random piece
random_piece = Piece(BLOCK_SIZE, random.choice(list(PieceType)))
# put piece in board
# random_piece = Piece(BLOCK_SIZE, PieceType.I)
board.insert_piece(random_piece)


while running:
    screen.fill("white")
    dt = clock.tick()

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP and board.can_rotate(random_piece):
                board.move_piece(random_piece, 'up')
            elif event.key == pygame.K_RIGHT and board.can_move_right(random_piece):
                board.move_piece(random_piece, 'right')
            elif event.key == pygame.K_DOWN and board.can_move_down(random_piece):
                board.move_piece(random_piece, 'down')
            elif event.key == pygame.K_LEFT and board.can_move_left(random_piece):
                board.move_piece(random_piece, 'left')
    # fill the screen with a color to wipe away anything from last frame
    time_elapsed_since_last_action += dt
    if time_elapsed_since_last_action > 200 and not board.game_over:

        # while piece hasnt touched
        if board.can_move_down(random_piece):
            # displace piece
            board.move_piece(random_piece, 'down')
        elif not board.can_move_down(random_piece):
            board.solidify_piece(random_piece)
            rows_to_remove = board.should_remove_rows()
            if (board.remove_rows(rows_to_remove)):
                board.move_pieces_down()
            random_piece = Piece(BLOCK_SIZE, random.choice(list(PieceType)))
            # random_piece = Piece(BLOCK_SIZE, PieceType.I)
            board.insert_piece(random_piece)

        # draw board
        board.draw_board(block_size=BLOCK_SIZE, starting_point_x=STARTING_POINT_X,
                         starting_point_y=STARTING_POINT_Y)
        # check if piece has touched
        # check if rows need to be removed
        # check if game over

        # flip() the display to put your work on screen
        pygame.display.flip()
        time_elapsed_since_last_action = 0  # reset it to 0 so you can count again
    if time_elapsed_since_last_action > 200 and board.game_over:
        screen.fill('red')
        pygame.display.flip()


pygame.quit()
