# LXL 체스판

# 연쇄적으로 밀리는데 벽이 막고 있으면 모든 기사는 이동 X

dx = (-1, 0, 1, 0)
dy = (0, 1, 0, -1)

# 초기 기사들의 체력은 유지하고

# 기사들 체력 관리할 변수 하나씩 더 만들어 관리

# 사라진 기사 명령은 넘기고

# 기사 밀기 -> 벽있으면 못민다
# dfs, 백트래킹으로 구현

# 밀려난 곳에 함정이 있다면 데미지
# -> 밀린 이후에 함정 확인
# 명령받은 기사는 피해를 입지 않는다
import sys
import copy
L, N, Q = map(int,sys.stdin.readline().rstrip().split())

originK = [0] * (N+1)
board = []
for _ in range(L):
    board.append(list(map(int,sys.stdin.readline().rstrip().split())))
knights = [[]]
kBoard = [[0] * L for _ in range(L)]
for idx in range(1, N+1):
    # 좌상단, 우하단으로 저장하자
    r, c, h, w, k = map(int,sys.stdin.readline().rstrip().split())
    x1, y1, x2, y2 = r-1, c-1, r-1+h-1, c-1+w-1
    knights.append([x1,y1,x2,y2, k])
    for i in range(x1, x2+1):
        for j in range(y1, y2+1):
            kBoard[i][j] = idx
    originK[idx] = k

# dfs로 기사 밀기
flag = True

moved = [False] * (N+1)
def move(idx, d, visited):
    global flag

    if not flag:
        return False

    x1, y1, x2, y2, k = knights[idx]

    # 방향대로 좌상단 우상단 이동
    nx1 = x1 + dx[d]
    ny1 = y1 + dy[d]
    nx2 = x2 + dx[d]
    ny2 = y2 + dy[d]

    # 벽이면 이동 X
    if not ( 0<= nx1 < L and 0 <= ny1 < L and 0 <= nx2 < L and 0<=ny2 < L):
        return False

    # 벽이 아니고
    # 다른 기사 있는지
    # 이동한 범위 확인해서 포함된 기사 idx 넣기
    pushed = set()
    for i in range(nx1, nx2 + 1):
        for j in range(ny1, ny2 + 1):
            if kBoard[i][j] != idx and kBoard[i][j]>0:
                pushed.add(kBoard[i][j])
            if board[i][j] == 2:
                return False

    # 재귀로 move호출
    for pushedIdx in list(pushed):
        if pushedIdx not in visited:
            visited.add(pushedIdx)
            flag = move(pushedIdx, d, copy.deepcopy(visited))

    if flag:
        for i in range(x1, x2 + 1):
            for j in range(y1, y2 + 1):
                if kBoard[i][j] == idx:
                    kBoard[i][j] = 0
        for i in range(nx1, nx2 + 1):
            for j in range(ny1, ny2 + 1):
                kBoard[i][j] = idx
        knights[idx] = [nx1, ny1, nx2, ny2, k]
        moved[idx] = True
        return True
    return False
    #재귀 리턴하면서 이동 못했으면 자기도 원래 위치로

def trap(idx):
    for index in range(1,N+1):
        if index == idx:
            continue

        if not moved[index]:
            continue

        x1, y1, x2, y2, k = knights[index]

        cnt = 0
        for i in range(x1, x2+ 1):
            for j in range(y1, y2+1):
                if board[i][j] == 1:
                    cnt += 1

        k -= cnt

        # 사라지면 kboard도 지우기
        if k <= 0:
            for i in range(x1, x2 + 1):
                for j in range(y1, y2 + 1):
                    kBoard[i][j] = 0

        knights[index] = [x1, y1, x2, y2, k]


for _ in range(Q):
    idx, d = map(int,sys.stdin.readline().rstrip().split())

    # 기사 이동

    # 기사 체력 0이하면 넘어가기
    x1,y1,x2,y2,k = knights[idx]
    if k <= 0:
        continue

    flag = move(idx, d, set())
    # 이동햇는지 확인하고 이동 안했으면 체력 안깎음
    if not flag:
        flag = True
    else:
        # 자신외에 밀린 다른 기사들 함정 개수 해서 체력 깎기
        trap(idx)
    moved = [False] * (N+1)
answer = 0
for i in range(1, N+1):
    k = knights[i][4]
    if k <= 0:
        continue
    answer += originK[i] - k
print(answer)