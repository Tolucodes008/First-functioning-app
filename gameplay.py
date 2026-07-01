import pygame
import sys
from coordinates import positions, North, South, East, West, NorthEast, NorthWest, SouthWest, SouthEast, CYAN, OFF_WHITE, GRAY, DARK_GRAY, Player, PieceType, MoveType, endreason, counting 
window = pygame.display.set_mode((2560, 1440)) 
from typing import Optional
# Initialize pygame
pygame.init()
# Load font
base_font = pygame.font.SysFont("Segoe UI", 48)
button_font = pygame.font.SysFont("Segoe UI", 30)
bold_font = pygame.font.SysFont("Segoe UI", 30, bold =True)
menu_font = pygame.font.SysFont("arial", 48, bold=True)
pygame.display.set_caption("Toluchess")





class draw_board:

    def __init__(self, screen):
        self.pawn_skip_position: dict[Player, Optional[positions]] = {
            Player.White: None,
            Player.Black: None
        }
        self.selectedpos = None
        self.screen = screen
        self.COLS = 8
        self.ROWS = 8
        self.grid_size = 1000
        self.player_points = {
            Player.White: 0,
            Player.Black:0
        }
        self.promotion = False
        self.black_player = "Anonymous"
        self.white_player = "Anonymous"
        self.cell_size = self.grid_size//self.COLS
        self.board = [[NonePiece() for i in range(self.COLS) ] for j in range(self.ROWS)]
        self.offset_x =  1200 - self.grid_size//2
        self.offset_y = 700 - self.grid_size//2
        self.currentHighlights = []
        self.movecache = {}
        self.gamestate = Gamestate(self, Player.White)
        self.menu_button_rect = pygame.Rect(1900, 1300, 300, 60)
        self.menu_button_rect_text = base_font.render("Go to menu", True, (DARK_GRAY))
        self.table_button_rect = pygame.Rect(1900, 1300, 300, 60)
        self.table_button_rect_text = base_font.render("See table", True, (DARK_GRAY))
        self.points_for_white_button = pygame.Rect(150, 1150, 500, 100)
        self.points_for_black_button = pygame.Rect(150, 150, 500, 100)
        self.whitetimer_rect = pygame.Rect(1900, 1150, 300, 100)
        self.blacktimer_rect = pygame.Rect(1900, 150, 300, 100)
        self.white_timer = Timer(600)
        self.black_timer = Timer(600)
        self.white_timer.start()
        
    def draw_grid(self):
        self.screen.fill(DARK_GRAY)
        letters = {0:"a", 1:"b", 2:"c", 3:"d", 4:"e", 5:"f", 6:"g", 7:"h"}
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if (row + col) % 2 == 0:
                    self.cell_colour = OFF_WHITE
                    colour = CYAN
                        
                else:
                    self.cell_colour = CYAN
                    colour = OFF_WHITE
                self.cell = pygame.Rect((self.offset_x + (col * self.cell_size)),
                                         (self.offset_y + (row * self.cell_size)), 
                                         self.cell_size, self.cell_size ) 
                pygame.draw.rect(self.screen, self.cell_colour, self.cell )
               
                
                if col == 0:
                    num = str((row-8) * -1)
                    column_text = button_font.render(num, True, (colour))
                    center_column_text = column_text.get_rect()
                    center_column_text.bottomleft = self.cell.bottomleft
                    self.screen.blit(column_text, center_column_text)
                if row == 7:
                    letter = letters[col]
                    row_text = button_font.render(letter, True, (colour))
                    center_row_text = row_text.get_rect()
                    center_row_text.bottomright = self.cell.bottomright
                    self.screen.blit(row_text, center_row_text)
                

    

    def draw_pieces(self, screen, image_loader):
            for row in range(self.ROWS):
                for col in range(self.COLS):
                    piece = self.board[row][col]


                    if not isinstance(piece, NonePiece):
                        image = image_loader.get_image(piece.colour(), piece.type())
                        x = self.offset_x + col * self.cell_size
                        y = self.offset_y + row * self.cell_size
                        screen.blit(image, (x, y))

    def cacheMoves(self, from_pos):
        self.movecache.clear()
        for move in self.gamestate.legalMovesforpieces(from_pos):
            to_pos = move.To_pos()
            self.movecache[to_pos]= move

    def showHighlightedMoves(self):
        highlighted_colour = (0,128,0, 100)
        for key in self.currentHighlights:
            highlight_cell = pygame.Rect((self.offset_x + (key.column * self.cell_size)),
                                         (self.offset_y + (key.row * self.cell_size)), 
                                         self.cell_size, self.cell_size )
            s = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
            s.fill(highlighted_colour)
            self.screen.blit(s, (highlight_cell.x, highlight_cell.y))
        






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
        else:
            return False
        
    def isEmpty(self, pos:positions):
        if isinstance(self[pos], NonePiece):
            return True
        else:
            return False



    

    def Onfrompositionselected(self, pos):
        piece = self[pos]
        if isinstance(piece, NonePiece):
            return None

        if piece.colour() != self.gamestate.currentplayer:
            return None

        self.selectedpos = pos
        moves = self.gamestate.legalMovesforpieces(pos)
        if moves:
            self.cacheMoves(pos)
            self.currentHighlights = list(self.movecache.keys())
            

    def OnTopositionselected(self, pos):

        if pos in self.movecache:
            self.move: Move = self.movecache[pos]
            if self.move.type() == MoveType.Pawnpromotion:
                self.promotion = True
            else:
                self.HandleMove(self.move)
            self.selectedpos = None 
            self.currentHighlights = []
        else:
            self.Onfrompositionselected(pos)

    def draw_promotion_menu(self):
        prom_menu = pawnprom_menu(self, self.gamestate)
        prom_menu.draw_menu()
        prom_menu.draw_Image()

    def handle_promotion(self, event):
        if isinstance(self.move, pawn_promotion):
            self.move.newType=PieceType.Pawn
            if event.type == pygame.KEYDOWN:         
                if event.key == pygame.K_k:
                    self.move.newType = PieceType.Knight
                elif event.key == pygame.K_r:
                    self.move.newType = PieceType.Rook
                elif event.key == pygame.K_b:
                    self.move.newType = PieceType.Bishop
                elif event.key == pygame.K_q:
                    self.move.newType = PieceType.Queen
                if self.move.newType != PieceType.Pawn:
                    self.gamestate.MakeMove(self.move)
                    self.promotion = False


       
        
    def HandleMove(self, move):
        self.gamestate.MakeMove(move)


    def boardgrid_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
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

    def opponent(self, player):
        if player == Player.Black:
            return Player.White
        elif player == Player.White:
            return Player.Black
        else:
            return Player.none
        

    def piecepositions(self):
        for r in range(8):
            for c in range(8):
                pos = positions(r, c)
                if not self.isEmpty(pos):
                    yield pos
    
    def piecepositionsFor(self, player: Player):
        for pos in self.piecepositions():
            if self[pos].colour() == player:
                yield pos
    
    def isIncheck(self, player):
        for pos in self.piecepositionsFor(self.opponent(player)):
            piece = self[pos]
            if isinstance(piece, Piece) and piece.canCaptureOpponentKing(pos, self):
                return True
        return False

    
    def getPawnSkipPosition(self, player):
        return self.pawn_skip_position[player]

    def setPawnSkippedPosition(self, player, pos: Optional[positions]):
        self.pawn_skip_position[player] = pos
    
    def board_copy(self):
        copy = draw_board(self.screen)
        for pos in self.piecepositions():
            copy[pos] = self[pos].copy()
        return copy

    def countingpieces(self):
        Counting = counting()
        for pos in self.piecepositions():
            piece = self[pos]
            if not isinstance(piece, NonePiece):
                Counting.increment(piece.colour(), piece.type())
        return Counting
    
    def insufficientMaterial(self):
        counting = self.countingpieces()
        if self.iskingVking(counting) or self.iskingbishopVking(counting) or self.iskingknightVking(counting) or self.iskingbishopVkingbishop(counting):
            return True

    def iskingVking(self, Counting):
        if Counting.totalCount() == 2:
            return True
    def iskingbishopVking(self, Counting):
        if Counting.totalCount() == 3 and (Counting.White(PieceType.Bishop) == 1 or Counting.Black(PieceType.Bishop) == 1):
            return True
        
    def iskingknightVking(self, Counting):
        if Counting.totalCount() == 3 and (Counting.White(PieceType.Knight) == 1 or Counting.Black(PieceType.Knight) == 1):
            return True

    def iskingbishopVkingbishop(self, Counting):
        if Counting.totalCount() != 4:
            return False
        if Counting.White(PieceType.Bishop) != 1 and Counting.Black(PieceType.Bishop) != 1:
            return False
        wbishoppos = self.findpiece(Player.White, PieceType.Bishop)
        bbishoppos = self.findpiece(Player.Black, PieceType.Bishop)
        if wbishoppos is not None and bbishoppos is not None:
            if wbishoppos.checksquarecolour() == bbishoppos.checksquarecolour():
                return True
    def findpiece(self, color: Player, type: PieceType):
        for pos in self.piecepositionsFor(color):
            if self[pos].type() == type:
                return pos   


    def isunmovedkingandrook(self,king_pos: positions, rook_pos: positions):
        if self.isEmpty(king_pos) or self.isEmpty(rook_pos):
            return False
        rook = self[rook_pos]
        king = self[king_pos]
        if not rook.hasMoved and not king.hasMoved:
            return True
        
    def castlerightKS(self, player):
        if player == Player.White:
            return self.isunmovedkingandrook(positions(7, 4), positions(7,7))  
        elif player == Player.Black:
            return self.isunmovedkingandrook(positions(0, 4), positions(0,7)) 
        else:
            return False
        
    def castleftQs(self, player):
        if player == Player.White:
            return self.isunmovedkingandrook(positions(7, 4), positions(7,0))  
        elif player == Player.Black:
            return self.isunmovedkingandrook(positions(0, 4), positions(0,0)) 
        else:
            return False
        
    def Cancaptureenpassant(self, player):
        skippedpos = self.getPawnSkipPosition(self.opponent(player))
        if skippedpos == None:
            return False
        if player == Player.White:
            pawnpositions = [skippedpos + SouthEast, skippedpos + SouthWest]
        elif player == Player.Black:
            pawnpositions = [skippedpos + NorthEast, skippedpos + NorthWest]
        else:
            pawnpositions = []
        return self.HasPawnInPosition(player, pawnpositions, skippedpos)

    def HasPawnInPosition(self, player, pawnpositions: list[positions], skippedpos: positions):
        for pos in pawnpositions:
            if self.isInside(pos):
                pawn = self[pos]
                if isinstance(pawn, NonePiece) or pawn.type != PieceType.Pawn or pawn.colour() != player:
                    continue
                move = enPassant(pos, skippedpos, player)
                if move.is_Legal(self):
                    return True

    def draw_go_to_menu_button(self):
        pygame.draw.rect(self.screen, GRAY, self.menu_button_rect, 0, border_radius=10)   
        self.screen.blit(self.menu_button_rect_text, (self.menu_button_rect.x, self.menu_button_rect.y))
        
    def handle_go_to_menu_click(self, menu, event): 
        if event and event.type == pygame.MOUSEBUTTONDOWN:
                if self.menu_button_rect.collidepoint(event.pos):
                    menu.stage = "menu"

    def draw_go_to_table_button(self):
        pygame.draw.rect(self.screen, GRAY, self.table_button_rect, 0, border_radius=10)   
        self.screen.blit(self.table_button_rect_text, self.table_button_rect_text.get_rect(center = self.table_button_rect.center))
        
    def handle_go_to_table_click(self, menu, event):   
        if event and event.type == pygame.MOUSEBUTTONDOWN:
                if self.table_button_rect.collidepoint(event.pos):
                    menu.stage = "table"
    def points_for_pieces_taken(self):
        pygame.draw.rect(self.screen, OFF_WHITE, self.points_for_black_button, 0, border_radius=10)   
        pygame.draw.rect(self.screen, OFF_WHITE, self.points_for_white_button, 0, border_radius=10)  
        self.black_player_text = bold_font.render(self.black_player, True, (0,0,0))
        self.white_player_text = bold_font.render(self.white_player, True, (0,0,0)) 
        self.screen.blit(self.black_player_text, (self.points_for_black_button.x +10, self.points_for_black_button.y))
        self.screen.blit(self.white_player_text, (self.points_for_white_button.x +10, self.points_for_white_button.y))
        self.points_for_white_button_text = button_font.render(f"points from pieces taken: {str(self.player_points[Player.White])}", True, (0,0,0))
        self.points_for_black_button_text = button_font.render(f"points from pieces taken: {str(self.player_points[Player.Black])}", True, (0,0,0))
        self.screen.blit(self.points_for_black_button_text, (self.points_for_black_button.x +10, self.points_for_black_button.y +40))
        self.screen.blit(self.points_for_white_button_text, (self.points_for_white_button.x +10, self.points_for_white_button.y +40))


    def timers(self):
        pygame.draw.rect(self.screen, CYAN, self.blacktimer_rect, 10, border_radius=10)
        pygame.draw.rect(self.screen, CYAN, self.whitetimer_rect, 10, border_radius=10)
        self.white_time = self.white_timer.format_time()
        self.black_time = self.black_timer.format_time()
        self.white_timer_text = base_font.render(self.white_time, True, OFF_WHITE)
        self.black_timer_text = base_font.render(self.black_time, True, OFF_WHITE)
        self.screen.blit(self.white_timer_text, (self.white_timer_text.get_rect(center = self.whitetimer_rect.center)) )
        self.screen.blit(self.black_timer_text, (self.black_timer_text.get_rect(center = self.blacktimer_rect.center)))

    def final_points_forpieces_taken(self):
        if self.gamestate.Isgameover():
            return self.player_points
    def who_won(self):
        if isinstance(self.gamestate.Result, result): 
            return self.gamestate.Result.Winner   


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

    def canCaptureOpponentKing(self, From: positions, board: draw_board):
        return any(
            isinstance(piece := board[move.To_pos()], Piece) and piece.type() == PieceType.King
            for move in self.Get_moves(From, board)
        )




