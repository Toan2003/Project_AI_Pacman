import random
import time
import re
import math
import copy
def inputMaze(filename):
    f=open(filename, mode='r')
    content=f.readline()
    size=re.findall(r'\d+',content)
    n=int(size[0])
    m=int(size[1])
    # print(n,m)
    maze=[]
    for i in range(0,m):
        content=f.readline()
        arrNum=re.findall(r'\d+',content)
        llen=len(arrNum)
        for j in range(0,llen):
            arrNum[j]=int(arrNum[j])
        maze.append(arrNum)
    content=f.readline()
    size=re.findall(r'\d+',content)
    initialX=int(size[0])
    initialY=int(size[1])
    return maze, initialX, initialY ,m,n  

def plusPadding(maze):
    temp=[]
    for i in range (0,36):
        temp.append(1)
    for i in range (0,11):
        maze[i].append(1)
        maze[i].append(1)
        maze[i].insert(0,1)
        maze[i].insert(0,1)
    maze.append(temp)
    maze.append(temp)
    maze.insert(0,temp)
    maze.insert(0,temp)
    return maze
def createNewBoard(board, pacman):
    tileFull=[]
    x=pacman[0]
    y=pacman[1]
    for i in range (-3,4):
        tilePacman=[[x+i,y-3],[x+i,y-2],[x+i,y-1],[x+i,y],[x+i,y+1],[x+i,y+2],[x+i,y+3]]
        tileFull.append(tilePacman)
    return tileFull

#def heuristicValue(tilePacman,maze, direction):
    #tinh nua tren
    # heuristicUp=10000
    # heuristicDown=10000
    # heuristicLeft=10000
    # heuristicRight=10000
    # # print(tilePacman)
    # for k in range (0,len(direction)):
    #     if(direction[k]=="tren"):
    #         heuristicUp=0
    #         for i in range (0,3):
    #             for j in range (0,7):
    #                 x=tilePacman[i][j][0]
    #                 y=tilePacman[i][j][1]
    #                 if(maze[x][y]==2):
    #                     if (i==0):
    #                         heuristicUp+=5
    #                     elif (i==1):
    #                         heuristicUp+=10
    #                     elif (i==2):
    #                         heuristicUp+=35
    #                 elif (maze[x][y]==3):
    #                     if (i==0):
    #                         heuristicUp-=10
    #                     elif (i==1):
    #                         heuristicUp=-math.inf
    #                     elif (i==2):
    #                         heuristicUp=-math.inf
    #     elif (direction[k]=="duoi"):
    #         heuristicDown=0
    #         for i in range (4,7):
    #             for j in range (0,7):
    #                 x=tilePacman[i][j][0]
    #                 y=tilePacman[i][j][1]
    #                 if(maze[x][y]==2):
    #                     if (i==6):
    #                         heuristicDown+=5
    #                     elif (i==5):
    #                         heuristicDown+=10
    #                     elif (i==4):
    #                         heuristicDown+=35
    #                 elif (maze[x][y]==3):
    #                     if (i==6):
    #                         heuristicDown-=10
    #                     elif (i==5):
    #                         heuristicDown=-math.inf
    #                     elif (i==4):
    #                         heuristicDown=-math.inf
    #     elif(direction[k]=="trai"):
    #         heuristicLeft=0
    #         for i in range (0,7):
    #             for j in range (0,3):
    #                 x=tilePacman[i][j][0]
    #                 y=tilePacman[i][j][1]
    #                 if(maze[x][y]==2):
    #                     if (j==0):
    #                         heuristicLeft+=5
    #                     elif (j==1):
    #                         heuristicLeft+=10
    #                     elif (j==2):
    #                         heuristicLeft+=35
    #                 elif (maze[x][y]==3):
    #                     if (j==0):
    #                         heuristicLeft-=10
    #                     elif (j==1):
    #                         heuristicLeft=-math.inf
    #                     elif (j==2):
    #                         heuristicLeft=-math.inf
    #     elif (direction[k]=="phai"):
    #         heuristicRight=0
    #         for i in range (0,7):
    #             for j in range (4,7):
    #                 x=tilePacman[i][j][0]
    #                 y=tilePacman[i][j][1]
                    
    #                 if(maze[x][y]==2):
    #                     # print("hhhh")
    #                     if (j==6):
    #                         #print("gggg")
    #                         heuristicRight+=5
    #                     elif (j==5):
    #                         heuristicRight+=10
    #                     elif (j==4):
    #                         heuristicRight+=35
    #                 elif (maze[x][y]==3):
    #                     if (j==6):
    #                         heuristicRight-=10
    #                     elif (j==5):
    #                         heuristicRight=-math.inf
    #                     elif (j==4):
    #                         heuristicRight=-math.inf
    # return heuristicUp, heuristicDown, heuristicLeft, heuristicRight


