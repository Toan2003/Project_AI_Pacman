import pygame
import sys
import copy
import time 
from level1_2 import chooseLevel
from level3 import ingame, plusPadding, inputMaze
from level4 import readFile, getInfo, level4

#SET SIZE
one_block_size = 30 #pixel
SCREEN_HEIGHT = 20 * one_block_size
SCREEN_WIDTH = SCREEN_HEIGHT * 2

#SOME VARIABLE 
GAME_NAME = 'Pacman'
FPS = 30
running = True

#SET COLORS
WALL_COLOR = (3, 64, 214)
GHOST_COLOR = (255, 0, 0) #red
PACMAN_COLOR = (255,255,0)
FOODS_COLOR = (255, 255, 255)
BLACK = (0, 0, 0)

#CheckFinish
WIN = 0
LOSE = 1
CONTINUE = 2

def initGameScreen():
    pygame.init()
    pygame.display.set_caption(GAME_NAME)
    pygame.font.init()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(BLACK)
    clock = pygame.time.Clock()
    
    return screen, clock

class sprite:
    def __init__(self,position) -> None:
        self.currentPosition = position
        self.surface = pygame.Surface((one_block_size,one_block_size))
        self.surface.fill(BLACK)
    def changePosition(self, newPosition):
        self.currentPosition = newPosition
    def draw(self):
        screen.blit(self.surface, (self.currentPosition[1]*one_block_size, self.currentPosition[0]*one_block_size))

class Wall(sprite):
    def __init__(self, position) -> None:
        super().__init__(position)
        pygame.draw.rect(self.surface, WALL_COLOR ,(0,0,30,30), 2)
        self.draw()

class Ghost(sprite):
    def __init__(self, position) -> None:
        super().__init__(position)
        pygame.draw.circle(self.surface, GHOST_COLOR,((one_block_size)/2,(one_block_size)/2), one_block_size / 2, 0)
        self.draw()
        

class Pacman(sprite):
    DEAD = False
    def __init__(self, position) -> None:
        super().__init__(position)
        pygame.draw.circle(self.surface, PACMAN_COLOR,((one_block_size)/2,(one_block_size)/2), one_block_size / 2, 0)
        self.draw()
    
class Food(sprite):
    def __init__(self, position) -> None:
        super().__init__(position)
        pygame.draw.circle(self.surface, FOODS_COLOR,((one_block_size)/2,(one_block_size)/2), one_block_size / 4, 0)
        self.draw()

class Game:
    Foods = []
    Ghosts = []
    Player = -1
    Point = 0
    def __init__(self,Matrix,pacman) -> None:
        self.Player = Pacman(pacman)
        for row in range(len(Matrix)):
            for column in range(len(Matrix[row])):
                if Matrix[row][column] == 1:
                    temp = Wall((row,column))
                elif Matrix[row][column] == 2:
                    temp = Food((row,column))
                    self.Foods.append(temp)
                elif Matrix[row][column] == 3:
                    temp = Ghost((row,column))
                    self.Ghosts.append(temp)

    def checkGameFinish(self):
        isFinish = False
        if self.Player.DEAD:
            isFinish = True
            return isFinish, LOSE
        if len(self.Foods) == 0:
            isFinish = True
            return isFinish, WIN
        return isFinish, CONTINUE
        

    def ghostMove(self, position, idx):
        # position = functionn to move
        # print(position)
        # input(222)
        # newPosition = position
        self.Ghosts[idx].changePosition(position)

        # self.Player.DEAD = self.checkColision()
        # self.checkGameFinish()
        # self.Player.currentPosition(-1,-1)
        

    def pacmanMove(self, position):
        # position = functionn to move
        newPosition = position

        self.Player.changePosition(newPosition)

        # isPacmanEatGhost, ghostIndex = self.checkColision()
        # if isPacmanEatGhost:
        #     self.Ghosts.pop(ghostIndex)

        # isPacmanDead = self.checkColision()
        # if isPacmanDead:
        #     self.Player.DEAD = True
        #     self.checkGameFinish()

        isPacmanEatFood, foodIndex = self.checkEatFood()
        if isPacmanEatFood:
            self.Point += 20
            # self.Matrix[self.Foods[foodIndex].currentPosition[0]][self.Foods[foodIndex].currentPosition[1]] = 0
            self.Foods.pop(foodIndex)
        
        self.Point -= 1

    def checkColision(self):
        # for ghost in self.Ghosts:
        #     if ghost.currentPosition == self.Player.currentPosition:
        #         return True, self.Ghosts.index(ghost)
        # return False, -1
        for ghost in self.Ghosts:
            if ghost.currentPosition[0] == self.Player.currentPosition[0] and ghost.currentPosition[1] == self.Player.currentPosition[1]:
                return True
        return False
    
    def checkEatFood(self):
        for food in self.Foods:
            if food.currentPosition[0] == self.Player.currentPosition[0] and food.currentPosition[1] == self.Player.currentPosition[1]:
                return True, self.Foods.index(food)
        return False, -1
    
    def clearAnimation(self):
        temp = sprite(self.Player.currentPosition)
        temp.draw()
        for ghost in self.Ghosts:
            temp.currentPosition = ghost.currentPosition
            temp.draw()

# vòng lặp là:
#     while true:
#         xóa màn hình vị trí pacman và ghost
#         Pacman di chuyển -> kiểm tra ăn được thức ăn ko, kiểm tra có ăn ma không
#         Ghost di chuyển -> kiểm tra có ăn được pacman ko
#         Vẽ Pacman và Ghost
#         checkFinish dừng vòng lặp

