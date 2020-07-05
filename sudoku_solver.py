import sys


class Sudoku:
    """
        Sudoku class, which models a Sudoku game. Based on Peter Norvig's Suggested Sudoku setup

        Uses Constraint Propagation (Forward Checking) and Backtracking using Minimum Remaining Values (MRV) heuristic

        To run:
        python sudoku_solver.py <sudoku_file_paths>
        python sudoku_solver.py input/sudoku_easy1.txt input/sudoku_easy2.txt


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
        Constraint Propagation using Forward Checking
        """

        def propagate_constraints(_square, _value):
            """
            removes value from a square's domain and from the square's peers
            """
            # if value value has already being removed, don't propagate constraints
            if _value not in self.values[_square]:
                return

            # remove value from square's domain
            self.values[_square] = self.values[_square].replace(_value, '')

            # if square's domain is reduced to one digit, remove the domain value from the square's peers
            if len(self.values[_square]) == 1:
                self.grid[_square] = self.values[_square]
                for peer in self.peers[_square]:
                    propagate_constraints(peer, self.values[_square])

        for square, value in self.grid.items():
            if value in self.digits:
                # get remaining values in square's domain
                remaining_values = self.values[square].replace(value, '')
                # remove the remaining values from the square's domain and its peers
                for other_value in remaining_values:
                    propagate_constraints(square, other_value)

        return self.values

    def search(self, values):
        self.values = values

        # check if sudoku puzzle is already solved
        if all(len(v) == 1 for s, v in self.values.items()):
            return True

        # get next blank square using minimum remaining values heuristic
        next_blank_square = self.get_square_with_minimum_remaining_possible_values()

        # save next_blank_square current domain before changing it
        # incase we need to restore them
        current_domain = self.values[next_blank_square]

        # attempt to assign each  value from next_blank_square's domain
        for domain_value in self.values[next_blank_square]:

            # check if domain value can be assigned to the square's units
            if self.is_allowed_in_square(next_blank_square, domain_value):

                # place value in square
                self.grid[next_blank_square] = domain_value
                # update square's domain
                self.values[next_blank_square] = domain_value

                # check if sudoku has been solved
                if self.search(self.values):
                    return self.values

                # clear assignment
                self.grid[next_blank_square] = ''
                self.values[next_blank_square] = current_domain

        return False

    def get_square_with_minimum_remaining_possible_values(self):
        """
            Uses Mininmum Remaining Values heuristic to the get the blank square  with the lowest number
            of domain values (possible values)
        :return:
        """

        #  get the blank squares
        blank_squares = {s: len(self.values[s]) for s, v in self.values.items() if len(v) > 1}

        # sort blank squares based on the number of domain values in ascending order
        blank_squares = sorted(blank_squares.items(), key=lambda x: x[1])
        # get the first square in sorted set
        next_blank_square = blank_squares[0][0]

        return next_blank_square

    def is_allowed_in_square(self, square, value):
        """
        Checks if value can be placed in square. Checks if value is in any other square peers
        :param square:
        :param value:
        :return: True if value is not in square's unit, else returns false
        """
        for peer in self.peers[square]:
            if peer != square and value in self.grid[peer]:
                return False
        return True


def main():
    '''
        The loop reads in as many files as you've passed on the command line.
        Example to read two easy files from the command line:
            python sudoku_solver.py input/sudoku_easy1.txt input/sudoku_easy2.txt
    '''
    for x in range(1, len(sys.argv)):
        s = Sudoku()
        s.load_file(sys.argv[x])
        print("\n==============================================")
        print(sys.argv[x].center(46))
        print("==============================================\n")
        print(s)
        print("\n----------------------------------------------\n")
        s.solve()
        print(s)



main()