def heurisicValue(tilePacman, board, direction):
    heuristicVal=[]
    for i in range (0, len(direction)):
        heuristic=0
        if(direction[i]=="tren"):
            for k in range (2,5):
                x=tilePacman[2][k][0]
                y=tilePacman[2][k][1]
                if (board[x][y]==2):
                    heuristic+=35
                elif (board[x][y]==3):
                    heuristic=-math.inf
            for k in range (1,6):
                x=tilePacman[1][k][0]
                y=tilePacman[1][k][1]
                if (board[x][y]==2):
                    heuristic+=10
                elif (board[x][y]==3):
                    if(k==3):
                        heuristic=-math.inf
                    else: 
                        # print("sssss")
                        heuristic-=50
            for k in range (0,7):
                x=tilePacman[0][k][0]
                y=tilePacman[0][k][1]
                if (board[x][y]==2):
                    heuristic+=5
                elif (board[x][y]==3):
                    heuristic-=100
        elif (direction[i]=="duoi"):
            for k in range (2,5):
                x=tilePacman[4][k][0]
                y=tilePacman[4][k][1]
                if (board[x][y]==2):
                    heuristic+=35
                elif (board[x][y]==3):
                    heuristic=-math.inf
            for k in range (1,6):
                x=tilePacman[5][k][0]
                y=tilePacman[5][k][1]
                if (board[x][y]==2):
                    heuristic+=10
                elif (board[x][y]==3):
                    if(k==3):
                        heuristic=-math.inf
                    else: 
                        # print("sssss")
                        heuristic-=50
            for k in range (0,7):
                x=tilePacman[6][k][0]
                y=tilePacman[6][k][1]
                if (board[x][y]==2):
                    heuristic+=5
                elif (board[x][y]==3):
                    heuristic-=100
        elif (direction[i]=="trai"):
            # print("ddddd")
            for k in range (2,5):
                x=tilePacman[k][2][0]
                y=tilePacman[k][2][1]
                if (board[x][y]==2):
                    heuristic+=35
                elif (board[x][y]==3):
                    heuristic=-math.inf
            for k in range (1,6):
                x=tilePacman[k][1][0]
                y=tilePacman[k][1][1]
                if (board[x][y]==2):
                    heuristic+=10
                elif (board[x][y]==3):
                    if(k==3):
                        heuristic=-math.inf
                    else: 
                        # print("sssss")
                        heuristic-=50
            for k in range (0,7):
                x=tilePacman[k][0][0]
                y=tilePacman[k][0][1]
                if (board[x][y]==2):
                    heuristic+=5
                elif (board[x][y]==3):
                    heuristic-=100
        elif (direction[i]=="phai"):
            # print("cccoosos")
            for k in range (2,5):
                x=tilePacman[k][4][0]
                y=tilePacman[k][4][1]
                if (board[x][y]==2):
                    heuristic+=35
                elif (board[x][y]==3):
                    heuristic=-math.inf
            for k in range (1,6):
                x=tilePacman[k][5][0]
                y=tilePacman[k][5][1]
                if (board[x][y]==2):
                    heuristic+=10
                elif (board[x][y]==3):
                    if(k==3):
                        heuristic=-math.inf
                    else: 
                        # print("sssss")
                        heuristic-=50
            for k in range (0,7):
                x=tilePacman[k][6][0]
                y=tilePacman[k][6][1]
                if (board[x][y]==2):
                    heuristic+=5
                elif (board[x][y]==3):
                    heuristic-=100
        heuristicVal.append(heuristic)
    # print(heuristicVal)
    return heuristicVal

