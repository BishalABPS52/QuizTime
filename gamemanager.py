import pygame
import sys
from highscore import show_high_scores
from help import show_help
from end import main as end_game

# Initialize Pygame
pygame.init()

# Load assets
background_image = pygame.image.load("/home/bishal-shrestha/MyProjects/UbuntuPythonFiles/Files/assets/startbg.jpg")
golden_font = pygame.font.Font("/home/bishal-shrestha/MyProjects/UbuntuPythonFiles/Files/assets/CaviarDreams_Bold.ttf", 28)
title_font = pygame.font.Font("/home/bishal-shrestha/MyProjects/UbuntuPythonFiles/Files/assets/KnightWarrior.otf", 60)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLDEN = (255, 215, 0)

# Button Class
class Button:
    def __init__(self, text, font, color, rect, bg_color=GOLDEN):
        self.text = text
        self.font = font
        self.color = color
        self.rect = pygame.Rect(rect)
        self.bg_color = bg_color
        self.text_surf = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, surface):
        pygame.draw.rect(surface, self.bg_color, self.rect)
        surface.blit(self.text_surf, self.text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def main_menu():
    from main import main as start_quiz  

    screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
    pygame.display.set_caption("Quiz Game")

    buttons = [
        Button("New Quiz", golden_font, BLACK, (500, 300, 200, 50)),
        Button("High Scores", golden_font, BLACK, (500, 400, 200, 50)),
        Button("Help", golden_font, BLACK, (500, 500, 200, 50)),
        Button("Quit", golden_font, BLACK, (500, 600, 200, 50))
    ]

    running = True
    while running:
        screen.fill(BLACK)
        screen.blit(pygame.transform.scale(background_image, (screen.get_width(), screen.get_height())), (0, 0))

        # Display game title
        title_surf = title_font.render("To Be Millionaire", True, GOLDEN)
        title_rect = title_surf.get_rect(center=(screen.get_width() // 2, 100))
        screen.blit(title_surf, title_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if buttons[0].is_clicked((mx, my)):
                    start_quiz()
                elif buttons[1].is_clicked((mx, my)):
                    show_high_scores()
                elif buttons[2].is_clicked((mx, my)):
                    show_help()
                elif buttons[3].is_clicked((mx, my)):
                    running = False
                    pygame.quit()
                    sys.exit()

        for button in buttons:
            button.draw(screen)

        pygame.display.update()

def end_screen():
    screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
    pygame.display.set_caption("End of Game")

    buttons = [
        Button("Main Menu", golden_font, BLACK, (500, 300, 200, 50)),
        Button("Quit Game", golden_font, BLACK, (500, 400, 200, 50)),
        Button("Bonus Round", golden_font, BLACK, (500, 500, 200, 50))
    ]

    running = True
    while running:
        screen.fill(BLACK)
        screen.blit(pygame.transform.scale(background_image, (screen.get_width(), screen.get_height())), (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if buttons[0].is_clicked((mx, my)):
                    main_menu()
                elif buttons[1].is_clicked((mx, my)):
                    running = False
                    pygame.quit()
                    sys.exit()
                elif buttons[2].is_clicked((mx, my)):
                    # Implement bonus round functionality here
                    pass

        for button in buttons:
            button.draw(screen)

        pygame.display.update()

if __name__ == "__main__":
    main_menu()
