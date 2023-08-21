from enum import Enum


class Piece:
    def __init__(self, block_size, piece_type) -> None:
        self.positions = []
        self.x = 0
        self.y = 0
        self.block_size = block_size
        self.piece_type = piece_type
        self.rotations = self.piece_type.value
        self.current_rotation = 0

    def __repr__(self) -> str:
        return self.piece_type

    def get_piece_shape_array(self):
        return self.piece_type.value[0]

    def move_down(self):
        for block in self.positions:
           # increase y coord
            if block.value == 1:
                block.y += 1
        self.y += 1

    def move_right(self):
        for block in self.positions:
           # increase x coord
            if block.value == 1:
                block.x += 1
        self.x += 1

    def move_left(self):
        for block in self.positions:
           # decrease y coord
            if block.value == 1:
                block.x -= 1
        self.x -= 1

    def rotate(self):
        self.current_rotation += 1
        if self.current_rotation >= len(self.rotations):
            self.current_rotation = 0

        current_rotation_array = self.rotations[self.current_rotation]
        new_positions = []
        for y, row in enumerate(current_rotation_array):
            for x, value in enumerate(row):
                if value == 1:
                    block = Block(y + self.y, x + self.x, value)
                    new_positions.append(block)
        self.positions = new_positions


class Block:
    def __init__(self, y, x, value) -> None:
        self.x = x
        self.y = y
        self.value = value

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __gt__(self, other):
        if self.x == other.x:
            return self.y > other.y
        else:
            return self.x > other.x

    def __lt__(self, other):
        if self.x == other.x:
            return self.y < other.y
        else:
            return self.x < other.x

    def __repr__(self) -> str:
        return f'x:{self.x}, y:{self.y}, value:{self.value}'

    def __str__(self) -> str:
        return f'x:{self.x}, y:{self.y}, value:{self.value}'


piece_types = {
    'I':
        [
            [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
            ],
            [
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
            ],
        ],
    'J':
        [
            [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0],
                [0, 1, 1, 1, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
            ],
            [
                [0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 1, 0],
                [0, 0, 0, 0, 0],
            ],
            [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 1, 1, 1, 0],
                [0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0],
            ],
            [
                [0, 0, 0, 0, 0],
                [0, 1, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0],
            ],

        ],
    'L':
        [
            [
                [0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0],
                [0, 1, 1, 1, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
            ],
            [
                [0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 1, 1, 0, 0],
                [0, 0, 0, 0, 0],
            ],
            [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 1, 1, 1, 0],
                [0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0],
            ],
            [
                [0, 0, 0, 0, 0],
                [0, 0, 1, 1, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0],
            ],
        ],
    'O':
        [
            [
                [0, 0, 0, 0, 0],
                [0, 1, 1, 0, 0],
                [0, 1, 1, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
            ]
        ],
    'S':
        [
            [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 1, 1, 0],
                [0, 1, 1, 0, 0],
                [0, 0, 0, 0, 0],
            ],
            [
                [0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0],
                [0, 1, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0],
            ],
        ],
    'Z':
        [
            [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 1, 1, 0, 0],
                [0, 0, 1, 1, 0],
                [0, 0, 0, 0, 0],
            ],
            [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0],
                [0, 0, 1, 1, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0],
            ],
        ],
    'T':
        [
            [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 1, 1, 1, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0],
            ],
            [
                [0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 1, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0],
            ],
            [
                [0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 1, 1, 1, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
            ],
            [
                [0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 1, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0],
            ],
        ],
}


class PieceType(Enum):
    I = piece_types['I']
    J = piece_types['J']
    L = piece_types['L']
    O = piece_types['O']
    S = piece_types['S']
    T = piece_types['T']
    Z = piece_types['Z']