def createPacmanTile(pacman):                                                         #tạo ô mới cho pacman đi nè
    i=pacman[0]
    j=pacman[1]  
    maze=[[i,j-1], [i,j+1], [i-1,j], [i+1,j]]
    return maze

def availableTilePacman(board, maze,remembered):                          #board laf nguyen cai maze
    available=[]
    direction=[]
    # print(remembered)
    # print(maze)
    for i in range (0,4):
        x=maze[i][0]
        y=maze[i][1]
        # print(x,y)
        if (board[x][y]!=1):        
            available.append([x,y])
            if(i==0):
                direction.append("trai")
            elif (i==1):
                direction.append("phai")
            elif (i==2):
                direction.append("tren")
            elif (i==3):
                direction.append("duoi")
    # if (len(available)>1):
    #     for i in range (0,4):
    #         if (available[i][0]==remembered[0] and available[i][1]==remembered[1]):
    #             print("co chay ")
    #             available.pop(i)
    #             print(available)
    #             direction.pop(i)
    #         break
    # print(available)
    # time.sleep(1)
    return available, direction
def localsearch(board,pacman, remembered, visited):
    mazePacman=createPacmanTile(pacman)                         ##xem 4 huong
    tilePacman=createNewBoard(board,pacman)                     ##oo 7x7
    # print(tilePacman)
    available, direction=availableTilePacman(board,mazePacman,remembered)                ##huong nao di duoc
    # print(available)
    # heuristicUp, heuristicDown, heuristicLeft, heuristicRight=heuristicValue(tilePacman, board, direction)
    ##neu chung value ma huong do bi chan thi uu tien di huong di duoc
    ##khong cho di lai duong cu tru khi do la option duy nhat
    heuristicVal=heurisicValue(tilePacman, board, direction)
    # print(heuristicVal)
    countVisited=0
    count=[]
    for i in range (0,len(available)):
        if (remembered[0]==available[i][0] and remembered[1]==available[i][1]):
            countVisited+=1000
        for j in range (0, len(visited)):                   #[[f,f],[ff]]
            if (visited[j][0]==available[i][0] and visited[j][1]==available[i][1]):
                # print("co chay")
                countVisited+=1   
            else:
                countVisited+=0
        count.append(countVisited)
        countVisited=0
    # print(heuristicUp, heuristicDown, heuristicLeft, heuristicRight)
    # heuristicAvailable=[]
    # for i in range (0, len(direction)):
    #     if (direction[i]=="duoi"):
    #         if heuristicDown!=10000:
    #             heuristicDown-=count[i]
    #             heuristicAvailable.append(heuristicDown)
    #     if (direction[i]=="tren"):
    #         if heuristicUp!=10000:
    #             heuristicUp-=count[i]
    #             heuristicAvailable.append(heuristicUp)
    #     if (direction[i]=="trai"):
    #         if heuristicLeft!=10000:
    #             heuristicLeft-=count[i]
    #             heuristicAvailable.append(heuristicLeft) 
    #     if(direction[i]=="phai"):
    #         if heuristicRight!=10000:
    #             heuristicRight-=count[i]
    #             heuristicAvailable.append(heuristicRight)   
    heuristicAvailable=[]
    for i in range (0, len(direction)):
        heuristicVal[i]-=count[i]
    
    maxheuristic=max(heuristicVal)
    index=heuristicVal.index(maxheuristic)
    # print(heuristicVal)
    # print(available)
    # print(maxheuristic)
    # print(available[index])
    # time.sleep(2
    #            )
    # print(heuristicAvailable)
    # print(available)
    # print(maxheuristic)
    
    # print(available[index])
    # time.sleep(1)

    # for i in range (0,len(available)):
    #     if (direction[i]=="tren"):
    #         heuristicUp-=count[i]
    #     elif (direction[i]=="duoi"):
    #         heuristicDown-=count[i]
    #     elif (direction[i]=="trai"):
    #         heuristicLeft-=count[i]
    #     elif (direction[i]=="phai"):
    #         heuristicRight-=count[i]
    
    # maxheuristic=max(heuristicUp,heuristicDown,heuristicLeft,heuristicRight)
    # print(heuristicUp, heuristicDown, heuristicLeft, heuristicRight)
    # print(maxheuristic)
    # randomHeurisitc=[]
    # if(heuristicUp==maxheuristic):
    #     randomHeurisitc.append("tren")
    # if (heuristicDown==maxheuristic):
    #     randomHeurisitc.append("duoi")
    # if (heuristicLeft==maxheuristic):
    #     randomHeurisitc.append("trai")
    # if (heuristicRight==maxheuristic):
    #     randomHeurisitc.append("phai")
    # print(randomHeurisitc)
    # path=[]
    # # print(direction)
    # # print(available)
    # for i in range (0,len(randomHeurisitc)):
    #     for j in range (0,len(direction)):
    #         if (randomHeurisitc[i]==direction[j]):
    #             # print("cccc")
    #             path.append(j)
    # print(path)
    # countVisited=0
    # count=[]
    # for i in range (0,len(available)):
    #     for j in range (0, len(visited)):                   #[[f,f],[ff]]
    #         if (visited[j][0]==available[i][0] and visited[j][1]==available[i][1]):
    #             print("co chay")
    #             countVisited+=j   
    #         else:
    #             countVisited+=0
    #     count.append(countVisited)
    #     countVisited=0
    # count_index=0
    # if (len(count)>0):
    #     countVisited=min(count)
    #     count_index=count.index(countVisited)
    # bestVal=[]
    # temp=[]
    # if(len(path)>=1): 
    #     index=random.choice(path) 
    # else:
    #     ##trong số available chọn cái lớn nhất
    #     for i in range (0,len(direction)):
    #         if(direction[i]=="tren"):
    #             bestVal.append(heuristicUp)
    #         elif (direction[i]=="duoi"):
    #             bestVal.append(heuristicDown)
    #         elif (direction[i]=="trai"):
    #             bestVal.append(heuristicLeft)
    #         elif (direction[i]=="phai"):
    #             bestVal.append(heuristicRight)
    #         temp.append(i)
    #     maxVal=max(bestVal)
    #     index=bestVal.index(maxVal)
    #     index=temp[index]
        
    # #     index=count_index
    # print(index)
    # print(available)
    # print(direction)
    # time.sleep(3)
    remembered[0]=pacman[0]
    remembered[1]=pacman[1]
    return available[index], remembered
