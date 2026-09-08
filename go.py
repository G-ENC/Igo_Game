import pygame
import sys
import numpy as np
from numpy import *
from board_square import BoardSquare
from board import generateBoardArray
from board_square import Stone, BoardSquare
from utils import *
import copy
import random
import math
import time

pygame.init()

SCREEN_WIDTH = 900;
SCREEN_HEIGHT = 900;
CELL_NUMBER = 9
DEBUG = False
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("WEIQI")

font = pygame.font.Font(None, 36)

clock = pygame.time.Clock()
FPS = 120

go_board_arr = generateBoardArray(CELL_NUMBER, SCREEN_WIDTH,SCREEN_HEIGHT)
one_board_square = go_board_arr[0][0]
running = True
update = False
player1_color = '#1A1A1A'
player2_color = '#F5F5F5'
player1_stone = Stone(one_board_square.width_height*3/8,player1_color,1)
player2_stone = Stone(one_board_square.width_height*3/8,player2_color,2)

def turnIndicatorOverlay(turn, first_color, second_color, square:BoardSquare, screen_width):
    pygame.draw.circle(screen, first_color if turn%2==0 else second_color, ( screen_width, 0), square.width_height*3/9)
    # text_surface = font.render("White's turn" if turn%2 != 0 else "Black's turn", True, (255,255,255) if turn%2 != 0 else (0,0,0)) 
    # screen.blit(text_surface, (SCREEN_WIDTH/2.28, SCREEN_HEIGHT*1/60)) 

def generateBoard(board):
    for row in board:
        for square in row:
            if square.is_white == True:
                pygame.draw.rect(screen, '#3E2723', (square.x_start,square.y_start,square.width_height, square.width_height))
            else:
                pygame.draw.rect(screen, '#D2B48C', (square.x_start,square.y_start,square.width_height, square.width_height))

def generateOverlay(board):
    index = 0
    for row in board:
        pygame.draw.line(screen, '#3E2723', (0,row[index].y_start+one_board_square.width_height/2), (SCREEN_WIDTH,row[index].y_start+one_board_square.width_height/2), 5)
        pygame.draw.line(screen, '#3E2723', (row[index].x_start+one_board_square.width_height/2,0), (row[index].x_start+one_board_square.width_height/2,SCREEN_HEIGHT), 5)
        index += 1

def updateConstraintOverlay(board_arr):
    for row in board_arr:
        for square in row:
            if square.constraint == True:
                pygame.draw.circle(screen, (240, 20, 20), (square.x_start+square.width_height/2, square.y_start+square.width_height/2), one_board_square.width_height*1/5)

def updateKoOverlay(board_arr):
    for row in board_arr:
        for square in row:
            if square.ko == True:
                pygame.draw.circle(screen, (20, 20, 240), (square.x_start+square.width_height/2, square.y_start+square.width_height/2), one_board_square.width_height*1/5)


def findOneLibertyInNeighbor(n, x, y, board_array):
    one_liberty_stone = []
    offset = [(1,0),(0,1),(-1,0),(0,-1)]
    current_coordinate = (x,y)
    if(board_array[y][x].constraint == True):
        for o in offset:
            x,y = tuple(sum(x) for x in zip(current_coordinate, o))
            if (x<0 or x>=n or y<0 or y>=n) == True:
                continue
            else:
                if(board_array[y][x].stone != None and board_array[y][x].stone.liberty == 1):
                    one_liberty_stone.append(board_array[y][x].stone)  
    return one_liberty_stone

def findPlayerConstraints(n, player_stone, board_array):
    constraint_array = []
    one_liberty_stone_list = []
    for y in range(n):
        for x in range(n):
            board_array[y][x].constraint = False
            square = board_array[y][x]
            if square.stone == None:
                putStoneToCoordinate(n, x, y, board_array, player_stone)
                # updateOponentLiberty(CELL_NUMBER, player_stone, board_array)
                # removeZeroLibertyStones(go_board_arr)
                if (getLiberty(n, player_stone, board_array) == 0):
                    board_array[y][x].constraint = True
                    constraint_array.append((player_stone.cell_coordinate[0],player_stone.cell_coordinate[1]))
                # updateAllyLiberty(CELL_NUMBER, player_stone, board_array)
                one_liberty_stone_list = findOneLibertyInNeighbor(n, player_stone.cell_coordinate[0], player_stone.cell_coordinate[1], board_array)
                for s in one_liberty_stone_list:
                    if s.player != player_stone.player and len(constraint_array) != 0:
                        board_array[y][x].constraint = False
                        constraint_array.pop()
                board_array[y][x].stone = None
    return constraint_array

