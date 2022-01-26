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


class Apple():
    def __init__(self, height, width, board):
        self.height = height
        self.width = width
        self.color = ["255", "000", "000"]
        self.board = board
        self.position = self.__randomPos()
        self.appleIdColor = int(
            str(3) + str(self.color[0]) + str(self.color[1]) + str(self.color[2]))

    def __randomPos(self):
        blanks = []
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i, j] == 0:
                    blanks += [[i, j]]
        return random.Random().choices(blanks)[0]
