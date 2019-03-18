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
            '''
            removes value from a square's domain and from the square's domain
            :param square:
            :param value:
            :return:
            '''
            # if value is not yet removed
            if value in self.values[square]:
                self.values[square] = self.values[square].replace(value, '')
                if len(self.values[square]) == 1:
                    self.grid[square] = self.values[square]
                    for peer in self.peers[square]:
                        remove_value(peer, self.values[square])
            return

        for square, value in self.grid.items():
            if value in self.digits:
                # get remaining values in square's domain
                remaining_values = self.values[square].replace(value, '')
                # remove the remaining values from the square's domain and its peers
                for other_value in remaining_values:
                    remove_value(square, other_value)

        # update grid
        #self.grid = self.values

        return self.values

    # return self.values
    def search(self, values):
        if all(v != '0' for s, v in self.grid.items()):
            return True  # sudoku is solved

        # get the next unassigned square

        unassigned_squares = [s for s,v in self.grid.items() if v =='' or v== '0']

        #get the next unassigned square using minimum remaining values heuristic

        #unassigned_squares = sorted(self.values.items(),key=lambda x:len(x[1]))

        next_unassigned_square = unassigned_squares[0]
        for i in self.digits:

            # check if i can be assigned to the square
            occurence_in_unit = 0
            for unit in self.units[next_unassigned_square]:
                occurence_in_unit = len([square for square in unit if i in self.grid[square]])
            if occurence_in_unit == 0:
                self.grid[next_unassigned_square] = i
                #old_domain = self.values[next_unassigned_square]
                #self.values[next_unassigned_square] = i
                # backtrack
                if self.search(self.grid.items()):
                    return True
                self.grid[next_unassigned_square] = '0'


        return False


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
