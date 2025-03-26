import pygame
import sys

# Initialize Pygame
pygame.init()

# Load assets
background_image = pygame.image.load("/home/bishal-shrestha/MyProjects/UbuntuPythonFiles/Files/assets/end.jpg")
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

def main():
    from main import main as start_main
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
                    start_main()
                elif buttons[1].is_clicked((mx, my)):
                    running = False
                    pygame.quit()
                    sys.exit()
                elif buttons[2].is_clicked((mx, my)):
                    # Implement bonus round functionality here
                    #incomplete
                    pass

        for button in buttons:
            button.draw(screen)

        pygame.display.update()

if __name__ == "__main__":
    main()
