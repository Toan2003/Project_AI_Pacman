import pygame
import sys
import time
import copy 
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

#move
LEFT = 3
RIGHT = 4 
UP = 5
DOWN = 6
STAY = 7

def initGameScreen():
    pygame.init()
    pygame.display.set_caption(GAME_NAME)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(BLACK)
    clock = pygame.time.Clock()
    return screen, clock

def handle_input():
    level = int(input("Enter the level (1, 2, 3, 4): "))
    if level == 1:
        map_name = "map1.txt"
    elif level == 2:
        map_name = "map2.txt"
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

SCREEN_HEIGHT = (m+2)*one_block_size
SCREEN_WIDTH = n*one_block_size
screen, clock = initGameScreen()

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


class Ghost(sprite):
    def __init__(self, position) -> None:
        super().__init__(position)
        pygame.draw.circle(self.surface, GHOST_COLOR,((one_block_size)/2,(one_block_size)/2), one_block_size / 2, 0)

        

class Pacman(sprite):
    DEAD = False
    def __init__(self, position) -> None:
        super().__init__(position)
        pygame.draw.circle(self.surface, PACMAN_COLOR,((one_block_size)/2,(one_block_size)/2), one_block_size / 2, 0)

    
class Food(sprite):
    def __init__(self, position) -> None:
        super().__init__(position)
        pygame.draw.circle(self.surface, FOODS_COLOR,((one_block_size)/2,(one_block_size)/2), one_block_size / 4, 0)



def makeSubGame(matrix, pacman):
    return Game(matrix,pacman)

class Object:
    def __init__(self,object) -> None:
        self.currentPosition = copy.deepcopy(object.currentPosition)



class GameState:
    def __init__(self, player, ghosts, foods, matrix, point, action) -> None:
        self.Player = Object(player)
        self.Ghosts = [Object(obj) for obj in ghosts ]
        self.Foods = [Object(obj) for obj in foods ]
        self.Matrix = matrix
        self.Point = point
        self.generateSuccessor(0, action)

    def checkGameFinish(self):
        isFinish = False
        # if self.Player.DEAD:
        #     isFinish = True
        #     return isFinish, LOSE
        if len(self.Foods) == 0:
            isFinish = True
            return isFinish, WIN
        return isFinish, CONTINUE
    def generateSuccessor(self, agent, action):
        subState = GameState(self.Player,self.Ghosts,self.Foods,self.Matrix,self.Point)
        if agent == 0: #pacman
            if action == LEFT:
                subState.Player.currentPosition[1] -= 1
            if action == RIGHT:
                subState.Player.currentPosition[1] += 1
            if action == DOWN:
                subState.Player.currentPosition[0] += 1
            elif action == UP:
                subState.Player.currentPosition[0] -= 1
        else:
            if action == LEFT:
                subState.Ghosts[agent-2].currentPosition[1] -= 1
            elif action == RIGHT:
                subState.Ghosts[agent-2].currentPosition[1] += 1
            elif action == DOWN:
                subState.Ghosts[agent-2].currentPosition[0] -= 1
            elif action == UP:
                subState.Ghosts[agent-2].currentPosition[0] += 1
        return 
    
