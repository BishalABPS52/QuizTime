import pygame
import sys
 
# Initialize Pygame
pygame.init()

# Load assets
background_image = pygame.image.load("/home/bishal-shrestha/MyProjects/UbuntuPythonFiles/Files/assets/help.jpg")
golden_font = pygame.font.Font("/home/bishal-shrestha/MyProjects/UbuntuPythonFiles/Files/assets/CaviarDreams_Bold.ttf", 28)

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

def show_help():
    from gamemanager import main_menu  

    screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
    pygame.display.set_caption("Help")

    rules = [
        "1. Answer the questions within the time limit.",
        "2. Use lifelines wisely to help you answer difficult questions.",
        "3. You can use each lifeline only once per game. ",
        "4. The game ends if you answer a question incorrectly or run out of time.",
        "5. Try to reach the highest prize level by answering all questions correctly."
    ]

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

        # Display rules
        start_y = 100
        for i, rule in enumerate(rules):
            text_surf = golden_font.render(rule, True, GOLDEN)
            screen.blit(text_surf, (100, start_y + i * 40))

        main_menu_button.draw(screen)
        pygame.display.update()

if __name__ == "__main__":
    show_help()
