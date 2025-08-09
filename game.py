import random
import os
import sys
import tty
import termios


def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")


def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        if ch == "\x1b":
            ch += sys.stdin.read(2)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


class Game2048:
    def __init__(self):
        self.size = 4
        self.score = 0
        self.board = [[0] * self.size for _ in range(self.size)]
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty_cells = [
            (r, c)
            for r in range(self.size)
            for c in range(self.size)
            if self.board[r][c] == 0
        ]
        if empty_cells:
            r, c = random.choice(empty_cells)
            self.board[r][c] = 4 if random.random() < 0.1 else 2

    def can_move(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == 0:
                    return True
                if c < self.size - 1 and self.board[r][c] == self.board[r][c + 1]:
                    return True
                if r < self.size - 1 and self.board[r][c] == self.board[r + 1][c]:
                    return True
        return False

    def compress(self, row):
        new_row = [i for i in row if i != 0]
        new_row += [0] * (self.size - len(new_row))
        return new_row

    def merge(self, row):
        for i in range(self.size - 1):
            if row[i] != 0 and row[i] == row[i + 1]:
                row[i] *= 2
                self.score += row[i]
                row[i + 1] = 0
        return row

    def move_left(self):
        moved = False
        for i in range(self.size):
            original = list(self.board[i])
            compressed = self.compress(original)
            merged = self.merge(compressed)
            new_row = self.compress(merged)
            self.board[i] = new_row
            if new_row != original:
                moved = True
        return moved

    def move_right(self):
        self.reverse()
        moved = self.move_left()
        self.reverse()
        return moved

    def move_up(self):
        self.transpose()
        moved = self.move_left()
        self.transpose()
        return moved

    def move_down(self):
        self.transpose()
        moved = self.move_right()
        self.transpose()
        return moved

    def reverse(self):
        for i in range(self.size):
            self.board[i].reverse()

    def transpose(self):
        self.board = [list(row) for row in zip(*self.board)]

    def draw(self):
        clear_screen()
        print(f"Score: {self.score}\n")
        for row in self.board:
            print("+------" * self.size + "+")
            print(
                "".join(
                    f'|{str(num).center(6) if num != 0 else "      "}' for num in row
                )
                + "|"
            )
        print("+------" * self.size + "+")
        print("\nUse arrow keys to move. Press 'q' to quit.")

    def play(self):
        while True:
            self.draw()
            if not self.can_move():
                print("Game Over! No more moves.")
                break
            key = getch()
            moved = False
            if key == "\x1b[A":
                moved = self.move_up()
            elif key == "\x1b[B":
                moved = self.move_down()
            elif key == "\x1b[C":
                moved = self.move_right()
            elif key == "\x1b[D":
                moved = self.move_left()
            elif key in ("q", "Q"):
                print("Quitting game...")
                break
            if moved:
                self.add_new_tile()


if __name__ == "__main__":
    game = Game2048()
    game.play()
