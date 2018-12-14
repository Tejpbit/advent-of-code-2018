import functools
f = open("data/01.data")

lines = f.readlines()
lines = list(map(lambda x: x.strip(), lines))


res = 0
for l in lines:
    operator = l[0]
    number = int(l[1:])
    if operator == "+":
        res += number
    elif operator == "-":
        res -= number

print("final frequency:", res)


# 2

global freq


def genFrequencies():
    freq = 0
    yield 0
    while(True):
        for l in lines:
            operator = l[0]
            number = int(l[1:])
            if operator == "+":
                freq += number
            elif operator == "-":
                freq -= number
            yield freq


oldFrequencies = set()
for fr in genFrequencies():
    if fr in oldFrequencies:
        print("reched twice", fr)
        break
    oldFrequencies.add(fr)