def drawScore():
    text_font = pygame.font.SysFont("Arial", 36)
    surface = pygame.Surface((10*one_block_size,2*one_block_size))
    surface.fill(BLACK)
    screen.blit(surface,((3*one_block_size, m*one_block_size)))
    score = text_font.render(f'Score: {game.Point}', True, (255, 255, 255))
    screen.blit(score, (one_block_size, m*one_block_size))

def handle_input():
    level = int(input("Enter the level (1, 2, 3, 4): "))
    map_name = input("Enter map name: ")
    map_name = '../Input/' + map_name
    if level not in [1, 2, 3, 4]:
        return None, None, None, None
    
    file = open (map_name, 'r') 
        #count number of line
    cnt_line = len(file.readlines())
    file.close()

    file = open(map_name, 'r')
    MAP = []
    idx = 0
    for line in file:
        if idx == 0:
            size = line.split()
        elif idx == cnt_line - 1:
            position = line.split()
        else:
            MAP.append([int(x) for x in line.split()])
        idx += 1
    file.close()
    
    size_x = int(size[0])
    size_y = int(size[1])

    x = int(position[0])
    y = int(position[1])
    pos = [x, y]

    return size_x, size_y, MAP, pos, level, map_name #map_name này cho level 3 của Phát
    
def menu():
    n, m, matrix, pacman, level, map_name = handle_input()
    path_ghost = None
    point = 0
    if level == 1 or level == 2:
        #cái này chỉ để lấy path thôi
        path = chooseLevel(level, n, m, matrix, pacman)
    elif level == 3:
        #cái này là làm theo cách chạy hàm của Hòa
        currghost,initialghost = [],[]
        food = 0
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == 3:
                    currghost.append([i+2,j+2])
                    initialghost.append([i+2,j+2])
                if matrix[i][j] == 2:
                    food+=1
        pacman[0] +=2
        pacman[1] +=2
        # print(pacman)
        # print(food)
        # print(currghost)
        # input("test")
        board=plusPadding(copy.deepcopy(matrix))                        #tạo padding 
        # print(board)
        # input(board)
        actionsPacman,path_ghost=ingame(pacman, board, currghost,initialghost,food)
        path = []
        for item in actionsPacman:
            temp = []
            for coor in item:
                temp.append(coor - 2)
            path.append(temp)
        for i in range(len(path_ghost)): 
            for j in range(len(path_ghost[i])):
                path_ghost[i][j][0] -=2
                path_ghost[i][j][1] -=2
        pacman[0] -=2
        pacman[1] -=2
    elif level == 4:
        #cái này là làm theo cách chạy hàm của Phát
        path_file =  str(map_name)
        map = readFile(path_file)
        inf = getInfo(map)
        output = level4(map, inf[1], inf[0], pacman)
        point = output[0]
        path = output[1]
        path_ghost = output[2]
    #Trả về kích thước x, y, vị trí pacman, điểm, path_ghost, level
    return n, m, matrix, pacman, point, path, path_ghost, level

def drawFinish(state): 
    text_font = pygame.font.SysFont("Arial", 36)
    if state == WIN:
        text = text_font.render("WIN", True, PACMAN_COLOR)
    else:
        text = text_font.render("LOSE", True, GHOST_COLOR)

    screen.blit(text, ((n/2 - 1)*one_block_size, m*one_block_size))
    
if __name__ == "__main__":
    n, m, matrix, pacman, point, path, path_ghost, level = menu()
    
    SCREEN_HEIGHT = (m + 2)*one_block_size
    SCREEN_WIDTH = n*one_block_size
    screen, clock = initGameScreen()
    game = Game(matrix,pacman)
    game.Player.draw()
    drawScore()
    pygame.display.update()
    ghostmove = 0
    idx = 0
    while True:
        # print("pacmanPosiiton")
        # print(game.Player.currentPosition)
        # print("GhostPoisition")
        # for ghost in game.Ghosts:
        #     print(ghost.currentPosition)
        # input("vongn")
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                sys.exit(0)
        for food in game.Foods:
            food.draw()  
        game.clearAnimation()
        game.pacmanMove(path[idx])
        game.Player.draw()

        game.Player.DEAD = game.checkColision()
        if game.checkColision():
            for ghost in game.Ghosts:
                ghost.draw()  
            break
        # #level để kiểm tra xem có vẽ ma hay không
        if level == 2:
            for ghost in game.Ghosts:
                ghost.draw()
        elif level == 4:
            for path_idx in range(len(game.Ghosts)):
                path_ = path_ghost[path_idx]
                game.ghostMove(path_[idx], path_idx)
                game.Ghosts[path_idx].draw()
        elif level == 3:
            for path_idx in range(len(game.Ghosts)):
                game.ghostMove(path_ghost[ghostmove][path_idx], path_idx)
                game.Ghosts[path_idx].draw()
            ghostmove += 1
        
            # print(gsm])
            # print(pacman)
            # input(1)
        
        game.Player.DEAD = game.checkColision()
        if game.checkColision():
            print(game.Player.DEAD)
            break
            
        drawScore()

        pygame.display.update()
        idx += 1

        if (idx == len(path)):
            game.Player.DEAD = game.checkColision()
            isFinsihed , state = game.checkGameFinish()
            break
                
        isFinsihed , state = game.checkGameFinish()
        if isFinsihed == True:
            break
        time.sleep(0.1)        
        clock.tick(30)

    
    drawFinish(state)
    pygame.display.update()
    time.sleep(5)
    # print(isFinsihed, state)