class NonePiece(Piece):
    def __init__(self):
        super().__init__(Player.none)
    def colour(self):
        return Player.none
    def type(self):
        return "none"
    
    def copy(self):
        copy = NonePiece()
        copy.hasMoved = self.hasMoved
        return copy
    
    def Get_moves(self, From: positions, board: draw_board):
        return []
    
    def canCaptureOpponentKing(self, From: positions, board: draw_board):
        return False


class pawn(Piece):

    def __init__(self, Colour: Player):
        super().__init__(Colour)
        if self.Colour == Player.Black:
            self.forward = South
        elif self.Colour == Player.White:
            self.forward = North
        else:
            self.forward = positions(0,0)
        
        
    
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
        else:
            return False
        
    def canCaptureTo(self, pos:positions, board: draw_board):
        if not board.isInside(pos):
            return False

        if board.isEmpty(pos):
            return False
        target: Piece = board[pos]
        if not board.isEmpty(pos):
            if target.colour() != self.colour():
                return True
            else:
                return False

            
    def ForwardMoves(self, From: positions, board: draw_board):

        oneMove = From + self.forward
        twoMove = oneMove + self.forward

        
        if self.canMoveTo(oneMove, board):
            if oneMove.row == 0 or oneMove.row == 7:
                for promMove in self.Promotionmoves(From, oneMove):
                    yield promMove
            else:
                yield Normalmove(From, oneMove, self)
            if self.hasMoved == False:
                if self.canMoveTo(twoMove, board):
                    yield DoublePawn(From, twoMove)




    def CaptureMoves(self, From:positions, board: draw_board):
        dirs: list[positions] = [East, West]
        for dir in dirs:
            to = From + self.forward + dir
            if to == board.getPawnSkipPosition(board.opponent(self.colour())):
                yield enPassant(From, to, self.colour())
            elif self.canCaptureTo(to, board):
                if to.row == 0 or to.row == 7:
                    for promMove in self.Promotionmoves(From, to):
                        yield promMove
                else:
                    yield Normalmove(From, to, self)


    def Get_moves(self, From: positions, board: draw_board):
        yield from self.ForwardMoves(From, board)
        yield from self.CaptureMoves(From, board)

    def canCaptureOpponentKing(self, From: positions, board: draw_board):
        return any(
            isinstance(piece:= board[move.To_pos()], Piece) and piece.type() == PieceType.King
            for move in self.CaptureMoves(From, board)
        )
    
    def Promotionmoves(self, From, To):
        self.From = From
        self.To = To
        yield pawn_promotion(self.From, self.To, PieceType.Knight)
        yield pawn_promotion(self.From, self.To, PieceType.Rook)
        yield pawn_promotion(self.From, self.To, PieceType.Bishop)
        yield pawn_promotion(self.From, self.To, PieceType.Queen)

    
    
    
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
    
    def canCaptureOpponentKing(self, From: positions, board: draw_board):
        return super().canCaptureOpponentKing(From, board)


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
    
    def canCaptureOpponentKing(self, From: positions, board: draw_board):
        return super().canCaptureOpponentKing(From, board)
    

    
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
    
    def canCaptureOpponentKing(self, From: positions, board: draw_board):
        return super().canCaptureOpponentKing(From, board)
    

    

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

    def canCaptureOpponentKing(self, From: positions, board: draw_board):
        return super().canCaptureOpponentKing(From, board)
    
