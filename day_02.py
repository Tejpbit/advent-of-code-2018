import toolz
f = open("data/02.data")
lines = f.readlines()


lines = list(map(lambda x: x.strip(), lines))


def charFrequency(str):
    freqDict = {}
    for c in str:
        if c in freqDict:
            freqDict[c] += 1
        else:
            freqDict[c] = 1
    return freqDict


charFrequencies = list(map(charFrequency, lines))

twos = len(list(filter(lambda x: 2 in x.values(), charFrequencies)))
threes = len(list(filter(lambda x: 3 in x.values(), charFrequencies)))

print("part1", twos * threes)


def differByOne(str1, str2):
    if not len(str1) == len(str2):
        return False
    diff = 0
    for i in range(len(str1)):
        if not str1[i] == str2[i]:
            diff += 1

    return diff == 1


def findDifferByOneLines(lines):
    for line1 in lines:
        for line2 in lines:
            if not line1 == line2:
                if differByOne(line1, line2):
                    return (line1, line2)


(l1, l2) = findDifferByOneLines(lines)
for i in range(len(l1)):
    if not l1[i] == l2[i]:
        print(l1[:i] + l1[i+1:])
