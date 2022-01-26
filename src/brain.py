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
from node import Node


class Brain():
    def __init__(self, snake):
        self.snake = snake

    def __solvePath(self, currentNode):
        path = []
        current = currentNode
        while current is not None:
            path.append(current.position)
            current = current.parent
        path = path[::-1]
        if len(path) > 1:
            return [path[1][0]-self.snake.head[0], path[1][1]-self.snake.head[1]]
        else:
            self.snake.alive = False
            return [0, 0]

    def shortestPath(self, end=None):
        startNode = Node(None, self.snake.head)
        toVisit = []
        visited = []
        toVisit.append(startNode)
        while len(toVisit) > 0:
            distance = None
            currentNode = toVisit.pop(0)
            for apple in self.snake.board.appleList:
                if distance is None:
                    distance = (((currentNode.position[0]-apple.position[0]) ** 2) + (
                        (currentNode.position[1]-apple.position[1]) ** 2))**0.5
                    selectedApple = apple
                    endNode = Node(None, (end or selectedApple.position))
                elif (((currentNode.position[0]-apple.position[0]) ** 2) + ((currentNode.position[1]-apple.position[1]) ** 2))**0.5 > distance:
                    continue
                distance = (((currentNode.position[0]-apple.position[0]) ** 2) + (
                    (currentNode.position[1]-apple.position[1]) ** 2))**0.5
                selectedApple = apple
                endNode = Node(None, (end or selectedApple.position))
            visited.append(currentNode)
            if currentNode == endNode:
                return self.__solvePath(currentNode)
            for direction in self.snake.directions:
                newPosition = [currentNode.position[0] +
                               direction[0], currentNode.position[1] + direction[1]]
                if (newPosition[0] > (self.snake.board.height-1) or
                        newPosition[0] < 0 or
                        newPosition[1] > (self.snake.board.width-1) or
                        newPosition[1] < 0):
                    continue
                if int(str(self.snake.board.board[newPosition[0]][newPosition[1]])[:1]) == 1:
                    continue
                if int(str(self.snake.board.board[newPosition[0]][newPosition[1]])[:1]) == 2:
                    continue
                newNode = Node(currentNode, newPosition)
                newNode.g = currentNode.g + self.snake.cost
                newNode.h = (((newNode.position[0]-endNode.position[0]) ** 2) + (
                    (newNode.position[1]-endNode.position[1]) ** 2))**0.5
                newNode.f = newNode.g + newNode.h
                if newNode in visited:
                    continue
                if newNode not in toVisit:
                    toVisit.insert(0, newNode)
                    toVisit.sort(key=lambda x: x.f)
                    if endNode.position != selectedApple.position:
                        toVisit.reverse()

    def largestPath(self):
        blanks = []
        visited = []
        toVisit = []
        toVisit.append(self.snake.head)
        blanks.append(self.snake.head)
        temp = 0
        near = None
        while len(toVisit) > 0:
            distance = None
            position = toVisit.pop(0)
            for apple in self.snake.board.appleList:
                if distance is None:
                    distance = (((position[0]-apple.position[0]) ** 2) + (
                        (position[1]-apple.position[1]) ** 2))**0.5
                    selectedApple = apple
                else:
                    if (((position[0]-apple.position[0]) ** 2) + ((position[1]-apple.position[1]) ** 2))**0.5 > distance:
                        continue
                    distance = (((position[0]-apple.position[0]) ** 2) + (
                        (position[1]-apple.position[1]) ** 2))**0.5
                    selectedApple = apple
            visited.append(position)
            for direction in self.snake.directions:
                newPosition = [position[0] + direction[0],
                               position[1] + direction[1]]
                if (newPosition[0] > (self.snake.board.height-1) or
                        newPosition[0] < 0 or
                        newPosition[1] > (self.snake.board.width-1) or
                        newPosition[1] < 0):
                    continue
                if int(str(self.snake.board.board[newPosition[0]][newPosition[1]])[:1]) == 1:
                    continue
                if int(str(self.snake.board.board[newPosition[0]][newPosition[1]])[:1]) == 2:
                    continue
                if newPosition in visited:
                    continue
                if newPosition not in toVisit:
                    toVisit.append(newPosition)
                    blanks.append(newPosition)
        for i in range(len(blanks)):
            heuristic = ((blanks[i][0]-selectedApple.position[0])**2 +
                         (blanks[i][1]-selectedApple.position[1])**2)**0.5
            if heuristic > temp:
                temp = heuristic
                near = blanks[i].copy()
        return self.shortestPath(near)
