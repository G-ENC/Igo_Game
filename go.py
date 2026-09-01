import pygame
import sys
import numpy as np
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
                if square.stone.player == 1:
                    pygame.draw.circle(screen, square.stone.color, (square.x_start+square.width_height/2, square.y_start+square.width_height/2),player1_stone.radius)
                elif square.stone.player == 2:
                    pygame.draw.circle(screen, square.stone.color, (square.x_start+square.width_height/2, square.y_start+square.width_height/2),player2_stone.radius)

mouse_pos = (0,0)

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.unicode == 'r':
                resetBoard(go_board_arr)
            update = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            left_click = pygame.mouse.get_pressed()[0]
            right_click = pygame.mouse.get_pressed()[2]
            mouse_cell_number = getCellCoordinate(mouse_pos[0],mouse_pos[1],one_board_square.width_height)
            cell_x, cell_y = mouse_cell_number

            if go_board_arr[cell_y][cell_x].stone == None:
                p1_stone = Stone(one_board_square.width_height*3/8,player1_color,1)
                p2_stone = Stone(one_board_square.width_height*3/8,player2_color,2)
                putStoneToCoordinate(CELL_NUMBER, cell_x, cell_y, go_board_arr, (p1_stone if left_click else p2_stone))
                # checkNeighbors(CELL_NUMBER, p1_stone, go_board_arr)
                # print(p1_stone.neighbors if left_click else p2_stone.neighbors)
                # dfs(CELL_NUMBER, p1_stone, go_board_arr)
                print(getLiberty(CELL_NUMBER, p1_stone, go_board_arr))
                
                print("\n\n\n\n")
            update = False

    if mouse_pos != pygame.mouse.get_pos():
        mouse_pos = pygame.mouse.get_pos()
        update = False
    
    if not update:
        # generateBoard(go_board_arr)
        screen.fill('#D2B48C')
        generateOverlay(go_board_arr)
        updateStones(go_board_arr)
        update = True
    
    if DEBUG == True:
        cell_coo = getCellCoordinate(mouse_pos[0],mouse_pos[1],one_board_square.width_height)
        print(f"cell_coordinate: {cell_coo}")

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
sys.exit()