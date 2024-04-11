# 최단거리 bfs ↑, ←, →, ↓ 의 우선 순위
# 편의점 도착하면 다른 사람들은 해당 편의점 칸 이동 X
# 베이스 캠프도 마찬가지, 즉 이후 절대 못지나가는 칸 있음

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
visited = [[[False] * n for _ in range(n)] for _ in range(m)]
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

        for k in range(4):
            nx = x + dx[k]
            ny = y + dy[k]

            if not (0 <= nx < n and 0 <= ny < n):
                continue


            if not cantMove[nx][ny] and not visited[idx][nx][ny]:
                if (nx,ny) == stores[idx]:
                    answer += 1
                    res[idx] = True
                    break

                visited[idx][nx][ny] = True
                people.append((idx, nx,ny))

    # 격자에 있는 사람들이 모두 이동한 뒤에 해당 칸을 지나갈 수 없어짐에 유의합니다.
    for i in range(m):
        if res[i] and not cantMove[stores[i][0]][stores[i][1]]:
            cantMove[stores[i][0]][stores[i][1]] = True
            for _ in range(len(people)):
                idx, x, y = people.popleft()
                if idx == i or (x, y) == stores[i]:
                    continue
                else:
                    people.append((idx,x,y))

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
    # 유의합니다. 마찬가지로 격자에 있는 사람들이 모두 이동한 뒤에 해당 칸을 지나갈 수 없어짐에
    # 유의합니다.
    if time <= m:
        idx = time-1
        # 편의점과 가장 가까운 베이스 캠프
        baseX, baseY = computeNarrowBase(stores[idx][0], stores[idx][1])
        people.append([idx, baseX, baseY])
        for _ in range(len(people)):
            i, x, y = people.popleft()
            if i != idx and (x, y) == (baseX, baseY):
                continue
            else:
                people.append((i,x,y))
        cantMove[baseX][baseY] = True

print(time)