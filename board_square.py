class Stone:
    # x and y are the middle point of the stone
    def __init__(self, radius, color, player:int, liberty: int=None, cell_coordinate: tuple=(), neighbors: list=[]):
        self.radius = radius
        self.color = color
        self.player = player
        self.liberty = liberty
        self.cell_coordinate = cell_coordinate
        self.neighbors = neighbors


class BoardSquare:
    #square x and y is anchhored at top left corner
    def __init__(self, x_start, y_start, width_height:int, is_white:bool, Stone:Stone = None, constraint:bool = False, ko:bool= False):
        self.x_start = x_start
        self.y_start = y_start
        self.width_height = width_height
        self.is_white = is_white
        self.stone = Stone
        self.constraint = constraint
        self.ko = ko


