# Q 50000
# N 50000
# 채점기 빈거 바로 가져와야하기 때문에 채점기 heapq
# 채점 시작, 채점 종료시간 기록

import sys
from heapq import heappop, heapify, heappush
from collections import defaultdict

Q = int(sys.stdin.readline())
command, N, u0 = sys.stdin.readline().rstrip().split()
command, N = int(command), int(N)
domain, id = u0.split('/')
id = int(id)

answer = 1
# 빈 채점기 빠르게 가져올 힙큐
judger = list(range(1,N+1))

# 채점기가 무슨 url 채점 중인가
judging = ["" for _ in range(N+1)]

readyQ = []
heappush(readyQ, (1, 0, domain, id))
# readyQ에 (우선순위, 들어온 시간, 도메인, id) 저장

# 도메인별 채점 시작, 채점 종료시간
history = defaultdict(list)

# 도메인별 id가 대기큐에 있는지
domains = defaultdict(set)
domains[domain].add(id)

def request(t, p, u):
    global answer
    # 레디큐에 넣기
    # 대기큐에 도메인과 id가 일치하는 url에 있는지
    domain, id = u.split('/')
    id = int(id)

    if id in domains[domain]:
        return

    else:
        domains[domain].add(id)
        readyQ.append((p, t, domain, id))
        answer += 1

def tryJudge(t):
    global answer

    # 채점기 빈거 없으면 안해
    if not judger:
        return

    heapify(readyQ)
    for idx in range(answer):
        priority, time, domain, id = readyQ[idx]
        # 도메인이 현재 채점 진행 중인지
        if history[domain] and history[domain][1] == -1:
            continue

        # 도메인의 최근 채점
        if history[domain] and history[domain][0] != -1 and  history[domain][1] != -1:
            start, end = history[domain]
            if t < start + 3 * (end - start):
                continue

        readyQ.pop(idx)
        jId = heappop(judger)
        judging[jId] = domain
        history[domain] = [t, -1]
        domains[domain].remove(id)
        answer -= 1
        return

def finish(t, J_id):
    if judging[J_id] == "":
        return

    history[judging[J_id]][1] = t
    judging[J_id] = ""
    heappush(judger, J_id)

for _ in range(Q-1):
    command, *args = sys.stdin.readline().rstrip().split()
    command = int(command)

    if command == 200:
        request(int(args[0]), int(args[1]), args[2])

    elif command == 300:
        tryJudge(int(args[0]))

    elif command == 400:
        finish(int(args[0]), int(args[1]))

    else:
        print(answer)
    # print(command, *args)
    # print(readyQ)
    # print(domains)
    # print(history)
    # print(judger)
    # print(judging)
    # print(answer)
    # print()