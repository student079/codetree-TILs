# 주어진 선따라 이동
# 각팀마다 머리사람 따라 이동
# 라운드마다 공 던짐
# 최초에 공 만나는 사람 점수
# 머리사람 부터 k 번째면 K*K 만큼 점수 추가
# 점수 얻으면 머리사람과 꼬리사람이 바뀜 -> 방향 바뀜

# 격자판 n 3~20
# 팀 수 m 1 ~ 5
# 라운드 수 k 1~1000
# 0 은 빈칸, 1은 머리사람, 2는 머리사람과 꼬리사람이 아닌 나머지, 3은 꼬리사람, 4는 이동 선
# 이동 선 안겹침
# 팀 최소 세명

import sys
from collections import deque

n, m, k = map(int,sys.stdin.readline().rstrip().split())
board = []
for _ in range(n):
    board.append(list(map(int, sys.stdin.readline().rstrip().split())))
dx = (0, -1, 0, 1)
dy = (1, 0, -1, 0)
def searchPeople(x, y):
    people = deque([[x, y]])
    while True:
        for k in range(4):
            nx = x + dx[k]
            ny = y + dy[k]

            if not (0 <= nx < n and 0 <= ny < n):
                continue

            if board[nx][ny] == 3:
                people.append([nx, ny])
                return people
            elif board[nx][ny] == 2 and [nx, ny] not in people:
                people.append([nx, ny])
                x = nx
                y = ny
                break

def moveTeam(team):
    for idx in range(len(team)):
        x, y = team.popleft()
        for k in range(4):
            nx = x + dx[k]
            ny = y + dy[k]

            if not (0 <= nx < n and 0 <= ny < n):
                continue

            if idx == 0:
                if board[nx][ny] == 4:
                    team.append([nx, ny])
                    board[nx][ny] = board[x][y]
                    board[x][y] = -1
                    break
            else:
                if board[nx][ny] == -1:
                    team.append([nx, ny])
                    board[nx][ny] = board[x][y]
                    if idx == len(team) - 1:
                        board[x][y] = 4
                    else:
                        board[x][y] = -1
                    break

def throwBall(round, teams):
    direction = (round//n)%4
    distance = round%n
    
    if direction %2 == 0:
        x, y = distance, 0
    else:
        x, y = 0 ,distance
        
    addX = dx[direction]
    addY = dy[direction]

    for _ in range(n):
        if board[x][y] in (1,2,3):
            # 팀에서 몇번째인지 찾기
            for idxTeam in range(m):
                for idxPerson in range(len(teams[idxTeam])):
                    if x == teams[idxTeam][idxPerson][0] and y == teams[idxTeam][idxPerson][1]:
                        # 꼬리, 머리 바꾸기
                        head = teams[idxTeam].popleft()
                        tail = teams[idxTeam].pop()
                        board[head[0]][head[1]] = 3
                        board[tail[0]][tail[1]] = 1
                        teams[idxTeam].append(head)
                        teams[idxTeam].appendleft(tail)

                        # 점수 추가
                        return (idxPerson+1)**2

        x += addX
        y += addY

teams = []
# 팀별 사람 좌표 넣기
for i in range(n):
    for j in range(n):
        if board[i][j] == 1:
            people = searchPeople(i, j)
            teams.append(people)

# 라운드 0,1, 2 증가하다가 n 이랑 같으면 나누고 나머지
# 함수로 빼자
answer = 0

for round in range(k):
    # 머리사람 따라 한칸 이동
    for team in teams:
        moveTeam(team)

    # 공 던지기 + 사람 있는지 + 팀 머리꼬리 방향 바꾸고
    answer += throwBall(round, teams)
print(answer)