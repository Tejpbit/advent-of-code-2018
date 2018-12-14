f = open("data/03.data")
lines = f.readlines()

fabricMatrix = [[[] for x in range(1000)] for x in range(1000)]
#fabricMatrix = [[[] for x in range(8)] for x in range(8)]

# lines = [
#    "#1 @ 1,3: 4x4\n",
#    "#2 @ 3,1: 4x4\n",
#    "#3 @ 5,5: 2x2\n"
# ]


def parseInts(int_str, divider, trash):
    int_str = int_str.replace(trash, "")
    parts = int_str.split(divider)
    return (int(parts[0]), int(parts[1]))


for line in lines:
    #    #1 @ 53,238: 26x24
    parts = line.split(" ")
    id = int(parts[0][1:])
    (x, y) = parseInts(parts[2], ',', ':')
    (w, h) = parseInts(parts[3], 'x', '\n')

    for a in range(x, x+w):
        for b in range(y, y+h):
            fabricMatrix[a][b] += [id]


def printFabricMatrix(fabricMatrix):
    overlapping = 0
    for column in fabricMatrix:
        for cell in column:
            if len(cell) == 0:
                #print(".", end="", flush=False)
                pass
            elif len(cell) == 1:
                #print(cell[0], end="", flush=False)
                pass
            else:
                #print("x", end="", flush=False)
                overlapping += 1
        # print(flush=False)
    print("Number of overlapping square inches:", overlapping, flush=True)


printFabricMatrix(fabricMatrix)


def notOverlaps(fabricMatrix, x, y, w, h):
    for a in range(x, x+w):
        for b in range(y, y+h):
            if len(fabricMatrix[a][b]) > 1:
                return False
    return True


for line in lines:
    parts = line.split(" ")
    id = int(parts[0][1:])
    (x, y) = parseInts(parts[2], ',', ':')
    (w, h) = parseInts(parts[3], 'x', '\n')

    if notOverlaps(fabricMatrix, x, y, w, h):
        print("Non overlap id:", id)
