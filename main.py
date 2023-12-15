import pygame
import random
from typing import List
from time import sleep

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


# TODO : check when all the cells are filled but no one won (in check_win function)


class TicTacToe:
    def __init__(self) -> None:
        # -1 -> Circle (Bot) / 0 -> Empty cell / 1 -> Cross (Player)
        self.grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.winner = None

    def check_win(self):
        for line in self.grid:
            # Lines
            if line[0] != 0 and line[0] == line[1] == line[2]:
                self.winner = line[0]
                return self.winner
            
            # Columns
            for i in range(3):
                if self.grid[0][i] != 0 and self.grid[0][i] == self.grid[1][i] == self.grid[2][i]:
                    self.winner = self.grid[0][0]
                    return self.winner

        # Diagonals
        if self.grid[1][1] != 0 and ( (self.grid[0][0] == self.grid[1][1] == self.grid[2][2]) or (
            self.grid[0][2] == self.grid[1][1] == self.grid[2][0] )
        ):
            self.winner = self.grid[1][1]
            return self.winner

    def input_player(self, mouse_pos) -> None:
        i, j = 0, 0
        if 0 < mouse_pos[0] < 200:
            j = 0
        elif 200 < mouse_pos[0] < 400:
            j = 1
        elif 400 < mouse_pos[0] < 600:
            j = 2
        if 0 < mouse_pos[1] < 200:
            i = 0
        elif 200 < mouse_pos[1] < 400:
            i = 1
        elif 400 < mouse_pos[1] < 600:
            i = 2
        if self.grid[i][j] == 0:
            self.grid[i][j] = 1
        
    def input_bot(self) -> None:
        valid_coords = []
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] == 0:
                    valid_coords.append([i, j])
        if valid_coords:
          coord = random.choice(valid_coords)
          self.grid[coord[0]][coord[1]] = -1

class UserInterface:
    def __init__(self, grid: List[List[int]]) -> None:
        self.grid = grid
        pygame.init()
        self.font = pygame.font.SysFont("Segoe UI", 35, True)
        self.window = pygame.display.set_mode((600, 600))
    
    def update(self):
        self.draw_grid()
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] == 1:
                    self.draw_cross(j*200, i*200)
                elif self.grid[i][j] == -1:
                    self.draw_circle(j*200, i*200)

    def draw_grid(self):
        grid_coord = []
        for i in [200, 400]:
            grid_coord.append(pygame.Rect(0, i, 600, 2)) # Lines
            grid_coord.append(pygame.Rect(i, 0, 2, 600)) # Columns
        for rectangle in grid_coord:
            pygame.draw.rect(self.window, WHITE, rectangle,  2)

    
    def draw_cross(self, x:int, y:int):
        pygame.draw.line(self.window, RED, (x+50, y+50), (x+150, y+150), 10)
        pygame.draw.line(self.window, RED, (x+150, y+50), (x+50, y+150), 10)

    def draw_circle(self, x, y):
        pygame.draw.circle(self.window, BLUE, (x+100, y+100), 50, 10)

    def win_message(self, winner:int):
        if winner == 1:
          textsurface = self.font.render("YOU WON", False, GREEN)
        elif winner == -1:
          textsurface = self.font.render("YOU LOST", False, RED)
        else:
          textsurface = self.font.render("DRAW", False, WHITE)
            
        self.window.blit(textsurface, (210, 250))


def main():
    game = TicTacToe()
    ui = UserInterface(game.grid)
    running = True
    round = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if not game.winner:
                    round += 2
                    game.input_player(pos)
                    game.input_bot()
            elif event.type == pygame.QUIT:
                running = False
                
            game.check_win()
            if game.winner:
                ui.win_message(game.winner)
            if round >= 9:
                ui.win_message(0)

        ui.update()
        pygame.display.flip()

    pygame.quit()

for i in range(10):
    print("Bonjour")


if __name__ == '__main__':
    main()