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
    return [candidates[0], candidates[len(candidates)-1]]

dx = (0,1,0,-1, -1, -1, 1, 1)
dy = (1, 0, -1, 0, -1, 1, -1, 1)

def bfs(attackX, attackY, defenseX, defenseY):
    q = deque()
    q.append((attackX, attackY, {(attackX, attackY)}))
    
    while q:
        x, y, visited = q.popleft()
        
        if x == defenseX and y == defenseY:
            return visited
        
        for k in range(4):
            nx = (x + dx[k]) % N
            ny = (y + dy[k]) % M
            
            if board[nx][ny] > 0 and (nx, ny) not in visited:
                q.append((nx, ny, visited | {(nx, ny)}))
            
    return -1

def attackingLazer(defenseX, defenseY, realAttackPower):
    board[defenseX][defenseY] -= realAttackPower
    visited = {(defenseX, defenseY)}
    power = realAttackPower // 2
    for k in range(8):
        nx = (defenseX + dx[k]) % N
        ny = (defenseY + dy[k]) % M

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
        visited = attackingLazer(defenseX, defenseY, realAttackPower)
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
    alive = 0
    for i in range(N):
        for j in range(M):
            if board[i][j] > 0:
                if (i,j) not in visited:
                    board[i][j] += 1
                alive += 1
    return alive

for step in range(1, K+1):
    attack, defense = getMostCanon()
    visited = attacking(attack, defense)
    # 포탑 정비
    alive = restore(visited)
    if alive < 1:
        break

answer = 0
for i in range(N):
    for j in range(M):
        answer = max(answer,board[i][j])
print(answer)