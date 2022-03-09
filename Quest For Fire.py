import pygame
import os

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1500, 850

BORDER = pygame.Rect((WIDTH/2)-5, 0, 10, HEIGHT)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quest For Fire 1.0")
FPS = 60

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

GRASS = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'grassy.png')), (WIDTH, HEIGHT))

def draw_window():
    WIN.blit(GRASS, (0,0))

    pygame.display.update()

def main():

    clock = pygame.time.Clock()
    run = True

    while run:

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        draw_window()

if __name__== "__main__":
    main()