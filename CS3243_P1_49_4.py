import os
import sys
import heapq
import time
import math


def swap(state, blank_tile_index, target_tile_index, debug=False):
        """ Swaps target tile with blank tile. Returns a new array.
        """
        new_state = state[:]
        temp = new_state[target_tile_index]
        new_state[target_tile_index] = state[blank_tile_index]
        new_state[blank_tile_index] = temp

        return new_state

def get_blank_tile(self, debug=False):
    i = self.state.index(0)
    result = {"index" : i}
    return result

def state_to_string(state):
    result = "".join(str(x) for x in state)
    return result

def is_legal_tile(target_tile_index, blank_tile_index, k, debug=False):
    
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

def opposite_actions(action, latest_action):
    if action == Actions.DOWN:
        return latest_action == Actions.UP
    if action == Actions.UP:
        return latest_action == Actions.DOWN
    if action == Actions.RIGHT:
        return latest_action == Actions.LEFT
    if action == Actions.LEFT:
        return latest_action == Actions.RIGHT

def is_goal_state(k, state, goal_state):
    for i in range(k * k):
        if state[i] != goal_state[i]:
                return False
    
    return True

def flatten_array(unflattened_array):
    flattened_arr = []
    for array in unflattened_array:
        for i in array:
            flattened_arr.append(i)

    return flattened_arr

def isEven(count):
        return count % 2 == 0

class Actions:
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    ACTIONS = [UP, DOWN, LEFT, RIGHT]

