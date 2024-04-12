# Q 5만
# 2000번까지만 가능
# N개의 채점기 50000
# heapq로 대기 관리하면 logN으로 가능

import sys
import heapq
from collections import defaultdict

Q = int(sys.stdin.readline())
num, N, u0 = sys.stdin.readline().rstrip().split()
num, N = int(num), int(N)
#도메인별 관리
# (채점 시작 시간, 채점 종료시간)
# -1 이면 아직
domains = defaultdict(list)
domains[u0] = [-1, -1]

history = defaultdict(list)

# 채점기 5만개라 가능한 채점기 찾는거 힘든데
# 채점기도 우선순위 큐에 넣자
# 있는지 보고 있으면 빼고
# 없으면 넘기고
# 채점종료되면 다시 넣고
# logn이니까 가능
judger = list(range(1, N+1))

judging = ["" for _ in range(N+1)]

readyQ = []
# 우선순위 1, 들어온 시간 0, url
# heapq.heappush(readyQ, (1, 0, u0))
readyQ.append((1, 0, u0))
count = 1

def request(t, p, u):
    global count
    # 단, 채점 대기 큐에 있는 task 중 정확히 u와 일치하는 url이 단 하나라도 존재한다면
    # 큐에 추가하지 않고 넘어갑니다.

    # 있는지 확인
    if domains[u] and domains[u][0] == -1:
        return

    else:
        domains[u] = [-1, -1]
        # heapq.heappush(readyQ, (p, t, u))
        readyQ.append((p, t, u))
        count += 1
        return

def tryJugge(t):
    global count

    # 채점기 확인
    if not judger:
        return

    # readyQ에서 확인해서 가능하면 빼기
    heapq.heapify(readyQ)
    for idx in range(count):
        # priority, inTime, dm = heapq.heappop(readyQ)
        priority, inTime, dm = readyQ[idx]
        plainDomain = dm.split('/')[0]

        # 진행중인 도메인인지
        if domains[dm] and domains[dm][0] != -1 and domains[dm][1] == -1:
            # heapq.heappush(readyQ, (priority, inTime, dm))
            continue

        # 최근 진행된 채점 시간 체크
        if history[plainDomain]:
            start, end = history[plainDomain]
            if end == -1:
                # heapq.heappush(readyQ, (priority, inTime, dm))
                continue
            if t < start + 3 * (end - start):
                # heapq.heappush(readyQ, (priority, inTime, dm))
                continue

        readyQ.pop(idx)
        judging[heapq.heappop(judger)] = dm
        domains[dm][0] = t
        count-=1
        history[plainDomain] = [t, -1]
        return

    return

def finish(t, J_id):

    # 채점 종료
    if judging[J_id] == "":
        return

    dm = judging[J_id]
    # 채점기 채점 중 업데이트
    judging[J_id] = ""

    # domain 업데이트
    domains[dm][1] = t

    # history 업데이트
    plainDomain = dm.split('/')[0]
    history[plainDomain][1] = t

    # 채점기 다시 넣기
    heapq.heappush(judger, J_id)


for _ in range(Q-1):
    num, *args = sys.stdin.readline().rstrip().split()
    num = int(num)

    if num == 200:
        request(int(args[0]), int(args[1]), args[2])

    elif num == 300:
        tryJugge(int(args[0]))

    elif num == 400:
        finish(int(args[0]), int(args[1]))

    else:
        print(count)