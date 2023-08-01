# symbol in matrix
GHOST = 3
FOOD = 2
PATH = 0 
BLOCK = 1
import random


def distanceToTheGhost(x,y,x_ghost,y_ghost):
    return (abs(x-x_ghost) + abs(y-y_ghost))

def distanceToTheFood(x,y,x_food,y_food):
    return (abs(x-x_food) + abs(y-y_food))

def calValue(ob, food, ghost, visitedMatrix):
    result =0 
    distanceF = 0


    if len(food) != 0:
        distanceF= distanceToTheFood(ob[0],ob[1],food[0][0],food[0][1])
        for i in range(1,len(food)):
            temp = distanceToTheFood(ob[0],ob[1],food[i][0],food[i][1])
            if distanceF > temp: 
                distanceF = temp
    # print(distanceF)
    # input(3)
    if len(ghost) != 0:
        for i in range(0,len(ghost)):
            temp = distanceToTheGhost(ob[0], ob[1], ghost[i][0],ghost[i][1])
            # if distanceG > temp:
            #     distanceG = temp
            if temp <= 2: 
            # input("here")
                return -999
    # print(distanceG)
    # input(4)

    result = -distanceF - visitedMatrix[ob[0]][ob[1]]
    return result

def randomO(list):
    x = random.randint(0,len(list)-1)
    return list[x]

def evaluateFunction(x,y,matrix, successor, old,visitedMatrix):
    n, m = len(matrix), len(matrix[0])
    result = -1
    x_top = x-3
    x_bot = x+3
    if x_top <= 0: x_top = 1
    if x_bot >= n: x_bot = n-2
    y_left = y-3
    y_right = y+3
    if y_left <= 0: y_left = 1
    if y_right >= m: y_right = m-2
    # submatrix = matrix[x_top:x_bot,y_left:y_right]
    ghost = []
    food = []
    for i in range(x_top,x_bot):
        for j in range(y_left,y_right):
            try:
                if matrix[i][j] == 3:
                    ghost.append([i,j])
                elif  matrix[i][j] == 2:
                    food.append([i,j])
            except:
                print(i,j)
                input("loi o day")
    # print(ghost)
    # input(1)
    # if len(food) == 0 and len(ghost) == 0:
    #     while True:
    #         result = randomO(successor)
    #         if compare2Position(result,old):
    #             break
    #         else:
    #             if len(successor) != 1:
    #                 successor.remove(result)
    #             break
    #     return result

    result = [x,y]
    temp = -998
    for su in successor:
        # t = compare2Position(su,old)
        # if not t:
        #     if len(successor) != 1:
        #         continue
        temp1 = calValue(su,food,ghost,visitedMatrix)
        # if temp1 == -9999:
        #     print(successor)
        #     print(su)
        #     print(calValue(su,food,ghost,visitedMatrix))
        #     input()
        # print(temp1)
        # input(2)
        if temp1 > temp:
            temp = temp1
            result = su
    # print(result)
    # input("result")
    return result

def compare2Position(pos1, pos2): #true: khác nhau, false giống nhau
    try: 
        if pos1[0] != pos2[0] or pos1[1] != pos2[1]:
            return True
    except:
        print("loi ơ đây")
        input()
    return False


def generatePossibleSuccessor(x,y, matrix):
    succesors =[]
    if matrix[x-1][y] != 1: # lên trên
        succesors.append([x-1,y])
    if matrix[x][y-1] != 1: # sang trái
        succesors.append([x,y-1])
    if matrix[x][y+1] != 1: # sang phải
        succesors.append([x,y+1])
    if matrix[x+1][y] != 1: # xuống dưới
        succesors.append([x+1,y])
    return succesors


def generateGhostMove(x,y,matrix, originalPosition):
    succesors = generatePossibleSuccessor(originalPosition[0],originalPosition[1],matrix)
    temp = [x,y]
    if not compare2Position(temp,originalPosition):
        return succesors
    else:
        return [[originalPosition[0],originalPosition[1]]]
            
def evaluateF(x,y,matrix,succesor, old):
    if len(succesor) ==1:
        return succesor[0]
    else:
        while True:
            result = randomO(succesor)
            if compare2Position(result,old):
                break
            else:
                if len(succesor) != 1:
                    succesor.remove(result)
                break
        return result 