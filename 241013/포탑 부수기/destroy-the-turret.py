# N, M 10
# K 1000
# 100 * 1000 = 100000

import sys
from collections import deque

N, M, K = map(int ,sys.stdin.readline().rstrip().split())
board = []
for _ in range(N):
    board.append(list(map(int,sys.stdin.readline().rstrip().split())))
attackCanonTime = [[0] * M for _ in range(N)]

def getMostCanon():
    # 100
    candidates = []
    for i in range(N):
        for j in range(M):
            attack = board[i][j]
            if attack > 0:
                candidates.append((i, j, attack))

    candidates.sort(key = lambda x: (x[2], -attackCanonTime[x[0]][x[1]], -(x[0]+x[1]), -x[1]))
    alive = len(candidates)
    return [candidates[0], candidates[alive-1], alive]

dx = (0,1,0,-1, -1, -1, 1, 1)
dy = (1, 0, -1, 0, -1, 1, -1, 1)

def bfs(attackX, attackY, defenseX, defenseY):
    q = deque()
    q.append((attackX, attackY))
    visited = [[0] * M for _ in range(N)]
    visited[attackX][attackY] = -1
    
    while q:
        x, y= q.popleft()
        
        if x == defenseX and y == defenseY:
            temp = set()
            while visited[x][y] != -1:
                temp.add((x, y))
                nextX, nextY = visited[x][y]
                x, y = nextX, nextY
            
            return temp
        
        for k in range(4):
            nx = (x + dx[k]) % N
            ny = (y + dy[k]) % M
            
            if board[nx][ny] > 0 and visited[nx][ny] == 0:
                q.append((nx, ny))
                visited[nx][ny] = (x, y)
            
    return -1

def attackingLazer(attackX, attackY,defenseX, defenseY, realAttackPower):
    board[defenseX][defenseY] -= realAttackPower
    visited = {(defenseX, defenseY)}
    power = realAttackPower // 2
    for k in range(8):
        nx = (defenseX + dx[k]) % N
        ny = (defenseY + dy[k]) % M

        if nx == attackX and ny == attackY:
            continue

        if board[nx][ny] > 0:
            visited.add((nx ,ny))
            board[nx][ny] -= power

    return visited

def attacking(attack, defense):
    attackX, attackY, attackPower = attack
    attackCanonTime[attackX][attackY] = step
    realAttackPower = attackPower + N + M
    board[attackX][attackY] = realAttackPower
    defenseX, defenseY, defensePower = defense
    
    visited = bfs(attackX, attackY, defenseX, defenseY)
    if visited == -1:
        visited = attackingLazer(attackX, attackY,defenseX, defenseY, realAttackPower)
    else:
        visited -= {(defenseX, defenseY)}
        visited -= {(attackX, attackY)}
        power = realAttackPower // 2
        board[defenseX][defenseY] -= realAttackPower
        for x, y in visited:
            board[x][y] -= power
        visited.add((defenseX, defenseY))
    visited.add((attackX, attackY))
    return visited

def restore(visited):
    for i in range(N):
        for j in range(M):
            if board[i][j] > 0:
                if (i,j) not in visited:
                    board[i][j] += 1

for step in range(1, K+1):
    attack, defense, alive = getMostCanon()
    if alive <= 1:
        break
    visited = attacking(attack, defense)

    # 포탑 정비
    restore(visited)

answer = 0
for i in range(N):
    for j in range(M):
        answer = max(answer,board[i][j])
print(answer)