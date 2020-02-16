# CS3243 Project 1

## Quick Setup
`./runner.py CS3243_P1_49_1.py 3 2`

`./runner.py CS3243_P1_49_i.py n j`, where 
1. i denotes the python file to run. For now, i = 1 (IDS)
2. n denotes the size of matrix 
3. j denotes the input number of test case. (for eg, if testing on input_3.txt, then j = 3)

> Read `runner.py` for more info.
 
## How to test?
**Integrated Test.** Running this script tests for correctness and complexity (both space and time). <br />
`./runner.py CS3243_P1_49_1.py n i`, where n denotes the size of matrix and i denotes the input number of test case.

**Unit Tests.** Within `puzzle.solve()`, there is a default driver test method `self.test()`, which performs unit tests. 

## How to debug?
1. Running `runner.py` will show every action and state from the initial state to the goal state.
2. For IDS, `Puzzle.iterative_deepening_search(puzzle, debug=True` will print every explored state 
(including unsuccessful explorations)

## Optimisation Tips (just larry's own POV))
1. Replace `deepcopy`. Very expensive operation (according to my friend who did). Instead, implement your own deep copy.
2. Find a data structure which 1) compares goal state in O(1) and 2) transitions from node n to node n' in O(1). This
is important because the number of visited nodes is the entire search space (O(b^d)). Every visited node 
triggers the operation 1) and 2), making the total time complexity O((b^d)(n + n)). Ideally if these 2 operations are 
constant, we'll achieve the optimal complexity of O((b^d)(1 + 1)) = O(b^d).
    1. The current state is stored as a 2D array and `transition` is implemented as a deterministic function 
    (ie it returns a new node), thus `transition` complexity is O(n).
    2. The states in the explored set are stored as a string (you can only store immutable objects in sets, thus I 
    stored them as lists instead of string), thus `is_goal_state` runs in O(n) as well. 

## Timeline
### Week 5
1. Meet to talk about individual ideas
2. Split the project workload
### Week 6
1. Implementation
### Recess Week
1. Report
### Week 7
1. Buffer