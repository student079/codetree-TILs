# 최단거리 bfs ↑, ←, →, ↓ 의 우선 순위
# 편의점 도착하면 다른 사람들은 해당 편의점 칸 이동 X
# 베이스 캠프도 마찬가지, 즉 이후 절대 못지나가는 칸 있음

# 격자에 있는 사람들 모두가 본인이 가고 싶은 편의점 방향을 향해서 1 칸 움직입니다. 최단거리로 움직이며 최단 거리로 움직이는 방법이 여러가지라면 ↑, ←, →, ↓ 의 우선 순위로 움직이게 됩니다. 여기서 최단거리라 함은 상하좌우 인접한 칸 중 이동가능한 칸으로만 이동하여 도달하기까지 거쳐야 하는 칸의 수가 최소가 되는 거리

import sys
from collections import deque

n, m = map(int, sys.stdin.readline().rstrip().split())
board = []
for _ in range(n):
    board.append(list(map(int,sys.stdin.readline().rstrip().split())))
stores = []
for _ in range(m):
    x, y = map(int,sys.stdin.readline().rstrip().split())
    stores.append((x-1,y-1))
cantMove = [[False] * n for _ in range(n)]

people = deque()
dx = (-1, 0, 0, 1)
dy = (0, -1, 1, 0)
step = [[] for _ in range(m)]
def computeNarrowBase(ax, ay):

    q = deque()
    q.append((ax,ay))
    visited = [[False] * n for _ in range(n)]
    visited[ax][ay] = True

    while q:
        x, y = q.popleft()

        for k in range(4):
            nx = x + dx[k]
            ny = y + dy[k]

            if not ( 0<= nx < n and 0 <= ny < n):
                continue

            if not cantMove[nx][ny] and not visited[nx][ny]:
                if board[nx][ny] == 1:
                    return (nx, ny)
                visited[nx][ny] = True
                q.append((nx, ny))

def movePerson(idx, x, y):
    # x y에서 모든곳 걸리는 거리
    q = deque()
    q.append((x, y))
    step[idx] = [[-1] * n for _ in range(n)]
    step[idx][x][y] = 0

    while q:
        x, y = q.popleft()
        for k in range(4):
            nx = x + dx[k]
            ny = y + dy[k]

            if not (0 <= nx < n and 0 <= ny < n) or cantMove[nx][ny]:
                continue

            if step[idx][nx][ny] == -1 or step[idx][nx][ny] > step[idx][x][y]+1:
                step[idx][nx][ny] = step[idx][x][y]+1
                q.append((nx, ny))
time = 0
answer = 0
res = [False] * m
while answer < m:
    time+=1

    # 격자에 있는 사람들 모두가 본인이 가고 싶은 편의점 방향을 향해서 1 칸 움직입니다.
    # 최단거리로 움직이며 최단 거리로 움직이는 방법이 여러가지라면
    # ↑, ←, →, ↓ 의 우선 순위로 움직이게 됩니다.
    # 여기서 최단거리라 함은 상하좌우 인접한 칸 중 이동가능한 칸으로만 이동하여 도달하기까지
    # 거쳐야 하는 칸의 수가 최소가 되는 거리를 뜻합니다.

    for _ in range(len(people)):
        person = people.popleft()
        idx, x, y = person
        if res[idx]:
            continue

        # step 조정
        movePerson(idx, stores[idx][0], stores[idx][1])
        toX, toY = -1, -1
        # 최소 step인 곳으로 이동
        distance = float('inf')
        for k in range(4):
            nx = x + dx[k]
            ny = y + dy[k]

            if not (0 <= nx < n and 0 <= ny < n):
                continue

            if not cantMove[nx][ny] and step[idx][nx][ny] != -1:
                if step[idx][nx][ny] == 0:
                    answer += 1
                    res[idx] = True
                    break
                if distance > step[idx][nx][ny]:
                    distance = step[idx][nx][ny]
                    toX, toY = nx, ny
        people.append((idx, toX, toY))

    # 격자에 있는 사람들이 모두 이동한 뒤에 해당 칸을 지나갈 수 없어짐에 유의합니다.
    for i in range(m):
        if res[i] and not cantMove[stores[i][0]][stores[i][1]]:
            cantMove[stores[i][0]][stores[i][1]] = True

    #만약 편의점에 도착한다면 해당 편의점에서 멈추게 되고,
    # 이때부터 다른 사람들은 해당 편의점이 있는 칸을 지나갈 수 없게 됩니다.
    # 격자에 있는 사람들이 모두 이동한 뒤에 해당 칸을 지나갈 수 없어짐에 유의합니다.

    # 현재 시간이 t분이고 t ≤ m를 만족한다면, t번 사람은 자신이 가고 싶은 편의점과
    # 가장 가까이 있는 베이스 캠프에 들어갑니다.
    # 여기서 가장 가까이에 있다는 뜻 역시 1에서와 같이 최단거리에 해당하는 곳을 의미합니다.
    # 가장 가까운 베이스캠프가 여러 가지인 경우에는 그 중 행이 작은 베이스캠프,
    # 행이 같다면 열이 작은 베이스 캠프로 들어갑니다.
    # t번 사람이 베이스 캠프로 이동하는 데에는 시간이 전혀 소요되지 않습니다.
    # 이때부터 다른 사람들은 해당 베이스 캠프가 있는 칸을 지나갈 수 없게 됩니다.
    # t번 사람이 편의점을 향해 움직이기 시작했더라도 해당 베이스 캠프는 앞으로 절대 지나갈 수 없음에
    # 유의합니다.

    # 마찬가지로 격자에 있는 사람들이 모두 이동한 뒤에 해당 칸을 지나갈 수 없어짐에 유의합니다.
    if time <= m:
        idx = time-1
        # 편의점과 가장 가까운 베이스 캠프
        movePerson(idx, stores[idx][0], stores[idx][1])
        distance = float('inf')
        baseX, baseY = -1, -1
        for i in range(n):
            for j in range(n):
                if board[i][j] == 1 and step[idx][i][j] != -1 and distance> step[idx][i][j]:
                    distance = step[idx][i][j]
                    baseX = i
                    baseY = j
        people.append([idx, baseX, baseY])
        cantMove[baseX][baseY] = True

print(time)