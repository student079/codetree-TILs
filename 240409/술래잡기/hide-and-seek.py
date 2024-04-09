# n * n 격자
# 술래 정중앙
# m 명의 도망자
# 도망자 좌우or 상하로만 움직임 (좌우는 우선 오른쪽 시작, 상하는 우선 아래쪽 시작)
# h개의 나무
# 겹치기 가능
# 현재 술래와의 거리가 3이하인 도망자만 움직인다
# 도망자 움직이는 규칙
# 1. 이후 움직이는 칸에 술래가 있음 X
# 2. 술래 없으면 이동 (나무 있어도 ㄱㅊ)
# 3. 격자 벗어난다면 방향 반대로 틀고나서!! 그 방향으로 1칸 움직일대 술래 없으면 이동
# 이동 도중에 도망자들이 겹칠 수 있음
# 술래 이동
# 이동방향틀어지는 칸이면 바로 시선 틀어줌
# 양끝에 해당하는 위치인 (1행, 1열) 혹은 정중앙에 도달하게 된다면 이 경우 역시 방향을 바로 틀어줘야 함에 유의합니다.
# 시야 내의 도망자 잡음 (현재칸 포함해서 3칸)
# 나무있는 칸은 넘기고 다음칸
#  t번째 턴이라고 했을 때 t x 현재 턴에서 잡힌 도망자의 수
# 도망자 사라짐

import sys
from collections import deque


# 엣지케이스 테스트
n, m, h, k = map(int, sys.stdin.readline().rstrip().split())
board = [[0] * n for _ in range(n)]

X, Y, D = n//2, n//2, 0
runners = deque()
for _ in range(m):
    x, y, d = map(int, sys.stdin.readline().rstrip().split())
    runners.append((x-1,y-1,d))
for _ in range(h):
    x, y= map(int, sys.stdin.readline().rstrip().split())
    board[x-1][y-1] = -1 # 나무 위치
dx = (-1, 0, 1, 0)
dy = (0, 1, 0, -1)
# 상 우 하 좌

def moveRunners(runners):
    for _ in range(len(runners)):
        x, y, d = runners.popleft()

        # 술래랑 3칸 이하만 움직임
        if abs(abs(X-x) + abs(Y-y)) <= 3:
            nx = x + dx[d]
            ny = y + dy[d]

            # 방향 틀어주기
            if not (0 <= nx < n and 0 <= ny < n):
                # 1우 -> 3좌, 3좌 -> 1우, 2하 -> 0상, 0상 -> 2하
                d = (d+2)%4
                nx = x + dx[d]
                ny = y + dy[d]

            # 술래 있는지
            if nx == X and ny == Y:
                runners.append((x, y, d))
            else:
                runners.append((nx, ny, d))
        else:
            runners.append((x, y, d))

cnt = 0
rotateCnt = 0
dis = 1
answer = 0
for turn in range(k):
    # 도망자 움직이기
    moveRunners(runners)

    # 술래 움직임
    X = X + dx[D]
    Y = Y + dy[D]
    cnt += 1
    if cnt == dis:
        if turn // ((n ** 2)-1) % 2 == 0:
            D = (D + 1) % 4
        else:
            D = (D - 1) % 4

        cnt = 0
        rotateCnt += 1
        if rotateCnt == 2:
            rotateCnt = 0
            if turn//((n ** 2)-1) % 2 == 0:
                dis += 1
            else:
                dis -= 1

    if X == 0 and Y == 0:
        D = 2
        cnt = 0
        rotateCnt = -1
        dis = n-1
    if X == n//2 and Y == n//2:
        D = 0
        cnt = 0
        rotateCnt = 0
        dis = 1

    # 현재 시야에 도망자 잡기 나무 체크
    res = 0
    for i in range(3):
        nx = X + (dx[D] * i)
        ny = Y + (dy[D] * i)
        if not ( 0<= nx < n and 0 <= ny < n):
            break

        if board[nx][ny] != -1:
            for _ in range(len(runners)):
                x, y ,d = runners.popleft()
                if x == nx and y == ny:
                    res += 1
                else:
                    runners.append((x, y ,d))
    answer += (turn+1) * res

print(answer)