def findPlayerKo(n, player_stone, board_histroy, board_array):
    ko_cells = []
    future_board = copy.deepcopy(board_array)
    #place a stone if the board is the same as it was before after updatingOpponentLIberties then mark the spot as ko; a ko cell cannot be palced 
    for y in range(n):
        for x in range(n):
            board_array[y][x].ko = False
            square = board_array[y][x]
            if square.stone == None:
                putStoneToCoordinate(n, x, y, future_board, player_stone)
                updateOponentLiberty(n, player_stone, future_board)
                removeZeroLibertyStones(future_board)

                # print(np.array(getCellBoardArray(CELL_NUMBER,future_board)))

                
                if (len(board_histroy)==3) and (getCellBoardArray(n, board_histroy[1]) == getCellBoardArray(n, future_board)):
                    square.ko = True
                    ko_cells.append((x,y))
                    
                future_board[y][x].stone = None
    return ko_cells

def updateStoneOverlay(board_array):
    for row in board_array:
        for square in row:
            if square.stone != None:
                if square.stone.liberty == 0:
                    square.stone = None
                elif square.stone.player == 1:
                    pygame.draw.circle(screen, square.stone.color, (square.x_start+square.width_height/2, square.y_start+square.width_height/2),player1_stone.radius)
                elif square.stone.player == 2:
                    pygame.draw.circle(screen, square.stone.color, (square.x_start+square.width_height/2, square.y_start+square.width_height/2),player2_stone.radius)

def placeStoneAtRandom(n, turn, board_history, board_array): 
    stone = Stone(one_board_square.width_height*3/8,player1_color,1) if turn%2 == 0 else Stone(one_board_square.width_height*3/8,player2_color,2)

    constraint_cells = findPlayerConstraints(CELL_NUMBER, player1_stone if round_number%2==0 else player2_stone, go_board_arr)
    ko_cells = findPlayerKo(CELL_NUMBER, player1_stone if round_number%2==0 else player2_stone, board_history, go_board_arr)

    valid_moves = []

    for y in range(n):
        for x in range(n):
            if((x,y) not in constraint_cells or (x,y) not in ko_cells)and board_array[y][x].stone == None:
                valid_moves.append((x,y))

    random_coord = random.choice(valid_moves)
    cell_y = random_coord[1]
    cell_x = random_coord[0]

    # cell_y = math.floor(random.random()*n) 
    # cell_x = math.floor(random.random()*n)

    # coords = (cell_x, cell_y)


    # while((board_array[cell_y][cell_x].stone != None) and ((coords in constraint_cells) or (coords in ko_cells))):
    #     cell_y = math.floor(random.random()*n) 
    #     cell_x = math.floor(random.random()*n)
    #     for yindex in range(5):
    #         for xindex in range(5):
    #             cell_y +=  yindex
    #             cell_x +=  xindex
    #     coords = (cell_x, cell_y)
    

    # for board in board_history:
    #     print(np.array(getCellBoardArray(CELL_NUMBER,board)))
    if(board_array[cell_y][cell_x].stone == None):
        ko_cells = findPlayerKo(CELL_NUMBER, player1_stone if round_number%2==0 else player2_stone, board_history,go_board_arr)
        
        if (cell_x,cell_y) in ko_cells:
            print("Not allowed by Ko")
        else:
            if((cell_x,cell_y) in constraint_cells):
                # boardCellStack.pop()
                print("Not allowed by suicide")
            else:
                # print("Valid move")
                putStoneToCoordinate(CELL_NUMBER, cell_x, cell_y, board_array, stone)
                updateOponentLiberty(CELL_NUMBER, stone, board_array)
                removeZeroLibertyStones(board_array)
                updateAllyLiberty(CELL_NUMBER, stone, board_array)
                
                board_history.append(copy.deepcopy(board_array))
                len(board_history)>3 and board_history.pop(0)

    
                


def removeZeroLibertyStones(board_array):
    for row in board_array:
        for square in row:
            if square.stone != None:
                if square.stone.liberty == 0:
                    square.stone = None

def updateLiberty(n, board_array):
    seen = set()
    for y in range(n):
        for x in range(n):
            stone = board_array[y][x].stone
            if stone and (stone.cell_coordinate not in seen):
                for stone_coord in dfs(n, stone, board_array):
                    current_stone = board_array[stone_coord[1]][stone_coord[0]].stone
                    seen.add(stone_coord)
                    current_stone.liberty = getLiberty(n, current_stone, board_array)

