# Garden of Eden

## 1. What is a Garden of Eden

In Conway's Game of Life, a Garden of Eden is a configuration of cells, that has no predecessor, meaning it can't be created at any point while the game follows these rules:

1. If a cell is dead and has exactly 3 neighbors alive (in a 3x3 grid), it comes alive in the next generation.
2. If a cell is alive and has 2 or 3 neighbors alive, it lives on, or it dies if any other number of neighbors are alive.

This script takes the width and height of the configuration from the user, where 1 means a cell is alive and 0 means it is dead, encodes it into a formula in DIMACS CNF format and a SAT solver Glucose3 solves the formula.
If the formula has a valid model, it means there is a valid predecessor to the input configuration, thus it is not a garden of eden. However, if there are no valid models, we have a valid garden of eden.

## 2. SAT encoding

### Variables
There are a total of $2*width*height+1$ variables for any configuration, $width*height$ variables for the current generation and the previous generation and 1 for a cell out of bounds, which the script always marks as dead.

### Cell ID mapping
Each cell gets a unique id based on the formula $y*width+x+1$. The final ID is then returned if the cell is in the current generation (generation Y) or the total number of cells is added for the ancestor generation (generation X).

### Rules clauses
For each cell, we have to think of its state in the previous generation and the states of all 8 of its neighboring cells.
The function `checkAllPossibleAncestors` goes through all possible configurations in the previous generation and then calls for `gameOfLifeRulesGenerator` function, which creates clauses based on the state of the cells. Every literal is positive or negative based on the state of the cell.

### Input configuration and edge case
**Board edge:** cells that are on the edge get an id of 999999 and a unit clause -999999, whick permanently kills all cells out of bounds.
**Input configuration:** for each cell there is a unit clause CellID if the cell is alive, or -CellID if it is dead.

### Result interpretation
**SAT:** there exists a valid model for the final CNF formula, which means there is a valid predecessor, thus the configuration is *not* a Garden of Eden.

**UNSAT:** if there are no models, there are no predecessors that could create tne input configuration, thus it *is* a Garden of Eden.

### CNF formula size
For a matrix of width W and height H there are a total of $2WH + 1$ variables and $512WH+WH+1$ clauses. The length growth is linear according to number of cells in the matrix.

## 3. Code structure
**getCellID(x, y, width, height, isCurrGen):** calculates a unique ID for each cell in the corresponding generation.
**gameOfLifeRulesGenerator(cellID, ancestorCellID, neighborsAncestorIDs):** generates all clauses for one cell and its neighbors to describe the transition from the last generation to the current.
**checkAllPossibleAncestors(solver, width, height):** checks all possible ancestor configurations for each cell, calls `gameOfLifeRulesGenerator` to generate the clauses and inputs them into the solver.
**__main__:** takes user input, encodes the input cells into unit clauses and runs the Glucose3 solver, then prints the result.

## 4. Installation and use
### Requirements
* Python 3.x
* python-sat library (install using `pip install python-sat`)

### Launch
`python garden-of-eden.py`

### Input format
1. Matrix width - positive integer
2. Matrix height - positive integer
3. The matrix itself - input in lines where 0 is a dead cell and 1 is an alive one

## 5. Test configurations
1. Satisfiable small input - the blinker<br>
Its ancestor is a vertical line of cells. This configuration would blink between these two states every generation, thus the name blinker.

```
000
111
000
```

<br>
<br>
<br>
<br>
<br>

2. Unsatisfiable small input<br>
This matrix has no way to ever be created while following the rules of The game of life.
```
111
111
111
```

3. Satisfiable large input - runs more than 10 seconds.<br>
Since the space complexity growth is linear, an input that runs more than 10 seconds should be at least 540*540 in size, which would create ~150 million clauses and crash with a MemoryError before even running the solver.

I tested a 5x5 SAT input (~0,06 seconds) and 100x100 input (~0,4 seconds).

$$\frac{0{,}4 - 0{,}06}{10\,000 - 25} \approx 3{,}41 \times 10^{-5}\text{ s/cell}$$

<br>

$$\frac{10}{3{,}41 \times 10^{-5}} \approx 293\,255\text{ cells}$$

<br>

$$\sqrt{293\,255} \approx 541,5$$