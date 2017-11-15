import time
import pygame

SIZE = 8

BLANK = 0
WHITE = 1
BLACK = 2

TIME_LIMIT = 20  # seconds


class Reversi:
    def __init__(self, board=None, player=None, discs=None):
        self.board = Reversi.gen_board() if board is None else board
        self.player = WHITE if player is None else player
        self.discs = [sum(self.board[i][j] == k for i in range(SIZE) for j in range(SIZE))
                      for k in range(2)] if discs is None else discs

    def __str__(self):
        board_copy = Reversi.gen_board()
        spaces = set(self.get_move_spaces())
        print(spaces)
        for i, row in enumerate(self.board):
            for j, val in enumerate(row):
                board_copy[i][j] = "X" if (i, j) in spaces else val
        return Reversi.print_board(board_copy)

    def execute(self, space):
        if space is not None:
            for x_delta in [-1, 0, 1]:
                for y_delta in [-1, 0, 1]:
                    if x_delta | y_delta == 0:
                        continue
                    to_change = []
                    pos = (space[0] + x_delta, space[1] + y_delta)
                    while all(0 <= i < SIZE for i in pos) and self.board[pos[0]][pos[1]] == Reversi.opposite(
                            self.player):
                        to_change.append(pos)
                        pos = (pos[0] + x_delta, pos[1] + y_delta)
                    if all(0 <= i < SIZE for i in pos) and self.board[pos[0]][pos[1]] == self.player:
                        for coord in to_change:
                            self.board[coord[0]][coord[1]] = self.player
                            self.discs[self.player] += 1
                            self.discs[Reversi.opposite(self.player)] -= 1
            self.board[space[0]][space[1]] = self.player
            self.discs[self.player] += 1
            self.discs[BLANK] -= 1
        self.player = Reversi.opposite(self.player)
        return self

    def evaluate(self):
        assert sum(self.discs) == SIZE ** 2
        if self.discs[BLANK] == 0:
            return float("inf") if self.discs[self.player] >= self.discs[Reversi.opposite(self.player)] else float(
                "-inf")

        disc_count = self.discs[self.player] - self.discs[Reversi.opposite(self.player)]
        moves_count = len(set(self.get_move_spaces())) - len(
            set(self.get_move_spaces(player=Reversi.opposite(self.player))))
        corner_count = sum(1 if self.board[i][j] == self.player else 0 for i in (0, SIZE - 1) for j in (0, SIZE - 1)) \
                       - sum(
            1 if self.board[i][j] == Reversi.opposite(self.player) else 0 for i in (0, SIZE - 1) for j in
            (0, SIZE - 1))  # TODO: Fix!!!
        return corner_count * 10 + moves_count + disc_count / 10

    def get_move_spaces(self, player=None):
        board = self.board
        player = self.player if player is None else player

        for i in (Reversi.get_move_spaces_worker(board, player)):
            yield i
        for i in ((j, i) for i, j in
                  Reversi.get_move_spaces_worker(((board[row][col] for row in range(SIZE)) for col in range(SIZE)),
                                                 player)):
            yield i
        for i in ((max(0, SIZE - 1 - delta) + index, max(0, 1 - SIZE + delta) + index)
                  for delta, index in
                  Reversi.get_move_spaces_worker(((board[max(0, -delta) + index][max(0, delta) + index]
                                                   for index in range(SIZE - abs(delta)))
                                                  for delta in range(1 - SIZE, SIZE)
                                                  ), player)):
            yield i
        for i in ((max(0, SIZE - 1 - delta) + index, SIZE - 1 - max(0, 1 - SIZE + delta) - index)
                  for delta, index in
                  Reversi.get_move_spaces_worker(((board[max(0, -delta) + index][SIZE - 1 - max(0, delta) - index]
                                                   for index in range(SIZE - abs(delta)))
                                                  for delta in range(1 - SIZE, SIZE)
                                                  ), player)):
            yield i

    @staticmethod
    def print_board(board):
        return "\n".join((" ".join(map(str, row)) for row in board))

    @staticmethod
    def gen_board():
        board = []
        for i in range(SIZE):
            board.append([BLANK] * SIZE)
        return board

    @staticmethod
    def get_move_spaces_worker(rows, player):
        # row_list = list([list(row) for row in rows])
        # print(row_list)
        enemy = Reversi.opposite(player)
        for row_index, row in enumerate(rows):
            potential = None
            state = 0  # [Blank]...
            for column_index, val in enumerate(row):
                if val == player:
                    if state == 0 or state == 1:
                        state = 1  # [Player]...
                    elif state == 2:
                        state = 1
                        if potential:
                            # print(potential)
                            yield potential
                    elif state == 3:
                        # raise ValueError("Invalid input board")
                        state = 1
                    potential = None
                elif val == enemy:
                    if state == 0:
                        state = 2  # [Enemy]...
                    elif state == 1:
                        state = 3  # [Player][Enemy]...
                elif val == BLANK:
                    potential = (row_index, column_index)
                    if state == 3:
                        yield potential
                        # print(potential)
                        potential = None
                        state = 0
                    elif state == 1 or state == 2:
                        state = 0
                        # print()

    @staticmethod
    def opposite(player):
        if player == BLANK:
            raise ValueError()
        return (player % 2) + 1

    def copy(self):
        return Reversi([row[:] for row in self.board],
                       player=self.player,
                       discs=self.discs[:])

    def hash(self):
        return "".join("".join(map(str, row)) for row in self.board) + str(self.player)


def draw_board(board):
    pygame.display.set_mode((800, 800))


def main():
    state = Reversi(board=[
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 2, 0, 0, 0],
        [0, 0, 0, 2, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]

    ], player=2, discs=[60, 2, 2])

    print(state)

    # computer_move = pick_move(state)
    # state.execute(computer_move)
    # print(computer_move)
    # print(state)

    while True:
        try:
            x, y = map(int, input().split())
            state.execute((x, y))
            print(state)
            computer_move = pick_move(state)
            state.execute(computer_move)
            print(computer_move)
            print(state)
        except KeyboardInterrupt as e:
            break


def alpha_beta(start, depth, alpha, beta, start_time,
               cache={}):  # Outputs estimated "value" of state for the next player to move
    if start_time + TIME_LIMIT < time.time():
        return None, None, True
    moves = list(start.get_move_spaces())
    if not moves:
        moves = [None]
    # print(moves)
    if depth == 0:
        evaluation = start.evaluate()
        cache[start.hash()] = evaluation
        return evaluation, cache, False
    next_states = [start.copy().execute(move) for move in moves]
    value = float("-inf")
    for next_state in sorted(next_states, key=lambda x: cache.get(x.hash(), x.evaluate()), reverse=True):
        temp = alpha_beta(next_state, depth - 1, -beta, -alpha, start_time)
        if temp[2]:
            return None, None, True
        value = max(value, -temp[0])
        alpha = max(alpha, value)
        if beta < alpha:
            break
    cache[start.hash()] = value
    return value, cache, False


def pick_move(start):
    moves = dict((move, float("-inf")) for move in start.get_move_spaces())
    start_time = time.time()
    depth = 3
    cache = {}
    while start_time + TIME_LIMIT > time.time():
        print(depth)
        out = alpha_beta(start, depth, float("-inf"), float("inf"), start_time)
        if not out[2]:
            cache = out[1]
        depth += 1
    print(len(cache))
    print(min([cache[start.copy().execute(x).hash()] for x in moves]))
    print(cache[start.hash()])
    return min(moves, key=lambda x: cache[start.copy().execute(x).hash()])


if __name__ == '__main__':
    pass
    # main()
