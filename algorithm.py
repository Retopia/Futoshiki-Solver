'''
Project 2:
Futoshiki Solver
Steven Han and Preston Tang
CS 4613
'''


def isValid(board, row, col, num):
    pass

def solveBoardHelper(board, col, row):
    pass

def getBoard():
    pass

def createOutput():
    pass

def main():
    board = getBoard()
    solveBoardHelper(board, 0, 0)

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