class Game:
    Point = 0
    def __init__(self,Matrix,pacman) -> None:
        self.Player = Pacman(pacman)
        self.Matrix = Matrix
        self.Foods = []
        self.Ghosts = []
        self.Walls = []
        for row in range(len(Matrix)):
            for column in range(len(Matrix[row])):
                if Matrix[row][column] == 1:
                    temp = Wall([row,column])
                    self.Walls.append(temp)
                elif Matrix[row][column] == 2:
                    temp = Food([row,column])
                    self.Foods.append(temp)
                elif Matrix[row][column] == 3:
                    temp = Ghost([row,column])
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

    def generateSuccessor(self, agent, action):
        subGame = -1
        if agent == 0: #pacman
            # print(len(self.Ghosts))
            # input("generate1")
            player =  copy.deepcopy(self.Player.currentPosition)
            # print(player, self.Player.currentPosition)
            matrix = copy.deepcopy(self.Matrix)
            # print(matrix)
            if action == STAY:
                subGame = Game(matrix,player)
                # input('test')
            elif action == LEFT:
                player[1] -= 1
                subGame = Game(matrix,player)
            elif action == RIGHT:
                player[1] += 1
                subGame = Game(matrix, player)
            elif action == DOWN:
                player[0] += 1
                subGame = Game(matrix, player)
            elif action == UP:
                player[0] -= 1
                subGame = Game(matrix, player)
        else:
            player =  copy.deepcopy(self.Player.currentPosition)
            # print(len(self.Ghosts))
            # input("generate")
            ghost = copy.deepcopy(self.Ghosts[agent-2].currentPosition)
            matrix = copy.deepcopy(self.Matrix)
            if action == STAY:
                subGame = Game(matrix, player)
            elif action == LEFT:
                matrix[ghost[0]][ghost[1]] = 0
                matrix[ghost[0]][ghost[1]-1] = 3
                subGame = Game(matrix,player)
            elif action == RIGHT:
                matrix[ghost[0]][ghost[1]] = 0
                matrix[ghost[0]][ghost[1]+1] = 3
                subGame = Game(matrix, player)
            elif action == DOWN:
                matrix[ghost[0]][ghost[1]] = 0
                matrix[ghost[0]+1][ghost[1]] = 3
                subGame = Game(matrix, player)
            elif action == UP:
                matrix[ghost[0]][ghost[1]] = 0
                matrix[ghost[0]-1][ghost[1]] = 3
                subGame = Game(matrix, player)
        return subGame
    
    def ghostMove(self, newPosition):
        for ghost in self.Ghosts:
            # position = functionn to move
            newPosition = (-1,1)
            Ghost(ghost).chanePosition(newPosition)

        self.Player.DEAD, ghostIndex = self.checkColision()

    def pacmanMove(self, position):
        # position = functionn to move
        newPosition = position
        self.Player.chanePosition(newPosition)


        isPacmanEatFood, foodIndex = self.checkEatFood()
        if isPacmanEatFood:
            self.Point += 5
            self.Foods.pop(foodIndex)
        
        self.Point -= 1

    def pacmanMoveDirection(self,direction):

        newPosition = self.Player.currentPosition
        if direction == RIGHT:
            newPosition[1] += 1
        elif direction == LEFT:
            newPosition[1] -= 1
        elif direction == UP:
            newPosition[0] -= 1
        elif direction == DOWN:
            newPosition[0] += 1

        self.Player.chanePosition(newPosition)

        isPacmanEatFood, foodIndex = self.checkEatFood()
        if isPacmanEatFood:
            self.Point += 5
            self.Matrix[self.Foods[foodIndex].currentPosition[0]][self.Foods[foodIndex].currentPosition[1]] = 0
            self.Foods.pop(foodIndex)
        self.Point -= 1

    def GhostMoveDirection(self,indexOfGhost, direction):

        newPosition = self.Ghosts[indexOfGhost].currentPosition
        if direction == RIGHT:
            newPosition[1] += 1
        elif direction == LEFT:
            newPosition[1] -= 1
        elif direction == UP:
            newPosition[0] -= 1
        elif direction == DOWN:
            newPosition[0] += 1

        self.Player.DEAD, ghostIndex = self.checkColision()

    def checkColision(self):
        for ghost in self.Ghosts:
            if ghost.currentPosition == self.Player.currentPosition:
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

def getLegalActionsNoStop(agent, gameState):
    action = []
    if agent ==0:
        position = gameState.Player.currentPosition
    else:
        position = gameState.Ghosts[agent-2].currentPosition
    x,y = position[0], position[1]
    try:
        if gameState.Matrix[x+1][y] != 1:
            action.append(DOWN)
        if gameState.Matrix[x-1][y] != 1:
            action.append(UP)
        if gameState.Matrix[x][y-1] != 1:
            action.append(LEFT)
        if gameState.Matrix[x][y+1] != 1:
            action.append(RIGHT)
        action.append(STAY)
    except:
        for j in gameState.Ghosts:
            print(j.currentPosition)
        print(agent, x)
        input()
    return action

#------------------------
#win = 1000
FOOD = 2
GHOST = 3
# class gameState:
#     def __init__(self, position, matrix, point) -> None:
#         self.position = position
#         self.matrix = matrix
#         self.point = point

max_depth = 3
def distanceToNearestGhost(pacman, ghosts):
    x1, y1 = pacman[0], pacman[1]
    distance =1000
    for ghost in ghosts:
        x, y = ghost.currentPosition[0],ghost.currentPosition[1]
        temp = abs(x1-x) + abs(y1-y)
        if distance > temp:
            distance = temp
    return distance

def distanceToNearestFood(pacman, foods):
    x1, y1 = pacman[0], pacman[1]
    distance =1000
    for food in foods:
        x, y = food.currentPosition[0],food.currentPosition[1]
        temp = abs(x1-x) + abs(y1-y)
        if distance > temp:
            distance = temp

    return distance


def evaluationFunction(gameState):
    disTF = distanceToNearestFood(gameState.Player.currentPosition,gameState.Foods)
    disTG = distanceToNearestGhost(gameState.Player.currentPosition, gameState.Ghosts)
    # avoid cetain death
    if disTG <= 2:
        return -9999
    
    return gameState.Point* 5 - disTF


def minimax(agent, depth, gameState):
 
    # if the game has finished return the value of the state
    isFinish, sth = gameState.checkGameFinish()
    if isFinish or depth == max_depth:
        return evaluationFunction(gameState)
 
    # if it's the maximizer's turn (the player is the agent 0)
    if agent == 0:
        # maximize player's reward and pass the next turn to the first ghost (agent 1)
        return max(minimax(1, depth, gameState.generateSuccessor(agent, action)) for action in 
                   getLegalActionsNoStop(0, gameState))
 
    # if it's the minimizer's turn (the ghosts are the agent 1 to num_agents)
    else:
        num_agents = len(gameState.Ghosts) + 2
        # print(num_agents)
        # input('min here') 
        nextAgent = agent + 1  # get the index of the next agent
        if num_agents == nextAgent:  # if all agents have moved, then the next agent is the player
            nextAgent = 0
        if nextAgent == 0:  # increase depth every time all agents have moved
            depth += 1
        # minimize ghost's reward and pass the next ghost or the player if all ghosts have already moved
        return min(minimax(nextAgent, depth, gameState.generateSuccessor(agent, action)) for action in
                   getLegalActionsNoStop(agent, gameState))

