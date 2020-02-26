import os
import sys
import heapq
import time

from copy import deepcopy


class Actions:
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    ACTIONS = [UP, DOWN, LEFT, RIGHT]

class Node:
    def __init__(self, state=None, parent=None, cost=0, depth=0, children=[]):
        self.state = state
        self.parent = parent
        self.cost = cost
        self.depth = depth
        self.children = children
        self.k = Node.get_k(state)
        self.actions_from_root = list()


    @staticmethod
    def swap(node, blank_tile, target_tile):
        """ Swaps target tile with blank tile. Returns a new node.
        """
        new_node = deepcopy(node)
        temp = new_node.state[target_tile["row"]][target_tile["col"]]
        new_node.state[target_tile["row"]][target_tile["col"]] = new_node.state[blank_tile["row"]][blank_tile["col"]]
        new_node.state[blank_tile["row"]][blank_tile["col"]] = temp

        return new_node

    def get_blank_tile(self):
        result = {"row": -1, "col": -1}
        for i in range(0, self.k):
            for j in range(0, self.k):
                if self.state[i][j] == 0:
                    result["row"] = i
                    result["col"] = j
        return result

    @staticmethod
    def state_to_string(state):
        result = "[" + ", ".join(str(x) for x in state) + "]"
        return result

    @staticmethod
    def get_k(state):
        """ Returns an integer indicating the dimension of the k x k matrix
        """
        k = len(state)
        return k

    @staticmethod
    def is_legal_tile(target_tile, k):
        return 0 <= target_tile["row"] < k and 0 <= target_tile["col"] < k


