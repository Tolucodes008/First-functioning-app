import pygame
import sys
from coordinates import positions, CYAN, GRAY, DARK_GRAY, OFF_WHITE
from gameplay import Piece, draw_board, Player, PieceType, NonePiece


print("nice")
print("Board id:", id(draw_board))

# Initialize pygame
pygame.init()

# Set up game window
window = pygame.display.set_mode((2560, 1440)) 
pygame.display.set_caption("Toluchess")
# Define colors





# Load font
base_font = pygame.font.SysFont("Segoe UI", 50)
button_font = pygame.font.SysFont("Segoe UI", 30)


class MainMenu:
    def __init__(self, screen):
        self.stage = "create account"
        self.logo = pygame.Rect(380, 100, 1500, 100)
        self.screen = screen
        #attributes for account creation
        self.username = ''
        self.input_rect = pygame.Rect(1000, 700, 300, 60)
        # creating buttons
        self.menu_button_rect = pygame.Rect(1500, 1000, 300, 60)
        self.play_game_button = pygame.Rect(1635, 680, 300, 100)
        self.tourn_menu_button = pygame.Rect(300, 550, 300, 100)
        self.past_games_button = pygame.Rect(800, 550, 300, 100)
        self.cust_button = pygame.Rect(550, 750, 300, 100)

        

        #creating string attributes for different buttons and rendering them
        self.logo_text = base_font.render("TOLUCHESS", True, (OFF_WHITE))
        self.menu_button_rect_text = base_font.render("Go to menu", True, (DARK_GRAY))
        self.play_game_button_text = button_font.render("PLAY GAME", True, (0,0,0))
        self.tourn_button_text_1 = button_font.render("TOURNAMENT", True, (0,0,0))
        self.tourn_button_text_2 = button_font.render("MENU", True, (0,0,0))
        self.past_games_button_text = button_font.render("PAST GAMES", True, (0,0,0))
        self.cust_button_text = button_font.render("CUSTOMISATION", True, (0,0,0))


        self.active = False
        self.rect_colour = CYAN
        
        self.menu_chess_board = pygame.image.load("Screenshot 2025-07-04 8.25.39 PM.png")
#username can be entered as input to be stored in a text file
    def create_account(self, event):
        
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_rect.collidepoint(event.pos):
                    self.active = True
                    self.rect_colour = (255,255,255)

            if event.type == pygame.KEYDOWN:
                if self.active == True:
                    if event.key == pygame.K_BACKSPACE:
                        self.username = self.username[:-1]
                    elif len(self.username) < 20:
                        self.username += event.unicode
                # checks for length validation
                    if event.key == pygame.K_RETURN:
                        clean_username = self.username.strip()
                        if len(clean_username) > 5:
                            with open("usernames.txt", "a") as file:
                                file.write(self.username + "\n")
                                file.close()
                                self.username = self.username[:-(len(self.username))]
                        else:
                            self.username = self.username[:-(len(self.username))]
                            
                                
            self.screen.fill(DARK_GRAY)
            #write instructions for user
            input_instruction = base_font.render("Enter usernames here", True, (255,255,255))
            self.screen.blit(input_instruction, (1000, 600))
                # Draw username text
            pygame.draw.rect(self.screen, self.rect_colour, self.input_rect, 2)
            text_surface = base_font.render(self.username, True, (255, 255, 255))
            self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y ))
            self.input_rect.w = max(50, text_surface.get_width() + 10)
            # drawing the go to menu button
            pygame.draw.rect(self.screen, GRAY, self.menu_button_rect, 0, border_radius=10)
            
            self.screen.blit(self.menu_button_rect_text, (self.menu_button_rect.x, self.menu_button_rect.y))

        #behaviour of go to menu button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.menu_button_rect.collidepoint(event.pos):
                    self.stage = "menu"
        
                
    def menu(self, event):
            self.screen.fill(DARK_GRAY)
            # Drawing the buttons and chess board
            self.screen.blit(self.menu_chess_board, (1500, 450))
            pygame.draw.rect(self.screen, OFF_WHITE, self.play_game_button, 0,border_radius=10 )
            pygame.draw.rect(self.screen, OFF_WHITE, self.tourn_menu_button, 0,border_radius=10 )
            pygame.draw.rect(self.screen, OFF_WHITE, self.past_games_button, 0,border_radius=10 )
            pygame.draw.rect(self.screen, OFF_WHITE, self.cust_button, 0,border_radius=10 )
            pygame.draw.rect(self.screen, CYAN, self.logo, 10,border_radius=10 )
            #writing the text in the boxes
            self.screen.blit(self.logo_text, (self.logo_text.get_rect(center=self.logo.center)))
            self.screen.blit(self.play_game_button_text, (self.play_game_button_text.get_rect(center=self.play_game_button.center)))
            self.screen.blit(self.tourn_button_text_1, (self.tourn_menu_button.x +40, self.tourn_menu_button.y+15))
            self.screen.blit(self.tourn_button_text_2, (self.tourn_menu_button.x+100, self.tourn_menu_button.y+50))
            self.screen.blit(self.past_games_button_text, (self.past_games_button_text.get_rect(center=self.past_games_button.center)))
            self.screen.blit(self.cust_button_text, (self.cust_button_text.get_rect(center=self.cust_button.center)))
            if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_game_button.collidepoint(event.pos):
                        self.stage = "draw board"

        
       






    


