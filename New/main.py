from Graphic import* 
from Algorithm import*
import time 
import numpy as np

game = Game(matrix,pacman)
pygame.display.update()
old = game.Player.currentPosition
visitedMatrix = np.zeros((m,n),int)
for i in range(len(visitedMatrix)):
    for j in range(len(visitedMatrix[0])):
        visitedMatrix[i][j] = 1
orignalPositionGhost = game.level3()

while True:
    game.Player.DEAD, index = game.checkColision()
    isFinish, state = game.checkGameFinish()
    if isFinish:
        break
    game.clearAnimation() 
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            pygame.quit()
            sys.exit(0)

    succesor = generatePossibleSuccessor(game.Player.currentPosition[0],game.Player.currentPosition[1],game.Matrix)
    newPosition = evaluateFunction(game.Player.currentPosition[0],game.Player.currentPosition[1],game.Matrix,succesor,old, visitedMatrix)
    try: 
        visitedMatrix[old[0]][old[1]] +=2
        # print(visitedMatrix[old[0]][old[1]])
        # print(game.visitedMatrix)
        # input()
    except:
        print(newPosition)
        print(succesor)
        input()
    # print(game.visitedMatrix[newPosition[0]][newPosition[1]])
    # print( game.visitedMatrix)
    # input()
    game.pacmanMove(newPosition)
    old = game.Player.currentPosition
    game.Player.draw()
    # ghost move
    i = 0
    for ghost in game.Ghosts:
        succesorGhost = generateGhostMove(ghost.currentPosition[0],ghost.currentPosition[1],matrix,orignalPositionGhost[i])
        oldGhot = ghost.currentPosition
        game.Matrix[oldGhot[0]][oldGhot[1]] = 0
        new = evaluateF(ghost.currentPosition[0],ghost.currentPosition[1],game.Matrix,succesorGhost, oldGhot)
        ghost.chanePosition(new)
        game.Matrix[new[0]][new[1]] = 3
        # print(game.Matrix[new[0]][new[1]])
        # print(game.Matrix[oldGhot[0]][oldGhot[1]])
        # print(new)
        # input()
        
        ghost.draw()
        i+=1
    pygame.display.update()
    time.sleep(0.2)
    clock.tick(30)

input("haha")

