import os
import sys
import heapq
import time
import math
from copy import deepcopy


class Actions:
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    ACTIONS = [UP, DOWN, LEFT, RIGHT]

class Node:
    def __init__(self, state=None, cost=0, depth=0):
        self.state = state
        self.cost = cost
        self.depth = depth
        self.k = Node.get_k(state)
        self.actions_from_root = list()


    @staticmethod
    def swap(state, blank_tile_index, target_tile_index, debug=True):
        """ Swaps target tile with blank tile. Returns a new array.
        """
        new_state = state[:]
        temp = new_state[target_tile_index]
        new_state[target_tile_index] = 0
        new_state[blank_tile_index] = temp

        return new_state

    @staticmethod
    def state_to_string(state):
        result = " ".join(str(x) for x in state)
        return result

    @staticmethod
    def get_k(state):
        """ Returns an integer indicating the dimension of the k x k matrix
        """
        k = int(math.sqrt(len(state)))
        return k

    @staticmethod
    def is_legal_move(target_tile_index, blank_tile_index, k, debug=True):
        list_right_edge = list()
        list_left_edge = list()
        for i in range(1, k + 1):
            list_right_edge.append(i * k - 1)
        for i in range(0, k):
            list_left_edge.append(i * k)
        # cannot move left
        if blank_tile_index in list_right_edge:
            return target_tile_index != blank_tile_index + 1 and 0 <= target_tile_index < k * k
        # cannot move right
        elif blank_tile_index in list_left_edge:
            return target_tile_index != blank_tile_index - 1 and 0 <= target_tile_index < k * k
        else:
            return 0 <= target_tile_index < k * k

