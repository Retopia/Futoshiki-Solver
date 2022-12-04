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

def isValid(board, row, col, num):
    # Checks to see if this number is in the same col or row
    for i in range(len(board)):
        if board[row][i] == num and col != i:
            return False

    for i in range(len(board[row])):
        if board[i][col] == num and row != i:
            return False

    # Checks constraint below
    if row >= 0 and row != len(board[row]) - 1 and int(board[row + 1][col]) != 0:
        if vertical_conditions[row][col] == "^":
            if num < int(board[row + 1][col]):
                return False
        if vertical_conditions[row][col] == "v":
            if num > int(board[row + 1][col]):
                return False

    # Checks constraint above
    if row <= len(board) - 1 and row != 0 and int(board[row - 1][col]) != 0:
        if vertical_conditions[row - 1][col] == "^":
            if num > int(board[row - 1][col]):
                return False
        if vertical_conditions[row - 1][col] == "v":
            if num < int(board[row - 1][col]):
                return False

    # Checks constraint to right
    if col >= 0 and col != len(board[row]) - 1 and int(board[row][col + 1]) != 0:
        if horizontal_conditions[row][col] == "<":
            if num < int(board[row][col + 1]):
                return False
        if horizontal_conditions[row][col] == ">":
            if num > int(board[row][col + 1]):
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


def select_unassigned_variable(board):
    pass

def solveBoard(board):
    # returns the board if it is complete
    for rows in board:
        if "0" not in rows:
            return board
    # to_test is a tuple of (row, col)
    to_test = select_unassigned_variable(board)
    for i in range(1, 6):
        if(isValid(board, to_test[0], to_test[1], i)):
            board[to_test[0]][to_test[1]] = str(i)
            ans = solveBoard(board)
            if(ans):
                return ans
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

    # for p in parts:
    #     print(p, "\n")


    # Parse first section and put it in initial_state
    global initial_state
    board_row = parts[0].split("\n")
    for r in range(5):
        board_col = board_row[r].split(" ")
        for c in range(5):
            initial_state[r][c] = board_col[c]

    # print('\n'.join([' '.join([str(cell) for cell in row]) for row in initial_state]))
    # print()

    # Parse second section and put it in horizontal_conditions
    global horizontal_conditions
    hc_row = parts[1].split("\n")
    for r in range(5):
        hc_col = hc_row[r].split(" ")
        for c in range(4):
            horizontal_conditions[r][c] = hc_col[c]

    # print('\n'.join([' '.join([str(cell) for cell in row]) for row in horizontal_conditions]))
    # print()

    # Parse third section and put it in vertical_conditions
    global vertical_conditions
    vc_row = parts[2].split("\n")
    for r in range(4):
        vc_col = vc_row[r].split(" ")
        for c in range(5):
            vertical_conditions[r][c] = vc_col[c]
    # print('\n'.join([' '.join([str(cell) for cell in row]) for row in vertical_conditions]))

    # print("board", len(initial_state), len(initial_state[0]))
    # print("horizontal_conditions", len(horizontal_conditions), len(horizontal_conditions[0]))
    # print("vertical_conditions", len(vertical_conditions), len(vertical_conditions[0]))


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

    # start the algorithm
    valid = solveBoard(initial_state, 0, 0)
    # if there is no solutions
    if not valid:
        file_number = int("".join(filter(str.isdigit, input_file)))
        f = open("Output" + str(file_number) + ".txt", "w+")
        f.write("No Solution")
        f.close()
    else:
        write_solution_to_file(valid)
    

if __name__ == "__main__":
    main()