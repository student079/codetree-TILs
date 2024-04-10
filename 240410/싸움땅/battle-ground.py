# n * n 격자
# 플레이어 각각의 방향
# 격자 벗어나면 반대 방향
# 플레이어가 없다면 총이 있는지 확인
# 가지고 있는 총과 공격력 비교해서 더 높은거
# 낮은거는 내려놓기
# 플레이어가 있으면 초기 능력치 + 공격력으로 비교
# 같으면 초기 능력치 높은 순
# 차이만큼 포인트 획득
# 진플레이어는 총 내려놓고 이동
# 다른 플레이어 있거나 격자 바깥이면 오른쪽 90도 회전해서 빈칸 있으면 이동
# 총이 있으면 공격력 놓은 총 획득
# 총이 여러개 있을 수도 -> 큰거만 저장하기 보다는 딕셔너리 좌표로 총들 공격력 리스트 저장
# 이긴플레이어는 떨어져있는 총들과 가지고 있던 총 중 공격력이 높은 총 획득하고 나머지는 내려놓기

import sys
from collections import defaultdict

n, m, k = map(int,sys.stdin.readline().rstrip().split())
board = []
for _ in range(n):
    board.append(list(map(int,sys.stdin.readline().rstrip().split())))

weapons = defaultdict(list)
for i in range(n):
    for j in range(n):
        at = board[i][j]
        if at > 0:
            weapons[(i,j)].append(at)
        board[i][j] = -1

# board에 플레이어 위치, 인덱스 저장
players = []
for idx in range(m):
    x, y, d, s = map(int,sys.stdin.readline().rstrip().split())
    board[x-1][y-1] = idx
    # 방향, 초기능력치, 무기 공격력, x, y
    players.append((d,s,0,x-1 ,y-1))

dx = (-1, 0, 1, 0)
dy = (0, 1, 0, -1)
points = [0]*m

