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
        return positions(int(self.row + other.row), int(self.column + other.column))
    def __mul__(self,scalar):
        if not isinstance(scalar, int):
            return NotImplemented
        return positions(
            self.row * scalar, self.column * scalar
        )
    def checksquarecolour(self):
        if (self.row + self.column) % 2 == 0:
            return "white"
        else:
            return "black"
    


 
North = positions(-1,0)
South = positions(1,0)
East =positions(0,1)
West = positions(0,-1)
NorthEast = North + East
SouthEast = South + East
NorthWest = North + West
SouthWest = South + West

from enum import Enum
class Player(Enum):
    none = 1
    White = 2
    Black = 3

class PieceType(Enum):
    King = 1
    Queen = 2
    Rook = 3
    Knight = 4
    Bishop = 5
    Pawn = 6

class MoveType(Enum):
    Normal = 1
    Castleks = 2
    CastleQS = 3
    Doublepawn = 4
    EnPassant = 5
    Pawnpromotion = 6

class endreason(Enum):
    Checkmate = 1
    Stalemate = 2
    fiftyMoverule = 3
    insuffecientMaterial = 4
    Threefoldrepition = 5
    Timeout = 6


class counting:        
    def __init__(self):
        self.whiteCount = {
            PieceType.Pawn:0,
            PieceType.Bishop:0,
            PieceType.Rook:0,
            PieceType.Knight:0,
            PieceType.King:0,
            PieceType.Queen:0
        }
        self.blackCount = {
            PieceType.Pawn:0,
            PieceType.Bishop:0,
            PieceType.Rook:0,
            PieceType.Knight:0,
            PieceType.King:0,
            PieceType.Queen:0
        }
        self.totalcount = 0
    def totalCount(self):
        return self.totalcount
    def increment(self, color: Player, type: PieceType):
        if color == Player.White:
            self.whiteCount[type] += 1
        elif color == Player.Black:
            self.blackCount[type] += 1
        self.totalcount += 1
    
    def White(self, type):
        return self.whiteCount[type]
    
    def Black(self, type):
        return self.blackCount[type]



             


    
