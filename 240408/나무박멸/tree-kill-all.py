# 제초제 k 범위만큼 대각선 -> dxdy 대각선
# 나무 성장 동시에
# 다른나무, 제초제, 벽 없는 칸에 번식
# 가능한 칸 개수 만큼 번식
# 나머지 버리기
# 나무 제일 많이 박멸되는 칸에 제초제 뿌리기
# 같으면 행, 열 작은 곳에
# c년 만큼 제초제 남아있음 -> 제초제용 배열

# 총 박멸한 나무 수 구하기

import sys
from collections import deque

n, m, k, c = map(int, sys.stdin.readline().rstrip().split())
board = []
for _ in range(n):
    board.append(list(map(int,sys.stdin.readline().rstrip().split())))
killers = [[0] * n for _ in range(n)]

answer = 0

def searchTree(i,j):
    dx = (0, 1, 0, -1)
    dy = (1, 0, -1, 0)
    cnt = 0
    for k in range(4):
        nx = i + dx[k]
        ny = j + dy[k]

        if not (0 <= nx < n and 0 <= ny < n):
            continue

        if board[nx][ny] > 0:
            cnt += 1

    return cnt

def grow(board):
    for i in range(n):
        for j in range(n):
            if board[i][j] > 0:
                board[i][j] += searchTree(i,j)

def regenerate(i,j,year, newBoard):
    dx = (0, 1, 0, -1)
    dy = (1, 0, -1, 0)

    cnt = 0
    target = []

    for t in range(4):
        nx = i + dx[t]
        ny = j + dy[t]

        if not (0 <= nx < n and 0 <= ny < n):
            continue

        if newBoard[nx][ny] == 0 and killers[nx][ny] < year:
            cnt += 1
            target.append([nx,ny])

    if cnt == 0:
        return

    old = newBoard[i][j]//cnt
    for t in target:
        x, y = t
        board[x][y] += old

def generate(board, year):
    newBoard = []
    for b in board:
        newBoard.append(b[::])

    for i in range(n):
        for j in range(n):
            if board[i][j] > 0:
                regenerate(i,j,year, newBoard)


def select(i,j, k):
    dx = (1, 1, -1, -1)
    dy = (1, -1, 1, -1)

    cnt = 0
    cnt += board[i][j]

    q = deque()
    # 대각선
    # 벽있으면 더이상 제초제 확산 X
    for d in range(4):
        nx = i + dx[d]
        ny = j + dy[d]

        if not (0 <= nx < n and 0 <= ny < n):
            continue

        if board[nx][ny] > 0 and killers[nx][ny] < year:
            q.append((nx,ny, 1, (dx[d], dy[d])))

    while q:
        nx, ny, times, d = q.popleft()

        cnt += board[nx][ny]

        if times + 1 > k:
            continue

        nnx = nx + d[0]
        nny = ny + d[1]

        if not (0 <= nnx < n and 0 <= nny < n):
            continue

        if board[nnx][nny] > 0 and killers[nnx][nny] < year:
            q.append((nnx,nny, times+1, d))

    return cnt



def selectKiller(board, k):
    cnt = 0
    sI = -1
    sJ = -1
    for i in range(n):
        for j in range(n):
            if board[i][j] > 0:
                temp = select(i,j, k)
                if temp > cnt:
                    cnt = temp
                    sI = i
                    sJ = j

    return (sI, sJ)

def kill(board,i,j, year):
    dx = (1, 1, -1, -1)
    dy = (1, -1, 1, -1)

    cnt = 0
    cnt += board[i][j]
    board[i][j] = 0
    killers[i][j] = year+c

    q = deque()
    # 대각선
    # 벽있으면 더이상 제초제 확산 X
    for d in range(4):
        nx = i + dx[d]
        ny = j + dy[d]

        if not (0 <= nx < n and 0 <= ny < n):
            continue

        if board[nx][ny] > 0:
            q.append((nx, ny, 1, (dx[d], dy[d])))

    while q:
        nx, ny, times, d = q.popleft()

        cnt += board[nx][ny]
        board[nx][ny] = 0
        killers[nx][ny] = year + c

        if times + 1 > k:
            continue

        nnx = nx + d[0]
        nny = ny + d[1]

        if not (0 <= nnx < n and 0 <= nny < n):
            continue

        if board[nnx][nny] > 0:
            q.append((nnx, nny, times + 1, d))

    return cnt

for year in range(1, m + 1):

    # 나무 성장
    grow(board)

    # 나무 번식
    generate(board, year)

    # 제초제 뿌릴 곳 선정
    i,j = selectKiller(board, k)

    if i == -1 and j == -1:
        continue

    # 제초제 뿌리기 (현재 년도 넣어서 제초제)
    answer += kill(board,i,j, year)

print(answer)