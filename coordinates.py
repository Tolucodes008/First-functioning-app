import pygame
import sys

CYAN = (35, 181, 211)
DARK_GRAY = (70, 73, 76)
GRAY = (158, 158, 158)
OFF_WHITE = (223, 224, 226)

class positions:
    def __init__(self, row, column):
        self.row = row
        self.column = column
    def __hash__(self):
        return hash((self.row, self.column))
    def __eq__(self, other):
        if not isinstance(other, positions):
            return NotImplemented
        return self.row == other.row and self.column == other.column
    def __ne__(self, other):
        return not self == other
    def __add__(self,other):
        if not isinstance(other, positions):
            return NotImplemented
        return positions(self.row + other.row, self.column + other.column)
    def __mul__(self,scalar):
        if not isinstance(scalar, int):
            return NotImplemented
        return positions(
            self.row * scalar, self.column * scalar
        )



 
North = positions(-1,0)
South = positions(1,0)
East =positions(0,1)
West = positions(0,-1)
NorthEast = North + East
SouthEast = South + East
NorthWest = North + West
SouthWest = South + West