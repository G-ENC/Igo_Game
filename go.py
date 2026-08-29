import pygame
import sys
import numpy as np
from board_square import BoardSquare
from board import generateBoardArray
from board_square import Stone, BoardSquare

pygame.init()

SCREEN_WIDTH = 600;
SCREEN_HEIGHT = 600;
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("WEIQI")

clock = pygame.time.Clock()
FPS = 60


go_board_arr = generateBoardArray(9, SCREEN_WIDTH,SCREEN_HEIGHT)
one_board_square = go_board_arr[0][0]
running = True
update = False
player1_color = '#3bceac'
player2_color = '#ee4266'
player1_stone = Stone(one_board_square.width_height*3/8,player1_color,1)
player2_stone = Stone(one_board_square.width_height*3/8,player2_color,2)


def generateBoard(board):
    for row in board:
        for square in row:
            if square.is_white == True:
                pygame.draw.rect(screen, '#540d6e', (square.x_start,square.y_start,square.width_height, square.width_height))
            else:
                pygame.draw.rect(screen, '#ffd23f', (square.x_start,square.y_start,square.width_height, square.width_height))

def updateStones(board_array):
    for row in board_array:
        for square in row:
            if square.stone != None:
                if square.stone.player == 1:
                    pygame.draw.circle(screen, square.stone.color, (square.x_start+square.width_height/2, square.y_start+square.width_height/2),player1_stone.radius)
                elif square.stone.player == 2:
                    pygame.draw.circle(screen, square.stone.color, (square.x_start+square.width_height/2, square.y_start+square.width_height/2),player2_stone.radius)

def putStoneToCoordinate(x_pos, y_pos, board_arr, player_stone):
    board_arr[y_pos][x_pos].stone = player_stone


def resetBoard(board_array):
    for row in board_array:
        for square in row:
            square.stone = None

screen.fill((50,50,50))
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
            mouse_cell_number = mouse_pos[0]//go_board_arr[0][0].width_height, mouse_pos[1]//go_board_arr[0][0].width_height

            if left_click:
                putStoneToCoordinate(mouse_cell_number[0],mouse_cell_number[1],go_board_arr, player1_stone)
            elif right_click:
                putStoneToCoordinate(mouse_cell_number[0],mouse_cell_number[1],go_board_arr, player2_stone)
            update = False

    if mouse_pos != pygame.mouse.get_pos():
        mouse_pos = pygame.mouse.get_pos()
        update = False
    
    if not update:
        generateBoard(go_board_arr)
        updateStones(go_board_arr)
        update = True
    
    # pygame.draw.rect(screen, (255,255,255), (20,20,400,400))

    # pygame.draw.rect(screen, (255,255,255), (square.x_start,square.y_start,square.width_height, square.width_height))

    pygame.display.flip()

    # print(f"= {np.array([go_board])}")
    clock.tick(FPS)

pygame.quit()
sys.exit()