class Puzzle(object):
    UNSOLVABLE = "UNSOLVABLE"
    CUTOFF = "CUTOFF"
    FAILURE = "FAILURE"

    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.flat_state = flatten_array(init_state)
        self.flat_goal_state = flatten_array(goal_state)
        self.init_state = self.flat_state
        self.init_node = {"state" : self.flat_state, "cost" : 0, "depth": 0, "actions_history": list()}
        self.goal_state = self.flat_goal_state
        self.actions = list()
        self.past_states = set()
        self.k = len(init_state)
        self.state_to_cost = {}
        self.nodes_in_memory = 0

    def transition(self, node, action):
        """ Moves the blank tile in the OPPOSITE direction specified by the action. (p4 of project1.pdf!
        Returns a new state.
        """
        blank_tile_index = node["state"].index(0)
        target_tile_index = blank_tile_index

        if action == Actions.DOWN:
            target_tile_index -= self.k
        elif action == Actions.UP:
            target_tile_index += self.k
        elif action == Actions.RIGHT:
            target_tile_index -= 1
        elif action == Actions.LEFT:
            target_tile_index += 1

        self.past_states.add(state_to_string(node["state"]))
        new_state = swap(node["state"], blank_tile_index, target_tile_index)
        new_cost = node["cost"] + 1
        new_depth = node["depth"] + 1
        actions_history = node["actions_history"]
        new_actions_history = actions_history[:]
        new_actions_history.append(action)

        new_node = {"state" : new_state, "cost" : new_cost, "depth": new_depth, "actions_history" : new_actions_history}
        return new_node

    def valid_actions(self, node):
        """ Returns an array of valid actions
        """
        result = []
        blank_tile_index = node["state"].index(0)

        for action in Actions.ACTIONS:
            actions_count = len(node["actions_history"])
            if actions_count > 0:
                latest_action = node["actions_history"][actions_count - 1]
                if opposite_actions(action, latest_action):
                    continue

            target_tile_index = blank_tile_index

            if action == Actions.DOWN:
                target_tile_index -= self.k
            elif action == Actions.UP:
                target_tile_index += self.k
            elif action == Actions.RIGHT:
                target_tile_index -= 1
            elif action == Actions.LEFT:
                target_tile_index += 1

            if is_legal_tile(target_tile_index, blank_tile_index, self.k):
                state_string = state_to_string(swap(node["state"], blank_tile_index, target_tile_index))
                if not self.is_explored_state(state_string):
                    result.append(action)

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

    def is_explored_state(self, state_string):
        return state_string in self.past_states

    def is_solvable(self):
        k = int(math.sqrt(len(self.init_state)))
        no_of_inversions = Puzzle.count_inversions(self.init_state)

        isKEven = isEven(k)
        isEvenInversions = isEven(no_of_inversions)
        if (not isKEven):
            if isEvenInversions:
                return True
            else:
                return False

        else:
            blank_tile_posi = (self.init_state.index(0))
            blank_tile_row_posi = int(blank_tile_posi / k)
            sum_of_inversions_and_blank_tile_row_posi = blank_tile_row_posi + no_of_inversions
            isSumEven = isEven(sum_of_inversions_and_blank_tile_row_posi)

            if (not isSumEven):
                print("Puzzle is solvable!")
                return True
            else:
                print("Puzzle is not solvable!")
                return False
        # method from https://www.cs.princeton.edu/courses/archive/spring18/cos226/assignments/8puzzle/index.html


    @staticmethod
    def count_inversions(flattened_arr):
        no_of_inversions = 0

        for i in range(len(flattened_arr)):
            for j in range(i, len(flattened_arr), 1):
                if flattened_arr[i] > flattened_arr[j] != 0:
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
        # Stubbed puzzle
        stubbed_init_state = [[1, 2, 3], [4, 5, 6], [7, 0, 8]]
        stubbed_goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        puzzle = Puzzle(stubbed_init_state, stubbed_goal_state)
        # Unit test for transition
        stubbed_state = [1, 2, 3, 4, 5, 6, 7, 0, 8]
        stubbed_node = {"state" : stubbed_state, "cost" : 0, "depth": 0, "actions_history": list()}
        new_node = puzzle.transition(stubbed_node, Actions.LEFT)
        assert stubbed_node != new_node, "Unit test for transition is failing: transition should return a new node"
        assert new_node["state"][8] == 0, "Unit test for transition is failing: transition incorrectly"
        assert Actions.LEFT in new_node["actions_history"], \
            "Unit test for transition is failing: past actions should be updated"
        assert state_to_string(stubbed_state) in puzzle.past_states, \
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
        stubbed_target_tile_index = 7
        stubbed_blank_tile_index = 8
        new_state = swap(stubbed_state, stubbed_blank_tile_index, stubbed_target_tile_index)
        assert stubbed_state != new_state, "Unit test for swap node is failing: swap should return a new node"
        assert new_state[7] == 0, "Unit test for swap node is failing: swapping incorrectly"

        # Unit test for state to string
        stubbed_state = [1, 2, 3, 4, 5, 6, 8, 7, 0]
        # expected_state_string = "[1, 2, 3, 4, 5, 6, 8, 7, 0]"
        expected_state_string = "123456870"
        assert expected_state_string == state_to_string(stubbed_state), \
            "Unit test for state_to_string is failing."

        # Unit test for is_legal_tile
        stubbed_illegal_target_tile_index = 8
        stubbed_k = 3
        assert is_legal_tile(stubbed_illegal_target_tile_index, stubbed_blank_tile_index, stubbed_k) == True, \
            "Unit test for is_legal_tile is failing."

    def solve(self):
        
        start_time = time.time()

        if not self.is_solvable():
            self.actions.append(Puzzle.UNSOLVABLE)
        else:
            self.actions = self.a_star_search()

            print("Number of nodes passed through: " + str(len(self.past_states)))
            print("Actions to goal state:  " + str(len(self.actions)))
            print("--- %s seconds ---" % (time.time() - start_time))

        return self.actions 

    def getSolutionTime(self):
        start_time = time.time()

        self.solve()

        return time.time() - start_time
    
    def a_star_search(self):

        node = self.init_node

        # Initial node is entered into the queue
        frontier = [] 
        heapq.heappush(frontier,(0, id(node), node))

        while (True):

            # temp_list is the 3 - element tuple from the queue, holding the evaluation function, the id and the node
            temp_list = heapq.heappop(frontier)
            curr_node = temp_list[2]

            # If the goal state is reached
            if (Puzzle.is_goal_state(curr_node["state"], self.goal_state)):
                break

            curr_state_string = state_to_string(curr_node["state"])

            # If state has already been visited skip it (because we expanded it before)
            if (curr_state_string in self.past_states):
                continue
            else:
                # Add the state into the past states of the Puzzle to mark it as done
                self.past_states.add(curr_state_string)
           
            # Expand the current node
            for action in self.valid_actions(curr_node):
                child_node = self.transition(curr_node, action)
                child_state_string = state_to_string(child_node["state"])

                if child_state_string not in self.past_states:
                    heuristic = self.get_heuristic_Manhattan_linear(child_node)

                    # evaluation_func = g(child_node) + heuristic
                    evaluation_func = child_node["cost"] + heuristic

                    # Add the key (state) and value (cost) into a dictionary if its not already inside
                    if child_state_string not in self.state_to_cost:
                        self.state_to_cost[child_state_string] = evaluation_func
                    else:
                        # If the node is already in the frontier and its cost is lower than this current node, we skip it
                        if (self.state_to_cost[child_state_string] >= evaluation_func):
                            continue

                    # If not we simply add it into the frontier
                    heapq.heappush(frontier, ((evaluation_func, id(child_node), child_node)))

                    # Update maximum frontier size
                    self.nodes_in_memory = max(self.nodes_in_memory, len(frontier) + len(self.past_states))
                   
        return curr_node["actions_history"]

    def convert_val_to_coord(self, value):
        return value // self.k, value % self.k

    def get_heuristic_Manhattan_linear(self, node):
        return self.get_heuristic_Manhattan(node) + 2 * self.get_heuristic_linear_conflict(node)

    # Check if the two tiles who have the same GOAL row/ col are conflicting (not in order).
    def is_conflicting(self, curr_pos_j, goal_pos_j, curr_pos_k, goal_pos_k):
        return (curr_pos_j < curr_pos_k and goal_pos_j > goal_pos_k) \
            or (curr_pos_j > curr_pos_k and goal_pos_j < goal_pos_k)

    # Linear conflict heuristic
    def get_heuristic_linear_conflict(self, node):
        no_of_rows = self.k
        index = 0
        manhattan_sum = 0
        lin_conflict_row = 0
        lin_conflict_col = 0

        # Find linear conflict for each row.
        for row_index in range(no_of_rows):
            # Get the num of tiles which conflict with each tile in curr row.
            curr_row_arr = self.getIthRow(node["state"], row_index)
            list_num_conflicting_tiles_in_row = self.get_num_conflicting_tiles_in_row(row_index, curr_row_arr)
            highest_conflict_val = max(list_num_conflicting_tiles_in_row)

            # If num of highest conflict = 0, it means no more linear conflict in the row.
            while (highest_conflict_val > 0):
                col_index_with_most_conflict = list_num_conflicting_tiles_in_row.index(highest_conflict_val)
                
                # Let tile_k be the tile with most conflicts in the row.
                tile_k = curr_row_arr[col_index_with_most_conflict]
                tile_k_goal_row, tile_k_goal_col = self.convert_val_to_coord(tile_k)

                # Remove tile_k from curr_row, set num of conflict of tile_k to 0.
                list_num_conflicting_tiles_in_row[col_index_with_most_conflict] = 0

                # For every tile_j that was in conflict with tile_k, reduce the former's num of conflicting tiles.
                for tile_j_col in range(no_of_rows):
                    if (tile_j_col == col_index_with_most_conflict): continue
                    tile_j = curr_row_arr[tile_j_col]
                    tile_j_goal_row, tile_j_goal_col = self.convert_val_to_coord(tile_j)
                    if (tile_j != 0 and list_num_conflicting_tiles_in_row[tile_j_col] > 0 and tile_k_goal_row == tile_j_goal_row \
                        and self.is_conflicting(tile_j_col, tile_j_goal_col, col_index_with_most_conflict, tile_k_goal_col)):
                            list_num_conflicting_tiles_in_row[tile_j_col] -= 1

                lin_conflict_row += 1

                # Find new highest conflict value.
                highest_conflict_val = max(list_num_conflicting_tiles_in_row)


        for col_index in range(no_of_rows):
            # Get the num of tiles which conflict with each tile in curr col.
            curr_col_arr = self.getIthCol(node["state"], col_index)
            list_num_conflicting_tiles_in_col = self.get_num_conflicting_tiles_in_col(col_index, curr_col_arr)
            highest_conflict_val = max(list_num_conflicting_tiles_in_col)

            # If num of highest conflict = 0, it means no more linear conflict in the col.
            while (highest_conflict_val > 0):
                row_index_with_most_conflict = list_num_conflicting_tiles_in_col.index(highest_conflict_val)
                
                # Let tile_k be the tile with most conflicts in the col.
                tile_k = curr_col_arr[row_index_with_most_conflict]
                tile_k_goal_row, tile_k_goal_col = self.convert_val_to_coord(tile_k)

                # Remove tile_k from curr_col, set num of conflict of tile_k to 0.
                list_num_conflicting_tiles_in_col[row_index_with_most_conflict] = 0

                # For every tile_j that was in conflict with tile_k, reduce the former's num of conflicting tiles.
                for tile_j_row in range(no_of_rows):
                    if (tile_j_row == row_index_with_most_conflict): continue
                    tile_j = curr_col_arr[tile_j_row]
                    tile_j_goal_row, tile_j_goal_col = self.convert_val_to_coord(tile_j)
                    if (tile_j != 0 and list_num_conflicting_tiles_in_col[tile_j_row] > 0 and tile_k_goal_col == tile_j_goal_col \
                        and self.is_conflicting(tile_j_row, tile_j_goal_row, row_index_with_most_conflict, tile_k_goal_row)):
                            list_num_conflicting_tiles_in_col[tile_j_row] -= 1

                lin_conflict_col += 1

                # Find new highest conflict value.
                highest_conflict_val = max(list_num_conflicting_tiles_in_col)
        
        return lin_conflict_row + lin_conflict_col

    def getIthRow(self, state, i):
        start_index = i * self.k
        stop_index = start_index + self.k
        curr_row_arr = state[start_index : stop_index]
        return curr_row_arr

    def getIthCol(self, state, i):
        count = 0
        curr_col_arr = [0] * self.k
        while (count < self.k):
            curr_col_arr[count] = state[i + count * self.k]
            count += 1
        return curr_col_arr
        
    def get_num_conflicting_tiles_in_row(self, row_index, curr_row_arr):
        num_conflicting_tiles = [0] * self.k # Initialise the num of conflicting tiles list with 0.
        
        for col_index in range(self.k):
            val = curr_row_arr[col_index]
            if (val == 0): 
                continue
            
            curr_pos = row_index, col_index
            goal_pos = self.convert_val_to_coord(val - 1)
            if (curr_pos == goal_pos): 
                continue # If at the correct pos alr, skip.

            goal_row, goal_col = goal_pos[0], goal_pos[1]

            # If tile is in its goal row, loop thru next cols in the same row.
            if (row_index == goal_row):
                for next_col in range(col_index, self.k):
                    next_val = curr_row_arr[next_col]
                    if next_val == 0: 
                        continue # Skip blank tile
                    
                    next_goal_row, next_goal_col = self.convert_val_to_coord(next_val)

                    # If both are in the same row and have the same GOAL row, add num of conflicting tiles.
                    if (goal_row == next_goal_row \
                        and self.is_conflicting(col_index, goal_col, next_col, next_goal_col)):
                            num_conflicting_tiles[col_index] += 1
                            num_conflicting_tiles[next_col] += 1

        return num_conflicting_tiles

    def get_num_conflicting_tiles_in_col(self, col_index, curr_col_arr):
        num_conflicting_tiles = [0] * self.k # Initialise the num of conflicting tiles list with 0.
        for row_index in range(self.k):
            val = curr_col_arr[row_index]
            if (val == 0): continue
            curr_pos = row_index, col_index
            goal_pos = self.convert_val_to_coord(val - 1)
            if (curr_pos == goal_pos): continue # If at the correct pos alr, skip.

            goal_row, goal_col = goal_pos[0], goal_pos[1]

            # If tile is in its goal row, loop thru next rows in the same col.
            if (col_index == goal_col):
                for next_row in range(row_index, self.k):
                    next_val = curr_col_arr[next_row]
                    if next_val == 0: continue # Skip blank tile.
                    next_goal_row, next_goal_col = self.convert_val_to_coord(next_val)

                    # If both are in the same column and have the same GOAL column, add num of conflicting tiles.
                    if (goal_col == next_goal_col \
                        and self.is_conflicting(row_index, goal_row, next_row, next_goal_row)):
                            num_conflicting_tiles[row_index] += 1
                            num_conflicting_tiles[next_row] += 1

        return num_conflicting_tiles
          
    def get_heuristic_Manhattan(self, node):
        no_of_rows = self.k
        index = 0
        manhattan_sum = 0

        for val in node["state"]:
            if (val != 0):
                curr_row, curr_col = self.convert_val_to_coord(index)                    
                goal_row, goal_col = self.convert_val_to_coord(val - 1)

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