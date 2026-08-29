from board_square import BoardSquare

def generateBoardArray(n , screenWidth, screenHeight):

    go_board = []
    is_white = True

    cell_width_height = screenHeight//n

    if screenHeight>screenWidth:
        cell_width_height = screenWidth//n
    
    for y in range(n):
        row = []
        if(n%2 == 0):
            is_white = not is_white
        for x in range(n):
            row.append(BoardSquare(cell_width_height*x, cell_width_height*y, cell_width_height, is_white))
            is_white = not is_white
        go_board.append(row)
    
    return (go_board)