import sys
from collections import deque

R, C, K = map(int, sys.stdin.readline().split())

board = [[0] * C for _ in range(R + 3)]
exitBoard = [[False] * C for _ in range(R + 3)]
dx = (-1, 0, 1, 0)
dy = (0, 1, 0, -1)
answer = 0

def canGo(x, y):
    # 위, 지금 다 확인
    flag = 0 <= y - 1 and y + 1 < C and x + 1 < R + 3
    flag = flag and board[x - 1][ y - 1] == 0
    flag = flag and board[x - 1][ y] == 0
    flag = flag and board[x - 1][ y + 1] == 0
    flag = flag and board[x][ y - 1] == 0
    flag = flag and board[x][ y] == 0
    flag = flag and board[x][ y + 1] == 0
    flag = flag and board[x + 1][ y] == 0
    return flag

def move(x, y):
    visited = [[False] * C for _ in range(R + 3)]
    visited[x][y] = True
    q = deque()
    q.append((x, y))
    result = x

    while q:
        i, j = q.popleft()

        idx = board[i][j]
        isExit = exitBoard[i][j]

        for k in range(4):
            nx = i + dx[k]
            ny = j + dy[k]

            if not (0 <= nx < R + 3 and 0 <= ny < C):
                continue

            if(board[nx][ny] == idx or (isExit and board[nx][ny] != 0)) and not visited[nx][ny]:
                result = max(result, nx)
                q.append((nx, ny))
                visited[nx][ny] = True
    return result
                

for i in range(K):
    c, d = map(int, sys.stdin.readline().rstrip().split())
    x = 0
    y = c - 1

    while True:
        if canGo(x+1, y):
            x += 1
        elif canGo(x+1, y-1):
            x +=1
            y -= 1
            d = (d- 1) % 4
        elif canGo(x+1, y+1):
            x +=1
            y += 1
            d = (d + 1) % 4
        else:
            # 넘나 확인
            if 0 <= x < 3 or 0 <= x - 1 < 3:
                board = [[0] * C for _ in range(R + 3)]
                exitBoard = [[False] * C for _ in range(R + 3)]
            # 정령 이동
            else :
                board[x][y] = i+1
                for k in range(4):
                    board[x + dx[k]][y + dy[k]] = i+1
                exitBoard[x + dx[d]][y + dy[d]] = True
                answer += move(x, y) - 3 + 1
            break
print(answer)