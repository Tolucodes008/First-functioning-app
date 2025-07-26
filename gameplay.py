import pygame
import sys
from coordinates import positions, North, South, East, West, NorthEast, NorthWest, SouthWest, SouthEast, CYAN, OFF_WHITE, GRAY, DARK_GRAY
from typing import Optional

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




class draw_board:

    def __init__(self, screen):
        self.selectedpos = None
        self.screen = screen
        self.COLS = 8
        self.ROWS = 8
        self.grid_size = 800
        self.cell_size = self.grid_size//self.COLS
        self.board = [[NonePiece() for i in range(self.COLS) ] for j in range(self.ROWS)]
        self.offset_x =  1200 - self.grid_size//2
        self.offset_y = 700 - self.grid_size//2
        self.movecache = {}
        self.gamestate = Gamestate(self, Player.White)
    
    def print_board(self):
        for row in self.board:
            line = ""
            for piece in row:
                if isinstance(piece, NonePiece):
                    line += ". "  # use "." for empty
                else:
                    abbrev = piece.__class__.__name__[0].upper()
                    if piece.colour() == Player.White:
                        line += abbrev + "W "
                    elif piece.colour() == Player.Black:
                        line += abbrev + "B "
                    else:
                        line += abbrev + "? "
            print(line)
        print() 

    
    def draw_grid(self):
        self.screen.fill(DARK_GRAY)
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if (row + col) % 2 == 0:
                    self.cell_colour = OFF_WHITE
                else:
                    self.cell_colour = CYAN
                self.cell = pygame.Rect((self.offset_x + (col * self.cell_size)),
                                         (self.offset_y + (row * self.cell_size)), 
                                         self.cell_size, self.cell_size ) 
                pygame.draw.rect(self.screen, self.cell_colour, self.cell )
                

    

    def draw_pieces(self, screen, image_loader):
            for row in range(self.ROWS):
                for col in range(self.COLS):
                    piece = self.board[row][col]


                    if not isinstance(piece, NonePiece):
                        image = image_loader.get_image(piece.colour(), piece.type())
                        x = self.offset_x + col * self.cell_size
                        y = self.offset_y + row * self.cell_size
                        screen.blit(image, (x, y))


    def showHighlightedMoves(self):
        for key in self.movecache:
            highlight_cell = pygame.Rect((self.offset_x + (key.column * self.cell_size)),
                                         (self.offset_y + (key.row * self.cell_size)), 
                                         self.cell_size, self.cell_size )
            pygame.draw.rect(self.screen, (0,128,0), highlight_cell)
            print("im green")
            pygame.display.update()


    def HideHighlightedMoves(self, show):
        if show == True:
            for key in self.movecache:
                highlight_cell = pygame.Rect((self.offset_x + (key.column * self.cell_size)),
                                            (self.offset_y + (key.row * self.cell_size)), 
                                            self.cell_size, self.cell_size )
                pygame.draw.rect(self.screen, (0,128,0), highlight_cell)
                pygame.display.update()



    def __getitem__(self, pos: positions):
        return self.board[pos.row][pos.column]
    
    def __setitem__(self, pos: positions, value):
        self.board[pos.row][pos.column] = value

    def get_position(self, pos: positions):
        return self.board[pos.row][pos.column]
    
    def set_position(self, pos: positions, value):
        self.board[pos.row][pos.column] = value

    def initial(self, image_loader):
        self.image_loader = image_loader
        self.draw_grid()
        self.draw_pieces(self.screen, self.image_loader)
        

    def AddstartPieces(self):
       self[positions(0,0)] = rook(Player.Black)
       self[positions(0, 1)] = knight(Player.Black)
       self[positions(0, 2)] = bishop(Player.Black)
       self[positions(0, 3)] = queen(Player.Black)
       self[positions(0, 4)] = king(Player.Black)
       self[positions(0, 5)] = bishop(Player.Black)
       self[positions(0, 6)] = knight(Player.Black)
       self[positions(0, 7)] = rook(Player.Black)
       for col in range(8):
            self[positions(1, col)] = pawn(Player.Black)


       self[positions(7, 0)] = rook(Player.White)
       self[positions(7, 1)] = knight(Player.White)
       self[positions(7, 2)] = bishop(Player.White)
       self[positions(7, 3)] = queen(Player.White)
       self[positions(7, 4)] = king(Player.White)
       self[positions(7, 5)] = bishop(Player.White)
       self[positions(7, 6)] = knight(Player.White)
       self[positions(7, 7)] = rook(Player.White)
       for col in range(8):
            self[positions(6, col)] = pawn(Player.White)

    def isInside(self, pos:positions):
        if pos.row >= 0 and pos.row < 8 and pos.column >=0 and pos.column < 8:
            return True
        
    def isEmpty(self, pos:positions):
        if isinstance(self[pos], NonePiece):
            return True
        else:
            return False
        
    def cacheMoves(self, moves: list['Move']):
        self.movecache.clear()
        for move in moves:
            self.movecache[move.To_pos()] = move

    

    def Onfrompositionselected(self, pos):
        piece = self[pos]
        if isinstance(piece, NonePiece):
            return None

        if piece.colour() != self.gamestate.currentplayer:
            print("Cannot select opponent's piece")
            return None

        self.selectedpos = pos
        moves = self.gamestate.legalMovesforpieces(pos)
        if moves:
            self.cacheMoves(moves)
            self.showHighlightedMoves()

    def OnTopositionselected(self, pos):
        print("i'm empty")
        self.HideHighlightedMoves(False)
        if pos in self.movecache:
            move = self.movecache[pos]
            self.HandleMove(move)
            self.gamestate.PlayerSwitch()
            self.selectedpos = None 
        else:
            print(f"Clicked invalid move position or empty square without selection: {pos}")

    def HandleMove(self, pos):
        print(f"Handling move: {pos}")
        self.gamestate.MakeMove(pos)
 



    def boardgrid_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.print_board()
            mouse_x, mouse_y = event.pos
            grid_x = mouse_x - self.offset_x
            grid_y = mouse_y - self.offset_y

            if 0 <= grid_x < self.grid_size and 0 <= grid_y < self.grid_size:
                col = grid_x // self.cell_size
                row = grid_y // self.cell_size
                pos = positions(row, col)

                if self.selectedpos is None:
                    if not isinstance(self.board[row][col], NonePiece) and self[pos].colour() == self.gamestate.currentplayer:
                        self.Onfrompositionselected(pos)
                else:
                    self.OnTopositionselected(pos)


