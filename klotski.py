class Board:
    target = [[1, 4], [2, 4]]
    target_block = 'A'

    def __init__(self, grid, parent, action):
        self.grid = grid
        self.h = len(grid)
        self.w = len(grid[0])
        self.hash = hash(self.__repr__())
        self.parent = parent
        self.action = action
        if parent:
            self.moves = parent.moves
            if self.action != parent.action:
                self.moves += 1
        else:
            self.moves = 0

    def move(self, block, direction):
        coords = []
        for i, row in enumerate(self.grid):
            for j, element in enumerate(row):
                if element == block:
                    coords.append([j, i])

        current_pos = [tuple(coord) for coord in coords]
        for coord in coords:
            if direction == 'up':
                coord[1] -= 1
            elif direction == 'down':
                coord[1] += 1
            elif direction ==  'left':
                coord[0] -= 1
            elif direction == 'right':
                coord[0] += 1

            if not (0 <= coord[0] < self.w and 0 <= coord[1] < self.h and self.grid[coord[1]][coord[0]] in (block, ' ')):
                return False
        
        grid_new = [list(row) for row in self.grid]

        #clear grid
        for x,y in current_pos:
            grid_new[y][x] = ' '
        
        #new grid
        for x,y in coords:
            grid_new[y][x] = block

        grid_new_tup = [tuple(row) for row in grid_new]

        return Board(tuple(grid_new_tup), self, (block, direction))
    
    def goal_reached(self):
        for x, y in Board.target:
            if self.grid[y][x] != Board.target_block:
                return False
        return True

    def trace(self):
        if not self.parent:
            return [(self, 'Start')]
        return self.parent.trace() + [(self, self.action)]


    def print_grid(self):
        print('+---'*self.w, end='+\n')
        for index, row in enumerate(self.grid):
            #column separators
            print('| ', end='')
            for i in range(self.w-1):
                print(row[i], end='')
                if row[i] == row[i+1]:
                    print('   ', end='')
                else:
                    print(' | ', end='')
            print(row[-1], '|')

        #row separators
            if index + 1 < self.h:
                for j, element in enumerate(row):
                    print('+', end='')
                    if self.grid[index+1][j] == element:
                        print('   ', end='')
                    else:
                        print('---', end='')
                print('+')
        print('+---'*self.w, end='+\n')
        print()

    def __repr__(self):
        grid_repr = ''
        for row_n, row in enumerate(self.grid):
            grid_repr += '|'
            for i in range(self.w - 1):
                if row[i] == ' ':
                    grid_repr += ' '
                else:
                    grid_repr += '*'
                if row[i] == row[i+1]:
                    grid_repr += ' '
                else:
                    grid_repr += '|'
            if row[-1] == ' ':
                grid_repr += ' |\n'
            else:
                grid_repr += '*|\n'

            if row_n + 1 < self.h:
                for j, element in enumerate(row):
                    grid_repr += '+'
                    if self.grid[row_n+1][j] == element:
                        grid_repr += ' '
                    else:
                        grid_repr += '-'
                grid_repr += '+\n'

        return grid_repr

    def __hash__(self):
        return self.hash

    def __eq__(self, other):
        return self.hash == other.hash

def solve(starting_board):
    board_ls = [starting_board]
    closed_set = set()

    while board_ls:
        current = board_ls.pop(0)
        #print(len(closed_set))
        closed_set.add(current)
        if current.goal_reached():
            return current
        for block in ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'):
            for direction in ('left', 'right', 'up', 'down'):
                new_board = current.move(block, direction)

                if (new_board and 
                    new_board not in closed_set):
                    if new_board not in board_ls or board_ls[board_ls.index(new_board)].moves > new_board.moves:
                        if current.action == new_board.action:
                            board_ls.insert(0, new_board)
                        else:
                            board_ls.append(new_board)

def show_solution(steps):
    i = 1
    for board, action in steps:
        print(i)
        print(*action)
        board.print_grid()
        print()
        input()
        i += 1
    print('End')

def solution_len(steps):
    prev_action = None
    i = 1
    for board, action in steps:
        if prev_action != action:
            prev_action = action
            i += 1
    return i

starting_grid =(( 'B', 'A', 'A', 'C' ),
                ( 'B', 'A', 'A', 'C' ),
                ( 'D', 'E', 'E', 'F' ),
                ( 'D', 'G', 'H', 'F' ),
                ( 'I', ' ', ' ', 'J' ))

starting_board = Board(starting_grid, None, None)

solution = solve(starting_board)
steps = solution.trace()

show_solution(steps)
print(solution.moves)