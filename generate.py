import argparse

parser = argparse.ArgumentParser()
parser.add_argument("day")

def create_file(str):
    open(str, "w+")

if __name__ == '__main__':
    args = parser.parse_args()
    print(args)
    print(args.day)

    fileName = f"day_{args.day}.py"
    dataFile = f"day_{args.day}.data"
    exampleDataFile = f"day_{args.day}.example.data"

    create_file(fileName)
    create_file(dataFile)
    create_file(exampleDataFile)