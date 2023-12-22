"""
Tic-Tac-Toe Game

This Python script implements a simple Tic-Tac-Toe game using the Pygame library.

The game consists of three main classes:
- TicTacToe: Manages the game logic, including checking for a win or draw and player/bot moves.
- UserInterface: Handles the graphical user interface using Pygame for rendering the game.
- GameController: Orchestrates the game by interacting with both the logic and user interface components.

Note: Ensure you have the Pygame library installed to run this script.
"""

import pygame
import random as rd
from typing import List
from time import sleep

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
PLAYER_COLOR = (rd.randint(0, 200), rd.randint(0, 200), rd.randint(0, 200))
BOT_COLOR = (255 - PLAYER_COLOR[0], 255 - PLAYER_COLOR[1], 255 - PLAYER_COLOR[2])


class TicTacToe:
    def __init__(self):
        """
        Initialize a new Tic-Tac-Toe game.

        Initializes the game grid as a 3x3 matrix and sets the winner to 0 (no winner).
        """
        self.grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.winner = 0

    def check_winner(self) -> int:
        """
        Check for a winner in the Tic-Tac-Toe game.

        Returns:
            int: The winner (1 for player, -1 for bot, 0 for no winner).
        """
        self.winner = (
            self.check_rows()
            or self.check_columns()
            or self.check_diagonals()
            or self.check_tie()
        )
        return self.winner

    def check_rows(self) -> int:
        """
        Check for a winner in the rows of the game grid.

        Returns:
            int: The winner in the rows (1 for player, -1 for bot, 0 for no winner).
        """
        for row in self.grid:
            if all(value == row[0] and value != 0 for value in row):
                return row[0]
        return 0

    def check_columns(self) -> int:
        """
        Check for a winner in the columns of the game grid.

        Returns:
            int: The winner in the columns (1 for player, -1 for bot, 0 for no winner).
        """
        for col in range(3):
            if all(
                row[col] == self.grid[0][col] and row[col] != 0 for row in self.grid
            ):
                return self.grid[0][col]
        return 0

    def check_diagonals(self) -> int:
        """
        Check for a winner in the diagonals of the game grid.

        Returns:
            int: The winner in the diagonals (1 for player, -1 for bot, 0 for no winner).
        """
        if all(
            self.grid[i][i] == self.grid[0][0] and self.grid[i][i] != 0
            for i in range(3)
        ):
            return self.grid[0][0]
        if all(
            self.grid[i][2 - i] == self.grid[0][2] and self.grid[i][2 - i] != 0
            for i in range(3)
        ):
            return self.grid[0][2]
        return 0

    def check_tie(self) -> int:
        """
        Check if the game has ended in a tie.

        Returns:
            int: 200 if the game is a tie, 0 otherwise.
        """
        return 200 if all(cell != 0 for row in self.grid for cell in row) else 0

    def player_move(self, i: int, j: int) -> bool:
        """
        Make a player's move in the game.

        Args:
            i (int): Row index.
            j (int): Column index.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        if self.grid[i][j] == 0:
            self.grid[i][j] = 1
            return True
        return False

    def bot_move(self) -> bool:
        """
        Make a bot's move in the game.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        valid_coords = [
            (i, j) for i in range(3) for j in range(3) if self.grid[i][j] == 0
        ]
        if valid_coords:
            coord = rd.choice(valid_coords)
            self.grid[coord[0]][coord[1]] = -1
            return True
        return False


