import sys


class Sudoku:
    """
        Sudoku class, which models a Sudoku game.

        Based on Peter Norvig's Suggested Sudoku setup
    """

    def __init__(self):
        """
            Initialize digits, rows, columns, the grid, squares, units, peers, and values.
        """
        self.digits = '123456789'
        self.rows = 'ABCDEFGHI'
        self.cols = self.digits
        self.grid = dict()
        self.squares = self.cross_product(self.rows, self.cols)
        unitlist = ([self.cross_product(self.rows, c) for c in self.cols] + \
                    [self.cross_product(r, self.cols) for r in self.rows] + \
                    [self.cross_product(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')])
        self.units = dict((s, [u for u in unitlist if s in u]) for s in self.squares)
        self.peers = dict((s, set(sum(self.units[s], [])) - set([s])) for s in self.squares)
        self.values = dict((s, self.digits) for s in self.squares)

    @staticmethod
    def cross_product(A, B):
        """
            Return the cross product of A and B
        """
        return [a + b for a in A for b in B]

    def __str__(self):
        """
            Convert the grid into a human-readable string
        """
        output = ''
        width = 2 + max(len(self.grid[s]) for s in self.squares)
        line = '+'.join(['-' * (width * 3)] * 3)
        for r in self.rows:
            output += (''.join(
                (self.grid[r + c] if self.grid[r + c] not in '0.' else '').center(width) + ('|' if c in '36' else '')
                for c in self.digits)) + "\n"
            if r in 'CF': output += line + "\n"
        return output

    def load_file(self, filename):
        """
            Load the file into the grid dictionary. Note that keys
            are in the form '[A-I][1-9]' (e.g., 'E5').
        """
        grid = ''
        with open(filename) as f:
            grid = ''.join(f.readlines())
        grid_values = self.grid_values(grid)
        self.grid = grid_values

    # print(self.peers.items())

    def grid_values(self, grid):
        """
            Convert grid into a dict of {square: char} with '0' or '.' for empties.
        """
        chars = [c for c in grid if c in self.digits or c in '0.']
        assert len(chars) == 81
        return dict(zip(self.squares, chars))

    def solve(self):
        """
            Solve the problem by propagation and backtracking.
        """
        self.search(self.propagate())

    def propagate(self):
        """
        Constraint Propagation
        :return:
        """
        def remove_value(square, value):
            if value in self.values[square]:
                self.values[square] = self.values[square].replace(value, '')
                if len(self.values[square]) == 1:
                    for peer in self.peers[square]:
                        remove_value(peer, self.values[square])

                for unit in self.units[square]:
                    possible_placements = [square for square in unit if value in self.values[square]]
                    if len(possible_placements) == 1:
                        self.grid[possible_placements[0]] = value
                        other_values = self.values[possible_placements[0]].replace(value, '')
                        for other_value in other_values:
                            remove_value(possible_placements[0], other_value)


        for square, digit in self.grid.items():
            if digit in self.digits:
                remaining_values = self.values[square].replace(digit, '')
                for other_value in remaining_values:
                    remove_value(square, other_value)

        return self.values


    # return self.values
    def search(self, values):
        """
            TODO: Code the Backtracking Search Technique Here
        """
        return values


def main():
    s = Sudoku()
    '''
        The loop reads in as many files as you've passed on the command line.
        Example to read two easy files from the command line:
            python sudoku_solver.py sudoku_easy1.txt sudoku_easy2.txt
    '''
    for x in range(1, len(sys.argv)):
        s.load_file(sys.argv[x])
        print("\n==============================================")
        print(sys.argv[x].center(46))
        print("==============================================\n")
        print(s)
        print("\n----------------------------------------------\n")
        s.solve()
        print(s)


main()