class Puzzle(object):
    UNSOLVABLE = "UNSOLVABLE"
    CUTOFF = "CUTOFF"
    FAILURE = "FAILURE"

    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.flat_state = Puzzle.flatten_array(init_state)
        self.flat_goal_state = Puzzle.flatten_array(goal_state)
        self.init_state = self.flat_state
        self.init_node = Node(self.flat_state)
        self.goal_state = Puzzle.flatten_array(goal_state)
        self.goal_node = Node(self.flat_goal_state)
        self.actions = list()
        self.past_states = set()

    @staticmethod
    def transition(past_states, node, action):
        """ Moves the blank tile in the OPPOSITE direction specified by the action. (p4 of project1.pdf!
        Returns a new state.
        """
        blank_tile_index = node.state.index(0)
        target_tile_index = blank_tile_index

        if action == Actions.DOWN:
            target_tile_index -= node.k
        elif action == Actions.UP:
            target_tile_index += node.k
        elif action == Actions.RIGHT:
            target_tile_index -= 1
        elif action == Actions.LEFT:
            target_tile_index += 1

        past_states.add(Node.state_to_string(node.state))
        new_state = Node.swap(node.state, blank_tile_index, target_tile_index)
        new_cost = node.cost + 1
        new_depth = node.depth + 1
        new_node = Node(new_state, new_cost, new_depth)
        new_node.actions_from_root = list(node.actions_from_root)
        new_node.actions_from_root.append(action)
        return new_node

    def valid_actions(self, node):
        """ Returns an array of valid actions
        """
        result = []

        for action in Actions.ACTIONS:
            if len(node.actions_from_root) > 0:
                latest_action = node.actions_from_root[-1]
                if puzzle.opposite_actions(action, latest_action):
                    continue

            blank_tile_index = node.state.index(0)
            target_tile_index = blank_tile_index

            if action == Actions.DOWN:
                target_tile_index -= node.k
            elif action == Actions.UP:
                target_tile_index += node.k
            elif action == Actions.RIGHT:
                target_tile_index -= 1
            elif action == Actions.LEFT:
                target_tile_index += 1


            if Node.is_legal_move(target_tile_index, blank_tile_index, node.k):
                state_string = Node.state_to_string(Node.swap(node.state, blank_tile_index, target_tile_index))
                if not Puzzle.is_explored_state(self.past_states, state_string):
                    result.append(action)
                    # Puzzle.random_insert(result, action)                   
        return result

    def opposite_actions(self, action, latest_action):
        if action == Actions.DOWN:
            return latest_action == Actions.UP
        if action == Actions.UP:
            return latest_action == Actions.DOWN
        if action == Actions.RIGHT:
            return latest_action == Actions.LEFT
        if action == Actions.LEFT:
            return latest_action == Actions.RIGHT

    @staticmethod
    def is_explored_state(past_states, state_string):
        return state_string in past_states

    @staticmethod
    def is_solvable(init_state):
        k = int(math.sqrt(len(init_state)))
        no_of_inversions = Puzzle.count_inversions(init_state)

        isKEven = Puzzle.even(k)
        isEvenInversions = Puzzle.even(no_of_inversions)
        if (not isKEven):
            if isEvenInversions:
                return True
            else:
                return False

        else:
            blank_tile_posi = (init_state.index(0))
            blank_tile_row_posi = int(blank_tile_posi / k)
            sum_of_inversions_and_blank_tile_row_posi = blank_tile_row_posi + no_of_inversions
            isSumEven = Puzzle.even(sum_of_inversions_and_blank_tile_row_posi)

            if (not isSumEven):
                print("Puzzle is solvable!")
                return True
            else:
                print("Puzzle is not solvable!")
                return False
        # method from https://www.cs.princeton.edu/courses/archive/spring18/cos226/assignments/8puzzle/index.html

    @staticmethod
    def even(count):
        return count % 2 == 0

    @staticmethod
    def count_inversions(arr):
        no_of_inversions = 0

        for i in range(len(arr)):
            for j in range(i, len(arr), 1):
                if arr[i] > arr[j] != 0:
                    no_of_inversions += 1

        return no_of_inversions

    @staticmethod
    def flatten_array(unflattened_array):
        flattened_arr = []
        for array in unflattened_array:
            for i in array:
                flattened_arr.append(i)

        return flattened_arr

    @staticmethod
    def is_goal_state(state, goal_state):
        return state == goal_state

    def test(self):
        """ Unit tests for basic functions. Assumes the input file is n_equals_3/input_1.txt.

        """

        # Unit test for transition
        stubbed_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        stubbed_node = Node(state=stubbed_state)
        stubbed_past_states = set()
        new_node = Puzzle.transition(stubbed_past_states, stubbed_node, Actions.RIGHT)
        assert stubbed_node != new_node, "Unit test for transition is failing: transition should return a new node"
        assert new_node.state[7] == 0, "Unit test for transition is failing: transition incorrectly"
        assert Actions.RIGHT in new_node.actions_from_root, \
            "Unit test for transition is failing: past actions should be updated"
        assert Node.state_to_string(stubbed_state) in stubbed_past_states, \
            "Unit test for transition is failing: past states should be updated"

        # Unit test for solvable 3x3
        stubbed_state = [8, 1, 2, 0, 4, 3, 7, 6, 5]
        assert not Puzzle.is_solvable(stubbed_state) == True, \
            "Unit test for checking if 3x3 is unsolvable is failing"

        # Unit test for solvable 4x4
        stubbed_state = [3, 9, 1, 15, 14, 11, 4, 6, 13, 0, 10, 12, 2, 7, 8, 5]
        assert not Puzzle.is_solvable(stubbed_state) == True, \
            "Unit test for checking if 4x4 is unsolvable is failing"

        ### Node Tests

        # Unit test for swap
        stubbed_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        stubbed_target_tile = {"index": 7}
        stubbed_blank_tile = {"index": 8}
        new_state = Node.swap(stubbed_state, stubbed_blank_tile, stubbed_target_tile)
        assert stubbed_state != new_state, "Unit test for swap node is failing: swap should return a new node"
        assert new_state[7] == 0, "Unit test for swap node is failing: swapping incorrectly"

        # Unit test for state to string
        stubbed_state = [1, 2, 3, 4, 5, 6, 8, 7, 0]
        # expected_state_string = "[1, 2, 3, 4, 5, 6, 8, 7, 0]"
        expected_state_string = "123456870"
        assert expected_state_string == Node.state_to_string(stubbed_state), \
            "Unit test for state_to_string is failing."

        # Unit test for is_legal_move
        stubbed_illegal_target_tile = {"index" : 8}
        stubbed_k = 3
        assert Node.is_legal_move(stubbed_illegal_target_tile, stubbed_blank_tile, stubbed_k) == True, \
            "Unit test for is_legal_move is failing."

    def solve(self):
        
        start_time = time.time()

        if not Puzzle.is_solvable(self.init_state):
            self.actions.append(Puzzle.UNSOLVABLE)
        else:
            self.actions = self.a_star_search(puzzle)

        print("Number of nodes passed through " + str(len(self.past_states)))
        print("--- %s seconds ---" % (time.time() - start_time))

        return self.actions 
            
    def a_star_search(self, puzzle):

        
        """ heapq operates as a priority queue. It operates in the following format: 
            heapq.heappush( the queue, (first_comparator, second_comparator, item))
            In this case I added id(node) which returns a unique id -> as if you only have the heuristic, 
            there will be an error as all the comparators have to be unique.
        """

        queue = [] # contains a tuple(node cost, id of node, node)
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
                heuristic = Puzzle.get_heuristic_Euclidean(child_node)
                heapq.heappush(queue, ((node.cost + heuristic, id(child_node), child_node)))
            
        return queue
       
    @staticmethod
    def convert_val_to_coord(value, node):
        return value // node.k, value % node.k

    # Euclidean heuristic
    @staticmethod
    def get_heuristic_Euclidean(node):
        no_of_rows = node.k
        index = 0
        euclidean_sum = 0

        for val in node.state:
            if (val != 0):
                curr_row, curr_col = Puzzle.convert_val_to_coord(index, node)                    
                goal_row, goal_col = Puzzle.convert_val_to_coord(val - 1, node)

                dist_x = curr_col - goal_col
                dist_y = curr_row - goal_row
                
                euclidean_sum += math.sqrt((dist_x)**2 + (dist_y)**2)
                index += 1
                  
        return euclidean_sum
 
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