class UserInterface:
    def __init__(self, grid: List[List[int]], width: int, height: int):
        """
        Initialize the UserInterface for the Tic-Tac-Toe game.

        Args:
            grid (List[List[int]]): The game grid.
            width (int): Width of the game window.
            height (int): Height of the game window.
        """
        self.grid = grid
        self.width = width
        self.height = height

        pygame.init()
        self.font = pygame.font.SysFont("Segoe UI", 35, True)
        self.window = pygame.display.set_mode((self.width, self.height))

    def draw_game(self):
        """Draw the current state of the Tic-Tac-Toe game on the screen."""
        self.draw_grid()
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] == 1:
                    self.draw_cross(i, j)
                elif self.grid[i][j] == -1:
                    self.draw_circle(i, j)

    def draw_grid(self):
        """Draw the game grid on the screen."""
        line_thickness = 2

        rows = pygame.Rect(
            self.width // 3,
            -line_thickness,
            self.width // 3,
            self.height + line_thickness * 2,
        )

        colums = pygame.Rect(
            -line_thickness,
            self.height // 3,
            self.width + line_thickness * 2,
            self.height // 3,
        )

        pygame.draw.rect(self.window, WHITE, rows, line_thickness)
        pygame.draw.rect(self.window, WHITE, colums, line_thickness)

    def draw_cross(self, i: int, j: int):
        """
        Draw a 'X' (cross) symbol on the specified grid cell.

        Args:
            i (int): Row index.
            j (int): Column index.
        """
        coords_line_1 = [
            [
                j * self.width // 3 + self.width // 9,  # x1
                i * self.height // 3 + self.height // 9,  # y1
            ],
            [
                j * self.width // 3 + 2 * self.width // 9,  # x2
                i * self.height // 3 + 2 * self.height // 9,  # y2
            ],
        ]
        coords_line_2 = [
            [
                j * self.width // 3 + 2 * self.width // 9,  # x1
                i * self.height // 3 + self.height // 9,  # y1
            ],
            [
                j * self.width // 3 + self.width // 9,  # x2
                i * self.height // 3 + 2 * self.height // 9,  # y2
            ],
        ]
        pygame.draw.line(
            self.window, PLAYER_COLOR, coords_line_1[0], coords_line_1[1], 10
        )
        pygame.draw.line(
            self.window, PLAYER_COLOR, coords_line_2[0], coords_line_2[1], 10
        )

    def draw_circle(self, i: int, j: int):
        """
        Draw an 'O' (circle) symbol on the specified grid cell.

        Args:
            i (int): Row index.
            j (int): Column index.
        """
        radius = max(self.width // 15, self.height // 15)
        pygame.draw.circle(
            self.window,
            BOT_COLOR,
            (
                j * self.width // 3 + self.width // 6,
                i * self.height // 3 + self.height // 6,
            ),
            radius,
            10,
        )

    def display_win_message(self, winner: int):
        """
        Display a win or draw message on the screen.

        Args:
            winner (int): The winner (1 for player, -1 for bot, 0 for a draw).
        """
        if winner == 1:
            win_message = self.font.render("YOU WON", False, GREEN)
        elif winner == -1:
            win_message = self.font.render("YOU LOST", False, PLAYER_COLOR)
        else:
            win_message = self.font.render("DRAW", False, WHITE)

        text_rect = win_message.get_rect(center=(self.width / 2, self.height / 2))
        self.window.fill(BLACK, text_rect)
        self.window.blit(win_message, text_rect)


class GameController:
    def __init__(self, width: int, height: int):
        """
        Initialize the GameController for the Tic-Tac-Toe game.

        Args:
            width (int): Width of the game window.
            height (int): Height of the game window.
        """
        self.game = TicTacToe()
        self.width = width
        self.height = height
        self.ui = UserInterface(self.game.grid, self.width, self.height)
        self.running = True

    def run(self):
        """Start and run the Tic-Tac-Toe game loop."""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event)

            self.game.check_winner()
            self.update_ui()
            pygame.display.update()

    def handle_mouse_click(self, event: pygame.event.Event):
        """
        Handle mouse clicks during the game.

        Args:
            event (pygame.event.Event): Mouse click event.
        """
        x, y = event.pos
        i, j = y // (self.height // 3), x // (self.width // 3)

        if self.game.player_move(i, j):
            self.game.bot_move()

    def update_ui(self):
        """Update the game's user interface."""
        self.ui.window.fill((0, 0, 0))
        self.ui.draw_game()
        winner = self.game.check_winner()
        if winner:
            self.ui.display_win_message(winner)
            pygame.display.update()
            sleep(2)
            self.running = False


if __name__ == "__main__":
    controller = GameController(width=600, height=600)
    controller.run()
