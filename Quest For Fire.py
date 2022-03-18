import pygame
import os
import random

pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1536, 832

GAME_STATE = 1

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quest For Fire 1.0")
FPS = 60

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)

BANNER = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'title_card.png')), (WIDTH, HEIGHT))
GRASS = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'grass_texture_1.png')), (TILESIZE, TILESIZE))
PLAYER_TEMP = pygame.image.load(os.path.join('Assets','sam.png'))



class Sprite:

    def __init__(self, x, y, width, height):

        self.sprite = pygame.Rect(x, y, width, height)

class Shadow(Sprite):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

    def radius(self, other):
        return ((self.sprite.x-other.sprite.x)**2 + (self.sprite.y - other.sprite.y)**2)**0.5

    def show(self):
        pygame.draw.rect(WIN, BLACK, self.sprite)


class Fuel(Sprite):

    def __init__(self, x, y, width, height, fuel):
        super().__init__(x, y, width, height)
        self.fuel = fuel

    def show(self):
        FUEL = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'torch.png')), (self.sprite.width, self.sprite.height))
        WIN.blit(FUEL, (self.sprite.x,self.sprite.y))

class Entity(Sprite):

    def __init__(self, x, y, width, height, hp, vel):
        super().__init__(x, y,width, height)
        self.hp = hp
        self.vel = vel
        

class Enemy(Entity):

    def __init__(self):
        super().__init__()

class Player(Entity):
    
    def __init__(self, x, y, width, height, hp, vel):
        super().__init__(x, y, width, height, hp, vel)
        

    def player_movement(self, keys_pressed):
        if keys_pressed[pygame.K_a] and self.sprite.x - self.vel > 0: #left
            self.sprite.x -= self.vel
        
        if keys_pressed[pygame.K_d] and self.sprite.x + self.vel + self.sprite.width < WIDTH: #right
            self.sprite.x += self.vel

        if keys_pressed[pygame.K_w] and self.sprite.y - self.vel > 0: #Up
            self.sprite.y -= self.vel

        if keys_pressed[pygame.K_s] and self.sprite.y + self.vel + self.sprite.height < HEIGHT - 10: #down
            self.sprite.y += self.vel

    def show(self):

        PLAYER = pygame.transform.rotate(pygame.transform.scale(PLAYER_TEMP, (self.sprite.width,self.sprite.height)), 0)
        WIN.blit(PLAYER, (self.sprite.x,self.sprite.y))


class World:

    def __init__(self):
        self.player = Player(500,500,TILESIZE,TILESIZE,300,6)
        self.fuel = []
    def draw(self):
        WIN.fill(DARKGREY)
        self.draw_grid()
        self.player.show()
        self.collect_fuel()
        self.draw_shadow()
        pygame.display.update()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(WIN, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(WIN, LIGHTGREY, (0, y), (WIDTH, y))
        
        for x in range(0, WIDTH, TILESIZE):
            for y in range(0, HEIGHT, TILESIZE):
                WIN.blit(GRASS, (x,y))
        
    def collect_fuel(self):
        for obj in self.fuel:
            if self.player.sprite.colliderect(obj.sprite):
                self.fuel.remove(obj)
                self.player.hp += obj.fuel

            obj.show()

        r = random.randint(0,100)

        if r == 1:
            self.fuel.append(Fuel(random.randint(0,WIDTH),random.randint(0,WIDTH),TILESIZE, TILESIZE, 20))
       
    def draw_shadow(self):
        shadow = []
        for x in range(0, WIDTH, TILESIZE):
            for y in range(0, HEIGHT, TILESIZE):
                shadow.append(Shadow(x,y,TILESIZE,TILESIZE))

        for obj in shadow:
            if obj.radius(self.player)>self.player.hp:
                obj.show()


def main():

    world = World()

    clock = pygame.time.Clock()
    run = True

    while run:

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        keys_pressed = pygame.key.get_pressed()
        
        world.player.player_movement(keys_pressed)
        world.draw()
        world.collect_fuel()
        


if __name__== "__main__":
    main()