class Puzzle(object):
    UNSOLVABLE = "UNSOLVABLE"
    CUTOFF = "CUTOFF"
    FAILURE = "FAILURE"

    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.init_state = init_state
        self.init_node = Node(state=init_state)
        self.goal_state = goal_state
        self.goal_node = Node(state=goal_state)
        self.actions = list()
        self.past_states = set()

    @staticmethod
    def transition(past_states, node, action):
        """ Moves the blank tile in the OPPOSITE direction specified by the action. (p4 of project1.pdf!
        Returns a new state.
        """
        blank_tile = node.get_blank_tile()
        target_tile = deepcopy(blank_tile)
        if action == Actions.DOWN:
            target_tile["row"] -= 1
        elif action == Actions.UP:
            target_tile["row"] += 1
        elif action == Actions.RIGHT:
            target_tile["col"] -= 1
        elif action == Actions.LEFT:
            target_tile["col"] += 1

        past_states.add(Node.state_to_string(node.state))
        new_node = Node.swap(node, blank_tile, target_tile)
        new_node.cost += 1
        new_node.depth += 1
        new_node.actions_from_root.append(action)
        return new_node

    def valid_actions(self, node):
        """ Returns an array of valid actions
        """
        result = []
        blank_tile = node.get_blank_tile()

        for action in Actions.ACTIONS:
            target_tile = deepcopy(blank_tile)
            if action == Actions.DOWN:
                target_tile["row"] -= 1
            elif action == Actions.UP:
                target_tile["row"] += 1
            elif action == Actions.RIGHT:
                target_tile["col"] -= 1
            elif action == Actions.LEFT:
                target_tile["col"] += 1

            if Node.is_legal_tile(target_tile, node.k):
                state_string = Node.state_to_string(Node.swap(node, blank_tile, target_tile).state)
                if not Puzzle.is_explored_state(self.past_states, state_string):
                    result.append(action)
        return result

    @staticmethod
    def is_explored_state(past_states, state_string):
        return state_string in past_states

    @staticmethod
    def flatten_array(unflattened_array):
        flattened_arr = []
        for array in unflattened_array:
            for i in array:
                flattened_arr.append(i)

        return flattened_arr

    @staticmethod
    def is_solvable(init_state):

        flattened_arr = Puzzle.flatten_array(init_state)
        no_of_rows = len(init_state)
        no_of_inversions = Puzzle.count_inversions(flattened_arr)

        isEvenRows = Puzzle.even(no_of_rows)
        isEvenInversions = Puzzle.even(no_of_inversions)
        if (not isEvenRows):
            if isEvenInversions:
                return True
            else:
                return False

        else:
            blank_tile_posi = (flattened_arr.index(0))
            count_frm_btm = no_of_rows - int(blank_tile_posi / no_of_rows)
            isEvenFrmBtm = Puzzle.even(count_frm_btm)

            if (not isEvenInversions and isEvenFrmBtm) \
                    or (isEvenInversions and not isEvenFrmBtm):
                return True
            else:
                return False
        # method from https://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/

    @staticmethod
    def even(count):
        return count % 2 == 0

    @staticmethod
    def count_inversions(flattened_arr):
        no_of_inversions = 0

        for i in range(len(flattened_arr)):
            for j in range(i, len(flattened_arr), 1):
                if flattened_arr[i] > flattened_arr[j] != 0:
                    no_of_inversions += 1

        return no_of_inversions

    @staticmethod
    def is_goal_state(state, goal_state):
        return state == goal_state

    def test(self):
        """ Unit tests for basic functions. Assumes the input file is n_equals_3/input_1.txt.

        """

        # Unit test for transition
        stubbed_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        stubbed_node = Node(state=stubbed_state)
        stubbed_past_states = set()
        new_node = Puzzle.transition(stubbed_past_states, stubbed_node, Actions.RIGHT)
        assert stubbed_node != new_node, "Unit test for transition is failing: transition should return a new node"
        assert new_node.state[2][1] == 0, "Unit test for transition is failing: transition incorrectly"
        assert Actions.RIGHT in new_node.actions_from_root, \
            "Unit test for transition is failing: past actions should be updated"
        assert Node.state_to_string(stubbed_state) in stubbed_past_states, \
            "Unit test for transition is failing: past states should be updated"

        # Unit test for solvable 3x3
        stubbed_state = [[8, 1, 2], [0, 4, 3], [7, 6, 5]]
        assert not Puzzle.is_solvable(stubbed_state) == True, \
            "Unit test for checking if 3x3 is unsolvable is failing"

        # Unit test for solvable 4x4
        stubbed_state = [[3, 9, 1, 15], [14, 11, 4, 6], [13, 0, 10, 12], [2, 7, 8, 5]]
        assert not Puzzle.is_solvable(stubbed_state) == True, \
            "Unit test for checking if 4x4 is unsolvable is failing"

        ### Node Tests

        # Unit test for swap node
        stubbed_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        stubbed_target_tile = {"row": 2, "col": 1}
        stubbed_blank_tile = {"row": 2, "col": 2}
        node = Node(state=stubbed_state)
        new_node = Node.swap(node, stubbed_blank_tile, stubbed_target_tile)
        assert node != new_node, "Unit test for swap node is failing: swap should return a new node"
        assert new_node.state[2][1] == 0, "Unit test for swap node is failing: swapping incorrectly"

        # Unit test for state to string
        stubbed_state = [[1, 2, 3], [4, 5, 6], [8, 7, 0]]
        expected_state_string = "[[1, 2, 3], [4, 5, 6], [8, 7, 0]]"
        assert expected_state_string == Node.state_to_string(stubbed_state), \
            "Unit test for state_to_string is failing."

        # Unit test for is_legal_tile
        stubbed_illegal_target_tile = {"row": 2, "col": 2}
        stubbed_k = 3
        assert Node.is_legal_tile(stubbed_illegal_target_tile, stubbed_k) == True, \
            "Unit test for is_legal_tile is failing."




    def solve(self):
        
        start_time = time.time()

        if not Puzzle.is_solvable(self.init_state):
            self.actions.append(Puzzle.UNSOLVABLE)
        else:
            self.actions = self.a_star_search(puzzle)

        print("Number of nodes passed through " + str(len(self.past_states)))
        print("--- %s seconds ---" % (time.time() - start_time))

        return self.actions 
            



        """ heapq operates as a priority queue. It operates in the following format: 
            heapq.heappush( the queue, (first_comparator, second_comparator, item))
            In this case I added id(node) which returns a unique id -> as if you only have the heuristic, 
            there will be an error as all the comparators have to be unique.
        """
    def a_star_search(self, puzzle):
        queue = []
        node = puzzle.init_node

        # Initial node is entered into the queue
        heapq.heappush(queue,(0, id(node), node))

        # queue[0][2] is the first node in the priority queue
        while (not Puzzle.is_goal_state(queue[0][2].state, self.goal_state)):

            # temp_list is the 3 - element tuple from the queue, holding the evaluation function, the id and the node
            temp_list = heapq.heappop(queue)

            curr_node = temp_list[2]
            queue = self.explore_next_states(curr_node, queue, puzzle)

        return queue[0][2].actions_from_root
     
        
    def explore_next_states(self, node, queue, puzzle):

        for action in puzzle.valid_actions(node):
            child_node = Puzzle.transition(puzzle.past_states, node, action)
            
            if Node.state_to_string(child_node.state) not in puzzle.past_states:
                heuristic = Puzzle.get_heuristic_Manhattan(child_node)
                heapq.heappush(queue, ((node.cost + heuristic, id(child_node), child_node)))
            
        return queue
       
    @staticmethod
    def convert_val_to_coord(value, node):
        return value // node.k, value % node.k

    # Manhattan heuristic
    @staticmethod
    def get_heuristic_Manhattan(node):
        no_of_rows = node.k
        index = 0
        manhattan_sum = 0

        for row in node.state:
            for val in row:
                if (val != 0):
                    curr_row, curr_col = Puzzle.convert_val_to_coord(index, node)                    
                    goal_row, goal_col = Puzzle.convert_val_to_coord(val - 1, node)

                    dist_x = curr_col - goal_col
                    dist_y = curr_row - goal_row
                    
                    manhattan_sum += abs(dist_x) + abs(dist_y)
                    index += 1
                  
        return manhattan_sum
 
if __name__ == "__main__":
    # do NOT modify below

    # argv[0] represents the name of the file that is being executed
    # argv[1] represents name of input file
    # argv[2] represents name of destination output file
    if len(sys.argv) != 3:
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        raise IOError("Input file not found!")

    lines = f.readlines()
    
    # n = num rows in input file
    n = len(lines)
    # max_num = n to the power of 2 - 1
    max_num = n ** 2 - 1

    # Instantiate a 2D list of size n x n
    init_state = [[0 for i in range(n)] for j in range(n)]
    goal_state = [[0 for i in range(n)] for j in range(n)]
    

    i,j = 0, 0
    for line in lines:
        for number in line.split(" "):
            if number == '':
                continue
            value = int(number , base = 10)
            if  0 <= value <= max_num:
                init_state[i][j] = value
                j += 1
                if j == n:
                    i += 1
                    j = 0

    for i in range(1, max_num + 1):
        goal_state[(i-1)//n][(i-1)%n] = i
    goal_state[n - 1][n - 1] = 0

    puzzle = Puzzle(init_state, goal_state)
    ans = puzzle.solve()

    with open(sys.argv[2], 'a') as f:
        for answer in ans:
            f.write(answer+'\n')




