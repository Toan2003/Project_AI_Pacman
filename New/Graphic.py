import pygame
import sys
import numpy as np
#SET SIZE
one_block_size = 30 #pixel
# Default screen size
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
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(BLACK)
    clock = pygame.time.Clock()
    return screen, clock

class sprite:
    def __init__(self,position) -> None:
        self.currentPosition = position
        self.surface = pygame.Surface((one_block_size,one_block_size))
        self.surface.fill(BLACK)
    def chanePosition(self, newPosition):
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
        self.Matrix = Matrix
        self.visitedMatrix = np.zeros((len(Matrix),len(Matrix[0])),int)
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
        
    def ghostMove(self):
        for ghost in self.Ghosts:
            # position = functionn to move
            newPosition = (-1,1)
            Ghost(ghost).chanePosition(newPosition)

        self.Player.DEAD, ghostIndex = self.checkColision()
        self.Player.currentPosition(-1,-1)

    def pacmanMove(self, newPosition):
        # position = functionn to move
        self.Player.chanePosition(newPosition)

        isPacmanEatFood, foodIndex = self.checkEatFood()
        if isPacmanEatFood:
            self.Point += 5
            self.Matrix[self.Foods[foodIndex].currentPosition[0]][self.Foods[foodIndex].currentPosition[1]] = 0
            self.Foods.pop(foodIndex)
        
        self.Point -= 1

    def checkColision(self):
        for ghost in self.Ghosts:
            if ghost.currentPosition[0] == self.Player.currentPosition[0] and ghost.currentPosition[1] == self.Player.currentPosition[1]:
                return True, self.Ghosts.index(ghost)
        return False, -1
    
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
     
    def level3(self):
        ghost_original_position = []
        for ghost in self.Ghosts:
            ghost_original_position.append(ghost.currentPosition)
        return ghost_original_position
# vòng lặp là:
#     while true:
#         xóa màn hình vị trí pacman và ghost
#         Pacman di chuyển -> kiểm tra ăn được thức ăn ko, kiểm tra có ăn ma không
#         Ghost di chuyển -> kiểm tra có ăn được pacman ko
#         Vẽ Pacman và Ghost
#         checkFinish dừng vòng lặp

#n, m, matrix, []
def handle_input():
    level = int(input("Enter the level (1, 2, 3, 4): "))
    if level == 1:
        map_name = "map1.txt"
    elif level == 2:
        map_name == "map2.txt"
    elif level == 3:
        map_name = "map3.txt"
    else:
        map_name = "map4.txt"

    if level not in [1, 2, 3, 4]:
        return None, None, None, None
    
    with open (map_name, 'r') as file:
        #count number of line
        cnt_line = len(file.readlines())
        file.close()

    with open(map_name, 'r') as file:
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

    return size_x, size_y, MAP, pos 

n,m,matrix, pacman = handle_input()

SCREEN_HEIGHT = m*one_block_size
SCREEN_WIDTH = n*one_block_size

screen, clock = initGameScreen()