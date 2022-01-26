# Copyright (C) 2022 Gaëtan LE HEURT-FINOT
# This file is part of nokIA* <https://github.com/gaetanlhf/nokIASTAR>.

# nokIA* is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# nokIA* is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with nokIA*.  If not, see <http://www.gnu.org/licenses/>.

import numpy
from snake import Snake
from apple import Apple
from node import Node


class Board():
    def __init__(self, height, width, nbSnake, nbApple):
        self.playing = True
        self.height = height
        self.width = width
        self.nbSnake = nbSnake
        self.board = numpy.zeros([self.height, self.width], dtype=int)
        self.globalScore = 0
        self.snakeList = []
        self.appleList = []
        for i in range(nbSnake):
            snake = Snake(self, self.height, self.width)
            for s in snake.body:
                self.board[s[0], s[1]] = snake.bodyIdColor
            self.board[snake.head[0], snake.head[1]] = snake.headIdColor
            self.snakeList.append(snake)

        for i in range(nbApple):
            self.__addApple()

    def updateBoard(self):
        if len(self.snakeList) != 0:
            for snake in self.snakeList:
                snake.update()
                if snake.alive == False:
                    print(f"A snake died with a score of {snake.ownScore}.")
                    snake.clear()
                    self.snakeList.remove(snake)
                    del snake
        else:
            self.playing = False

    def __addApple(self):
        apple = Apple(self.height, self.width, self.board)
        self.board[apple.position[0], apple.position[1]] = apple.appleIdColor
        self.appleList.append(apple)

    def appleEaten(self, pos):
        for apple in self.appleList:
            if apple.position == pos:
                a = self.appleList.index(apple)
                a = self.appleList.pop(a)
                del apple
        self.__addApple()
