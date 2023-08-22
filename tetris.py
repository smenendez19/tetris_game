# Tetris en Python
# Desarrollado por Santiago Menendez, pero no llegue a los 40 minutos permitidos por lo que no quede

import os
import random
import time

import keyboard

# Blocks


class Block:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.shape = []
        self.x_shape = 0
        self.y_shape = 0

    def move(self, move):
        if move == "down":
            self.y += 1
        elif move == "left":
            self.x -= 1
        elif move == "right":
            self.x += 1
        else:
            self.y += 1

    def rotate(self):
        # Rotate shape to right
        self.shape = list(zip(*self.shape[::-1]))
        # Update shape size
        self.x_shape, self.y_shape = self.y_shape, self.x_shape

    def __str__(self):
        return str(self.__class__.__name__)


class OShape(Block):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.shape = [[1, 1], [1, 1]]
        self.x_shape = 2
        self.y_shape = 2


class IShape(Block):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.shape = [[1], [1], [1], [1]]
        self.x_shape = 1
        self.y_shape = 4


class JShape(Block):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.shape = [[0, 1], [0, 1], [1, 1]]
        self.x_shape = 2
        self.y_shape = 3


class LShape(Block):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.shape = [[1, 0], [1, 0], [1, 1]]
        self.x_shape = 2
        self.y_shape = 3


class TShape(Block):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.shape = [[1, 1, 1], [0, 1, 0]]
        self.x_shape = 3
        self.y_shape = 2


class SShape(Block):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.shape = [[0, 1, 1], [1, 1, 0]]
        self.x_shape = 3
        self.y_shape = 2


class ZShape(Block):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.shape = [[1, 1, 0], [0, 1, 1]]
        self.x_shape = 3
        self.y_shape = 2


