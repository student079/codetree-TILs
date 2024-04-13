# 기사 밀리는 거 bfs 로 q에 넣으면서 구현

import sys
from collections import deque

L, N, Q = map(int,sys.stdin.readline().rstrip().split())
board = []
for _ in range(L):
    board.append(list(map(int,sys.stdin.readline().rstrip().split())))
kBoard = [[0] * L for _ in range(L)]
knights = [[]]
originK = [0] * (N+1)
for idx in range(1, N+1):
    r, c, h, w, k = map(int,sys.stdin.readline().rstrip().split())
    x1, y1, x2, y2 = r-1, c-1, r-1 + h-1, c-1+w-1
    originK[idx] = k
    knights.append([x1, y1,x2, y2, k])
    for i in range(x1, x2+1):
        for j in range(y1, y2+1):
            kBoard[i][j] = idx

isMoved = [False] * (N+1)

dx = (-1, 0, 1, 0)
dy = (0, 1, 0, -1)

def tryMove(idx, d):
    x1, y1, x2, y2, k = knights[idx]
    visited = set()
    visited.add(idx)

    if k <= 0:
        return False
    q = deque()
    q.append(idx)

    while q:
        index = q.popleft()
        x1, y1, x2, y2, k = knights[index]

        nx1 = x1 + dx[d]
        ny1 = y1 + dy[d]
        nx2 = x2 + dx[d]
        ny2 = y2 + dy[d]

        if not (0<=nx1< L and 0 <= ny1 < L and 0 <= nx2 < L and 0 <= ny2 < L):
            return False

        for i in range(nx1, nx2+1):
            for j in range(ny1, ny2+1):
                if board[i][j] == 2:
                    return False
                temp = kBoard[i][j]
                if temp != 0 and temp not in visited:
                    visited.add(temp)
                    q.append(temp)

    # 여기까지 오면 가능한거
    for index in list(visited):
        isMoved[index] = True

        x1, y1, x2, y2, k = knights[index]

        for i in range(x1, x2 + 1):
            for j in range(y1, y2 + 1):
                kBoard[i][j] = 0

        nx1 = x1 + dx[d]
        ny1 = y1 + dy[d]
        nx2 = x2 + dx[d]
        ny2 = y2 + dy[d]

        for i in range(nx1, nx2+1):
            for j in range(ny1, ny2+1):
                kBoard[i][j] = index

        knights[index] = [nx1, ny1, nx2, ny2, k]
    return True

# k <= 0 이면 죽은거
def moveKnight(idx, d):

    if tryMove(idx, d):
        # 자신 빼주기
        isMoved[idx] = False

        # 움직인거 함정 계산
        for index in range(1, N+1):
            if isMoved[index]:
                isMoved[index] = False

                cnt = 0
                x1, y1, x2, y2, k = knights[index]

                # k 계산해서 죽으면 좌표에서 없애기
                for i in range(x1, x2+1):
                    for j in range(y1, y2+1):
                        if board[i][j] == 1:
                            cnt += 1

                k -= cnt
                if k <= 0:
                    for i in range(x1, x2 + 1):
                        for j in range(y1, y2 + 1):
                            kBoard[i][j] = 0

                knights[index] =  [x1, y1, x2, y2, k]

for _ in range(Q):
    idx, d = map(int,sys.stdin.readline().rstrip().split())

    moveKnight(idx, d)

answer = 0
for i in range(1, N+1):
    if knights[i][4] <= 0:
        continue
    answer += originK[i] - knights[i][4]

print(answer)