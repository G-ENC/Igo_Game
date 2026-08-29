from board_square import BoardSquare, Stone
from board import generateBoardArray
def libertyCalculator(n, board_arr):
    for y in range(n):
        for x in range(n):
            