class Piece():
    def __init__(self, Colour: Player):
         self.hasMoved = False 
         self.Colour = Colour
    def type(self):
        raise NotImplementedError("Subclasses must override type()")
    def colour(self):
        raise NotImplementedError("Subclasses must override colour()")
    
    def copy(self):
        raise NotImplementedError("Subclasses must override copy()")
    def Get_moves(self, From: positions, board: draw_board) :
        raise NotImplementedError("Subclasses must override Get_moves()")

    def _Movepositionsindir(self, From: positions, board: draw_board, dir : positions):
        pos = From + dir
        while board.isInside(pos) == True:
                piece: Piece = board[pos]
                if isinstance(piece, NonePiece):
                    yield pos
                else:
                    
                    if piece.colour() != self.colour():
                        yield pos
                    print(pos)
                    
                    break

                pos += dir

    def move_positions_in_dirs(self, From: positions, board: draw_board, dirs: list):
        for dir in dirs:
            yield from self._Movepositionsindir(From, board, dir)


class NonePiece(Piece):
    def __init__(self):
        super().__init__(Player.none)
    def colour(self):
        return Player.none
    def type(self):
        return "none"

class pawn(Piece):

    def __init__(self, Colour: Player):
        super().__init__(Colour)
        self.Colour = Colour
        if self.Colour == Player.Black:
            self.forward = South
        elif self.Colour == Player.White:
            self.forward = North
        else:
            self.forward = None
    
    def type(self):
        return PieceType.Pawn
    
    def colour(self):
        return self.Colour
    
    def copy(self):
        copy = pawn(self.Colour)
        copy.hasMoved = self.hasMoved
        return copy
    
    def canMoveTo(self, pos: positions, board: draw_board):
        if board.isEmpty(pos) == True and board.isInside(pos) == True:
            return True
        
    def canCaptureTo(self, pos:positions, board: draw_board):
        if not board.isInside(pos):
            return False

        if board.isEmpty(pos):
            return False
        target: Piece = board[pos]
        if not board.isEmpty(pos) and target.colour() != None:
            if target.colour() != self.colour():
                return True
            else:
                return False

            
    def ForwardMoves(self, From: positions, board: draw_board):
        oneMove = From + self.forward
        twoMove = oneMove +self.forward
        if self.canMoveTo(oneMove, board) == True:
            yield Normalmove(From, oneMove, self)
            if self.hasMoved == False and self.canMoveTo(twoMove, board) == True:
                yield Normalmove(From, twoMove, self)

    def CaptureMoves(self, From:positions, board: draw_board):
        dirs: list[positions] = [East, West]
        for dir in dirs:
            to = From + self.forward + dir
            if self.canCaptureTo(to, board) == True:
                yield Normalmove(From, to, self)

    def Get_moves(self, From: positions, board: draw_board):
        yield from self.ForwardMoves(From, board)
        yield from self.CaptureMoves(From, board)
    
    
    
class bishop(Piece):
    def __init__(self, Colour: Player):
        super().__init__(Colour)
    def type(self):
        return PieceType.Bishop
    def colour(self):
        return self.Colour
    def copy(self):
        copy = bishop(self.Colour)
        copy.hasMoved = self.hasMoved
        return copy
   
    def Get_moves(self, From: positions, board: draw_board):
        dirs: list[positions] = [NorthEast, NorthWest, SouthEast, SouthWest]
        return map(lambda to: Normalmove(From, to, self), self.move_positions_in_dirs(From, board, dirs))