for _ in range(k):
    # 플레이어 순서대로 이동
    for idx in range(m):
        d, startStat, weaponStat,x, y = players[idx]
        board[x][y] = -1

        nx = x + dx[d]
        ny = y + dy[d]

        if not (0 <= nx < n and 0 <= ny < n):
            d = (d+2) % 4
            nx = x + dx[d]
            ny = y + dy[d]

        # 가는 곳에 플레이어 있는지
        if board[nx][ny] >= 0:
            # 싸우기
            opPlayerIdx = board[nx][ny]
            opPlayerD, opPlayerStartStat, opPlayerWeaponStat, opPlayerX, opPlayerY = players[opPlayerIdx]

            if startStat + weaponStat > opPlayerStartStat+opPlayerWeaponStat:
                points[idx] += (startStat + weaponStat) - (opPlayerStartStat+opPlayerWeaponStat)
                # 진 플레이어 총 놓기
                if opPlayerWeaponStat > 0:
                    weapons[(nx, ny)].append(opPlayerWeaponStat)
                    opPlayerWeaponStat = 0
                # 진 플레이어 이동
                while True:
                    opNX, opNY = opPlayerX + dx[opPlayerD], opPlayerY + dy[opPlayerD]
                    if (not (0 <= opNX < n and 0 <= opNY < n)) or board[opNX][opNY] >= 0:
                        opPlayerD = (opPlayerD+1) % 4
                    else:
                        board[opNX][opNY] = opPlayerIdx
                        # 총있으면 먹기
                        if weapons[(opNX, opNY)]:
                            weapons[(opNX, opNY)].sort(reverse=True)
                            opPlayerWeaponStat = weapons[(opNX, opNY)].pop(0)
                        opPlayerX, opPlayerY = opNX, opNY
                        break
                players[opPlayerIdx] = (opPlayerD, opPlayerStartStat, opPlayerWeaponStat, opPlayerX, opPlayerY)

                # 이긴 플레이어 총 먹기
                if weapons[(nx,ny)]:
                    weapons[(nx,ny)].sort(reverse=True)
                    if weapons[(nx,ny)][0] > weaponStat:
                        weapons[(nx, ny)].append(weaponStat)
                        weaponStat = weapons[(nx,ny)].pop(0)

                # 방향, 초기능력치, 무기 공격력, x, y
                players[idx] = (d, startStat, weaponStat, nx, ny)
                board[nx][ny] = idx

            elif startStat + weaponStat == opPlayerStartStat+opPlayerWeaponStat:
                if startStat > opPlayerStartStat:
                    # 진 플레이어 총 놓기
                    if opPlayerWeaponStat > 0:
                        weapons[(nx, ny)].append(opPlayerWeaponStat)
                        opPlayerWeaponStat = 0
                    # 진 플레이어 이동
                    while True:
                        opNX, opNY = opPlayerX + dx[opPlayerD], opPlayerY + dy[opPlayerD]
                        if (not (0 <= opNX < n and 0 <= opNY < n)) or board[opNX][opNY] >= 0:
                            opPlayerD = (opPlayerD + 1) % 4
                        else:
                            board[opNX][opNY] = opPlayerIdx
                            # 총있으면 먹기
                            if weapons[(opNX, opNY)]:
                                weapons[(opNX, opNY)].sort(reverse=True)
                                opPlayerWeaponStat = weapons[(opNX, opNY)].pop(0)
                            opPlayerX, opPlayerY = opNX, opNY
                            break
                    players[opPlayerIdx] = (opPlayerD, opPlayerStartStat, opPlayerWeaponStat, opPlayerX, opPlayerY)

                    # 이긴 플레이어 총 먹기
                    if weapons[(nx, ny)]:
                        weapons[(nx, ny)].sort(reverse=True)
                        if weapons[(nx, ny)][0] > weaponStat:
                            weapons[(nx, ny)].append(weaponStat)
                            weaponStat = weapons[(nx, ny)].pop(0)

                    # 방향, 초기능력치, 무기 공격력, x, y
                    players[idx] = (d, startStat, weaponStat, nx, ny)
                    board[nx][ny] = idx
                else:
                    # 진 플레이어 총 놓기
                    if weaponStat > 0:
                        weapons[(nx, ny)].append(weaponStat)
                        weaponStat = 0
                    # 진 플레이어 이동
                    while True:
                        nnx, nny = nx + dx[d], ny + dy[d]
                        if (not (0 <= nnx < n and 0 <= nny < n)) or board[nnx][nny] >= 0:
                            d = (d + 1) % 4
                        else:
                            board[nnx][nny] = idx
                            # 총있으면 먹기
                            if weapons[(nnx, nny)]:
                                weapons[(nnx, nny)].sort(reverse=True)
                                weaponStat = weapons[(nnx, nny)].pop(0)
                            nx, ny = nnx, nny
                            break
                    players[idx] = (d, startStat, weaponStat, nx, ny)

                    # 이긴 플레이어 총 먹기
                    if weapons[(opPlayerX, opPlayerY)]:
                        weapons[(opPlayerX, opPlayerY)].sort(reverse=True)
                        if weapons[(opPlayerX, opPlayerY)][0] > opPlayerWeaponStat:
                            weapons[(opPlayerX, opPlayerY)].append(opPlayerWeaponStat)
                            opPlayerWeaponStat = weapons[(opPlayerX, opPlayerY)].pop(0)

                    # 방향, 초기능력치, 무기 공격력, x, y
                    players[opPlayerIdx] = (opPlayerD, opPlayerStartStat, opPlayerWeaponStat, opPlayerX, opPlayerY)
                    board[opPlayerX][opPlayerY] = opPlayerIdx
            else:
                points[opPlayerIdx] += (opPlayerStartStat + opPlayerWeaponStat) - (startStat + weaponStat)
                # 진 플레이어 총 놓기
                if weaponStat > 0:
                    weapons[(nx, ny)].append(weaponStat)
                    weaponStat = 0
                # 진 플레이어 이동
                while True:
                    nnx, nny = nx + dx[d], ny + dy[d]
                    if (not (0 <= nnx < n and 0 <= nny < n)) or board[nnx][nny] >= 0:
                        d = (d + 1) % 4
                    else:
                        board[nnx][nny] = idx
                        # 총있으면 먹기
                        if weapons[(nnx,nny )]:
                            weapons[(nnx, nny)].sort(reverse=True)
                            weaponStat = weapons[(nnx, nny)].pop(0)
                        nx, ny = nnx, nny
                        break
                players[idx] = (d, startStat, weaponStat, nx, ny)

                # 이긴 플레이어 총 먹기
                if weapons[(opPlayerX, opPlayerY)]:
                    weapons[(opPlayerX, opPlayerY)].sort(reverse=True)
                    if weapons[(opPlayerX, opPlayerY)][0] > opPlayerWeaponStat:
                        weapons[(opPlayerX, opPlayerY)].append(opPlayerWeaponStat)
                        opPlayerWeaponStat = weapons[(opPlayerX, opPlayerY)].pop(0)

                # 방향, 초기능력치, 무기 공격력, x, y
                players[opPlayerIdx] = (opPlayerD, opPlayerStartStat, opPlayerWeaponStat, opPlayerX, opPlayerY)
                board[opPlayerX][opPlayerY] = opPlayerIdx

        # 플레이어 없음
        else:
            # 총있으면 자기거랑 비교하고 가장 센 총 줍기
            if weapons[(nx,ny)]:
                weapons[(nx,ny)].sort(reverse=True)
                if weapons[(nx,ny)][0] > weaponStat:
                    if weaponStat > 0:
                        weapons[(nx, ny)].append(weaponStat)
                    weaponStat = weapons[(nx,ny)].pop(0)

            # 방향, 초기능력치, 무기 공격력, x, y
            players[idx] = (d, startStat, weaponStat, nx, ny)
            board[nx][ny] = idx
print(points)