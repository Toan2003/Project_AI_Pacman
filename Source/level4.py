import math
import copy
import pygame
#PHẦN NHẬP TỪ FILE
#----------------------------------------------------------------
def readFile(path):#'./Input/input.txt'
    global pacmanX , pacmanY
    f = open(path, 'r')

    size = [int (x) for x in f.readline().strip().split(' ')]
    Nrow = size[0]
    Ncol = size[1]

    adjacencyMatrix = []
    for i in range(Ncol):
        adjacencyMatrix.append(f.readline().rstrip('\n').split())
    
    pos = [int (x) for x in f.readline().strip().split(' ')]
    pacmanX = pos[0]
    pacmanY = pos[1]
    
    f.close()
    for x in range(len(adjacencyMatrix)):
        for y in range(len(adjacencyMatrix[x])): 
            adjacencyMatrix[x][y] = int(adjacencyMatrix[x][y])

    return adjacencyMatrix

#hàm lấy vị trí quái và số lượng thức ăn từ map
def getInfo(map):
    monsters = []
    numOfFood = 0
    for x in range(len(map)):
        for y in range(len(map[x])):
            if map[x][y] == 3:
                map[x][y] = 0
                monsters.append((x, y))
            elif map[x][y] == 2:
                numOfFood += 1
    return (monsters, numOfFood)

#PHẦN THUẬT TOÁN
#----------------------------------------------------------------
#hàm cho ma di chuyển
def monstersMove(map , monsterPos, pacman):
    if monsterPos[0] == pacman[0] and monsterPos[1] == pacman[1]:
        return (monsterPos[0], monsterPos[1])

    option = []
    #thêm các ô lân cận nếu không phải tường
    if int(map[monsterPos[0] - 1][monsterPos[1]]) != 1:
        option.append((monsterPos[0] - 1, monsterPos[1]))
    if int(map[monsterPos[0]][monsterPos[1] + 1]) != 1:
        option.append((monsterPos[0], monsterPos[1] + 1))
    if int(map[monsterPos[0] + 1][monsterPos[1]]) != 1:
        option.append((monsterPos[0] + 1, monsterPos[1]))
    if int(map[monsterPos[0]][monsterPos[1] - 1]) != 1:
        option.append((monsterPos[0], monsterPos[1] - 1))

    #nếu 4 ô lân cận đều là tường thì giữ nguyên vị trí cũ, không có đâu nhưng làm cho chắc :v
    if not option:
        return (monsterPos[0], monsterPos[1])

    distance = []
    for x in option:
        distance.append(((x[0] - pacman[0])**2 + (x[1] - pacman[1])**2))

    shortest = distance.index(min(distance))
    
    return option[shortest]
#hàm kiểm tra đụng nhau chưa
def isCollide(pacman, monsters):# hàm kiểm tra xem có va chạm với quái vật chưa
    for m in monsters:
        if m[0] == pacman[0] and m[1] == pacman[1]:
            return True
    return False
#hàm max cỉa minimax
def pacmanMove_max(map, currentPos, lastPos, monsters, numOfFood, score, trace):
    trace2 = copy.deepcopy(trace) 
    trace2.append(currentPos)#thêm vào mảng trace để trả về kết quả cuối cùng

   #nếu trong các lựa chọn để đi có đụng monster 
    if isCollide(currentPos, monsters) or len(trace) > 20:
        return (score, trace2, "collide")
    
    if map[currentPos[0]][currentPos[1]] == 2:
        numOfFood -= 1
        score += 1
        map[currentPos[0]][currentPos[1]] = 0
        return (score, trace2, "found 1 food")

    if numOfFood == 0:
        return (score, trace2, "out of food")

    option = []#các lựa chọn để đi
    #thêm các ô lân cận nếu không phải tường và quái vật
    if map[currentPos[0] - 1][currentPos[1]] != 1 and map[currentPos[0] - 1][currentPos[1]] != 3:
        option.append((currentPos[0] - 1, currentPos[1]))
    if map[currentPos[0]][currentPos[1] + 1] != 1 and map[currentPos[0]][currentPos[1] + 1] != 3:
        option.append((currentPos[0], currentPos[1] + 1))
    if map[currentPos[0] + 1][currentPos[1]] != 1 and map[currentPos[0] + 1][currentPos[1]] != 3:
        option.append((currentPos[0] + 1, currentPos[1]))
    if map[currentPos[0]][currentPos[1] - 1] != 1 and map[currentPos[0]][currentPos[1] - 1] != 3:
        option.append((currentPos[0], currentPos[1] - 1))

    for m in monsters:
        for i in option:
            if i[0] == m[0] and i[1] == m[1]:
                option.pop(option.index(i))

    if not option:
        return (score, trace2, "no option")
    else:
        for i in option:
            if i == lastPos:
                option.pop(option.index(i))

    #trả về option đi để có điểm lớn nhất
    result = (-math.inf, [])
    for x in option:
        output = pacmanMove_min(copy.deepcopy(map), x, currentPos, copy.deepcopy(monsters), numOfFood,score, trace2)
        if output[0] > result[0]:
            result = output
        elif output[0] == result[0] and len(output[1]) < len(result[1]):
            result = output
   
    return result    
#hàm min của minimax
def pacmanMove_min(map, currentPos, lastPos, monsters, numOfFood, score, trace): 
    trace2 = copy.deepcopy(trace)

    for i in range(len(monsters)):#cập nhật lại vị trí mới của quái vật trong mảng monster
        monsters[i] = monstersMove(map, monsters[i], currentPos)
  
    result = pacmanMove_max(copy.deepcopy(map), currentPos, lastPos, copy.deepcopy(monsters), numOfFood, score, trace2)
    return result

#hàm level 4, chỉ càn gọi hàm này là được
def level4(map, numOfFood, monsters, pacman):
    map_copy = copy.deepcopy(map)
    monstersPos = copy.deepcopy(monsters)#không làm ảnh hưởng mảng gốc

    #khởi tạo mảng để lưu bước đi của monster
    monstersMoveList = []
    if monsters:
        for i in range(len(monsters)):
            monstersMoveList.append([])
            monstersMoveList[i].append(monsters[i])
    pacmanMoveList = [pacman]
    numEaten = 0
    while numOfFood > 0:
        output = pacmanMove_max(map_copy, pacmanMoveList[-1], pacmanMoveList[-1], monstersPos, numOfFood, 0, [])

        # print(len(output[1]), output[1], output[2])
        
        if not output[1]:
            print("stop by break")
            break

        numOfFood -= output[0]
        
        numEaten += output[0]
        
        temp = output[1].pop(0)
        pacmanMoveList = pacmanMoveList + output[1]
        for p in output[1]:
            for m in range(len(monstersMoveList)):
                monstersMoveList[m].append(monstersMove(map, monstersMoveList[m][-1], p))
        for y in range(len(monstersMoveList)):
            monstersPos[y] = monstersMoveList[y][-1]
    
        map_copy = copy.deepcopy(map)
        for x in pacmanMoveList:
            map_copy[x[0]][x[1]] = 0
        
        if output[2] == "collide": 
            break

        if output[2] == "no option":
            pacmanMoveList = pacmanMoveList + [temp]
            for m in range(len(monstersMoveList)):
                monstersMoveList[m].append(monstersMove(map, monstersMoveList[m][-1], temp))
            break
    
    return (numEaten, pacmanMoveList, monstersMoveList, output[2])
