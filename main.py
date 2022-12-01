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
    pass

def solveBoard(board, col, row):
    # Go to next row
    if(col == 5):
        row += 1
        col = 0
    # Gone through the entire board
    if(row == 5):
        return board
    if(board[col][row] == "0"):
        for i in range(1,5):
            if(isValid(board, row, col, i)):
                board[row][col] == i
                # Keep going until it returns a valid board
                return solveBoard(board, col + 1, row)
        # If no valid states, backtrack
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


def main():
    # Gets what file to read from command line
    parser = argparse.ArgumentParser(description='Solves Futoshiki Puzzles using Backtracking Search for'
                                                 'Constraint Satisfaction Problems')
    parser.add_argument('input_file', action='store', type=str, help='The text file containing the futoshiki puzzle input')
    args = parser.parse_args()

    global input_file
    input_file = args.input_file

    read_file(input_file)
    write_solution_to_file(initial_state)

    # start the algorithm
    valid = solveBoard(initial_state, 0, 0)
    # if there is no solutions
    if not valid:
        write_solution_to_file("No Valid Solutions")
    write_solution_to_file(valid)
    

if __name__ == "__main__":
    main()

''' Steven's Sudoku Solver in C++ for reference
class Solution {
public:
    bool isValid(vector<vector<char>>& board, int row, int col, char num)
    {
        for(int i = 0; i < 9; i++)
        {
            if(board[i][col] == num)
                return false;
            if(board[row][i] == num)
                return false;
            if(board[3 * (row / 3) + i / 3][3 * (col / 3) + i % 3] == num)
                return false;
        }
        return true;
    }
    
    bool solveSudokuHelp(vector<vector<char>>& board, int col, int row)
    {
        if(col == 9)
        {
            row += 1;
            col = 0;
        }
        if(row == 9)
            return true;
        if(board[row][col] == '.')
        {
            for(char i = '1'; i <= '9'; i++)
            {
                if(isValid(board, row, col, i))
                {
                    board[row][col] = i;
                    if (solveSudokuHelp(board, col + 1, row))
                        return true;
                }
                board[row][col] = '.';
            }
            return false;
        }
        return solveSudokuHelp(board, col + 1, row);
    }
    void solveSudoku(vector<vector<char>>& board) {
        solveSudokuHelp(board, 0, 0);
    }
};
'''