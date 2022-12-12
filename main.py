'''
Project 2:
Futoshiki Solver
Steven Han and Preston Tang
CS 4613
'''


import argparse

initial_state = [["0"] * 5 for x in range(5)]
horizontal_conditions = [["0"] * 4 for x in range(5)]
vertical_conditions = [["0"] * 5 for x in range(4)]
input_file = ""
min_rem_val_heuristic = [[0] * 5 for x in range(5)]


# checks to see if the current selected number would work for the current selected cell
def isValid(board, row, col, num):
    # Checks to see if this number is in the same col or row
    for i in range(len(board)):
        if board[row][i] == str(num) and col != i:
            return False

    for i in range(len(board[row])):
        if board[i][col] == str(num) and row != i:
            return False

    # Checks constraint below
    if row >= 0 and row != len(board[row]) - 1 and int(board[row + 1][col]) != 0:
        if vertical_conditions[row][col] == "^":
            if num > int(board[row + 1][col]):
                return False
        if vertical_conditions[row][col] == "v":
            if num < int(board[row + 1][col]):
                return False

    # Checks constraint above
    if row <= len(board) - 1 and row != 0 and int(board[row - 1][col]) != 0:
        if vertical_conditions[row - 1][col] == "^":
            if num < int(board[row - 1][col]):
                return False
        if vertical_conditions[row - 1][col] == "v":
            if num > int(board[row - 1][col]):
                return False

    # Checks constraint to right
    if col >= 0 and col != len(board[row]) - 1 and int(board[row][col + 1]) != 0:
        if horizontal_conditions[row][col] == "<":
            if num > int(board[row][col + 1]):
                return False
        if horizontal_conditions[row][col] == ">":
            if num < int(board[row][col + 1]):
                return False

    # Checks constraint to left
    if col <= len(board[row]) - 1 and col != 0 and int(board[row][col - 1]) != 0:
        if horizontal_conditions[row][col - 1] == "<":
            if num < int(board[row][col - 1]):
                return False
        if horizontal_conditions[row][col - 1] == ">":
            if num > int(board[row][col - 1]):
                return False
    return True

# Selects based on minimum remainder value, and if tied, use degree heuristic to break the tie
def select_unassigned_variable(board):
    curr_min = 5
    # List of (x,y) tuples showing the location of tied minimum values
    tied_for_curr_min = []
    for i in range(len(min_rem_val_heuristic)):
        for j in range(len(min_rem_val_heuristic[i])):
            if(board[i][j] != "0"):
                continue
            # If there is a new minimum, reset the inCurrMin and set the currMin to the new min
            if 5 - len(min_rem_val_heuristic[i][j]) < curr_min:
                currMin = len(min_rem_val_heuristic[i][j])
                tied_for_curr_min = [(i, j)]
            elif 5 - len(min_rem_val_heuristic[i][j]) == curr_min:
                tied_for_curr_min.append((i, j))

    # If no tiebreaker needed, return the cell with the minimum remainder value
    if len(tied_for_curr_min) == 1:
        return tied_for_curr_min[0]
    else:
        # A tiebreaker is needed, so we use the degree heuristic to tie-break
        return degree_heuristic(board, tied_for_curr_min)

# Takes in an array of tuples
def degree_heuristic(board, cells):
    # Create a dictionary that maps each cell to the number of unassigned neighbors
    degree = {}
    for x, y in cells:
        # Count the number of unassigned neighbors
        count = 0
        for i in range(len(board)):
            if board[i][y] == "0":
                count += 1
        for j in range(len(board[y])):
            if board[x][j] == "0":
                count += 1
        # Subtract 1 from the count because the cell itself is included in the count
        degree[(x, y)] = count - 1

    # Pick the cell with the most unassigned neighbors
    max_degree = 0
    chosen_cell = None
    for cell, count in degree.items():
        if count > max_degree:
            max_degree = count
            chosen_cell = cell

    # Return the chosen cell
    return chosen_cell