class king(Piece):
    def __init__(self, Colour: Player):
        super().__init__(Colour)
        
    def type(self):
        return PieceType.King
    def colour(self):
        return self.Colour
    def copy(self):
        copy = king(self.Colour)
        copy.hasMoved = self.hasMoved
        return copy
    def MovePositions(self, From: positions, board: draw_board):
        self.dirs: list[positions] = [North, South, East, West, SouthEast, SouthWest, NorthEast, NorthWest]
        for dir in self.dirs:
            to = From + dir
            if board.isInside(to) == False:
                continue
            if board.isEmpty(to) or  board[to].colour() != self.Colour:
                yield to

    def Get_moves(self, From: positions, board: draw_board):
        for to in self.MovePositions(From, board):
            yield Normalmove(From, to, self)
        if self.CanCastleKingSide(From, board):
            yield castle(MoveType.Castleks, From, self.colour())
        if self.CanCastleQueenSide(From, board):
            yield castle(MoveType.CastleQS, From, self.colour())

    def canCaptureOpponentKing(self, From: positions, board: draw_board):
        return any(
            isinstance(piece:= board[move], Piece) and piece.type() == PieceType.King
            for move in self.MovePositions(From, board)
        )
    
    def isUnmovedRook(self, pos, board:draw_board):
        if board.isEmpty(pos):
            return False
        piece = board[pos]
        if piece.type() == PieceType.Rook and piece.hasMoved == False:
            return True
        
    def Allempty(self, positions: list[positions], board: draw_board):
        allempty = True
        for pos in positions:
            if board.isEmpty(pos) == False:
                allempty = False
        return allempty

    def CanCastleKingSide(self, From, board):
        if self.hasMoved:
            return False
        rookpos = positions(From.row, 7)
        betweenpositions: list[positions] = [positions(From.row, 6), positions(From.row, 5)]
        if self.Allempty(betweenpositions, board) and self.isUnmovedRook(rookpos, board):
            return True
        
    def CanCastleQueenSide(self, From, board):
        if self.hasMoved:
            return False
        rookpos = positions(From.row, 0)
        betweenpositions: list[positions] = [positions(From.row, 1), positions(From.row, 2), positions(From.row, 3)]
        if self.Allempty(betweenpositions, board) and self.isUnmovedRook(rookpos, board):
            return True






