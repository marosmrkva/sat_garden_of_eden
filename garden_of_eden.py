from pysat.solvers import Glucose3
from pysat.formula import CNF
import itertools

solver = Glucose3(use_timer=True)
allClauses = []


def getCellID(x, y, width, height, isCurrGen):

    cellID = y * width + x + 1

    if (isCurrGen):
        cellID += (width*height)

    return cellID


def gameOfLifeRulesGenerator(cellID, ancestorCellID, neighborAncestorIDs):
    clauses = []

    for combination in itertools.product([True, False], repeat = 9):
        cellState = combination[0]
        neighborsStates = combination[1:]

        aliveNeighbors = sum(neighborsStates)

        expectedCellState = False

        if (cellState):
            if (aliveNeighbors in [2, 3]):
                expectedCellState = True
        else:
            if (aliveNeighbors == 3):
                expectedCellState = True

        clause = []

        if (cellState):
            clause.append(-ancestorCellID)
        else:
            clause.append(ancestorCellID)

        for neighborState, neighborID in zip(neighborsStates, neighborAncestorIDs):
            if (neighborState):
                clause.append(-neighborID)
            else:
                clause.append(neighborID)

        if (expectedCellState):
            clause.append(cellID)
        else:
            clause.append(-cellID)

        clauses.append(clause)

    return clauses


def checkAllPossibleAncestors(solver, width, height):
    for xCoordinate in range(width):
        for yCoordinate in range(height):
            cellID = getCellID(xCoordinate, yCoordinate, width, height, isCurrGen=True)
            cellIDGenX = getCellID(xCoordinate, yCoordinate, width, height, isCurrGen=False)

            neighborsIDs = []

            for xOffset in [-1, 0, 1]:
                for yOffset in [-1, 0, 1]:
                    if (xOffset == 0 and yOffset == 0):
                        continue

                    neighborX = xCoordinate + xOffset
                    neighborY = yCoordinate + yOffset

                    if (neighborX < 0 or neighborX >= width or neighborY < 0 or neighborY >= height):
                        neighborsIDs.append(999999)
                    else:
                        neighborsIDs.append(getCellID(neighborX, neighborY, width, height, isCurrGen=False))

            currCellClauses = gameOfLifeRulesGenerator(cellID, cellIDGenX, neighborsIDs)

            for clause in currCellClauses:
                solver.add_clause(clause)
                allClauses.append(clause)

    solver.add_clause([-999999])
    allClauses.append([-999999])

def __main__():
    inputWidth = int(input("Width: "))
    inputHeight = int(input("Height: "))

    matrix = []

    print("Configuration:\n")

    for _ in range(inputHeight):
        line = input().strip()
        matrix.append(list(line))

    checkAllPossibleAncestors(solver, inputWidth, inputHeight)
    
    for xCoordinate in range (inputWidth):
        for yCoordinate in range (inputHeight):
            cellID = getCellID(xCoordinate, yCoordinate, inputWidth, inputHeight, isCurrGen=True)

            if (matrix[yCoordinate][xCoordinate] == "1"):
                solver.add_clause([cellID])
                allClauses.append([cellID])
            else:
                solver.add_clause([-cellID])
                allClauses.append([-cellID])

    dimacsFile = open("dimacs.cnf", "w")

    dimacsFile.write(f"p cnf {2*inputWidth*inputHeight+1} {512-inputWidth*inputHeight+inputWidth*inputHeight+1}\n")

    for clause in allClauses:
        for variable in clause:
            dimacsFile.write(f"{variable} ")
        dimacsFile.write("0\n")


    if solver.solve():
        print("Not a Garden of Eden.")
    else:
        print("Garden of Eden!")


    print(f"Solver working time: {solver.time()}")
    



if __name__ == "__main__":
    __main__()