import pygame
import math
pygame.init()
import pandas as pd
from main_gameplay import button_font, bold_font, base_font, menu_font
from coordinates import CYAN, OFF_WHITE, GRAY, DARK_GRAY, Player
import random



class tournament:
    def __init__(self, screen):
        self.screen = screen
        self.available_users = []
        self.player = ""
        self.players = []
        self.active = False
        self.input_rect_colour = CYAN
        self.title = menu_font.render("CREATE A TOURNAMENT", True, (255, 255, 255))
        self.instructions = base_font.render("Enter a valid username and then press enter", True, (255, 255, 255))
        self.input_rect = pygame.Rect(800, 900, 300, 60)
        self.tournament_button_rect = pygame.Rect(1700, 1300, 470, 60)
        self.next_game_rect = pygame.Rect(1800, 1100, 350, 60)
        self.tournament_button_rect_text = base_font.render("Create tournament", True, (DARK_GRAY))
        self.winner = None
        self.tournament_over = False
        self.game_played = {
             
        }
        self.table = pd.DataFrame(columns=[
            "Name",
            "capturing points",
            "tourney points",
            "wins",
            "losses",
            "draws"
        ])
        
        with open("usernames.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                self.available_users.append(line.strip())

        

        # Column widths (pixels)
        self.col_widths = [200, 300, 270, 200, 200, 200] 
        self.row_height = 60
        
    def draw_table(self):
        self.next_game_rect_text = base_font.render("Next game", True, DARK_GRAY)
        self.screen.fill(DARK_GRAY)
        start_x = 500
        start_y = 500
        columns = list(self.table.columns)
        self.data = [columns] + self.table.values.tolist()
        # Draw table
        for row_index, row in enumerate(self.data):
            y = start_y + row_index * self.row_height
            
            for col_index, cell in enumerate(row):
                x = start_x + sum(self.col_widths[:col_index])  # Calculate x based on previous column widths
                
                # Draw cell background
                pygame.draw.rect(self.screen, OFF_WHITE, (x, y, self.col_widths[col_index], self.row_height))
                
                # Draw cell border
                pygame.draw.rect(self.screen, (0,0,0), (x, y, self.col_widths[col_index], self.row_height), 2)

                # Use bold font for header row
                if row_index == 0:
                    current_font = bold_font
                else:
                    current_font = button_font
                
                # Render text
                text_surface = current_font.render(str(cell), True, (0,0,0))
                self.screen.blit(text_surface, (x + 10, y + 8))
                pygame.draw.rect(self.screen, GRAY, self.next_game_rect, border_radius=10)
                self.screen.blit(self.next_game_rect_text, (self.next_game_rect_text.get_rect(center = self.next_game_rect.center)))
    def create_tournament(self, event, menu):
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_rect.collidepoint(event.pos):
                self.input_rect_colour = (255,255, 255)
                self.active = True
        if self.active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.player = self.player[:-1]
            elif event.key == pygame.K_RETURN:
                if self.player in self.available_users:
                        self.players.append(self.player)
                        self.available_users.remove(self.player)
                        self.player = ""
                        self.input_rect_colour = CYAN
                self.player = ""
                self.active = False
                

            else:
                if len(self.player) < 20:
                    self.player += event.unicode
                    print(f"Player after adding char: '{self.player}'")
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.tournament_button_rect.collidepoint(event.pos) and len(self.players) >= 3:
                    for player_name in self.players:
                        new_row = pd.DataFrame({
                            'Name': [player_name],
                            'capturing points': [0],
                            'tourney points': [0],
                            'wins': [0],
                            'losses': [0],
                            'draws': [0]
                        })
                        self.table = pd.concat([self.table, new_row], ignore_index=True)
                    menu.stage = "draw board"
    def tournament_render(self):
        self.screen.fill(DARK_GRAY)
        y_pos = 400
        for line in self.available_users:
                user = button_font.render(line, True, OFF_WHITE)
                self.screen.blit(user, (400, y_pos))
                y_pos += 50
                
        pygame.draw.rect(self.screen, self.input_rect_colour, self.input_rect, 2)
        self.screen.blit(self.instructions, (200, 300))
        self.screen.blit(self.title, (700, 100))
        player_text = base_font.render(self.player, True, OFF_WHITE)
        self.screen.blit(player_text, (self.input_rect.x + 10, self.input_rect.y))
        self.input_rect.w = max(50, player_text.get_width() + 10)
        pygame.draw.rect(self.screen, GRAY, self.tournament_button_rect, 0, border_radius=10)    
        self.screen.blit(self.tournament_button_rect_text, (self.tournament_button_rect_text.get_rect(center = self.tournament_button_rect.center)))

    def table_to_board(self,event,menu):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.next_game_rect.collidepoint(event.pos):
                menu.stage = "draw board"

    def record_games(self, black_player, white_player):
         match_key = tuple(sorted([black_player, white_player]))
         self.game_played[match_key] = self.game_played.get(match_key, 0) + 1
    
    def has_game_happened_twice(self, black_player, white_player):
        match_key = tuple(sorted([black_player, white_player]))
        return self.game_played.get(match_key, 0) >= 2 
         
    def schedule_games(self, board):
            n = len(self.players)
            max_attempts = int(math.factorial(n)/(math.factorial(n-2)*2))  
            attempts = 0
            
            while attempts < max_attempts:
                # Pick 2 different players
                selected_players = random.sample(self.players, 2)
                player1, player2 = selected_players[0], selected_players[1]
                
                # Check if they've already played twice
                if not self.has_game_happened_twice(player1, player2):
                    board.black_player = player1
                    board.white_player = player2
                    self.record_games(player1, player2)
                    return True  # Successfully scheduled
                
                attempts += 1
            
            # No more valid matchups - tournament is over
            print("No more valid matchups - ending tournament")
            max_value = self.table["tourney points"].max()
            max_cp_value = self.table["capturing points"].max()
            tp_tied_players = self.table[self.table["tourney points"] == max_value]
            count_max = (self.table["tourney points"] == max_value).sum()
            
            if count_max == 1:
                max_value_id = self.table["tourney points"].idxmax()
                self.winner = str(self.table.loc[max_value_id, "Name"])  # Convert to string
            else:
                max_value_id = tp_tied_players[tp_tied_players["capturing points"] == max_cp_value].iloc[0]
                self.winner = str(self.table.loc[max_value_id, "Name"])  # Convert to string

            self.tournament_over = True
            return False  # Could not schedule

        
             
             
            
    def update_table(self, board):
        self.table.loc[self.table["Name"] == board.black_player, ["capturing points"]] += board.final_points_forpieces_taken()[Player.Black]
        self.table.loc[self.table["Name"] == board.white_player, ["capturing points"]] += board.final_points_forpieces_taken()[Player.White]
        if board.who_won() == Player.White:
                self.table.loc[self.table["Name"] == board.white_player, ["wins"]] += 1
                self.table.loc[self.table["Name"] == board.black_player, ["losses"]] += 1
                self.table.loc[self.table["Name"] == board.white_player, ["tourney points"]] += 3
        elif board.who_won() == Player.Black:
                self.table.loc[self.table["Name"] == board.black_player, ["wins"]] += 1
                self.table.loc[self.table["Name"] == board.white_player, ["losses"]] += 1
                self.table.loc[self.table["Name"] == board.black_player, ["tourney points"]] += 3
        else:
                self.table.loc[self.table["Name"] == board.white_player, ["draws"]] += 1
                self.table.loc[self.table["Name"] == board.black_player, ["draws"]] += 1
                self.table.loc[self.table["Name"] == board.black_player, ["tourney points"]] += 1
                self.table.loc[self.table["Name"] == board.white_player, ["tourney points"]] += 1

    
    def tournament_over_screen(self):

        self.screen.fill(DARK_GRAY)
        wins = int(self.table.loc[self.table["Name"] == self.winner, "wins"].iloc[0])
        captured_points = int(self.table.loc[self.table["Name"] == self.winner, "capturing points"].iloc[0])

        # Create the menu box
        menu = pygame.Rect(900, 200, 700, 850)
        pygame.draw.rect(self.screen, OFF_WHITE, menu, 0, border_radius=25)
        
        # Winner text
        title = menu_font.render("TOURNAMENT OVER!", True, CYAN)
        winner_text = menu_font.render(f"{self.winner} WINS!", True, CYAN)
        wins_text = menu_font.render(f"{wins} WINS!", True, CYAN)
        points_from_capturing_text = bold_font.render(f"{captured_points} POINTS FROM PIECES CAPTURED", True, CYAN)
        
        # Center the text
        title_rect = title.get_rect(center=menu.center)
        title_rect.y -= 100  # Move up
        wins_rect = wins_text.get_rect(center = menu.center)
        wins_rect.y += 100
        points_from_capturing_rect = points_from_capturing_text.get_rect(center = menu.center)
        points_from_capturing_rect.y +=200
        winner_rect = winner_text.get_rect(center=menu.center)
        
        self.screen.blit(title, title_rect)
        self.screen.blit(winner_text, winner_rect)
        self.screen.blit(wins_text, wins_rect)
        self.screen.blit(points_from_capturing_text, points_from_capturing_rect)

        self.menu_button_rect = pygame.Rect(1800, 1000, 300, 60)
        self.menu_button_rect_text = base_font.render("Go to menu", True, DARK_GRAY)
        pygame.draw.rect(self.screen, GRAY, self.menu_button_rect, 0, border_radius=10)
            
        self.screen.blit(self.menu_button_rect_text, self.menu_button_rect_text.get_rect(center= self.menu_button_rect.center))

    def tournament_to_menu(self, event, menu):
        

        #behaviour of go to menu button
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.menu_button_rect.collidepoint(event.pos):
                menu.stage = "menu"
            

            
            


    
            
            











