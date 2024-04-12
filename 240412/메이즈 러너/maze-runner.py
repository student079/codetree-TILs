# N 4 ~ 10
# M 1 ~ 10
# K 1 ~100
import sys
from collections import deque

N, M, K = map(int, sys.stdin.readline().rstrip().split())
maze = []
for _ in range(N):
    maze.append(list(map(int, sys.stdin.readline().rstrip().split())))
players = deque()
playerXY = [[0] * N for _ in range(N)]
for _ in range(M):
    x, y = map(int, sys.stdin.readline().rstrip().split())
    players.append([x-1,y-1])
    playerXY[x-1][y-1] += 1
x, y = map(int, sys.stdin.readline().rstrip().split())
exit = (x-1, y-1)

dx = (-1 ,1, 0, 0)
dy = (0, 0, -1, 1)

# 움직인 칸은 현재 머물러 있던 칸보다 출구까지의 최단 거리가 가까워야 합니다.
# -> 출구까지 최단거리 구하는 bfs
# 출구에서 모든 좌표까지 bfs 걸리는 시간 구하면 한번에 가능 X
# 최단거리가 명시되어 있으니 그거대로 하자
# 움직일 수 있는 칸이 2개 이상이라면, 상하로 움직이는 것을 우선시합니다.
# 움직일 수 없으면 움직이지 않는다


def selectSquare(exit):
    for length in range(2, N+1):
        # 좌상단 0, 0부터 확인
        for x1 in range(N-length+1):
            for y1 in range(N - length+1):
                # 우하단
                x2 = x1 + length - 1
                y2 = y1 + length - 1

                # 출구 포함 하는지
                if not (x1 <= exit[0] <= x2 and y1 <= exit[1] <= y2):
                    continue

                # 플레이어 포함하는지
                for i in range(x1,x2+1):
                    for j in range(y1, y2 + 1):
                        if playerXY[i][j] >= 1:
                            return x1, y1, x2, y2
    print()
def rotateMaze(exit):
    x1, y1, x2, y2 = selectSquare(exit)
    length = x2 - x1

    newMaze = []
    newPlayerXY = []
    for i in range(N):
        newMaze.append(maze[i][:])
        newPlayerXY.append(playerXY[i][:])

    # 시계 방향 회전  + 플레이어도 이동
    for i in range(x1, x2+ 1):
        for j in range(y1, y2 + 1):
            # 0, 0으로 이동
            x = i - x1
            y = j - y1
            newX = y
            newY = length - x
            newMaze[newX + x1][newY + y1] = maze[i][j]
            newPlayerXY[newX + x1][newY + y1] = playerXY[i][j]

    for _ in range(len(players)):
        a, b = players.popleft()
        if (x1 <= a <= x2 and y1 <= b <= y2):
            x = a - x1
            y = b - y1
            nx = y + x1
            ny = length - x + y1
            players.append([nx, ny])
        else:
            players.append([a, b])


    # + 벽 빼주기
    for i in range(x1, x2+ 1):
        for j in range(y1, y2 + 1):
            if newMaze[i][j] > 0:
                newMaze[i][j] -= 1

    # 출구좌표 변경
    ex = exit[1] - y1 + x1
    ey = length - (exit[0] - x1) + y1

    return (newMaze, newPlayerXY, (ex,ey))

answer = 0
moveDistance = 0
for _ in range(K):

    # 플레이어들 상하좌우 순서로 살펴보면서 최단거리 작은 값으로 이동
    for _ in range(len(players)):
        x, y = players.popleft()

        resX, resY = -1, -1
        distance = abs(exit[0] - x) + abs(exit[1] - y)
        for k in range(4):
            nx = x+dx[k]
            ny = y+dy[k]

            if not ( 0<= nx < N and 0 <= ny < N):
                continue

            d = abs(exit[0] - nx) + abs(exit[1] - ny)
            if maze[nx][ny] == 0 and distance > d:
                distance = d
                resX, resY = nx, ny

        if (resX, resY) == exit:
            answer += 1
            moveDistance += 1
            playerXY[x][y] -= 1
            continue

        # 그대로 있기
        if (resX, resY) == (-1, -1):
            players.append([x, y])
        else:
            players.append([resX, resY])
            moveDistance += 1
            playerXY[x][y] -= 1
            playerXY[resX][resY] += 1

    if answer == M:
        break

    # 미로 회전
    # 회전할때 내구도 깎임
    # 한 명 이상의 참가자와 출구를 포함한 가장 작은 정사각형을 잡습니다.
    # 왼쪽 위부터 왼 -> 오, 위 -> 아래
    maze, playerXY, exit = rotateMaze(exit)

print(moveDistance)
print(exit[0] + 1, exit[1] + 1)