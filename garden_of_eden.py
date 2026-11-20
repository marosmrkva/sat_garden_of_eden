from pysat.solvers import Glucose4

solver = Glucose4()


def getCellID(x, y, width, height, isCurrGen):

    cellID = y * width + x + 1

    if (isCurrGen):
        cellID += (width*height)

    return cellID








if solver.solve():
    print("Not a garden")
else:
    print("garden")



