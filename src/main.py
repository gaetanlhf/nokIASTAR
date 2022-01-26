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

from os import environ
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
from window import Window
from board import Board
import argparse
import math


class Main():
    def __init__(self, height, width, cellSize, fps, nbSnake, nbApple):
        self.height = height
        self.width = width
        self.fps = fps
        self.cellSize = cellSize
        self.nbSnake = nbSnake
        self.nbApple = nbApple
        self.board = Board(self.height, self.width, self.nbSnake, self.nbApple)
        self.window = Window(self.height, self.width, self.fps,
                             self.cellSize, self.board)
        pygame.init()
        self.clock = pygame.time.Clock()
        self.startTime = pygame.time.get_ticks()
        self.time = None
        self.quit = False

    def run(self):
        print("Welcome to the nokIA* Simulation Software.")
        print(
            f"Stating simulation with a height of {self.height} cells, a width of {self.width} cells, a cell size of {self.cellSize}, {self.fps} frame(s) per second, {self.nbSnake} snake(s) and {self.nbApple} apple(s).")

        while self.quit == False:
            self.clock.tick(60)
            if self.board.playing == True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.quit = True
                self.window.drawBoard()
                self.clock.tick(self.fps)
                self.time = pygame.time.get_ticks() - self.startTime
            else:
                self.__end()
        self.__end()

    def __end(self):
        pygame.quit()
        timeMin = str(math.floor(self.time/60000)).zfill(2)
        timeSec = str(math.floor((self.time % 60000)/1000)).zfill(2)
        timeMili = str(math.floor(self.time % 1000)).zfill(3)
        if self.quit == True:
            print("The simulation has been stopped by the user.")
        else:
            print("The simulation is now complete.")
        print(
            f"A total amount of {self.board.globalScore} apple(s) have been eaten by snake(s).")
        print(f"The simulation lasted {timeMin}m {timeSec}s {timeMili}ms.")
        quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="The nokIA* snake simuluation software")
    parser.add_argument("-ch", "--cellHeight", help="The number of cells in the height",
                        default="20", type=int, required=True)
    parser.add_argument("-cw", "--cellWidth", help="The number of cells in the width",
                        default="20", type=int, required=True)
    parser.add_argument("-cs", "--cellSize", help="The cell size",
                        default="20", type=int, required=True)
    parser.add_argument("-f", "--fps", help="The number of frames per second",
                        default="60", type=int, required=True)
    parser.add_argument("-s", "--snake", help="The number of snakes",
                        default="1", type=int, required=True)
    parser.add_argument("-a", "--apple", help="The number of apples",
                        default="1", type=int, required=True)
    args = parser.parse_args()
    main = Main(args.cellHeight, args.cellWidth,
                args.cellSize, args.fps, args.snake, args.apple)
    main.run()
