import pygame
import random
import math
import time
from queue import PriorityQueue

WIDTH = 700
WIN = pygame.display.set_mode((WIDTH+150, WIDTH))
pygame.display.set_caption("Optima")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (200, 200, 200)
TURQUOISE = (64, 224, 208)
TURQUOISE2 = (190, 255, 255)

class Spot:
 def __init__(self, row, col, width, total_rows):
  self.row = row
  self.col = col
  self.x = row * width
  self.y = col * width
  self.color = WHITE
  self.neighbors = []
  self.width = width
  self.total_rows = total_rows

 def get_pos(self):
  return self.row, self.col

 def is_closed(self):
  return self.color == RED

 def is_open(self):
  return self.color == GREEN

 def is_barrier(self):
  return self.color == BLACK

 def is_start(self):
  return self.color == ORANGE

 def is_end(self):
  return self.color == TURQUOISE

 def is_empty(self):
    return self.color == WHITE

 def is_indicator(self):
    return self.color == GREY

 def reset(self):
  self.color = WHITE

 def make_start(self):
  self.color = ORANGE

 def make_barrier(self):
  self.color = BLACK

 def make_end(self):
  self.color = TURQUOISE

 def make_path(self):
  self.color = GREEN

 def make_player_path(self):
  self.color = RED

 def make_player(self):
    self.color = PURPLE

 def make_indicator(self, color=GREY):
    self.color = color

 def draw(self, win):
  pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

 def update_neighbors(self, grid):
  self.neighbors = []
  if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
   self.neighbors.append(grid[self.row + 1][self.col])

  if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
   self.neighbors.append(grid[self.row - 1][self.col])

  if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
   self.neighbors.append(grid[self.row][self.col + 1])

  if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
   self.neighbors.append(grid[self.row][self.col - 1])

 def clear_neighbors(self):
    self.neighbors = []

 def __lt__(self, other):
  return False

