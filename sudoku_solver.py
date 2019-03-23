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
        """

        def propagate_constraints(square, value):
            '''
            removes value from a square's domain and from the square's peers
            '''
            # if value value has already being removed, don't propagate constraints
            if value not in self.values[square]:
                return
            # remove value from square's domain
            self.values[square] = self.values[square].replace(value, '')

            # if square's domain is reduced to one digit, remove the domain value from its peers
            if len(self.values[square]) == 1:
                self.grid[square] = self.values[square]
                for peer in self.peers[square]:
                    propagate_constraints(peer, self.values[square])

        for square, value in self.grid.items():
            if value in self.digits:
                # get remaining values in square's domain
                remaining_values = self.values[square].replace(value, '')
                # remove the remaining values from the square's domain and its peers
                for other_value in remaining_values:
                    propagate_constraints(square, other_value)

        return self.values

    # return self.values
    def search(self, values):

        # check if sudoku puzzle is already solved
        if all(len(v) == 1 for s, v in self.values.items()):
            return True

        # get next blank square using minimum remaining values heuristic
        next_blank_square = self.get_square_with_minimum_remaining_possible_values()

        # get current values
        current_grid_value = self.grid[next_blank_square]
        current_domain = self.values[next_blank_square]

        for i in self.values[next_blank_square]:

            # check if i can be assigned to the square's units
            if self.is_allowed_in_square(next_blank_square, i):

                # update values
                self.grid[next_blank_square] = i
                self.values[next_blank_square] = i

                # check if sudoku has been solved
                if self.search(self.values.items()):
                    return self.values

                # reset values to current , if solution is not found
                self.grid[next_blank_square] = current_grid_value
                self.values[next_blank_square] = current_domain

        return False

    def get_square_with_minimum_remaining_possible_values(self):

        #  get the next unassigned square using minimum remaining values heuristic
        blank_squares = {s: len(self.values[s]) for s in [s for s, v in self.grid.items() if v not in self.digits]}

        # sort blank cells based on the number of domain values
        blank_squares = sorted(blank_squares.items(), key=lambda x: x[1])
        # get the square with the lowest number of domain values
        next_blank_square = blank_squares[0][0]

        return next_blank_square

    def is_allowed_in_square(self, square, value):
        '''
        Checks if value can be placed in square. Checks if value is in any other square in square's (param) unit
        :param square:
        :param value:
        :return: True if value is not in square's unit, else returns false
        '''

        count = 0
        for unit in self.units[square]:
            count += len([square for square in unit if value in self.grid[square]])
        if count > 0:
            return False
        return True


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