class Move:
    def __init__(self, From: positions, to: positions, piece):
        self.From = From
        self.to = to
        self.piece = piece
    def type(self):
        raise NotImplementedError("Subclasses must override type()")
    def Frompos(self):
        raise NotImplementedError("Subclasses must override Frompos()")
    def To_pos(self):
        raise NotImplementedError("Subclasses must override To_pos()")
    def execute(self, board: draw_board):
        raise NotImplementedError("Subclasses must override execute()")
    def is_Legal(self, board: draw_board):
        player = board[self.From].colour()
        board_copy = board.board_copy()
        self.execute(board_copy)
        if not board_copy.isIncheck(player):
            return True
        else:
            return False
    

class Normalmove(Move):

    def __init__(self, From: positions, to: positions, piece):
        super().__init__(From, to, piece)
    def type(self):
        return MoveType.Normal
    def Frompos(self):
        return self.From
    def To_pos(self):
        return self.to
    
    def execute(self, board: draw_board):    
        capture = False
        if not board.isEmpty(self.to):
            capture = True
        if not board.isEmpty(self.From):
            board[self.to] = self.piece
            board[self.From] = NonePiece()

        if capture == True or self.piece.type() == PieceType.Pawn:
            return True

    def is_Legal(self, board: draw_board):
        return super().is_Legal(board)


