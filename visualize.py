import sys, pygame


SIZE = WIDTH, HEIGHT = 800, 800
WINDOW = pygame.display.set_mode(SIZE)
GRID = []

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

pygame.init()

class Tile:
    def __init__(self, row, col, height, width):
        self.row = row
        self.col = col
        self.height = height
        self.width = width
        self.x = row * width
        self.y = col * height
        self.color = WHITE
        self.neighbors = []
    
    def setTileColor(self, color):
        self.color = color
        pygame.draw.rect(WINDOW, self.color, (self.x, self.y, self.width, self.height))
        pygame.display.update()
        
    def exploreTile(self):
        self.setTileColor(YELLOW)
    
    def addNeighbor(self, other):
        self.neighbors.append(other)

    # def draw(self):
    #     pygame.draw.rect(WINDOW, self.color, (self.x, self.y, self.width, self.height))
    #     draw_grid(WINDOW, rows, cols)
    #     pygame.display.update()

    def __str__(self):
        return "row: " + str(self.row) + " col: " + str(self.col)
        
        


def draw_grid(WINDOW, rows, cols):
    for i in range(rows):
        pygame.draw.line(WINDOW, BLACK, (0, i * (WIDTH // cols)), (WIDTH, i * (WIDTH // cols)))
    for j in range(cols):
        pygame.draw.line(WINDOW, BLACK, (j * (HEIGHT // rows), 0), ((j * (HEIGHT // rows)), HEIGHT))
    pygame.display.update()


def make_grid(WINDOW, grid, rows, cols):
    for i in range(rows):
        grid.append([])
        for j in range(cols):
            grid[i].append(Tile(i, j, WIDTH // cols, HEIGHT // rows))
            

def convert_position(mouse_position, rows, cols, width, height):
    return GRID[mouse_position[0]//(width//cols)][mouse_position[1]//(height//rows)]


def __main__():
    rows = 30
    cols = 30
    start_tile = None
    end_tile = None

    make_grid(WINDOW, GRID, rows, cols)
    WINDOW.fill(WHITE)
    draw_grid(WINDOW, rows, cols)
    pygame.display.update()
    
    while True:
        # DRAW GRID
        
        # LEFT CLICK FOR START TILE/BARRIER TILES
        if pygame.mouse.get_pressed()[0]:
            mouse_position = pygame.mouse.get_pos()
            if start_tile:
                #do barrier
                barrier_tile = convert_position(mouse_position, rows, cols, WIDTH, HEIGHT)
                if barrier_tile is not start_tile and barrier_tile is not end_tile:
                    barrier_tile.setTileColor(GREY)
                    draw_grid(WINDOW, rows, cols)
            else:
                start_tile = convert_position(mouse_position, rows, cols, WIDTH, HEIGHT)
                print(start_tile)
                start_tile.setTileColor(GREEN)
                draw_grid(WINDOW, rows, cols)

        # RIGHT CLICK FOR END TILE
        if pygame.mouse.get_pressed()[2]:
            mouse_position = pygame.mouse.get_pos()
            clicked_tile = convert_position(mouse_position, rows, cols, WIDTH, HEIGHT)
            if end_tile and end_tile is not clicked_tile:
                end_tile.setTileColor(WHITE)
                draw_grid(WINDOW, rows, cols)
            end_tile = clicked_tile
            print(end_tile)
            end_tile.setTileColor(RED)
            draw_grid(WINDOW, rows, cols)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    pygame.quit()


__main__()