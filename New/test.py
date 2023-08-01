import numpy as np


visit = [[1,2,4],[3,4,5]]
for i in range(len(visit)):
    for j in range(len(visit[0])):
        visit[i][j] =7
print(visit)