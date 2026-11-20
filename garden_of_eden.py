from pysat.solvers import Glucose4

solver = Glucose4()


def getCellID(x, y, width, height, isCurrGen):

    cellID = y * width + x + 1

    if (isCurrGen):
        cellID += (width*height)

    return cellID


def __main__():
    inputWidth = int(input("Width: "))
    inputHeight = int(input("Height: "))

    inputMatrix = input("Configuration:\n").split()
    matrix = []

    for line in inputMatrix:
        matrix.append(list(line))

    
    


    if solver.solve():
        print("Not a garden")
    else:
        print("garden")



if __name__ == "__main__":
    __main__()