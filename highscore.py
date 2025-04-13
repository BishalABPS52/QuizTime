import pygame
import sys
import json

# Initialize Pygame
pygame.init()

# Load assets
background_image = pygame.image.load("/home/bishal-shrestha/MyProjects/UbuntuPythonFiles/Files/assets/highscore.jpg")
golden_font = pygame.font.Font("/home/bishal-shrestha/MyProjects/UbuntuPythonFiles/Files/assets/CaviarDreams_Bold.ttf", 20)
green_font = pygame.font.Font("/home/bishal-shrestha/MyProjects/UbuntuPythonFiles/Files/assets/CaviarDreams_Bold.ttf", 20)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLDEN = (255, 215, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Load high scores from file
def load_high_scores():
    try:
        with open("/home/bishal-shrestha/MyProjects/UbuntuPythonFiles/Files/high_scores.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save high scores to file
def save_high_scores(high_scores):
    with open("/home/bishal-shrestha/MyProjects/UbuntuPythonFiles/Files/high_scores.json", "w") as file:
        json.dump(high_scores, file)

# Sample high scores data
high_scores = load_high_scores()

# Sort high scores
high_scores.sort(key=lambda x: (-x["prize"], -x["questions"]))

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

def show_high_scores():
    from gamemanager import main_menu  # Import inside function to avoid circular import

    screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
    pygame.display.set_caption("High Scores")

    main_menu_button = Button("Main Menu", golden_font, BLACK, (screen.get_width() - 150, 20, 130, 40))

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
                if main_menu_button.is_clicked((mx, my)):
                    main_menu()

        # Display table headers
        headers = ["Rank", "User", "Prize", "Questions"]
        header_x_positions = [100, 300, 600, 900]
        for i, header in enumerate(headers):
            text_surf = golden_font.render(header, True, GOLDEN)
            screen.blit(text_surf, (header_x_positions[i], 50))

        # Display high scores
        start_y = 100
        for i, score in enumerate(high_scores):
            rank_text = f"{i+1}"
            user_text = score['name']
            prize_text = f"NPR {score['prize']:,}"
            questions_text = f"{score['questions']}"

            rank_surf = green_font.render(rank_text, True, GREEN)
            user_surf = golden_font.render(user_text, True, GOLDEN)
            prize_surf = golden_font.render(prize_text, True, GOLDEN)
            questions_surf = golden_font.render(questions_text, True, GOLDEN)

            screen.blit(rank_surf, (header_x_positions[0], start_y + i * 40))
            screen.blit(user_surf, (header_x_positions[1], start_y + i * 40))
            screen.blit(prize_surf, (header_x_positions[2], start_y + i * 40))
            screen.blit(questions_surf, (header_x_positions[3], start_y + i * 40))

        main_menu_button.draw(screen)
        pygame.display.update()

def save_high_score(name, prize, questions):
    high_scores.append({"name": name, "prize": prize, "questions": questions})
    high_scores.sort(key=lambda x: (-x["prize"], -x["questions"]))
    save_high_scores(high_scores)

if __name__ == "__main__":
    show_high_scores()
