import sys, pygame
from queue import PriorityQueue


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
        self.parent = None
        self.distFromStart = 0 
        self.distToGoal = 0 
        self.totalCost = 0 
    
    def setTileColor(self, color):
        self.color = color
        pygame.draw.rect(WINDOW, self.color, (self.x, self.y, self.width, self.height))
        pygame.display.update()
        
    def exploreTile(self):
        self.setTileColor(YELLOW)
    
    def addNeighbors(self):
        if self.row > 0 and not GRID[self.row - 1][self.col].is_barrier():
            self.neighbors.append(GRID[self.row - 1][self.col])
        if self.row < len(GRID) - 1 and not GRID[self.row + 1][self.col].is_barrier():
            self.neighbors.append(GRID[self.row + 1][self.col])
        if self.col > 0 and not GRID[self.row][self.col - 1].is_barrier():
            self.neighbors.append(GRID[self.row][self.col - 1])
        if self.col < len(GRID[0]) - 1 and not GRID[self.row][self.col + 1].is_barrier():
            self.neighbors.append(GRID[self.row][self.col + 1])

    def is_barrier(self):
        return self.color == GREY

    def initializeNeighbors():
        for row in GRID:
            for elem in row:
                elem.addNeighbors()
    # def draw(self):
    #     pygame.draw.rect(WINDOW, self.color, (self.x, self.y, self.width, self.height))
    #     draw_grid(WINDOW, rows, cols)
    #     pygame.display.update()

    def __str__(self):
        return "row: " + str(self.row) + " col: " + str(self.col)

    def __lt__(self, other):
        return self.totalCost < other.totalCost
        


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


def manhattan(start, end):
    # MANHATTAN DISTANCE
    x1, y1, = start.row, start.col
    x2, y2, = end.row, end.col
    return abs(x1 - x2) + abs(y1 - y2)


def dijkstra(start, end):
    astar(start, end, lambda x, y: 0)

def astar(start, end, heuristic = manhattan):
    distance_counter = 0
    open = PriorityQueue()
    open.put((0, distance_counter, start))
    fringe = {}
    distance = {}
    edgeTo = {}
    for row in GRID:
        for tile in row:
            distance[tile] = float("inf")
            fringe[tile] = float("inf")
    distance[start] = 0
    fringe[start] = heuristic(start, end)

    open_set = {start}

    while not open.empty():

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        currentTile = open.get()[2]
        open_set.remove(currentTile)

        if currentTile == end:
            while end in edgeTo:
                end = edgeTo[end]
                end.setTileColor(PURPLE)
            return True

        for neighborTile in currentTile.neighbors:
            temp = distance[currentTile] + 1
            if temp < distance[neighborTile]:
                edgeTo[neighborTile] = currentTile
                distance[neighborTile] = temp
                fringe[neighborTile] = temp + heuristic(neighborTile, end)
                if neighborTile not in open_set:
                    distance_counter += 1
                    open.put((fringe[neighborTile], distance_counter, neighborTile))
                    open_set.add(neighborTile)
                    neighborTile.setTileColor(TURQUOISE)

        pygame.display.update()

        if currentTile != start:
            currentTile.setTileColor(BLACK)

    pygame.display.update()
                
    return False


def menu():
    GRID[:] = []
    # pygame.init()
    __main__()

def HUD():
    X = 800
    Y = 800
    display_surface = pygame.display.set_mode((X, Y))
    pygame.display.set_caption('RULES')
    font = pygame.font.Font('freesansbold.ttf', 20)

    l1 = font.render("LEFT CLICK to set the start point, and then to set the walls.", True, BLACK, WHITE)
    l2 = font.render("RIGHT CLICK to set the end point.", True, BLACK, WHITE)
    l3 = font.render("PRESS A to run A* search, PRESS D to run DIJKSTRAS", True, BLACK, WHITE)
    l4 = font.render("PRESS SPACE to Reset, PRESS R to pull up the Rules", True, BLACK, WHITE)
    l5 = font.render("PRESS ESC to exit Rules", True, BLACK, WHITE)
  
    r1 = l1.get_rect()
    r2 = l2.get_rect()
    r3 = l3.get_rect()
    r4 = l4.get_rect()
    r5 = l5.get_rect()

    r1.center = (X // 2, 200)
    r2.center = (X // 2, 300)
    r3.center = (X // 2, 400)
    r4.center = (X // 2, 500)
    r5.center = (X // 2, 600)

    while True:
        display_surface.fill(WHITE)
        
        display_surface.blit(l1, r1)
        display_surface.blit(l2, r2)
        display_surface.blit(l3, r3)
        display_surface.blit(l4, r4)
        display_surface.blit(l5, r5)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.QUIT:
                sys.exit()

def __main__():
    SIZE = WIDTH, HEIGHT = 800, 800
    pygame.display.set_caption('SEARCH VISUALIZER')
    WINDOW = pygame.display.set_mode(SIZE)
    pygame.init()
    rows = 40
    cols = 40
    start_tile = None
    end_tile = None

    make_grid(WINDOW, GRID, rows, cols)

    # DRAW GRID
    WINDOW.fill(WHITE)
    draw_grid(WINDOW, rows, cols)
    pygame.display.update()
    
    while True:
        
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
                start_tile.setTileColor(GREEN)
                draw_grid(WINDOW, rows, cols)

        # RIGHT CLICK FOR END TILE
        if pygame.mouse.get_pressed()[2]:
            mouse_position = pygame.mouse.get_pos()
            clicked_tile = convert_position(mouse_position, rows, cols, WIDTH, HEIGHT)
            if clicked_tile is not start_tile:
                if end_tile and end_tile is not clicked_tile:
                    end_tile.setTileColor(WHITE)
                    draw_grid(WINDOW, rows, cols)
                end_tile = clicked_tile
                end_tile.setTileColor(RED)
            draw_grid(WINDOW, rows, cols)

        for event in pygame.event.get():
            # START ALGORITHM
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    Tile.initializeNeighbors()
                    astar(start_tile, end_tile)
                if event.key == pygame.K_d:
                    Tile.initializeNeighbors()
                    dijkstra(start_tile, end_tile)
                if event.key == pygame.K_r:
                    HUD()
                    menu()
                if event.key == pygame.K_SPACE:
                    menu()
            if event.type == pygame.QUIT:
                sys.exit()
    pygame.quit()
HUD()
menu()



