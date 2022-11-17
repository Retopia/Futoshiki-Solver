import argparse

initial_state = [[0] * 5 for x in range(5)]
horizontal_conditions = [[0] * 5 for x in range(4)]
vertical_conditions = [[0] * 4 for x in range(5)]
input_file = ""

# Reads an input text file
# Stores data in relevant global variables
# WIP (Untested for now)
def parse_input(file_name):
    data = ""
    # Reads the entire file into data
    with open(file_name) as file:
        data = file.read()

    # Should contain the 3 sections of an input file
    parts = data.split("\n\n")

    # Parse first section and put it in initial_state
    global initial_state
    board_row = parts[0].split("\n")
    for r in range(len(board_row)):
        for c in range(len(board_row[r].split(" "))):
            initial_state[r][c] = board_row[r][c]

    # Parse second section and put it in horizontal_conditions
    global horizontal_conditions
    hc_rows = parts[0].split("\n")
    for r in range(len(hc_rows)):
        for c in range(len(hc_rows[r].split(" "))):
            horizontal_conditions[r][c] = hc_rows[r][c]

    # Parse third section and put it in vertical_conditions
    global vertical_conditions
    vc_rows = parts[0].split("\n")
    for r in range(len(vc_rows)):
        for c in range(len(vc_rows[r].split(" "))):
            vertical_conditions[r][c] = vc_rows[r][c]


def main():
    # Gets what file to read from command line
    parser = argparse.ArgumentParser(description='Solves 15-puzzle program with Weighted A* Search')
    parser.add_argument('input_file', action='store', type=str, help='The text file containing the 15-puzzle input')
    args = parser.parse_args()

    global input_file
    input_file = args.input_file

    parse_input(input_file)

if __name__ == "__main__":
    main()