def checkStateGame(numfood, pacman, board):
    if (numfood==0):
        # print(numfood)
        return 1
    if (board[pacman[0]][pacman[1]]==3):
        return 2
def monsterMove(currghost,initialGhost,board ):
    available=[]
    available2=[]
    newpos=[]
    oldpos=copy.deepcopy(currghost)
    # print(oldpos)
    for index in range (0,len(currghost)):
        i=currghost[index][0]
        j=currghost[index][1]
        initialX=initialGhost[index][0]
        initialY=initialGhost[index][1]
        if (i==initialX and j==initialY):
            available.append([i-1,j])
            available.append([i+1,j])
            available.append([i,j-1])
            available.append([i,j+1])
        elif (i==initialX+1 or i==initialX-1):
            available.append([initialX,initialY])
        elif (j==initialY-1 or j==initialY+1):
            available.append([initialX,initialY])
        for k in range (0,len(available)):
            x=available[k][0]
            y=available[k][1]
            if(board[x][y]!=1):
                available2.append([x,y])
        if(len(available2)>1):
            randomchoice=random.randint(0, len(available2)-1)
        else:
            randomchoice=0
        randomVal=available2[randomchoice]
        available2.clear()
        available.clear()
        newpos.append(randomVal)
    # print(newpos)
    # time.sleep(3)
    return newpos, oldpos  
