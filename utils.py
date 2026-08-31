from board_square import BoardSquare, Stone
from board import generateBoardArray
import numpy as np


def putStoneToCoordinate(x_pos, y_pos, board_arr, player_stone):
    board_arr[y_pos][x_pos].stone = player_stone

def getCellBoardArray (n, board):
    cell_board = []
    for y in range(n):
        row = []
        for x in range(n):
            if board[y][x].stone != None:
                if board[y][x].stone.player == 1:
                    row.append(1)
                elif board[y][x].stone.player == 2:
                    row.append(2)
            else:
                row.append(0)
        cell_board.append(row)
    return cell_board

def resetBoard(board_array):
    for row in board_array:
        for square in row:
            square.stone = None

def getCellCoordinate(x_pos, y_pos, square_width_height):
    mouse_cell_number = x_pos//square_width_height, y_pos//square_width_height
    return mouse_cell_number

# def checkNeighbors(n, x_pos, y_pos, go_board):

#     neighbors = []

#     offset = np.array([(1,0),(0,1),(-1,0),(0,-1)])
#     current_coordinate = np.array((x_pos,y_pos))
#     available_spaces = np.array([])

#     for o in offset:
#         x,y = current_coordinate+o
#         if (x<0 or x>=n or y<0 or y>=n) == True:
#             continue
#         else:
#             np.append(available_spaces,(x,y))
    
#     for x,y in available_spaces:
#         if go_board[y][x].stone.player == go_board[y_pos][x_pos].stone.playe:


    
#     return available_spaces