class button():
    def __init__(self, x, y, w, l, text, color=GREY):
        self.x = x
        self.y = y
        self.w = w
        self.l = l
        self.text = text
        self.color = color
        self.tcolor = "black"
        self.active = False
        self.font = pygame.font.SysFont('arial', 40, True)

    def toggle(self, on=True):
        self.active = on
        if self.active:
            pygame.draw.rect(WIN, self.color, (self.x, self.y, self.w, self.l))
            buttonL = self.font.render(self.text, False, self.tcolor)
            if self.is_hovered():
                pygame.draw.rect(WIN, RED, (self.x, self.y, self.w, self.l), 5)
            WIN.blit(buttonL, (self.x+20//len(self.text), self.y, self.x+self.w, self.y))
            pygame.display.update()

    def is_hovered(self):
        x, y = pygame.mouse.get_pos()
        if self.active == True and x in range(self.x, self.x+self.w) and y in range(self.y, self.y+self.l):
            self.color = BLACK
            self.tcolor = "white"
            return True
        else:
            self.color = GREY
            self.tcolor = "black"
            return False

    def set_text(self, text):
        self.text = text



def h(p1, p2):
 x1, y1 = p1
 x2, y2 = p2
 return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw, test=False):
 i = 0
 while current in came_from:
  i += 1
  current = came_from[current]
  current.make_path()
  if draw != None:
    draw()
 return i

def algorithm(draw, grid, start, end):
 count = 0
 open_set = PriorityQueue()
 open_set.put((0, count, start))
 came_from = {}
 g_score = {spot: float("inf") for row in grid for spot in row}
 g_score[start] = 0
 f_score = {spot: float("inf") for row in grid for spot in row}
 f_score[start] = h(start.get_pos(), end.get_pos())

 open_set_hash = {start}

 for i in range(len(move_list)):
  grid[move_list[len(move_list)-i-1][0]][move_list[len(move_list)-i-1][1]].make_player_path()
  if draw != None:
    draw()

 while not open_set.empty():
  for event in pygame.event.get():
   if event.type == pygame.QUIT:
    pygame.quit()

  current = open_set.get()[2]
  open_set_hash.remove(current)

  if current == end:
   if draw != None:
    reconstruct_path(came_from, end, draw)
   end.make_end()
   return True

  for neighbor in current.neighbors:
   temp_g_score = g_score[current] + 1

   if temp_g_score < g_score[neighbor]:
    came_from[neighbor] = current
    g_score[neighbor] = temp_g_score
    f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
    if neighbor not in open_set_hash:
     count += 1
     open_set.put((f_score[neighbor], count, neighbor))
     open_set_hash.add(neighbor)

 if draw != None:
    draw()
 return False

def fastest(grid, start, end):
 count = 0
 open_set = PriorityQueue()
 open_set.put((0, count, start))
 came_from = {}
 g_score = {spot: float("inf") for row in grid for spot in row}
 g_score[start] = 0
 f_score = {spot: float("inf") for row in grid for spot in row}
 cost = 0
 f_score[start] = h(start.get_pos(), end.get_pos())

 open_set_hash = {start}

 for i in range(len(move_list)):
  grid[move_list[len(move_list)-i-1][0]][move_list[len(move_list)-i-1][1]].make_player_path()

 while not open_set.empty():
  for event in pygame.event.get():
   if event.type == pygame.QUIT:
    pygame.quit()

  current = open_set.get()[2]
  open_set_hash.remove(current)

  if current == end:
   cost += reconstruct_path(came_from, end, None, True)
   end.make_end()

  for neighbor in current.neighbors:
   temp_g_score = g_score[current] + 1

   if temp_g_score < g_score[neighbor]:
    came_from[neighbor] = current
    g_score[neighbor] = temp_g_score
    f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
    if neighbor not in open_set_hash:
     count += 1
     open_set.put((f_score[neighbor], count, neighbor))
     open_set_hash.add(neighbor)
     
 return len(move_list) - cost - 1

def make_grid(rows, width):
 grid = []
 gap = width // rows
 for i in range(rows):
  grid.append([])
  for j in range(rows):
   spot = Spot(i, j, gap, rows)
   grid[i].append(spot)

 return grid


def draw_grid(win, rows, width):
 gap = width // rows
 for i in range(rows):
  pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
  for j in range(rows+1):
   pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
 win.fill(BLACK)

 for row in grid:
  for spot in row:
   spot.draw(win)

 draw_grid(win, rows, width)
 pygame.display.update()


def get_clicked_pos(pos, rows, width):
 gap = width // rows
 y, x = pos

 row = y // gap
 col = x // gap

 return row, col

move_list = []

ROWS = 50
grid = make_grid(ROWS, WIDTH)

def draw_indicators(x, y, grid, color=GREY):
    for i in range(50):
        if grid[i][y].is_empty() or grid[i][y].is_indicator():
            grid[i][y].make_indicator(color)
        if grid[x][i].is_empty() or grid[x][i].is_indicator():
            grid[x][i].make_indicator(color)

def remove_indicators(x, y, grid):
    for i in range(50):
        if grid[i][y].is_indicator():
            grid[i][y].reset()
        if grid[x][i].is_indicator():
            grid[x][i].reset()
    
def main(win, width, grid):
 pygame.font.init()
 pygame.key.set_repeat(200, 100)
 restart = button(225,350,250,50, "play again?")

 settings = {
        "open": False,
        "time_rem": 30,
        "rounds": 5,
        "spawn_dist": 50
    }

 open_settings = button(712, 625, 125, 50, "settings")
 increaseD = button(400, 450, 50, 50, "+")
 decreaseD = button(350, 450, 50, 50, "-")
 increaseR = button(400, 500, 50, 50, "+")
 decreaseR = button(350, 500, 50, 50, "-")

 duration = button(50, 450, 250, 50, "time: {}s".format(settings["time_rem"]))
 rounds = button(50, 500, 250, 50, "rounds: {}".format(settings["rounds"]))
 reset = button(50, 550, 100, 50, "Reset")
 end_game = button(50, 600, 100, 50, "Exit")

 font = pygame.font.SysFont('arial', 40, True)
 fontT = pygame.font.SysFont('copperplate gothic', 80, True)
 draw(win, grid, ROWS, WIDTH)
 titleRect = (210, 150)  
 scoreRect = (725, 300)
 deltaRect = (725, 350)
 timeRect = (725, 400)
 runRect = (715, 25)

 currtime = time.time()

 time_rem = settings["time_rem"]
 score = 0
 xscore = 0
 runNum = 0

 game = False
 regen = False

 start = None
 end = None

 run = True
 while run:  
  if settings["open"]:
    increaseR.toggle()
    decreaseR.toggle()
    increaseD.toggle()
    decreaseD.toggle()
    duration.toggle()
    rounds.toggle()
    reset.toggle()
    end_game.toggle()
    duration.set_text("time: {}s".format(settings["time_rem"]))
    rounds.set_text("rounds: {}".format(settings["rounds"]))
  else:
    increaseR.toggle(False)
    decreaseR.toggle(False)
    increaseD.toggle(False)
    decreaseD.toggle(False)
    duration.toggle(False)
    rounds.toggle(False)
    reset.toggle(False)
    end_game.toggle(False)
  for event in pygame.event.get():
   if pygame.mouse.get_pressed()[0]:
    if reset.is_hovered():
        runNum = 0
        game = False
        settings["open"] = not(settings["open"])
        draw(WIN, grid, ROWS, WIDTH)
    if increaseR.is_hovered() and settings["rounds"] < 10:
        settings["rounds"] += 1
    if increaseD.is_hovered() and settings["time_rem"] < 60:
        settings["time_rem"] += 1
    if decreaseR.is_hovered() and settings["rounds"] > 1:
        settings["rounds"] -= 1
    if decreaseD.is_hovered() and settings["time_rem"] > 15:
        settings["time_rem"] -= 1

   if open_settings.is_hovered() and pygame.mouse.get_pressed()[0]:
    settings["open"] = not(settings["open"])
    draw(WIN, grid, ROWS, WIDTH)
   if regen or (restart.is_hovered() and pygame.mouse.get_pressed()[0]) or event.type == pygame.KEYDOWN and event.key == pygame.K_g:
    settings["open"] = False
    restart.toggle(False)
    fail = False
    time_rem = settings["time_rem"]
    if not regen:
        runNum += 1
    start = None
    end = None
    grid = make_grid(ROWS, width)
    move_list.clear()

    if runNum % settings["rounds"] == 0 or (game and not regen):
        score = 0
        xscore = 0
        runNum = 1

    map_type = random.randint(1, 3)
    if map_type == 1:

        for i in range(500):
            row, col = random.randint(0, 49), random.randint(0, 49)
            spot = grid[row][col]
            spot.make_barrier()

    if map_type == 2:
        for i in range(random.randint(30,50)):
            walldir, wallx, wally, walllen = random.randint(1, 2), random.randint(0, 49), random.randint(0, 49), random.randint(5, 15)
            spot = grid[wallx][wally]
            if walldir == 1:
                for j in range(walllen):
                    spot = grid[wallx-j][wally]
                    spot.make_barrier()
            else:
                for j in range(walllen):
                    spot = grid[wallx][wally-j]
                    spot.make_barrier()
    if map_type == 3:
        ct = random.randint(15,20)
        try:
            for j in range(ct):
                row, col, size, side = random.randint(0,49), random.randint(0,49), random.randint(5,10), random.randint(1,4)
                for i in range(size+1):
                    if side != 1 and row+size < 50 and col+i < 50:
                        spot = grid[row+size][col+i]
                        spot.make_barrier()
                    if side != 2 and row < 50 and col+i < 50:
                        spot = grid[row][col+i]
                        spot.make_barrier()
                    if side != 3 and row+i < 50 and col+size < 50:
                        spot = grid[row+i][col+size]
                        spot.make_barrier()
                    if side != 4 and row+i < 50 and col < 50:
                        spot = grid[row+i][col]
                        spot.make_barrier()
        except:
            fail = True

    row, col = random.randint(0, 49), random.randint(0, 49)
    move_list.append((row, col))
    spot = grid[row][col]
    start = spot
    start.make_start()

    row, col = random.randint(0, 49), random.randint(45, 49)
    while h(start.get_pos(), (row, col)) < settings["spawn_dist"]:
        row, col = random.randint(0, 49), random.randint(0, 49)
    
    end = grid[row][col]
    end.make_end()

    for row in grid:
        for spot in row:
          spot.update_neighbors(grid)

    if fail or not algorithm(None, grid, start, end):
        regen = True
    else:
        regen = False

    draw_indicators(end.get_pos()[0], end.get_pos()[1], grid, TURQUOISE2)
    draw(WIN, grid, ROWS, WIDTH)
    game = True

   if event.type == pygame.QUIT or (end_game.is_hovered() and pygame.mouse.get_pressed()[0]):
    run = False 

   if event.type == pygame.KEYDOWN:
    spot = grid[0][0]

    if game == True:
        restart.toggle(False)
        draw_indicators(end.get_pos()[0], end.get_pos()[1], grid, TURQUOISE2)
        if event.key == pygame.K_w or event.key == pygame.K_UP and start != None:
            row, col = move_list[len(move_list)-1]
            if not col == 0 and not grid[row][col-1].is_barrier():
                move_list.append((row, col-1))
                if len(move_list) > 2:
                    spot = grid[row][col]
                    spot.reset()
                spot = grid[row][col-1]
                spot.make_player()
                remove_indicators(row, col, grid)
                draw_indicators(row,col-1, grid)
        if event.key == pygame.K_a  or event.key == pygame.K_LEFT and start != None:
            row, col = move_list[len(move_list)-1]
            if not row == 0 and not grid[row-1][col].is_barrier():
                move_list.append((row-1, col))
                if len(move_list) > 2:
                    spot = grid[row][col]
                    spot.reset()
                spot = grid[row-1][col]
                spot.make_player()
                remove_indicators(row, col, grid)
                draw_indicators(row-1,col, grid)
        if event.key == pygame.K_s or event.key == pygame.K_DOWN and start != None:
            row, col = move_list[len(move_list)-1]
            if not col > 48 and not grid[row][col+1].is_barrier():
                move_list.append((row, col+1))
                if len(move_list) > 2:
                    spot = grid[row][col]
                    spot.reset()
                spot = grid[row][col+1]
                spot.make_player()
                remove_indicators(row, col, grid)
                draw_indicators(row,col+1, grid)
        if event.key == pygame.K_d or event.key == pygame.K_RIGHT and start != None:
            row, col = move_list[len(move_list)-1]
            if not row > 48 and not grid[row+1][col].is_barrier():
                move_list.append((row+1, col))
                if len(move_list) > 2:
                    spot = grid[row][col]
                    spot.reset()
                spot = grid[row+1][col]
                spot.make_player()
                remove_indicators(row, col, grid)
                draw_indicators(row+1,col, grid)

    if event.key in [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT]:
     settings["open"] = False
     draw(win, grid, ROWS, WIDTH)
     if spot == end:
        game = False
        for row in grid:
         for spot in row:
          spot.update_neighbors(grid)

        algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

        xscore = fastest(grid, start, end)
        score += fastest(grid, start, end)

        for row in grid:
         for spot in row:
          spot.clear_neighbors()

    if event.key == pygame.K_ESCAPE:
        settings["open"] = not(settings["open"])
        draw(WIN, grid, ROWS, WIDTH)

  if time.time() - currtime >= 1 and game:
    time_rem -= 1
    currtime = time.time()
    draw(win, grid, ROWS, WIDTH)

  if time_rem == 0:
    game = False

    for row in grid:
      for spot in row:
       spot.update_neighbors(grid)

    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
    move_list.clear()
    xscore = h(start.get_pos(), end.get_pos())
    score += h(start.get_pos(), end.get_pos())

    time_rem = 30

  scoreRect = (725, 300)
  scoreL = font.render("{}pts".format(score), False, "red")
  WIN.blit(scoreL, scoreRect)

  if not game:
    if runNum == 0:
        scoreRect = (725, 300)
        restart.set_text("Click to Begin")
        scoreL = font.render("{}pts".format(score), False, "red")
        WIN.blit(scoreL, scoreRect)
        titleL = fontT.render("Optima", False, "red", "black")
        WIN.blit(titleL, titleRect)
    elif runNum == settings["rounds"]:
        scoreRect = (200, 300)
        restart.set_text("Play Again?")
        scoreL = font.render("You scored {} points!".format(score), False, "white", "black")
        WIN.blit(scoreL, scoreRect)
        titleL = fontT.render("Optima", False, "red", "black")
        WIN.blit(titleL, titleRect)
    else:
        restart.set_text("Next Round")      
    restart.toggle()

  deltaScore = font.render("+{}pts".format(xscore), False, "white")
  WIN.blit(deltaScore, deltaRect)
  timeL = font.render("{}s".format(time_rem), False, "white")
  WIN.blit(timeL, timeRect)
  runL = font.render("Round {}".format(runNum), False, "white")
  WIN.blit(runL, runRect)

  open_settings.toggle()

  pygame.display.flip()

 pygame.quit()

main(WIN, WIDTH, grid)