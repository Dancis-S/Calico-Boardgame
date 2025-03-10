import pygame


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 50)
        self.start_button = pygame.Rect(300, 250, 200, 60)

    def run(self):
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        self.screen.fill((30, 30, 30))

        pygame.draw.rect(self.screen, (0, 150, 0), self.start_button)
        text = self.font.render("Start Game", True, (255, 255, 255))
        self.screen.blit(text, (self.start_button.x + 30, self.start_button.y + 15))

        if self.start_button.collidepoint(mouse_pos) and click[0]:
            return "start"

        return None
