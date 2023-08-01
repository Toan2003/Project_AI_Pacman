from Graphic import *

#win = 1000
FOOD = 2
GHOST = 3
# class gameState:
#     def __init__(self, position, matrix, point) -> None:
#         self.position = position
#         self.matrix = matrix
#         self.point = point

max_depth = 3
def distanceToGhost(position,matrix):
    x,y = position
    distance = 1000
    for i in range(x-1,x+1):
        for j in range(y-1,y+1):
            if matrix[i][j] == GHOST:
                temp = abs(x-i)+abs(y-j)
                if temp < distance:
                    distance = temp
    return distance

def distanceToFood(position,matrix):
    x,y = position
    distance = 1000
    for i in range(x-1,x+1):
        for j in range(y-1,y+1):
            if matrix[i][j] == FOOD:
                temp = abs(x-i)+abs(y-j)
                if temp < distance:
                    distance = temp
    return distance


def evaluationFunction(gameState:Game):
    position = gameState.Player.currentPosition
    matrix = gameState.Matrix
    disTG = distanceToGhost((position[0],position[1]), matrix) 
    disTF = distanceToFood((position[0],position[1]), matrix) 
    # avoid cetain death
    if disTG <= 2:
        return -9999
    
    return gameState.Point* 5 - disTF


def minimax(agent, depth, gameState:Game):
 
    # if the game has finished return the value of the state
    if gameState.isLose() or gameState.isWin() or depth == max_depth:
        return evaluationFunction(gameState)
 
    # if it's the maximizer's turn (the player is the agent 0)
    if agent == 0:
        # maximize player's reward and pass the next turn to the first ghost (agent 1)
        return max(minimax(1, depth, gameState.generateSuccessor(agent, action)) for action in getLegalActionsNoStop(0, gameState))
 
    # if it's the minimizer's turn (the ghosts are the agent 1 to num_agents)
    else:
        num_agents = gameState.Ghosts.count()
        nextAgent = agent + 1  # get the index of the next agent
        if num_agents == nextAgent:  # if all agents have moved, then the next agent is the player
            nextAgent = 0
        if nextAgent == 0:  # increase depth every time all agents have moved
            depth += 1
        # minimize ghost's reward and pass the next ghost or the player if all ghosts have already moved
        return min(minimax(nextAgent, depth, gameState.generateSuccessor(agent, action)) for action in
                   getLegalActionsNoStop(agent, gameState))