class pawn_promotion(Move):
    def __init__(self, From: positions, to:positions, newType: PieceType):
        super().__init__(From, to, None)
        self.newType = newType
    def type(self):
        return MoveType.Pawnpromotion
    def Frompos(self):
        return self.From
    def To_pos(self):
        return self.to
    def CreatePromotionPiece(self, color: Player):
        self.color = color
        if self.newType == PieceType.Knight:
            return knight(color)
        elif self.newType == PieceType.Bishop:
            return bishop(color)
        elif self.newType == PieceType.Rook:
            return rook(color)
        else:
            return queen(color)
    
    def execute(self, board: draw_board):
        Pawn = board[self.From]
        board[self.From] = NonePiece()
        promotionpiece = self.CreatePromotionPiece(Pawn.colour())
        promotionpiece.hasMoved = True
        board[self.to] = promotionpiece
        return True

class castle(Move):
    def __init__(self, Type: MoveType, kingpos: positions, color):
        self.From = kingpos
        self.Type = Type
        self.color = color
        if Type == MoveType.Castleks:
            self.Kingmovedir = East
            self.to = positions(kingpos.row, 6)
            self.rookfrompos = positions(kingpos.row, 7)
            self.rooktopos = positions(kingpos.row, 5)
        elif Type == MoveType.CastleQS:
            self.Kingmovedir = West
            self.to = positions(kingpos.row, 2)
            self.rookfrompos = positions(kingpos.row, 0)
            self.rooktopos = positions(kingpos.row, 3)
    def Frompos(self):
        return self.From
    def To_pos(self):
        return self.to
    def type(self):
        return self.Type

    def execute(self, board: draw_board):
        King = king(self.color)
        Rook = rook(self.color)
        Normalmove(self.From, self.to, King).execute(board)
        Normalmove(self.rookfrompos, self.rooktopos, Rook).execute(board)
        King.hasMoved = True
        Rook.hasMoved = True
        return False
    
    def is_Legal(self, board: draw_board):
        player = board[self.From].colour()
        kingFrompos = self.From
        if board.isIncheck(player):
            return False
        copy = board.board_copy()
        for i in range(2):
            Normalmove(kingFrompos, kingFrompos + self.Kingmovedir, king(player)).execute(copy)
            kingFrompos += self.Kingmovedir
            if copy.isIncheck(player):
                return False
        return True
    
class DoublePawn(Move):
    def __init__(self, From, to):
        self.From = From
        self.to = to
        self.skippedposition = positions((self.From.row + self.to.row)/2, self.From.column)
    def Frompos(self):
        return self.From
    def To_pos(self):
        return self.to
    def type(self):
        return MoveType.Doublepawn
    
    def execute(self, board: draw_board):
        player = board[self.From].colour()
        board.setPawnSkippedPosition(player, self.skippedposition)
        pawn = board[self.From]
        board[self.to] = pawn
        board[self.From] = NonePiece()
        pawn.hasMoved = True
        return True

class enPassant(Move):
    def __init__(self, From, to, color):
        self.From = From
        self.to = to  
        self.color = color
        self.capturepos = positions(self.From.row, self.to.column)
    def type(self):
        return MoveType.EnPassant  
    def Frompos(self):
        return self.From
    def To_pos(self):
        return self.to
    
    def execute(self, board: draw_board):
        Normalmove(self.From, self.to, pawn(self.color)).execute(board)
        board[self.capturepos] = NonePiece()
        return True
