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

import pygame


class Window():
    def __init__(self, height, width, fps, cellSize, board):
        self.fps = fps
        self.cellSize = cellSize
        self.board = board
        self.height = self.cellSize * self.board.height
        self.width = self.cellSize * self.board.width
        self.size = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("nokIA* Simulation Software")

    def drawBoard(self):
        self.board.updateBoard()
        self.screen.fill(pygame.Color("gray18"))
        for i in range(self.board.height):
            for j in range(self.board.width):
                typeElement = int(str(self.board.board[i, j])[:1])
                if typeElement != 0:
                    getColor = int(str(self.board.board[i, j])[1:])
                    if len(str(getColor)) < 9:
                        getColor = str(getColor).zfill(9)
                    colorList = list(map(int, str(getColor)))
                    color = (int(str(colorList[0]) + str(colorList[1]) + str(colorList[2])), int(str(colorList[3]) + str(
                        colorList[4]) + str(colorList[5])), int(str(colorList[6]) + str(colorList[7]) + str(colorList[8])))
                circle_loc = (int((j+0.5)*self.cellSize),
                              int((i+0.5)*self.cellSize))
                rect_loc = (j*self.cellSize, i*self.cellSize,
                            self.cellSize, self.cellSize)
                if typeElement == 1:
                    pygame.draw.circle(
                        self.screen, color, circle_loc, self.cellSize//2)
                elif typeElement == 2:
                    pygame.draw.rect(self.screen, color,
                                     rect_loc, 0, self.cellSize//3)
                elif typeElement == 3:
                    pygame.draw.circle(
                        self.screen, color, circle_loc, self.cellSize//4)
        pygame.display.update()
