# 시간 복잡도

import sys
from collections import deque
from collections import defaultdict

q = int(sys.stdin.readline())
command = list(map(int,sys.stdin.readline().rstrip().split()))
n, m = command[1], command[2]
command = command[3:]
boxes = defaultdict(list)
belts = []
idx = 0
brokenBelt = [False] * m
for i in range(m):
    temp = deque()
    for j in range(n//m):
        temp.append(command[idx])
        boxes[command[idx]] = [command[idx+n], i]
        idx += 1
    belts.append(temp)

def get(w_max):
    res = 0

    for i in range(m):
        if brokenBelt[i]:
            continue
        belt = belts[i]
        if belt:
            if boxes[belt[0]][0] <= w_max:
                box = belt.popleft()
                res += boxes[box][0]
                boxes[box][1] = -1
            else:
                belt.append(belt.popleft())
    return res

def remove(r_id):
    if not boxes[r_id] or boxes[r_id][1] == -1:
        return -1

    beltIdx = boxes[r_id][1]
    belt = belts[beltIdx]
    belt.remove(r_id)
    boxes[r_id][1] = -1
    return r_id

def check(f_id):
    if not boxes[f_id] or boxes[f_id][1] == -1:
        return -1

    beltIdx = boxes[f_id][1]
    bidx = belts[beltIdx].index(f_id)
    belts[beltIdx].extend(list(belts[beltIdx])[:bidx])
    belts[beltIdx] = deque(list(belts[beltIdx])[bidx:])
    return beltIdx + 1

def breakdown(b_num):
    b_num-=1
    if brokenBelt[b_num]:
        return -1

    g_num = (b_num+1)%m
    while True:
        if not brokenBelt[g_num]:
            brokenBelt[b_num] = True
            belt = belts[b_num]
            while belt:
                box = belt.popleft()
                boxes[box][1] = g_num
                belts[g_num].append(box)
            return b_num+1
        g_num = (g_num + 1) % m

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