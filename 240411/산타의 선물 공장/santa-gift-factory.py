import sys
from collections import deque

q = int(sys.stdin.readline())
weights = dict()
def make(command):
    n, m = command[1], command[2]
    boxes = deque(command[3:])
    for i in range(n):
        weights[boxes[i]] = boxes[n + i]
    belts = []
    for _ in range(m):
        temp = deque()
        for _ in range(n // m):
            temp.append(boxes.popleft())
        belts.append(temp)
    return (belts, n, m)

command = list(map(int, sys.stdin.readline().rstrip().split()))
belts, n, m = make(command)
brokenBelt = [False] * m

def get(w_max):
    weight = 0
    for idx in range(m):
        belt = belts[idx]
        if not belt:
            continue
        if weights[belt[0]] <= w_max:
            weight += weights[belt.popleft()]
        else:
            belt.append(belt.popleft())
    return weight


def remove(r_id):
    for idx in range(m):
        belt = belts[idx]
        if r_id in belt:
            belt.remove(r_id)
            return r_id
    return -1


def check(f_id):
    for idx in range(m):
        belt = belts[idx]

        if f_id in belt:
            while True:
                if belt[0] == f_id:
                    return idx + 1
                else:
                    belt.append(belt.popleft())
    return -1


def breakdown(b_num):
    b_num-=1
    if brokenBelt[b_num]:
        return -1

    g_num = (b_num+1) % m
    while True:
        if not brokenBelt[g_num]:
            belts[g_num].extend(belts[b_num])
            belts[b_num] = deque()
            brokenBelt[b_num] = True
            return b_num+1
        g_num = (g_num+1) % m


for _ in range(q-1):
    command = list(map(int,sys.stdin.readline().rstrip().split()))
    if command[0] == 200:
        print(get(command[1]))
    elif command[0] == 300:
        print(remove(command[1]))
    elif command[0] == 400:
        print(check(command[1]))
    elif command[0] == 500:
        print(breakdown(command[1]))