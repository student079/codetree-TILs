import sys

N, M, P, C, D = map(int, sys.stdin.readline().rstrip().split())
board = [[0] * N for _ in range(N)]
luR, luC = map(int, sys.stdin.readline().rstrip().split())
luR -= 1
luC -= 1
board[luR][luC] = -1
santas = []
scores = [0] * (P + 1)
fails = [False] * (P + 1)
failSantaCount = 0


def getDistance(r1, c1, r2, c2):
    return (r1 - r2) ** 2 + (c1 - c2) ** 2


def howMoveLu(luR, luC, toX, toY):
    r = toX - luR
    c = toY - luC

    if r > 0:
        r = min(1, r)
    elif r < 0:
        r = max(-1, r)
    if c > 0:
        c = min(1, c)
    elif c < 0:
        c = max(-1, c)
    return (r, c)


def getCloseSantaDirection(luR, luC, santas):
    sortedSantas = sorted(santas, key=lambda x: (x[1], x[2]), reverse=True)

    toX, toY = None, None
    distance = float("inf")
    for santaIndex, sR, sC, _ in sortedSantas:
        if fails[santaIndex]:
            continue
        currentDistance = getDistance(luR, luC, sR, sC)
        if currentDistance < distance:
            toX = sR
            toY = sC
            distance = currentDistance

    return howMoveLu(luR, luC, toX, toY)


def shock(santaIndex, toX, toY, weight):
    _, sR, sC, dizzy = santas[santaIndex - 1]
    resultX, resultY = sR + toX * weight, sC + toY * weight
    if 0 <= resultX < N and 0 <= resultY < N:
        otherSantaIndex = board[resultX][resultY]
        if otherSantaIndex != 0:
            shock(otherSantaIndex, toX, toY, 1)
        board[resultX][resultY] = santaIndex
        santas[santaIndex - 1] = [santaIndex, resultX, resultY, dizzy]
    else:
        fails[santaIndex] = True


def moveLu(luR, luC, toX, toY, step):
    board[luR][luC] = 0

    santaIndex = board[luR + toX][luC + toY]

    if santaIndex != 0:
        scores[santaIndex] += C
        santas[santaIndex - 1][3] = step + 1
        shock(santaIndex, toX, toY, C)
    board[luR + toX][luC + toY] = -1
    return (luR + toX, luC + toY)


dx = (-1, 0, 1, 0)
dy = (0, 1, 0, -1)


def moveSan(luR, luC, santas, step):
    for santaIndex, sR, sC, dizzy in santas:
        if fails[santaIndex] or dizzy >= step:
            continue

        # 현재 산타랑 루돌프 거리로 초기화
        distance = getDistance(luR, luC, sR, sC)
        toX, toY = sR, sC
        toK = -1
        for k in range(4):
            nx = sR + dx[k]
            ny = sC + dy[k]
            currentDistance = getDistance(luR, luC, nx, ny)
            if distance < currentDistance:
                continue

            if not (0 <= nx < N and 0 <= ny < N):
                continue

            if board[nx][ny] > 0:
                continue

            if distance > currentDistance:
                distance = currentDistance
                toX = nx
                toY = ny
                toK = k

        if sR == toX and sC == toY:
            continue

        board[sR][sC] = 0
        if board[toX][toY] == -1:
            scores[santaIndex] += D
            santas[santaIndex - 1] = [santaIndex, toX, toY, step + 1]
            shock(santaIndex, dx[toK] * -1, dy[toK] * -1, D)
        else:
            board[toX][toY] = santaIndex
            santas[santaIndex - 1] = [santaIndex, toX, toY, dizzy]


for _ in range(P):
    santaIndex, sR, sC = map(int, sys.stdin.readline().rstrip().split())
    board[sR - 1][sC - 1] = santaIndex
    santas.append([santaIndex, sR - 1, sC - 1, 0])

santas.sort()
for step in range(1, M+1):
    if fails.count(True) == P:
        break

    toX, toY = getCloseSantaDirection(luR, luC, santas)
    luR, luC = moveLu(luR, luC, toX, toY, step)
    moveSan(luR, luC, santas, step)

    for i in range(1, P + 1):
        if not fails[i]:
            scores[i] += 1

print(*scores[1:])