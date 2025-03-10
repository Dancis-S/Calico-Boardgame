import pygame
from menu import Menu
from game_screen import GameScreen


pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 800
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Calico Board Game")


def main():
    clock = pygame.time.Clock()
    running = True
    current_screen = "menu"

    menu = Menu(SCREEN)
    game_screen = GameScreen(SCREEN)

    while running:
        SCREEN.fill((0, 0, 0))

        if current_screen == "menu":
            action = menu.run()
            if action == "start":
                current_screen = "game"

        elif current_screen == "game":
            game_screen.run()

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
