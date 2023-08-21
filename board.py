import pygame
import copy
from piece import Piece, Block


class Board:
    def __init__(self, board_array, window):
        self.window = window
        self.board_array = board_array
        self.solid_blocks = set()
        self.solid_rows = dict()
        self.game_over = False

    def draw_board(self, starting_point_x, starting_point_y, block_size):
        for y_index in range(0, self.get_board_height()):
            for x_index in range(0, self.get_board_width()):
                value = self.board_array[y_index][x_index]
                x = x_index * block_size + starting_point_x
                y = y_index * block_size + starting_point_y
                if value == 0:
                    self.draw_empty_board_cube(self.window, x, y, block_size)
                else:
                    self.draw_full_board_cube(self.window, x, y, block_size)

    def draw_empty_board_cube(self, surface, x, y, block_size):
        pygame.draw.rect(surface, 'black', (x, y, block_size, block_size), 1)

    def draw_full_board_cube(self, surface, x, y, block_size):
        pygame.draw.rect(surface, 'black', (x, y, block_size, block_size))

    def insert_piece(self, piece: Piece):
        piece_array = piece.get_piece_shape_array()

        initial_x_position = self.get_board_width() // 2 - self.get_board_width() // 6
        piece.x = initial_x_position
        piece.y = 0
        for y_index, row in enumerate(piece_array):
            for x_index, value in enumerate(row):
                # initialize piece in board
                x_in_board = initial_x_position + x_index
                y_in_board = y_index - 1
                if (x_in_board, y_in_board) in self.solid_blocks:
                    self.game_over = True
                if value == 1:
                    self.board_array[y_in_board][x_in_board] = value
                    # create the piece's square blocks
                    block = Block(y_in_board, x_in_board, value)
                    piece.positions.append(block)

    def can_rotate(self, piece: Piece):
        copy_piece = copy.deepcopy(piece)
        copy_piece.rotate()
        for block in copy_piece.positions:
            if (block.x, block.y) in self.solid_blocks or \
                    block.x > self.get_board_width() or \
                    block.x < 0 \
                    or block.y > self.get_board_height():
                return False
        return True

    def can_move_down(self, piece: Piece):
        for block in piece.positions:
            (future_x, future_y) = block.x, block.y + 1
            if (future_x, future_y) in self.solid_blocks or future_y > self.get_board_height() - 1:
                return False
        return True

    def can_move_left(self, piece: Piece):
        for block in piece.positions:
            (future_x, future_y) = block.x - 1, block.y
            if (future_x, future_y) in self.solid_blocks or future_x < 0:
                return False
        return True

    def can_move_right(self, piece: Piece):
        for block in piece.positions:
            (future_x, future_y) = block.x + 1, block.y
            if (future_x, future_y) in self.solid_blocks or future_x > self.get_board_width() - 1:
                return False
        return True

    def move_piece(self, piece: Piece, direction):
        self.clear_piece_pos(piece)
        if direction == 'down':
            piece.move_down()
        elif direction == 'left':
            piece.move_left()
        elif direction == 'right':
            piece.move_right()
        elif direction == 'up':
            piece.rotate()
        for block in piece.positions:
            self.board_array[block.y][block.x] = block.value

    def clear_piece_pos(self, piece: Piece):
        for block in piece.positions:
            if block.value == 1:
                self.board_array[block.y][block.x] = 0

    def solidify_piece(self, piece):
        for block in piece.positions:
            if block.value == 1:
                self.solid_blocks.add((block.x, block.y))

                if block.y not in self.solid_rows:
                    # create an empty set and add (x,y) coord for that row
                    self.solid_rows[block.y] = set()
                    self.solid_rows[block.y].add((block.x, block.y))
                else:
                    self.solid_rows[block.y].add((block.x, block.y))

    def get_board_height(self):
        return len(self.board_array)

    def get_board_width(self):
        return len(self.board_array[0])

    def should_remove_rows(self):
        rows_to_remove = list()
        for solid_row in self.solid_rows.values():
            if len(solid_row) == self.get_board_width():
                rows_to_remove.append(solid_row)
        return rows_to_remove

    def remove_rows(self, rows_to_remove):
        if rows_to_remove:
            for row in rows_to_remove:
                self.solid_blocks.difference_update(row)
                for x, y in row:
                    self.board_array[y][x] = 0
                _, column = next(iter(row))
                self.solid_rows[column].difference_update(row)
            return True
        return False
        # TODO move pieces above down

    def move_pieces_down(self):
        for y in range(self.get_board_height()-1, -1, -1):
            for x in range(self.get_board_width()-1, -1, -1):
                if (x, y) in self.solid_blocks and y+1 < self.get_board_height():
                    if self.board_array[y+1][x] == 0:
                        self.board_array[y][x] = 0
                        self.board_array[y+1][x] = 1
                        self.solid_blocks.discard((x, y))
                        self.solid_blocks.add((x, y+1))
                        self.solid_rows[y].discard((x, y))
                        self.solid_rows[y+1].add((x, y+1))