class result:
    def __init__(self, Winner: Player, Reason: endreason):
        self.Winner = Winner
        self.Reason = Reason

    def winner(self):
        return self.Winner
    
    def reason(self):
        return self.Reason
    

    

class Gamestate:
    def __init__(self, board: draw_board, currentplayer: Player):
        self.board = board
        self.currentplayer = currentplayer
        self.Result = None
        self.noCaptureorpawnmoves = 0
        self.statehistory = {}
        self.state_string = statestring(board, currentplayer).toString()
        self.statehistory[self.state_string] = 1
        


    def Board(self):
        return self.board
    def Currentplayer(self):
        return self.currentplayer
    def result(self, result):
        return result
    def legalMovesforpieces(self, pos: positions):
        if self.board.isEmpty(pos):
            return []

        piece = self.board[pos]
        if piece.colour() != self.currentplayer:
            return []
        
        moveCandidate = piece.Get_moves(pos, self.board)
        return filter(lambda move: move.is_Legal(self.board), moveCandidate)
    
    def AlllegalMovesfor(self, player:Player):
        move_candidates = (
        move
        for pos in self.board.piecepositionsFor(player)
        for move in self.board[pos].Get_moves(pos, self.board)
        )
        return filter(lambda move: move.is_Legal(self.board), move_candidates)
    
    def checkForgameover(self):
        if self.timeout():
            self.timeout_screen()
            return

        legal_moves = list(self.AlllegalMovesfor(self.currentplayer))
        if not legal_moves:
            if self.board.isIncheck(self.currentplayer):
                self.Result = result(self.board.opponent(self.currentplayer), endreason.Checkmate)
                self.checkmate_screen()
                

            else:
                self.Result = result(Player.none, endreason.Stalemate)

                self.stalemate_screen()

        elif self.board.insufficientMaterial():
            self.Result = result(Player.none, endreason.insuffecientMaterial)
            self.insufficient_material_screen()
        elif self.fiftymoverule():
            self.Result = result(Player.none, endreason.fiftyMoverule)
            self.fifty_move_rule_screen()

        elif self.threefoldrepitition():
            self.Result = result(Player.none, endreason.Threefoldrepition)
            self.threefold_repitition_screen()  

          

        
    def MakeMove(self, move: Move):

        self.board.setPawnSkippedPosition(self.currentplayer, None)
        self.move = move
        if not isinstance(move, castle):
            piece = self.board[move.To_pos()]
        else:
            piece = NonePiece()
        if piece.colour != self.currentplayer:
            if piece.type() == PieceType.Pawn:
                self.board.player_points[self.currentplayer] += 1
            elif piece.type() == PieceType.Rook:
                self.board.player_points[self.currentplayer] += 5
            elif piece.type() == PieceType.Knight:
                self.board.player_points[self.currentplayer] += 3
            elif piece.type() == PieceType.Bishop:
                self.board.player_points[self.currentplayer] += 3
            elif piece.type() == PieceType.Queen:
                self.board.player_points[self.currentplayer] += 9
            else:
                self.board.player_points[self.currentplayer] += 0
        if isinstance(move, enPassant):
            self.board.player_points[self.currentplayer] += 1
        captureorpawn = move.execute(self.board)
        if captureorpawn:
            self.noCaptureorpawnmoves = 0
        else:
            self.noCaptureorpawnmoves += 1
            print(self.noCaptureorpawnmoves)
        if isinstance(move, Normalmove):
            move.piece.hasMoved = True
        
        if self.currentplayer == Player.Black:
            self.board.black_timer.pause()
        else:
            self.board.white_timer.pause()
        self.PlayerSwitch()
        if self.currentplayer == Player.Black:
            self.board.black_timer.start()
        else:
            self.board.white_timer.start()
        self.updatestatestring()
        self.checkForgameover()



    def updatestatestring(self):
        self.state_string = statestring(self.board, self.currentplayer).toString()
        if self.state_string not in self.statehistory.keys():
            self.statehistory[self.state_string] = 1
        else:
            self.statehistory[self.state_string] += 1 

    def fiftymoverule(self):
        fullmoves = self.noCaptureorpawnmoves // 2
        if fullmoves >= 50:
            return True
    
    def threefoldrepitition(self):
        if self.statehistory[self.state_string] >= 3:
            return True
        else:
            return False
        
    def timeout(self):
        if self.board.white_timer.is_expired():
            self.Result = result(Player.Black, endreason.Timeout)
            return True
        elif self.board.black_timer.is_expired():
            self.Result = result(Player.White, endreason.Timeout)
            return True
        else:
            return False
        

    def PlayerSwitch(self):
        if self.currentplayer == Player.Black:
            self.currentplayer = Player.White
        elif self.currentplayer == Player.White:
            self.currentplayer = Player.Black

    def Isgameover(self):
        if self.Result != None:
            return True
        
    def checkmate_screen(self):
        menu = pygame.Rect(900, 200, 700, 850)

        pygame.draw.rect(self.board.screen,OFF_WHITE , menu, 0, border_radius = 25)
        if self.board.opponent(self.currentplayer) == Player.Black:
            text_1 = menu_font.render("BLACK WINS", True, CYAN, )
            text_2 = menu_font.render("BY CHECKMATE!!", True, CYAN, )
        else:
            text_1 = menu_font.render("WHITE WINS", True, CYAN, )
            text_2 = menu_font.render("BY CHECKMATE!!", True, CYAN, )
        self.board.screen.blit(text_1, (text_1.get_rect(center = menu.center)))
        text_2_rect = text_2.get_rect(center = menu.center)
        text_2_rect.y += 40
        self.board.screen.blit(text_2, (text_2_rect))

    def timeout_screen(self):
        menu = pygame.Rect(900, 200, 700, 850)

        pygame.draw.rect(self.board.screen,OFF_WHITE , menu, 0, border_radius = 25)
        if self.board.opponent(self.currentplayer) == Player.Black:
            text_1 = menu_font.render("BLACK WINS", True, CYAN, )
            text_2 = menu_font.render("BY TIMEOUT!!", True, CYAN, )
        else:
            text_1 = menu_font.render("WHITE WINS", True, CYAN, )
            text_2 = menu_font.render("BY TIMEOUT!!", True, CYAN, )
        self.board.screen.blit(text_1, (text_1.get_rect(center = menu.center)))
        text_2_rect = text_2.get_rect(center = menu.center)
        text_2_rect.y += 40
        self.board.screen.blit(text_2, (text_2_rect))



    def stalemate_screen(self):
        menu = pygame.Rect(900, 200, 700, 850)
        pygame.draw.rect(self.board.screen, OFF_WHITE , menu, 0, border_radius = 25)
        text = bold_font.render("DRAW BY STALEMATE :(", True, CYAN, )
        self.board.screen.blit(text, (text.get_rect(center = menu.center)))

    def insufficient_material_screen(self):
        menu = pygame.Rect(900, 200, 700, 850)
        pygame.draw.rect(self.board.screen, OFF_WHITE , menu, 0, border_radius = 25)
        text = bold_font.render("INSUFFICIENT MATERIAL :(", True, CYAN, )
        self.board.screen.blit(text, (text.get_rect(center = menu.center)))
    
    def fifty_move_rule_screen(self):
        menu = pygame.Rect(900, 200, 700, 850)
        pygame.draw.rect(self.board.screen, OFF_WHITE , menu, 0, border_radius = 25)
        text = bold_font.render("DRAW BY 50 MOVE RULE", True, CYAN, )
        self.board.screen.blit(text, (text.get_rect(center = menu.center)))

    def threefold_repitition_screen(self):
        menu = pygame.Rect(900, 200, 700, 850)
        pygame.draw.rect(self.board.screen, OFF_WHITE , menu, 0, border_radius = 25)
        text = bold_font.render("DRAW BY THREEFOLD REPITITION", True, CYAN, )
        self.board.screen.blit(text, (text.get_rect(center = menu.center)))



                