def updateAllyLiberty(n, player_stone:Stone, board_array):
    seen = set()
    for y in range(n):
        for x in range(n):
            stone = board_array[y][x].stone
            if stone and (stone.cell_coordinate not in seen) and (stone.color == player_stone.color):
                for stone_coord in dfs(n, stone, board_array):
                    current_stone = board_array[stone_coord[1]][stone_coord[0]].stone
                    seen.add(stone_coord)
                    current_stone.liberty = getLiberty(n, current_stone, board_array)

def updateOponentLiberty(n, player_stone:Stone, board_array):
    seen = set()
    for y in range(n):
        for x in range(n):
            stone = board_array[y][x].stone
            if stone and (stone.cell_coordinate not in seen) and (stone.color != player_stone.color):
                for stone_coord in dfs(n, stone, board_array):
                    current_stone = board_array[stone_coord[1]][stone_coord[0]].stone
                    seen.add(stone_coord)
                    current_stone.liberty = getLiberty(n, current_stone, board_array)
   
mouse_pos = (0,0)
round_number = 0
boardCellStack = []
boardArrayStack = []

while running:

    time.sleep(0.0001)
    placeStoneAtRandom(CELL_NUMBER, round_number, boardArrayStack, go_board_arr)
    round_number += 1
    update = False

    constraint_cells = findPlayerConstraints(CELL_NUMBER, player1_stone if round_number%2==0 else player2_stone, go_board_arr)
    ko_cells = findPlayerKo(CELL_NUMBER, player1_stone if round_number%2==0 else player2_stone, boardArrayStack,go_board_arr)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.unicode == 'r':
                resetBoard(go_board_arr)
                update = False

            if event.unicode == 'a':
                placeStoneAtRandom(CELL_NUMBER, round_number, boardArrayStack, go_board_arr)
                round_number += 1
                update = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if(pygame.mouse.get_pressed()[0]):
                stone = Stone(one_board_square.width_height*3/8,player1_color,1) if round_number%2 == 0 else Stone(one_board_square.width_height*3/8,player2_color,2)
                cell_x, cell_y = getCellCoordinate(mouse_pos[0],mouse_pos[1],one_board_square.width_height)


                if go_board_arr[cell_y][cell_x].stone == None:

                    # for board in boardArrayStack:
                    #     print(np.array(getCellBoardArray(CELL_NUMBER,board)))

                    ko_cells = findPlayerKo(CELL_NUMBER, player1_stone if round_number%2==0 else player2_stone, boardArrayStack,go_board_arr)
                    
                    if (cell_x,cell_y) in ko_cells:
                        print("Not allowed by Ko")
                    else:
                        if((cell_x,cell_y) in constraint_cells):
                            # boardCellStack.pop()
                            print("Not allowed by suicide")

                        else:
                            # print("Valid move")
                            putStoneToCoordinate(CELL_NUMBER, cell_x, cell_y, go_board_arr, stone)
                            updateOponentLiberty(CELL_NUMBER, stone, go_board_arr)
                            removeZeroLibertyStones(go_board_arr)
                            updateAllyLiberty(CELL_NUMBER, stone, go_board_arr)
                            
                            boardArrayStack.append(copy.deepcopy(go_board_arr))
                            len(boardArrayStack)>3 and boardArrayStack.pop(0)

                            round_number += 1
                            update = False
                
            elif(pygame.mouse.get_pressed()[2]):
                DEBUG = True

    if mouse_pos != pygame.mouse.get_pos():
        mouse_pos = pygame.mouse.get_pos()
        update = False
    
    if not update:
        # generateBoard(go_board_arr)
        screen.fill('#D2B48C')
        generateOverlay(go_board_arr)
        updateStoneOverlay(go_board_arr)
        
        turnIndicatorOverlay(round_number, player1_color, player2_color, one_board_square, SCREEN_WIDTH)

        updateConstraintOverlay(go_board_arr)
        updateKoOverlay(go_board_arr)
        update = True
    
    if DEBUG == True:
        
        cell_coo = getCellCoordinate(mouse_pos[0],mouse_pos[1],one_board_square.width_height)
        stone_at_cell = go_board_arr[cell_coo[1]][cell_coo[0]].stone
        # print(f"cell_coordinate: {cell_coo}")
        if stone_at_cell:
            print(f"liberty: {stone_at_cell.liberty}")
        print(f"constraint:{go_board_arr[cell_coo[1]][cell_coo[0]].constraint}")
        print(f"ko: {go_board_arr[cell_coo[1]][cell_coo[0]].ko}")
        DEBUG = False

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
sys.exit()