class Game:
    def __init__(self):
        self.x_table = 10
        self.y_table = 15
        self.y_start_block = 0
        self.table = [
            [" " for _ in range(self.x_table)]
            for _ in range(self.y_table + self.y_start_block)
        ]
        self.lines = 0
        self.velocity = 5
        self.velocity_ticks = 5
        self.lose = False
        self.block = None
        self.next_block = None
        self.ticks = 0
        self.moved = True

    def start(self):
        self.block = self.generate_block(self.x_table // 2, 0)
        self.next_block = self.generate_block(self.x_table // 2, 0)

        while not self.lose:
            self.update()
            time.sleep(0.1)

    def delete_lines(self):
        # Delete lines
        lines_deleted = 0
        for i in range(0, self.y_table):
            delete_line = True
            for j in range(0, self.x_table):
                if self.table[i][j] != "0":
                    delete_line = False
                    break
            if delete_line:
                self.lines += 1
                lines_deleted += 1
                for k in range(i, 0, -1):
                    for j in range(0, self.x_table):
                        self.table[k][j] = self.table[k - 1][j]
                for j in range(0, self.x_table):
                    self.table[0][j] = " "
        return lines_deleted

    def clear_table(self):
        # Clear table
        for i in range(self.y_table):
            for j in range(self.x_table):
                if self.table[i][j] != "0":
                    self.table[i][j] = " "

    def draw(self):
        # Clear console
        os.system("cls")
        # Print top border
        for j in range(self.x_table + 2):
            print("-", end="")
        print()
        # Print table
        for i in range(self.y_start_block, self.y_table):
            for j in range(self.x_table):
                if j == 0:
                    print("|", end="")
                print(self.table[i][j], end="")
                if j == self.x_table - 1:
                    print("|", end="")
            print()
        # Print bottom border and info
        for j in range(self.x_table + 2):
            print("-", end="")
        print()
        print("Next block: " + str(self.next_block))
        print(
            "Lines: "
            + str(self.lines)
            + " | Ticks: "
            + str(self.ticks)
            + " | Velocity: "
            + str(self.velocity)
        )
        if self.block is not None:
            print("Block coords: " + str(self.block.x) + ", " + str(self.block.y))
        if self.lose:
            print("You lose!")

    def generate_block(self, x, y):
        if self.next_block is not None:
            self.block = self.next_block
        return random.choice(
            [
                JShape(x, y),
                LShape(x, y),
                OShape(x, y),
                IShape(x, y),
                TShape(x, y),
                SShape(x, y),
                ZShape(x, y),
            ]
        )

    def update(self):
        # Update ticks
        self.ticks += 1
        self.velocity_ticks -= 1

        lines_deleted = self.delete_lines()

        if lines_deleted > 0 and self.lines % 10 == 0 and self.velocity > 1:
            self.velocity -= 1

        self.clear_table()

        if self.lose:
            return

        # Move or generate new block
        if self.block is None:
            # Generate new block in table
            self.block = self.next_block
            self.next_block = self.generate_block(self.x_table // 2, 0)
            # Check if a block obstructs the spawn
            for i in range(0, self.block.y_shape):
                for j in range(0, self.block.x_shape):
                    if self.block.shape[i][j] == 1:
                        if self.table[self.block.y + i][self.block.x + j] == "0":
                            self.lose = True
                            break

            # Update block in table
            for i in range(self.block.y, self.block.y + self.block.y_shape):
                for j in range(self.block.x, self.block.x + self.block.x_shape):
                    if self.block.shape[i - self.block.y][j - self.block.x] == 1:
                        self.table[i][j] = "X"
        else:
            # Check keyboard press or move down in x time
            if self.moved:
                self.moved = False
            elif not self.moved:
                if keyboard.is_pressed("left"):
                    # Check collision left
                    move_left = True
                    for i in range(0, self.block.y_shape):
                        for j in range(0, self.block.x_shape):
                            # Collision with left border
                            if self.block.x == 0:
                                move_left = False
                                break
                            # Collision with another block
                            elif self.block.shape[i][j] == 1:
                                if (
                                    self.table[self.block.y + i][self.block.x - 1]
                                    == "0"
                                ):
                                    move_left = False
                                    break
                                else:
                                    move_left = True
                        if not move_left:
                            break
                    if move_left:
                        self.block.move("left")
                elif keyboard.is_pressed("right"):
                    # Check collision right
                    move_right = True
                    for i in range(0, self.block.y_shape):
                        for j in range(0, self.block.x_shape):
                            # Collision with right border
                            if self.block.x + self.block.x_shape == self.x_table:
                                move_right = False
                                break
                            # Collision with another block
                            elif self.block.shape[i][j] == 1:
                                if (
                                    self.table[self.block.y + i][self.block.x + j + 1]
                                    == "0"
                                ):
                                    move_right = False
                                    break
                                else:
                                    move_right = True
                        if not move_right:
                            break
                    if move_right:
                        self.block.move("right")
                elif keyboard.is_pressed("down"):
                    # Check colision down
                    move_down = True
                    for i in range(0, self.block.y_shape):
                        for j in range(0, self.block.x_shape):
                            # Collision with bottom border
                            if self.block.y + self.block.y_shape == self.y_table:
                                move_down = False
                                break
                            # Collision with another block
                            if self.block.shape[i][j] == 1:
                                if (
                                    self.table[self.block.y + i + 1][self.block.x + j]
                                    == "0"
                                ):
                                    move_down = False
                                    break
                                else:
                                    move_down = True
                        if not move_down:
                            break
                    if move_down:
                        self.block.move("down")
                # Rotate key
                elif keyboard.is_pressed("up"):
                    # Check if block can rotate
                    can_rotate = True
                    if self.block.x + self.block.y_shape > self.x_table:
                        can_rotate = False
                    else:
                        for i in range(self.block.y_shape):
                            for j in range(self.block.x_shape):
                                if self.block.shape[i][j] == 1:
                                    if (
                                        self.table[self.block.y + j][self.block.x + i]
                                        == "0"
                                    ):
                                        can_rotate = False
                                        break
                            if not can_rotate:
                                break
                    if can_rotate:
                        self.block.rotate()
                # Quit tetris
                elif keyboard.is_pressed("space"):
                    self.lose = True
            # Check if block is used
            used_block = False
            for i in range(0, self.block.y_shape):
                for j in range(0, self.block.x_shape):
                    # Collision with bottom border
                    if self.block.y + self.block.y_shape == self.y_table:
                        used_block = True
                        break
                    # Collision with another block
                    if self.block.shape[i][j] == 1:
                        if self.table[self.block.y + i + 1][self.block.x + j] == "0":
                            used_block = True
                            break
                        else:
                            used_block = False
                if used_block:
                    break
            if used_block:
                # Update block to used block in table
                for i in range(self.block.y, self.block.y + self.block.y_shape):
                    for j in range(self.block.x, self.block.x + self.block.x_shape):
                        if self.block.shape[i - self.block.y][j - self.block.x] == 1:
                            self.table[i][j] = "0"
                self.block = None

            # Update block in table
            if self.block is not None:
                for i in range(self.block.y, self.block.y + self.block.y_shape):
                    for j in range(self.block.x, self.block.x + self.block.x_shape):
                        if self.block.shape[i - self.block.y][j - self.block.x] == 1:
                            self.table[i][j] = "X"

        # Push down block
        if self.velocity_ticks == 0:
            self.velocity_ticks = self.velocity
            if self.block is not None:
                # Check colision down
                move_down = True
                for i in range(0, self.block.y_shape):
                    for j in range(0, self.block.x_shape):
                        # Collision with bottom border
                        if self.block.y + self.block.y_shape == self.y_table:
                            move_down = False
                            break
                        # Collision with another block
                        if self.block.shape[i][j] == 1:
                            if (
                                self.table[self.block.y + i + 1][self.block.x + j]
                                == "0"
                            ):
                                move_down = False
                                break
                            else:
                                move_down = True
                    if not move_down:
                        break
                if move_down:
                    self.block.move("down")

        # Draw table
        self.draw()


if __name__ == "__main__":
    game = Game().start()