def ingame(pacman, board, currghost, initialghost, numfood):
    actionsForPacman=[]
    actionsForGhost=[]
    visited=[]
    actionPacman=copy.deepcopy(pacman)
    remembered=copy.deepcopy(pacman)
    recursion=0
    ghost1=[]
    while(True):
        visited.append(actionPacman)
        actionPacman,remembered=localsearch(board, actionPacman,remembered, visited)
        actionsForPacman.append(actionPacman)

        # print(actionPacman)
        oldpos=copy.deepcopy(currghost)
        actionGhost, oldpos=monsterMove(currghost,initialghost,board )
        actionsForGhost.append(actionGhost)
        # print(actionGhost)
        # print(actionPacman)      
        # time.sleep(1)
        # print(actionGhost)
        for i in range (0,len(actionGhost)):
            x=actionGhost[i][0]
            y=actionGhost[i][1]
            currghost[i][0]=x
            currghost[i][1]=y
            board[x][y]=3
            # print(board[x][y])
            board[oldpos[i][0]][oldpos[i][1]]=0
        if (board[actionPacman[0]][actionPacman[1]]==2):
            numfood-=1
            board[actionPacman[0]][actionPacman[1]]=0
            # print(numfood)
        # if (board[actionPacman[0]][actionPacman[1]]==3):
            # print("tao chay qua ne")
            # board[actionPacman[0]][actionPacman[1]]=0      
        checkGame=checkStateGame(numfood,actionPacman,board)      
        if (checkGame==1):
            # print("sssss")
            return actionsForPacman,actionsForGhost
        elif (checkGame==2):
            # print("bi giet")
            return actionsForPacman,actionsForGhost
        # for i in range (0,len(actionGhost)):
        #     x=actionGhost[i][0]
        #     y=actionGhost[i][1]            
        #     print(board[x][y])
        # print(board)
        
        # time.sleep(3)
       
        recursion+=1
        # time.sleep(1)
    return actionsForPacman,actionsForGhost
#######
#vị trí của pacman (i+2, j+2) với i,j là vị trí ban đầu 
# board, initialX, initialY, m, n=inputMaze("map3.txt")
# pacman=[3,3]                #ban đầu là 1,1
# currghost=[[1+2, 11+2],                 #vị trí của ghost cũng v
# [1+2, 28+2],
# [7+2, 14+2],
# [8+2, 30+2],
# [9+2, 1+2]]
# initialghost=[[1+2, 11+2],
# [1+2, 28+2],
# [7+2, 14+2],
# [8+2, 30+2],
# [9+2, 1+2]]
# numfood=8
# remembered=[]
# board=plusPadding(board)                        #tạo padding 
# # print(board)
# actionsPacman, actionsGhost=ingame(pacman, board, currghost,initialghost,numfood)
# print(actionsPacman) 
# print(actionsGhost)

# print(actionsGhost)
#####Kết quả sau khi ra thì -2 ở cả tọa độ x và y, cả ma và pacman đều phải trừ
####actionPacman =[[x,y],[i,j],...]  với actionPacman[index] thì index là mỗi bước đi của pacman
###### actionGhost =[[[x1,y1],[x2,y2],[x3,y3],...],                 với actionGhost[0][0][0] và actionGhost[0][0][1] lần lượt là tọa độ x,y 
#                    [[x11,y11],[x22,y22],[x33,y33],...],...]            của con Ma thứ nhất ở lượt thứ nhất (số 0 đầu tiên là bằng cái index ở trên á là lần đi thứ mấy á, 
#                                                                               số 0 thứ hai là index của con ma, 0 vs 1 là tọa độ )
####                 