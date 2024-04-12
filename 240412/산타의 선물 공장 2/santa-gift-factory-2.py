import sys

q = int(sys.stdin.readline())
command, n, m, *bNums = map(int,sys.stdin.readline().rstrip().split())
belts = []
for _ in range(n):
    # head, tail, count
    belts.append([-1,-1,0])

# prev
boxes = dict()
for i in range(m):
    box = i+1
    head, tail, count = belts[bNums[i]-1]
    if count == 0:
        head = box
        tail = box
        # prev, next
        boxes[box] = [-1,-1]
        count += 1
    else:
        boxes[tail][1] = box
        boxes[box] = [tail, -1]
        tail = box
        count += 1
    belts[bNums[i]-1] = [head, tail, count]

def allMove(m_src, m_dst):
    m_src-=1
    sHead, sTail, sCount = belts[m_src]
    m_dst-=1
    dHead, dTail, dCount = belts[m_dst]

    if sCount == 0:
        return dCount

    # 목적지가 0일 경우는?
    if dCount == 0:
        dTail = sTail
    else:
        boxes[sTail][1] = dHead
        boxes[dHead][0] = sTail
    dHead = sHead
    dCount += sCount
    sCount = 0
    sHead = -1
    sTail = -1

    belts[m_src] = [sHead, sTail, sCount]
    belts[m_dst] = [dHead, dTail, dCount]

    return dCount

def removeHead(bNum):
    head, tail, count = belts[bNum]
    if count == 0:
        return -1

    if count == 1:
        id = head
        head = boxes[head][1]
        tail = -1
        count -= 1
        belts[bNum] = [head, tail, count]
        return id

    id = head
    head = boxes[head][1]
    boxes[head][0] = -1
    count -= 1
    belts[bNum] = [head, tail, count]
    return id

def addHead(bNum, boxId):
    if boxId == -1:
        return

    head, tail, count = belts[bNum]

    if count == 0:
        head = boxId
        tail = boxId
        count += 1
        boxes[boxId] = [-1,-1]

    else:
        boxes[head][0] = boxId
        boxes[boxId][1] = head
        boxes[boxId][0] = -1
        head = boxId
        count += 1

    belts[bNum] = [head, tail, count]



def changeHead(m_src, m_dst):
    m_src -= 1
    m_dst -= 1

    srcId = removeHead(m_src)
    dstId = removeHead(m_dst)
    addHead(m_src, dstId)
    addHead(m_dst, srcId)

    return belts[m_dst][2]


def shareBoxes(m_src, m_dst):
    m_src -= 1
    m_dst -= 1
    sHead, sTail, sCount = belts[m_src]
    dHead, dTail, dCount = belts[m_dst]

    # 목적지 Head == -1일경우

    moveBoxCount = sCount//2
    if moveBoxCount > 0:
        c = 1
        box = sHead
        while c < moveBoxCount:
            c+=1
            box = boxes[box][1]

        nextBox = boxes[box][1]
        # 목적지 벨트 업데이트
        if dCount == 0:
            dHead = sHead
            dTail = box
            boxes[box][1] = -1
        else:
            boxes[dHead][0] = box
            boxes[box][1] = dHead
            dHead = sHead
        dCount += moveBoxCount

        # 소스벨트 업데이트
        sHead = nextBox
        sCount -= moveBoxCount
        boxes[sHead][0] = -1

        belts[m_src] = [sHead, sTail, sCount]
        belts[m_dst] = [dHead, dTail, dCount]

    return dCount

def getBoxInfo(p_num):
    return boxes[p_num][0] + 2 * boxes[p_num][1]

def getBeltInfo(b_num):
    b_num-=1
    head, tail, count = belts[b_num]
    return head + 2*tail + 3*count

for _ in range(q-1):
    command, *args = map(int,sys.stdin.readline().rstrip().split())

    if command == 200:
        print(allMove(args[0], args[1]))

    elif command == 300:
        print(changeHead(args[0], args[1]))

    elif command == 400:
        print(shareBoxes(args[0], args[1]))

    elif command == 500:
        print(getBoxInfo(args[0]))

    elif command == 600:
        print(getBeltInfo(args[0]))