#------------------------

# vòng lặp là:
#     while true:
#         xóa màn hình vị trí pacman và ghost
#         Pacman di chuyển -> kiểm tra ăn được thức ăn ko, kiểm tra có ăn ma không
#         Ghost di chuyển -> kiểm tra có ăn được pacman ko
#         Vẽ Pacman và Ghost
#         checkFinish dừng vòng lặp


game = Game(matrix,pacman)
game.Player.draw()

for i in game.Walls:
    i.draw()
for i in game.Foods:
    i.draw()
# print(matrix, pacman, n, m)
# input()
# temp = Wall((0,0))
idx = 0
pygame.display.update()
while True:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            pygame.quit()
            sys.exit(0)

    game.clearAnimation()
    #pacman move
    actions = getLegalActionsNoStop(0,game)
    choice = -1
    temp = -9999999
    # if (idx == 4):
    #     print(actions)
    for i in actions:
        if i == LEFT:
            left = minimax(0,0,GameState(game.Player, game.Ghosts,game.Foods,game.Matrix,game.Point, LEFT))
            # if (idx >=4):
            #     print("left" , left)
            if temp < left:
                temp = left
                choice = LEFT
        elif i == RIGHT:
            right = minimax(0,1,GameState(game.Player, game.Ghosts,game.Foods,game.Matrix,game.Point, RIGHT))
            # if (idx >= 4):
            #     print("right" , right)
            if temp < right:
                temp = right
                choice = RIGHT
        elif i == DOWN:
            down = minimax(0,1,GameState(game.Player, game.Ghosts,game.Foods,game.Matrix,game.Point, DOWN))
            if temp < down:
                temp = down
                choice = DOWN
        elif i == UP:
            up = minimax(0,1,GameState(game.Player, game.Ghosts,game.Foods,game.Matrix,game.Point, UP))
            if temp < up:
                temp = up
                choice = UP
        # elif i == STAY:
        #     stay = minimax(0,2,game.generateSuccessor(0, STAY))
        #     if temp < stay:
        #         temp = stay
        #         choice = STAY
    # print(choice)
    # print(game.Player.currentPosition)
    # input("đi lần ")
    game.pacmanMoveDirection(choice)
    # print(game.Player.currentPosition)
    #pacman move done
    for j in range(2,len(game.Ghosts)+2):
        actions = getLegalActionsNoStop(j,game)
        choice = -1
        temp = 9999999
        for i in actions:
            if i == LEFT:
                left = minimax(j,1,GameState(game.Player, game.Ghosts,game.Foods,game.Matrix,game.Point, LEFT))
                if temp > left:
                    temp = left
                    choice = LEFT
            elif i == RIGHT:
                right = minimax(j,1,GameState(game.Player, game.Ghosts,game.Foods,game.Matrix,game.Point, RIGHT))
                if temp > right:
                    temp = right
                    choice = RIGHT
            elif i == DOWN:
                down = minimax(j,1,GameState(game.Player, game.Ghosts,game.Foods,game.Matrix,game.Point, DOWN))
                if temp > down:
                    temp = down
                    choice = DOWN
            elif i == UP:
                up = minimax(j,1,GameState(game.Player, game.Ghosts,game.Foods,game.Matrix,game.Point, UP))
                if temp > up:
                    temp = up
                    choice = UP
        game.GhostMoveDirection(j-2,choice)

    game.Player.draw()
    for i in game.Ghosts:
        print(i.currentPosition)
        i.draw()
    time.sleep(1)
    idx+=1
    pygame.display.update()
    clock.tick(30)

    # #pacman move
    # actions = getLegalActionsNoStop(0,game)
    # path = []
    # choice = -1
    # temp = -9999999
    # for i in actions:
    #     if i == STAY:
    #         stay = minimax(0,1,game.generateSuccessor(0, STAY))
    #         if temp < stay:
    #             temp = stay
    #             choice = STAY
    #     elif i == DOWN:
    #         down = minimax(0,1,game.generateSuccessor(0, DOWN))
    #         if temp < down:
    #             temp = down
    #             choice = DOWN
    #     elif i == LEFT:
    #         left = minimax(0,1,game.generateSuccessor(0, LEFT))
    #         if temp < left:
    #             temp = left
    #             choice = LEFT
    #     elif i == RIGHT:
    #         right = minimax(0,1,game.generateSuccessor(0, RIGHT))
    #         if temp < right:
    #             temp = right
    #             choice = RIGHT
    # game.pacmanMoveDirection(choice)
    # #pacman move done
