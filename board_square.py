class Stone:
    # x and y are the middle point of the stone
    def __init__(self, radius, color, player, liberty=None):
        self.radius = radius
        self.color = color
        self.player = player
        self.liberty = liberty


class BoardSquare:
    #square x and y is anchhored at top left corner
    def __init__(self, x_start, y_start, width_height, is_white, Stone = None):
        self.x_start = x_start
        self.y_start = y_start
        self.width_height = width_height
        self.is_white = is_white
        self.stone = Stone

