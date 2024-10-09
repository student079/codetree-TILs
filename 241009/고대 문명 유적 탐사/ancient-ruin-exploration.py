from collections import deque
import sys

# 5 5 격자
# 7가지 종류 유물 조각
# 3*3 선택하여 회전
# 회전 후 가치가 최대
# 같으면 각도 가장 작은 방법
# 같으면 열, 행이 가장 작은 구간
# 같은 숫자 3개 이상 연결된 경우
# 개수 합
# 조각 다시 채워짐
# 아래 왼쪽 순

# 시계 방향 회전
def rotate(i, j, k):
    newBoard = [row[:] for row in board]
    tempBoard = [row[:] for row in board]

    for _ in range(k):
        for x in range(3):
            for y in range(3):
                ox = i - 1 + x
                oy = j - 1 + y
                nx = -(j - 1 + y - j) + i
                ny = i - 1 + x - i + j
                newBoard[ox][oy] = tempBoard[nx][ny]
                
        tempBoard = [row[:] for row in newBoard]

    return newBoard

dx = (0 ,1, 0, -1)
dy = (1, 0, -1, 0)
def bfs(rotateBoard):
    result = []
    visited = [[False] * 5 for _ in range(5)]
    for i in range(5):
        for j in range(5):
            if not visited[i][j]:
                q = deque()
                q.append((i, j))
                v = rotateBoard[i][j]
                vs = [(i, j)]
                visited[i][j] = True
                while q:
                    x, y = q.popleft()
                    for k in range(4):
                        nx = x + dx[k]
                        ny = y + dy[k]

                        if not (0 <= nx < 5 and 0 <= ny < 5):
                            continue
                        
                        if not visited[nx][ny] and rotateBoard[nx][ny] == v:
                            q.append((nx, ny))
                            visited[nx][ny] = True
                            vs.append((nx, ny))
                if len(vs) >= 3:
                    result += vs
    
    return result

def searchMax():
    resultX = 0
    resultY = 0
    resultAngle = 0
    resultValues = []
    for k in range(4):
        for i in range(1, 4):
            for j in range(1, 4):
                rotateBoard = rotate(i, j, k)
                values = bfs(rotateBoard)
                s = len(values)
                if len(resultValues) < s:
                    resultValues = values[:]
                    resultX = i
                    resultY = j
                    resultAngle = k
    
    return (resultX, resultY, resultAngle, resultValues)

def getRest():
    for j in range(5):
        for i in range(4,-1,-1):
            if board[i][j] == 0:
                board[i][j] = rest.popleft()



K, M = map(int, sys.stdin.readline().rstrip().split())
board = [list(map(int,sys.stdin.readline().rstrip().split())) for _ in range(5)]
rest = deque(list(map(int,sys.stdin.readline().rstrip().split())))
answer = 0

# K 번 반복
for _ in range(K):
    resultX, resultY, resultAngle, resultValues = searchMax()
    s = len(resultValues)
    if s == 0:
        break
    
    board = rotate(resultX, resultY, resultAngle)
    for x, y in resultValues:
        board[x][y] = 0

    answer += s
    getRest()

    # 연쇄 획득
    while True:
        values = bfs(board)
        s = len(values)
        if s == 0:
            break
        for x, y in values:
            board[x][y] = 0
        answer += s
        getRest()

print(answer)