import pygame
import sys
import numpy as np
from numpy import *
from board_square import BoardSquare
from board import generateBoardArray
from board_square import Stone, BoardSquare
from utils import *

pygame.init()

SCREEN_WIDTH = 900;
SCREEN_HEIGHT = 900;
CELL_NUMBER = 9
DEBUG = False
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("WEIQI")

clock = pygame.time.Clock()
FPS = 60

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

def updateStones(board_array):
    for row in board_array:
        for square in row:
            
            if square.stone != None:
                if square.stone.liberty == 0:
                    square.stone = None
                elif square.stone.player == 1:
                    pygame.draw.circle(screen, square.stone.color, (square.x_start+square.width_height/2, square.y_start+square.width_height/2),player1_stone.radius)
                elif square.stone.player == 2:
                    pygame.draw.circle(screen, square.stone.color, (square.x_start+square.width_height/2, square.y_start+square.width_height/2),player2_stone.radius)

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
boardArrayStack = []

while running:

    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.unicode == 'r':
                resetBoard(go_board_arr)
            update = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if(pygame.mouse.get_pressed()[0]):
                stone = Stone(one_board_square.width_height*3/8,player1_color,1) if round_number%2 == 0 else Stone(one_board_square.width_height*3/8,player2_color,2) 
                cell_x, cell_y = getCellCoordinate(mouse_pos[0],mouse_pos[1],one_board_square.width_height)
                
                if go_board_arr[cell_y][cell_x].stone == None:

                    #log the boiard state to check if the move is valid


                    
                    putStoneToCoordinate(CELL_NUMBER, cell_x, cell_y, go_board_arr, stone)



                    boardArrayStack.append(getCellBoardArray(CELL_NUMBER, go_board_arr))

                    if(len(boardArrayStack)>3):
                        boardArrayStack.pop(0)
                    print("\n\n\n\n\n\n\n\n")
                    print(np.array(boardArrayStack))

                    if(len(boardArrayStack) == 3 and (boardArrayStack[2] == boardArrayStack[1])):
                        boardArrayStack.pop()
                        round_number -= 1
                    elif(len(boardArrayStack) == 3 and boardArrayStack[2] == boardArrayStack[0]):
                         go_board_arr[cell_y][cell_x].stone = None
                         

                    updateOponentLiberty(CELL_NUMBER, stone, go_board_arr)





                round_number += 1     
            update = False

    if mouse_pos != pygame.mouse.get_pos():
        mouse_pos = pygame.mouse.get_pos()
        update = False
    
    if not update:
        # generateBoard(go_board_arr)
        screen.fill('#D2B48C')
        generateOverlay(go_board_arr)
        updateStones(go_board_arr)
        turnIndicatorOverlay(round_number, player1_color, player2_color, one_board_square, SCREEN_WIDTH)
        updateLiberty(CELL_NUMBER, go_board_arr)
        update = True
    
    if DEBUG == True:
        cell_coo = getCellCoordinate(mouse_pos[0],mouse_pos[1],one_board_square.width_height)
        stone_at_cell = go_board_arr[cell_coo[1]][cell_coo[0]].stone
        print(f"cell_coordinate: {cell_coo}")
        if stone_at_cell:
            print(f"liberty: {stone_at_cell.liberty}")

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
sys.exit()