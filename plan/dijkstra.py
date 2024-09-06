import matplotlib.pyplot as plt
import numpy as np

map_name = 'maze' # maze2
if map_name == 'maze':
    start = (90, 5)
    target = (42, 116)
else:
    start = (18, 2)
    target = (18, 11)

def convertLocationToNum(rr, cc):
    table = [
        (-1,-1), (-1,0), (-1,1), 
        (0,-1), (0,0), (0,1), 
        (1,-1), (1,0), (1,1)
    ]
    return table.index((rr, cc))

def convertNumToLocation(num):
    table = [
        (-1,-1), (-1,0), (-1,1), 
        (0,-1), (0,0), (0,1), 
        (1,-1), (1,0), (1,1)
    ]
    return table[num]

# pixel[0]: 0->obstacle, 255->free, 125->visited
# pixel[1]: distance to start
# pixel[2]: parent

# read image as numpy array
map = np.array(plt.imread(map_name+'.jpg'))
# make sure just 0 and 255
shape = map.shape
for i in range(shape[0]):
    for j in range(shape[1]):
        for k in range(shape[2]):
            if map[i][j][k] < 125:
                map[i][j][k] = 0
            else:
                map[i][j][k] = 255

# mark start: visited, distance = 0, parent = self
map[start[0]][start[1]] = [125, 0, convertLocationToNum(0, 0)]
# mark target
map[target[0]][target[1]] = [255, 255, 0]

def updateNeighbors(map, node):
    r, c = node
    # my minimal distance to start
    distance = map[r][c][1]
    for rr in range(-1, 2):
        rrr = r + rr
        # out of map
        if rrr < 0 or rrr >= map.shape[0]:
            continue
        for cc in range(-1, 2):
            ccc = c + cc
            # out of map
            if ccc < 0 or ccc >= map.shape[1]:
                continue
            # self
            if rr == 0 and cc == 0:
                continue
            # obstacle
            if map[rrr][ccc][0] == 0:
                continue
            # visited
            if map[rrr][ccc][0] == 125:
                continue
            # update distance and parent
            if rr == 0 or cc == 0:
                child_distance = distance + 1
            else: # hypotenuse
                child_distance = distance + 2
            if child_distance > 255: # out of range
                child_distance = 255 
            if child_distance < map[rrr][ccc][1]:
                map[rrr][ccc][1] = child_distance
                map[rrr][ccc][2] = convertLocationToNum(rr, cc)
    # set myself as visited
    map[r][c][0] = 125

def findMinNode(map):
    min_idx = (-1, -1)
    min_distance = 255

    shape = map.shape
    for r in range(shape[0]):
        for c in range(shape[1]):
            # obstacle
            if map[r][c][0] == 0:
                continue
            # visited
            if map[r][c][0] == 125:
                continue
            if map[r][c][1] < min_distance:
                min_idx = (r, c)
                min_distance = map[r][c][1]
    if min_idx == (-1, -1):
        return None
    return min_idx

def showPath(map, target):
    # convertLocationToNum(0, 0) = 4 -> parent = it self -> start node
    if map[target][2] == 4:
        print('node parent is itself, reach start node')
        return # break recursive call
    # get parent r & c
    delta = convertNumToLocation(map[target][2])
    parent = (target[0] - delta[0], target[1] - delta[1])
    showPath(map, parent)
    # set target as blue
    map[target] = [0, 0, 255]

cnt = 0
min_node = start
while True:
    # update neighbors
    updateNeighbors(map, min_node)
    # next node which is caculated but not visited and closest to start
    min_node = findMinNode(map)
    if min_node == None:
        print('min node find fail')
        break
    # show map
    cnt += 1
    if cnt > 80:
        cnt = 0
        plt.cla()
        plt.imshow(map)
        plt.pause(0.001)

plt.cla()
showPath(map, target)
plt.imshow(map)
plt.show()

#####################################
'''
0. set all non-obstacle node's distance to max
1. find 8 neighbors
2. calculate my distance to each neighbor -> got neighbor to start distance
3. update neighbor's distance to start if it's smaller than current distance
4. at the same time, update neighbor's parent to me because neighbor is closer to start node through me
5. mark me as visited, so I won't be visited again
6. now, find the node which is closest to start and not visited
7. repeat 1-6 until all nodes are visited (osbstacle nodes)
8. now, the target node has the shortest path to start node, iterate target's parent until start node is the shortest path we need

Dijkstra is not efficient for this task, because it has no goal, use A* instead!
'''