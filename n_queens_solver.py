class QueensProblem:

    def __init__(self, n):
        self.n = n
        self.chess_table = [[0 for i in range(n)] for j in range(n)]

    def solve_n_queens(self):

        # we start with the first queen (with index 0)
        if self.solve(0):
            self.print_queens()
        else:
            # when we have considered all the possible configurations without a success
            # then it means there is no solution (3x3 with 3 queens)
            print('There is no solution to the problem...')

    # col_index is the same as the index of the queen
    def solve(self, col_index):
        print(f'\n{col_index}', end="")
        # we have solved the problem - base case
        if col_index == self.n:
            return True

        # let's try to find a position for queen (col_index) within a given column
        for row_index in range(self.n):
            if self.is_place_valid(row_index, col_index):
                # 1 means that there is a queen at the given location
                self.chess_table[row_index][col_index] = 1
                # self.mark_position(row_index, col_index)
                # self.print_queens()
                # print("-"*20)
                # we call the same function with col_index+1
                # we try to find the location of the next queen in the next column
                if self.solve(col_index+1):
                    return True

                # BACKTRACK
                # print(f'BACKTRACKING ... {col_index}-{row_index}')
                print(".", end="")
                self.chess_table[row_index][col_index] = 0
                self.mark_position(row_index, col_index, -2)
        #   self.print_queens()

        # when we have considered all the rows in a col without
        # finding a valid cell for the queen
        return False

    def mark_position(self, row_index, col_index, val=2):
        d = 1
        for x in range(col_index+1, self.n):
            self.chess_table[row_index][x] += val
            if row_index - d >= 0:
                self.chess_table[row_index-d][x] += val

            if row_index + d < self.n:
                self.chess_table[row_index+d][x] += val
            d += 1

    def is_place_valid(self, row_index, col_index):
        if self.chess_table[row_index][col_index]:
            return False
        # print(f"inside {row_index} {col_index}")

        self.mark_position(row_index, col_index)
        for x in range(self.n-1, col_index, -1):
            for y in range(self.n):
                if not self.chess_table[y][x]:
                    break
            else:
                # print(f"invalid {x} for {row_index} {col_index}")
                self.mark_position(row_index, col_index, -2)
                return False

        # self.mark_position(row_index, col_index, -2)
        return True

    def print_queens(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.chess_table[i][j] == 1:
                    print(' Q ', end='')
                elif self.chess_table[i][j] == 1:
                    print(' - ', end='')
                else:
                    print(f' {self.chess_table[i][j]//2} ', end='')
            print('\n')


if __name__ == '__main__':
    queens = QueensProblem(100)
    queens.solve_n_queens()
