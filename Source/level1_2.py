import queue
from collections import deque
from queue import PriorityQueue
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
    return size_x, size_y, MAP, pos, level

def detec_food(MAP,size_x,size_y):
    for i in range(size_y):
        for j in range (size_x):
            if MAP[i][j]==2:
                return (i,j)

def manhattan_dis(start_x,start_y,des_x,des_y):
    return (abs(des_x-start_x)+abs(des_x-des_y))

def level_1(MAP,pos,size_x,size_y):
    visited=[]
    path=[]
    temp_path={}
    queue=PriorityQueue()
    beg=(pos[0],pos[1])
    end=detec_food(MAP,size_x,size_y)
    queue.put((manhattan_dis(pos[0],pos[1],end[0],end[1]),beg))
    cost={}
    cost[beg]=0
    while queue!=None:
        v=queue.get()[1]
        visited.append(v)
        neighbor=[]
        if(v==end):
            path.append(v)
            while v!=beg:
                v=temp_path[v]
                path.append(v)
            path.reverse()
            return path
        if v[0]-1>=0 and MAP[v[0]-1][v[1]]!=1:
            neighbor_cur=(v[0]-1,v[1])
            neighbor.append(neighbor_cur)
        if v[0]+1<size_y-1 and MAP[v[0]+1][v[1]]!=1:
            neighbor_cur=(v[0]+1,v[1])
            neighbor.append(neighbor_cur)
        if v[1]-1>=0 and MAP[v[0]][v[1]-1]!=1:
            neighbor_cur=(v[0],v[1]-1)
            neighbor.append(neighbor_cur)
        if v[1]+1<size_x-1 and MAP[v[0]][v[1]+1]!=1:
            neighbor_cur=(v[0],v[1]+1)
            neighbor.append(neighbor_cur)
        for item in neighbor:
            if item not in visited:
                cost[item]=cost[v]+1
                queue.put((cost[item]+manhattan_dis(item[0],item[1],end[0],end[1]),item))
                temp_path[item]=v
                
def level_2(MAP,pos,size_x,size_y):
    visited=[]
    path=[]
    temp_path={}
    queue=PriorityQueue()
    beg=(pos[0],pos[1])
    end=detec_food(MAP,size_x,size_y)
    queue.put((manhattan_dis(pos[0],pos[1],end[0],end[1]),beg))
    cost={}
    cost[beg]=0
    while queue!=None:
        v=queue.get()[1]
        visited.append(v)
        neighbor=[]
        if(v==end):
            path.append(v)
            while v!=beg:
                v=temp_path[v]
                path.append(v)
            path.reverse()
            return path
        if v[0]-1>=0 and MAP[v[0]-1][v[1]]!=1 and MAP[v[0]-1][v[1]]!=3:
            neighbor_cur=(v[0]-1,v[1])
            neighbor.append(neighbor_cur)
        if v[0]+1<size_y-1 and MAP[v[0]+1][v[1]]!=1 and MAP[v[0]+1][v[1]]!=3:
            neighbor_cur=(v[0]+1,v[1])
            neighbor.append(neighbor_cur)
        if v[1]-1>=0 and MAP[v[0]][v[1]-1]!=1 and MAP[v[0]][v[1]-1]!=3:
            neighbor_cur=(v[0],v[1]-1)
            neighbor.append(neighbor_cur)
        if v[1]+1<size_x-1 and MAP[v[0]][v[1]+1]!=1 and MAP[v[0]][v[1]+1]!=3:
            neighbor_cur=(v[0],v[1]+1)
            neighbor.append(neighbor_cur)
        for item in neighbor:
            if item not in visited:
                cost[item]=cost[v]+1
                queue.put((cost[item]+manhattan_dis(item[0],item[1],end[0],end[1]),item))
                temp_path[item]=v 


#cái này để import qua file Graphic.py
def chooseLevel(level, sizeX, sizeY, MAP, posPacman):
    if level == 1:
        return level_1(MAP, posPacman, sizeX, sizeY)
    return level_2(MAP, posPacman, sizeX, sizeY)