# n * n 격자
# BFS로 그룹 설정
# -> 그룹 구역 설정할 배열 하나 더 생성
# -> 고유 인덱스로 어느 그룹인지 구분
# -> 리스트로 인덱스, 칸수, 고유 숫자 저장
# 예술 점수
# 다른 그룹과 맞닿아 있는 변의 수
# -> 그룹 구역 배열에 bfs 돌려서 그 인덱스랑 같은 번호 개수
# visited 잘 관리
# 모든 그룹 조합 점수 합 -> 초기 예술점수

# 그림 회전
# 십자모양, 그 외 부분
# 십자모양 - 반시계 90도 회전
# -> xy값 바꾸기
# 그 외부분 - 시계 90도 회전
# 가로 뜯어서 오른쪽부터 넣기
# 예술점수 구하기

# 3회전이후 예술점수 까지

# 예술점수 구하는 함수

# 회전 함수

import sys
from collections import deque
from itertools import combinations

n = int(sys.stdin.readline())
board = []
for _ in range(n):
    board.append(list(map(int,sys.stdin.readline().rstrip().split())))

dx = (0, 1, 0, -1)
dy = (1, 0, -1, 0)

def groupBfs(board, idx, i, j, groupBoard):
    number = board[i][j]
    q = deque()
    cnt = 1
    q.append((i,j))

    while q:
        x, y = q.popleft()

        for k in range(4):
            nx = x + dx[k]
            ny = y + dy[k]

            if not (0 <= nx < n and 0 <= ny < n):
                continue

            if groupBoard[nx][ny] == -1 and board[nx][ny] == number:
                cnt += 1
                groupBoard[nx][ny] = idx
                q.append((nx,ny))

    # -> 리스트로 인덱스, 칸수, 고유 숫자 저장
    return (idx, cnt, number)

def scoreBfs(a, b, groupBoard):
    visited = [[False] * n for _ in range(n)]

    cnt = 0
    for i in range(n):
        for j in range(n):
            if groupBoard[i][j] == a:
                q = deque()
                visited[i][j] = True
                q.append((i,j))

                while q:
                    x, y = q.popleft()

                    for k in range(4):
                        nx = x + dx[k]
                        ny = y + dy[k]

                        if not (0 <= nx < n and 0 <= ny < n):
                            continue

                        if groupBoard[nx][ny] == b:
                            cnt += 1
                        elif groupBoard[nx][ny] == a:
                            if not visited[nx][ny]:
                                q.append((nx, ny))
                                visited[nx][ny] = True
                return cnt


def rotate90rev(board):
    newBoard = [[-1] * n for _ in range(n)]

    i = n//2
    j = n//2
    row = board[i][:]
    col = []
    for k in range(n):
        col.append(board[k][j])

    # row를 col 반대로
    # col을 row로
    for k in range(n):
        newBoard[k][j] = row.pop()
    newBoard[i] = col[:]

    return newBoard


# 3회전 까지
# 그룹 설정
answer = 0
groups = []
groupBoard = [[-1] * n for _ in range(n)]
idx = 0

for i in range(n):
    for j in range(n):
        if groupBoard[i][j] == -1:
            groupBoard[i][j] = idx
            groups.append(groupBfs(board, idx, i, j, groupBoard))
            idx += 1

groupLen = len(groups)
comb = list(combinations(range(groupLen), 2))

# group: 인덱스, 칸수, 고유 숫자 저장

for c in comb:
    a, b = c
    # 맞닿아있는 변의 수
    answer += (groups[a][1] + groups[b][1]) * groups[a][2] * groups[b][2] * scoreBfs(a, b, groupBoard)

for _ in range(3):
    # 그림 회전
    newBoard= rotate90rev(board)

    # 구역 나눠서 그림 회전
    c = n//2
    #왼쪽 위
    for i in range(0,c):
        for j in range(0,c):
            newBoard[j][c-1-i] = board[i][j]
    #오른쪽 위
    for i in range(0,c):
        for j in range(c+1,n):
            #대칭이동
            oldX, oldY = i, j - c - 1
            newX, newY = oldY, c-1-oldX
            newBoard[newX][newY+c+1] = board[i][j]
    # 왼쪽 아래
    for i in range(c+1,n):
        for j in range(0,c):
            #대칭이동
            oldX, oldY = i - (c+1), j
            newX, newY = oldY, c-1-oldX
            newBoard[newX + c+1][newY] = board[i][j]
    # 오른쪽 아래
    for i in range(c+1, n):
        for j in range(c+1,n):
            oldX, oldY = i - (c+1), j - (c+1)
            newX, newY = oldY, c-1-oldX
            newBoard[newX+c+1][newY+c+1] = board[i][j]


    groups = []
    groupBoard = [[-1] * n for _ in range(n)]
    idx = 0

    for i in range(n):
        for j in range(n):
            if groupBoard[i][j] == -1:
                groupBoard[i][j] = idx
                groups.append(groupBfs(newBoard,idx, i, j, groupBoard))
                idx += 1

    groupLen = len(groups)
    comb = list(combinations(range(groupLen), 2))

    # group: 인덱스, 칸수, 고유 숫자 저장

    for c in comb:
        a, b = c
        # 맞닿아있는 변의 수
        answer += (groups[a][1] + groups[b][1]) * groups[a][2] * groups[b][2] * scoreBfs(a, b, groupBoard)

    board = newBoard

print(answer)