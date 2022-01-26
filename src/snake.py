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

import random
from brain import Brain


class Snake():
    def __init__(self, board, height, width):
        self.board = board
        self.height = height
        self.width = width
        self.directions = [[-1, 0], [0, -1], [1, 0], [0, 1]]
        self.direction = random.Random().choice(self.directions)
        self.cost = 1
        self.alive = True
        self.ownScore = 0
        self.headColor = self.__randomColor()
        self.bodyColor = self.__randomColor()
        self.headIdColor = int(
            str(1) + str(self.headColor[0]) + str(self.headColor[1]) + str(self.headColor[2]))
        self.bodyIdColor = int(
            str(2) + str(self.bodyColor[0]) + str(self.bodyColor[1]) + str(self.bodyColor[2]))
        self.body = []
        self.head = self.__randomPos()
        for i in range(3):
            self.body += [[self.head[0] - i*self.direction[0],
                           self.head[1] - i*self.direction[1]]]
        self.brain = Brain(self)

    def __randomColor(self):
        color = random.choices(range(256), k=3)
        for i in range(3):
            color[i] = str(color[i]).zfill(3)
        return color

    def __randomPos(self):
        row = []
        col = []
        for i in range(self.height):
            for j in range(self.width):
                if self.board.board[i, j] == 0:
                    row += [i]
                    col += [j]
        return [random.Random().choices(row)[0]//2,
                random.Random().choices(col)[0]//2]

    def update(self):
        self.direction = self.brain.shortestPath() or self.brain.largestPath()
        self.head[0] += self.direction[0]
        self.head[1] += self.direction[1]
        if self.head[0] < 0 or self.head[0] >= self.height:
            self.head = self.body[0].copy()
            self.alive = False
        elif self.head[1] < 0 or self.head[1] >= self.width:
            self.head = self.body[0].copy()
            self.alive = False
        elif self.head in self.body[2::]:
            self.head = self.body[0].copy()
            self.alive = False
        elif self.head not in self.body:
            if self.__searchPositionInList(self.board.appleList, self.head):
                self.board.globalScore += 1
                self.ownScore += 1
                self.body.insert(0, self.head.copy())
                self.board.board[self.body[1][0],
                                 self.body[1][1]] = self.bodyIdColor
                self.board.board[self.head[0], self.head[1]] = self.headIdColor
                self.board.appleEaten(self.head)
            else:
                self.body.insert(0, self.head.copy())
                self.board.board[self.body[1][0],
                                 self.body[1][1]] = self.bodyIdColor
                self.board.board[self.head[0], self.head[1]] = self.headIdColor
                remove = self.body.pop()
                self.board.board[remove[0], remove[1]] = 0
                i = 1
        else:
            self.head = self.body[0].copy()

    def __searchPositionInList(self, list, item):
        for i in range(len(list)):
            if list[i].position == item:
                return True
        return False

    def clear(self):
        self.board.board[self.head[0], self.head[1]] = 0
        for i in range(len(self.body)):
            self.board.board[self.body[i][0], self.body[i][1]] = 0