class knight(Piece):
    def __init__(self, Colour: Player):
        super().__init__(Colour)
    def type(self):
        return PieceType.Knight
    def colour(self):
        return self.Colour
    def copy(self):
        copy = knight(self.Colour)
        copy.hasMoved = self.hasMoved
        return copy
    
    def potentialTopositions(self, From):
        vdirs: list[positions] = [South, North]
        hdirs: list[positions] = [East, West]
        for vdir in vdirs:
            for hdir in hdirs:
                yield From + vdir * 2 + hdir
                yield From + hdir * 2 + vdir

    def Movepositions(self, From: positions, board: draw_board):
        for pos in self.potentialTopositions(From): 
            if board.isInside(pos) and (board[pos] is NonePiece or board[pos].Colour != self.Colour):
                yield pos

        
    def Get_moves(self, From: positions, board: draw_board):
        return map(lambda to: Normalmove(From, to, self), self.Movepositions(From, board))
    
class rook(Piece):
    def __init__(self, Colour: Player):
        super().__init__(Colour)
    def type(self):
        return PieceType.Rook
    def colour(self):
        return self.Colour
    def copy(self):
        copy = rook(self.Colour)
        copy.hasMoved = self.hasMoved
        return copy
    def Get_moves(self, From: positions, board: draw_board):
        dirs: list[positions] = [North, East, South, West]
        return map(lambda to: Normalmove(From, to, self), self.move_positions_in_dirs(From, board, dirs))
    

class queen(Piece):
    def __init__(self, Colour: Player):
        super().__init__(Colour)
    def type(self):
        return PieceType.Queen
    def colour(self):
        return self.Colour
    def copy(self):
        copy = queen(self.Colour)
        copy.hasMoved = self.hasMoved
        return copy
    def Get_moves(self, From: positions, board: draw_board):
        dirs: list[positions] = [NorthEast, NorthWest, SouthEast, SouthWest, North, South, East, West]
        return map(lambda to: Normalmove(From, to, self), self.move_positions_in_dirs(From, board, dirs))
    
class king(Piece):
    def __init__(self, Colour: Player):
        super().__init__(Colour)
        self.dirs: list[positions] = [North, South, East, West, SouthEast, SouthWest, NorthEast, NorthWest]
    def type(self):
        return PieceType.King
    def colour(self):
        return self.Colour
    def copy(self):
        copy = king(self.Colour)
        copy.hasMoved = self.hasMoved
        return copy
    def MovePositions(self, From: positions, board: draw_board):
        for dir in self.dirs:
            to = From + dir
            if board.isInside(to) == False:
                continue
            print(f"Checking position {to}: empty? {board.isEmpty(to)}, piece: {board[to]}")
            if board.isEmpty(to) or  board[to].colour() != self.Colour:
                yield to

    def Get_moves(self, From: positions, board: draw_board):
        for to in self.MovePositions(From, board):
            yield Normalmove(From, to, self)


class Move:
    def type(self):
        raise NotImplementedError("Subclasses must override type()")
    def Frompos(self):
        raise NotImplementedError("Subclasses must override Frompos()")
    def To_pos(self):
        raise NotImplementedError("Subclasses must override To_pos()")
    def execute(self, board: draw_board):
        raise NotImplementedError("Subclasses must override execute()")
    

class Normalmove(Move):

    def __init__(self, From: positions, to: positions, piece):
        self.From = From
        self.To = to
        self.piece = piece
    def type(self):
        return MoveType.Normal
    def Frompos(self):
        return self.From
    def To_pos(self):
        return self.To
    
    def execute(self, board: draw_board):
        print("I'm here")
        if not board.isEmpty(self.From):
            board[self.To] = self.piece
            board[self.From] = NonePiece()
            print(f"Moved {self.piece.type()} to {self.To}")
            if not isinstance(self.piece, NonePiece):
                self.piece.hasMoved = True
    


class Gamestate:
    def __init__(self, board: draw_board, currentplayer: Player):
        self.board = board
        self.currentplayer = currentplayer
    def Board(self):
        return self.board
    def Currentplayer(self):
        return self.currentplayer
    
    def legalMovesforpieces(self, pos: positions):
        if self.board.isEmpty(pos):
            return []

        piece = self.board[pos]
        if piece.colour() != self.currentplayer:
            return []
        else:
            return piece.Get_moves(pos, self.board)

        
    def MakeMove(self, move: Move):
        print(f"Making move from {move.Frompos()} to {move.To_pos()}")
        move.execute(self.board)

    def PlayerSwitch(self):
        if self.currentplayer == Player.Black:
            self.currentplayer = Player.White
        elif self.currentplayer == Player.White:
            self.currentplayer = Player.Black
        