class initial_board:
   
    def __init__(self):
        cell = draw_board(window).cell_size
        self.image_size = (cell, cell)  
        self.white_pieces = self.load_white_pieces()
        self.black_pieces = self.load_black_pieces()


    def load_white_pieces(self):
        return {
            PieceType.Pawn: pygame.transform.scale(pygame.image.load("ChessAssets/PawnW.png"), self.image_size),
            PieceType.Rook: pygame.transform.scale(pygame.image.load("ChessAssets/RookW.png"), self.image_size),
            PieceType.Knight: pygame.transform.scale(pygame.image.load("ChessAssets/KnightW.png"), self.image_size),
            PieceType.Bishop: pygame.transform.scale(pygame.image.load("ChessAssets/BishopW.png"), self.image_size),
            PieceType.King: pygame.transform.scale(pygame.image.load("ChessAssets/KingW.png"), self.image_size),
            PieceType.Queen: pygame.transform.scale(pygame.image.load("ChessAssets/QueenW.png"), self.image_size),
        }

    def load_black_pieces(self):
        return {
            PieceType.Pawn: pygame.transform.scale(pygame.image.load("ChessAssets/PawnB.png"), self.image_size),
            PieceType.Rook: pygame.transform.scale(pygame.image.load("ChessAssets/RookB.png"), self.image_size),
            PieceType.Knight: pygame.transform.scale(pygame.image.load("ChessAssets/KnightB.png"), self.image_size),
            PieceType.Bishop: pygame.transform.scale(pygame.image.load("ChessAssets/BishopB.png"), self.image_size),
            PieceType.King: pygame.transform.scale(pygame.image.load("ChessAssets/KingB.png"), self.image_size),
            PieceType.Queen: pygame.transform.scale(pygame.image.load("ChessAssets/QueenB.png"), self.image_size),
        }
        
    def get_image(self, colour: Player, type: PieceType):
        if colour == Player.White:
            return self.white_pieces[type]
        elif colour == Player.Black:
            return self.black_pieces[type]
        else:
            return None

    def get_Image(self, piece: Piece):
        self.piece = piece
        if piece == NonePiece:
            return None
        else:
            return initial_board().get_image(piece.colour(), piece.type())

      


    
   
        








    
    
# ---------------- Main Loop ----------------
class gameloop:
    def __init__(self):
        menu = MainMenu(window)
        board = draw_board(window)
        board.AddstartPieces()
        image_loader = initial_board()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if menu.stage == "create account":
                    menu.create_account(event)
                elif menu.stage == "menu":
                    menu.menu(event)
                elif menu.stage == "draw board":
                    board.initial(image_loader)
                    board.boardgrid_click(event)
                    
            pygame.display.flip()

gameloop()
            
            



        