# Updates the minimum remaining value heuristic for this specific area that changed
def update_MRV(board, row, col):
    # Go through same row and same col, if it's not a direct neighbor (1 away), add the inserted
    # value into the dictionary for that cell, if it is, call isValid on all the values that isn't in
    # the dict, if false add it to dict, if true do nothing.
    added_value = board[row][col]
    for i in range(len(board)):
        # If further away than 1
        if abs(row - i) > 1:
            min_rem_val_heuristic[row][i][added_value] = 0
        else:
            for num in range(1, 6):
                if not isValid(board, row, i, num):
                    min_rem_val_heuristic[row][i][num] = 0

    for i in range(len(board[row])):
        # If further away than 1
        if abs(col - i) > 1:
            min_rem_val_heuristic[i][col][added_value] = 0
        else:
            for num in range(1, 6):
                if not isValid(board, i, col, num):
                    min_rem_val_heuristic[i][col][num] = 0

# algorithm used to solve the board
def solveBoard(board):
    valid = True
    # returns the board if it is complete O(r * c) Full algo will be O(r^2 * c^2) or depends on isValid
    for rows in board:
        if "0" in rows:
            valid = False
    if valid:
        return True
    # to_test is a tuple of (row, col)
    to_test = select_unassigned_variable(board)
    for i in range(1, 6):
        if(isValid(board, to_test[0], to_test[1], i)):
            board[to_test[0]][to_test[1]] = str(i)
            update_MRV(board, to_test[0], to_test[1])
            if(solveBoard(board)):
                return True
            board[to_test[0]][to_test[1]] = "0"
    return False

# Assumes output is a 2D array
# Writes the solution to a txt file
def write_solution_to_file(output):
    file_number = int("".join(filter(str.isdigit, input_file)))
    result = ""

    # Converts the output to a nicely formatted string
    for r in range(len(output)):
        for c in range(len(output[r])):
            result += output[r][c] + " "
        result = result.rstrip()
        result += "\n"

    # Write result to file
    f = open("Output" + str(file_number) + ".txt", "w+")
    f.write(result)
    f.close()

# Reads an input text file
# Stores data in relevant global variables
def read_file(file_name):
    data = ""
    # Reads the entire file into data
    with open(file_name) as file:
        data = file.read()

    # Remove all trailing spaces from data
    temp_data = []
    for i in range(len(data.split("\n"))):
        temp_data.append(data.split("\n")[i].rstrip())
    data = "\n".join(temp_data)

    # Should contain the 3 sections of an input file
    parts = data.split("\n\n")

    # Parse first section and put it in initial_state
    global initial_state
    board_row = parts[0].split("\n")
    for r in range(5):
        board_col = board_row[r].split(" ")
        for c in range(5):
            initial_state[r][c] = board_col[c]

    # Parse second section and put it in horizontal_conditions
    global horizontal_conditions
    hc_row = parts[1].split("\n")
    for r in range(5):
        hc_col = hc_row[r].split(" ")
        for c in range(4):
            horizontal_conditions[r][c] = hc_col[c]

    # Parse third section and put it in vertical_conditions
    global vertical_conditions
    vc_row = parts[2].split("\n")
    for r in range(4):
        vc_col = vc_row[r].split(" ")
        for c in range(5):
            vertical_conditions[r][c] = vc_col[c]


def main():
    # Gets what file to read from command line
    parser = argparse.ArgumentParser(description='Solves Futoshiki Puzzles using Backtracking Search for'
                                                 'Constraint Satisfaction Problems')
    parser.add_argument('input_file', action='store', type=str, help='The text file containing the futoshiki puzzle input')
    args = parser.parse_args()

    global input_file
    input_file = args.input_file

    read_file(input_file)
    global initial_state
    # for r in range(len(initial_state)):
    #     for c in range(len(initial_state[r])):
    #         if not isValid(initial_state, r, c):
    #             print(r, c, initial_state[r][c], "Not Valid")
    #         else:
    #             print(r, c, initial_state[r][c], "Valid")

    # Initialize min_rem_val_heuristic with an empty dictionary
    global min_rem_val_heuristic
    for r in range(len(min_rem_val_heuristic)):
        for c in range(len(min_rem_val_heuristic[r])):
            min_rem_val_heuristic[r][c] = {}

    # start the algorithm
    valid = solveBoard(initial_state)
    # if there is no solutions
    if not valid:
        file_number = int("".join(filter(str.isdigit, input_file)))
        f = open("Output" + str(file_number) + ".txt", "w+")
        f.write("No Solution")
        f.close()
    else:
        write_solution_to_file(initial_state)

if __name__ == "__main__":
    main()