class pawnprom_menu:
    def __init__(self, board: draw_board, player: Gamestate):
        self.player = player
        self.board = board
        self.white_pieces = self.load_white_pieces()
        self.black_pieces = self.load_black_pieces()
    def draw_menu(self):
        if self.board.gamestate.Currentplayer() == Player.White:
            self.menu = pygame.Rect(900, 20, 600, 200)
        else:
            self.menu = pygame.Rect(900, 1100, 600, 200)
        pygame.draw.rect(self.board.screen, CYAN , self.menu, 0, border_radius = 10)
        text = button_font.render("Choose piece:", True, (0,0,0))
        self.board.screen.blit(text, (self.menu.x, self.menu.y+20 ))

    
    def load_white_pieces(self):
        return {
            PieceType.Rook: pygame.transform.scale(pygame.image.load("ChessAssets/RookW.png"), (self.board.cell_size,self.board.cell_size)),
            PieceType.Knight: pygame.transform.scale(pygame.image.load("ChessAssets/KnightW.png"), (self.board.cell_size,self.board.cell_size)),
            PieceType.Bishop: pygame.transform.scale(pygame.image.load("ChessAssets/BishopW.png"), (self.board.cell_size,self.board.cell_size)),
            PieceType.Queen: pygame.transform.scale(pygame.image.load("ChessAssets/QueenW.png"), (self.board.cell_size,self.board.cell_size)),
        }

    def load_black_pieces(self):
        return {
            PieceType.Rook: pygame.transform.scale(pygame.image.load("ChessAssets/RookB.png"), (self.board.cell_size,self.board.cell_size)),
            PieceType.Knight: pygame.transform.scale(pygame.image.load("ChessAssets/KnightB.png"), (self.board.cell_size,self.board.cell_size)),
            PieceType.Bishop: pygame.transform.scale(pygame.image.load("ChessAssets/BishopB.png"), (self.board.cell_size,self.board.cell_size)),
            PieceType.Queen: pygame.transform.scale(pygame.image.load("ChessAssets/QueenB.png"), (self.board.cell_size,self.board.cell_size)),
        }
    def get_image(self, colour: Player, type: PieceType):
        if colour == Player.White:
            return self.white_pieces[type]
        elif colour == Player.Black:
            return self.black_pieces[type]
        else:
            return None

    def draw_Image(self):
        piece = [PieceType.Knight, PieceType.Rook, PieceType.Bishop, PieceType.Queen]
        width = self.menu.width // 4
        for i, ptype in enumerate(piece):
            img = self.get_image(self.player.currentplayer, ptype)
            if img is None:
                continue
            x = self.menu.x + (width * i) + (width // 2)
            y = self.menu.y + 110

            img_rect = img.get_rect(center=(x, y))
            self.board.screen.blit(img, img_rect)


class statestring():
    def __init__(self, board, player):
        self.sb = []
        self.addpieceplacement(board)
        self.addcurrentplayer(player)
        self.addcastlingrights(board)
        self.addenpassant(board, player)
    
    def toString(self):
        string = " ".join(self.sb)
        return string

    
    def piecechar(self, piece: Piece):
        if piece.type() == PieceType.Bishop:
           c = "b"
        elif piece.type() == PieceType.Pawn:
           c = "p"
        elif piece.type() == PieceType.Rook:
           c = "r"
        elif piece.type() == PieceType.Knight:
           c = "n"
        elif piece.type() == PieceType.King:
           c = "k"
        elif piece.type() == PieceType.Queen:
           c = "q"

        else:
            c = " "
        if piece.colour() == Player.White:
            return c.upper()
        else:
            return c
        
    def Addrowdata(self, board: draw_board, row):
        empty = 0
        for col in range(8):
            piece = board[positions(row, col)]
            if isinstance(piece, NonePiece):
                empty += 1
                continue
            if empty > 0:
                self.sb.append(str(empty))
                empty = 0
            self.sb.append(self.piecechar(piece))
        if empty > 0:
            self.sb.append(str(empty))

    def addpieceplacement(self, board):
        for i in range(8):
            if i != 0:
                self.sb.append("/")
            self.Addrowdata(board, i)

    def addcurrentplayer(self, player):
        if player == Player.White:
            self.sb.append("w")
        else:
            self.sb.append("b")

    def addcastlingrights(self, board:draw_board):
        castleWQS = board.castleftQs(Player.White)
        castleBQS = board.castleftQs(Player.Black)
        castleWKS = board.castlerightKS(Player.White)
        castleBKS = board.castlerightKS(Player.Black)
        if not(castleBKS or castleBQS or castleWKS or castleWQS):
            self.sb.append("_")
            return
        if castleWQS:
            self.sb.append("Q")
        if castleWKS:
            self.sb.append("K")
        if castleBQS:
            self.sb.append("q")
        if castleBKS:
            self.sb.append("k")
        
    def addenpassant(self, board: draw_board, currentplayer):
        if not board.Cancaptureenpassant(currentplayer):
            self.sb.append("_")
            return
        pos = board.getPawnSkipPosition(board.opponent(currentplayer))
        files = ["a", "b", "c", "d", "e", "f", "g", "h"]
        if pos is not None:
            file = files[pos.column]
            rank = 8 - pos.row
            self.sb.append(file)
            self.sb.append(str(rank))
        

class Timer:
    def __init__(self, initial_seconds):
        self.initial_seconds = initial_seconds
        self.remaining_seconds = initial_seconds
        self.start_ticks = 0
        self.is_running = False
    
    def start(self):
        if not self.is_running:
            self.start_ticks = pygame.time.get_ticks()
            self.is_running = True
    
    def pause(self):
        if self.is_running:
            # Calculate how much time has passed
            elapsed = (pygame.time.get_ticks() - self.start_ticks) / 1000
            # Subtract from remaining time
            self.remaining_seconds -= elapsed
            # Stop the timer
            self.is_running = False
            self.start_ticks = 0
    
    def reset(self):
        self.remaining_seconds = self.initial_seconds
        self.start_ticks = 0
        self.is_running = False
    
    def get_time(self):
        if self.is_running:
            elapsed = (pygame.time.get_ticks() - self.start_ticks) / 1000
            time_left = self.remaining_seconds - elapsed
            return max(0, time_left)
        else:
            return max(0, self.remaining_seconds)
    
    def is_expired(self):

        return self.get_time() <= 0
    
    def format_time(self):
        time = self.get_time()
        minutes = int(time // 60)
        seconds = int(time % 60)
        return f"{minutes:02d}:{seconds:02d}"

