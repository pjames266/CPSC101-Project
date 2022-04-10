import pygame
import os
import random

pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1536, 832


#Game Window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quest For Fire 1.0")
FPS = 60

#Tiles
TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

#Colours
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
GREEN = (0,255,0)
DARKGREEN = (6,84,31)
BLUE = (0,0,255)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)

#loading images
BANNER = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'title_card.png')), (WIDTH, HEIGHT))
GRASS1 = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'grass_texture_1.png')), (TILESIZE, TILESIZE))
GRASS2 = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'grass_texture_2.png')), (TILESIZE, TILESIZE))
GRASS3 = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'grass_texture_3.png')), (TILESIZE, TILESIZE))
GRASS4 = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'grass_texture_4.png')), (TILESIZE, TILESIZE))
GRASS5 = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'grass_texture_5.png')), (TILESIZE, TILESIZE))
GRASS6 = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'grass_texture_6.png')), (TILESIZE, TILESIZE))
GRASS7 = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'grass_texture_7.png')), (TILESIZE, TILESIZE))
GRASS8 = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'grass_texture_8.png')), (TILESIZE, TILESIZE))
ENEMY_TEMP = pygame.image.load(os.path.join('Assets','sam.png'))
PLAYER_TEMP = pygame.image.load(os.path.join('Assets','james.png'))



class Sprite:

    def __init__(self, x, y, width, height):
        """Deafult Class for all Sprites

        Args:
            x (int): x-pos
            y (int): y-pos
            width (int): width
            height (int): height
        """
        self.sprite = pygame.Rect(x, y, width, height)

class Shadow(Sprite):
    def __init__(self, x, y, width, height):
        """Shadow Object

        Args:
            x (int): x-pos
            y (int): y-pos
            width (int): width
            height (int): height
        """
        super().__init__(x, y, width, height)

    def radius(self, other):
        """Finds radius

        Args:
            other (obj): object you want to find distance from

        Returns:
            float: radius
        """
        return ((self.sprite.x-other.sprite.x)**2 + (self.sprite.y - other.sprite.y)**2)**0.5

    def show(self):
        """Show Shadow
        """
        pygame.draw.rect(WIN, BLACK, self.sprite)

class Wall(Sprite):
    
    def __init__(self, x, y, width, height):
        """Wall Object

        Args:
            x (int): x-pos
            y (int): y-pos
            width (int): width
            height (int): height
        """
        super().__init__(x, y, width, height)
    
    def show(self):
        """Show Walls
        """
        pygame.draw.rect(WIN, DARKGREY, self.sprite)

class Water(Sprite):
    
    def __init__(self, x, y, width, height):
        """Water Object

        Args:
            x (int): x-pos
            y (int): y-pos
            width (int): width
            height (int): height
        """
        super().__init__(x, y, width, height)
    
    def show(self):
        """Show Water
        """
        pygame.draw.rect(WIN, BLUE, self.sprite)

class Tree(Sprite):
    
    def __init__(self, x, y, width, height):
        """Water Object

        Args:
            x (int): x-pos
            y (int): y-pos
            width (int): width
            height (int): height
        """
        super().__init__(x, y, width, height)
    
    def show(self):
        """Shows Tree
        """
        pygame.draw.rect(WIN, DARKGREEN, self.sprite)
    

class Fuel(Sprite):

    def __init__(self, x, y, width, height, fuel):
        """Fuel Object

        Args:
            x (int): x-pos
            y (int): y-pos
            width (int): width
            height (int): height
            fuel (int): Random value that is the amount of fuel it gives
        """
        super().__init__(x, y, width, height)
        self.fuel = fuel

    def show(self):
        """Shows Fuel icons
        """
        FUEL = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'torch.png')), (self.sprite.width, self.sprite.height))
        WIN.blit(FUEL, (self.sprite.x,self.sprite.y))

class Entity(Sprite):

    def __init__(self, x, y, width, height, hp, vel):
        """Class for all moving entities

        Args:
            x (int): x-pos
            y (int): y-pos
            width (int): width
            height (int): height
            hp (int): Health or vision
            vel (int): movement speed
        """
        super().__init__(x, y,width, height)
        self.hp = hp
        self.vel = vel
        

class Enemy(Entity):

    def __init__(self, x, y, width, height, hp, vel):
        """_summary_

        Args:
            x (int): x-pos
            y (int): y-pos
            width (int): width
            height (int): height
            hp (int): Health or vision
            vel (int): movement speed
        """
        super().__init__(x, y, width, height, hp, vel)


    def enemy_movement(self, other1, other2):
        """Facilitates Enemy Movement

        Args:
            other1 (Object): The Object/Player that is being chased
            other2 (object): List of obsticle objects
        """
        
        
        if other1.sprite.x > self.sprite.x: #right
            self.sprite.x += self.vel
            if other2.collide_with_wall(self):
                self.sprite.x -= self.vel
        
        if other1.sprite.x < self.sprite.x: #left
            self.sprite.x -= self.vel
            if other2.collide_with_wall(self):
                self.sprite.x += self.vel

        if other1.sprite.y < self.sprite.y: #up
            self.sprite.y -= self.vel
            if other2.collide_with_wall(self):
                self.sprite.y += self.vel

        if other1.sprite.y > self.sprite.y: #down
            self.sprite.y += self.vel
            if other2.collide_with_wall(self):
                self.sprite.y -= self.vel

    def show(self):

        ENEMY = pygame.transform.rotate(pygame.transform.scale(ENEMY_TEMP, (self.sprite.width,self.sprite.height)), 0)
        WIN.blit(ENEMY, (self.sprite.x,self.sprite.y))

class Player(Entity):
    
    def __init__(self, x, y, width, height, hp, vel):
        """_summary_

        Args:
            x (int): x-pos
            y (int): y-pos
            width (int): width
            height (int): height
            hp (int): Health or vision
            vel (int): movement speed
        """
        super().__init__(x, y, width, height, hp, vel)


    def player_movement(self, keys_pressed, other):
        """Facilitates Player Movement

        Args:
            keys_pressed (sequence[bool]): Event that stores key inputs
            walls (list): List of Objects that are obsticles
        """
        
        if keys_pressed[pygame.K_a] and self.sprite.x - self.vel > 0: #left
            self.sprite.x -= self.vel
            if other.collide_with_wall(self):
                self.sprite.x += self.vel
        
        if keys_pressed[pygame.K_d] and self.sprite.x + self.vel + self.sprite.width < WIDTH: #right
            self.sprite.x += self.vel
            if other.collide_with_wall(self):
                self.sprite.x -= self.vel

        if keys_pressed[pygame.K_w] and self.sprite.y - self.vel > 0: #Up
            self.sprite.y -= self.vel
            if other.collide_with_wall(self):
                self.sprite.y += self.vel

        if keys_pressed[pygame.K_s] and self.sprite.y + self.vel + self.sprite.height < HEIGHT - 10: #down
            self.sprite.y += self.vel
            if other.collide_with_wall(self):
                self.sprite.y -= self.vel

    
    def show(self):
        """Shows Player
        """

        PLAYER = pygame.transform.rotate(pygame.transform.scale(PLAYER_TEMP, (self.sprite.width,self.sprite.height)), 0)
        WIN.blit(PLAYER, (self.sprite.x,self.sprite.y))


class World:

    def __init__(self):
        """Initializes world setup
        """
        
        self.starting_hp = 300
       
        self.player = Player(500,500,TILESIZE,TILESIZE,self.starting_hp,6)
        self.enemy = Enemy(100,100,TILESIZE,TILESIZE,self.starting_hp,3)
        self.fuel = []
        self.shadow_growth = 0.08

       
        """Creates a map from list of all obsticles in the map.txt file in assets folder
        """
        self.player_start = ()
        self.enemy_start = ()
        self.map_data = []
        self.tree = []
        self.walls = []
        self.water = []

        with open(os.path.join('Assets', 'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)

        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    self.walls.append(Wall(col*TILESIZE, row*TILESIZE, TILESIZE, TILESIZE))
                if tile == '2':
                    self.water.append(Water(col*TILESIZE, row*TILESIZE, TILESIZE, TILESIZE))
                if tile == '3':
                    self.tree.append(Tree(col*TILESIZE, row*TILESIZE, TILESIZE, TILESIZE))
                if tile == 'P':
                    self.player_start = (col*TILESIZE, row*TILESIZE)
                if tile == 'E':
                    self.enemy_start = (col*TILESIZE, row*TILESIZE)

        """Draw all shadows
        """
        self.shadow = []
        for x in range(0, WIDTH, TILESIZE//2):
            for y in range(0, HEIGHT, TILESIZE//2):
                self.shadow.append(Shadow(x,y,TILESIZE//2,TILESIZE//2))

        """Create player and enemy objects
        """
        self.player = Player(self.player_start[0],self.player_start[1],TILESIZE,TILESIZE,self.starting_hp,6)
        self.enemy = Enemy(self.enemy_start[0],self.enemy_start[1],TILESIZE,TILESIZE,self.starting_hp,4)
    
    def draw_game(self):
        """Draws all the main game features
        """
        WIN.fill(DARKGREY)
        self.draw_grid()
        self.player.show()
        self.enemy.show()
        self.eaten()
        self.collect_fuel()
        self.draw_walls()
        self.draw_shadow()
        
        
        pygame.display.update()

    def draw_start(self):
        """Draws Start Screen
        """

        WIN.blit(BANNER, (0,0))
        
        font = pygame.font.SysFont("Comic Sans", 40)
        
        press_to_cont = font.render('Press Anywhere To Continue', False, WHITE)
        press_to_cont_rect = press_to_cont.get_rect()
        press_to_cont_rect.center = (WIDTH//2, 760)
        WIN.blit(press_to_cont,press_to_cont_rect)

        pygame.display.update()

    def draw_grid(self):
        """Draws Background
        """
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(WIN, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(WIN, LIGHTGREY, (0, y), (WIDTH, y))
        
        for x in range(0, WIDTH, TILESIZE):
            for y in range(0, HEIGHT, TILESIZE):
                WIN.blit(GRASS2, (x,y))
        
    def eaten(self):
        """Player takes Damage from enemy
        """
        if self.player.sprite.colliderect(self.enemy.sprite):
            self.player.hp -= 20

    def collect_fuel(self):
        """Shows and generates fuels as well as detects fuel collection
        """
        for obj in self.fuel:
            if self.player.sprite.colliderect(obj.sprite):
                self.fuel.remove(obj)
                self.player.hp += obj.fuel

            obj.show()

        self.player.hp -= self.shadow_growth
        r = random.randint(0,230)

        if r == 1 and len(self.fuel)<5:
            self.fuel.append(Fuel(random.randint(0,WIDTH),random.randint(0,HEIGHT),TILESIZE, TILESIZE, random.randint(20,50)))
            for obj in self.fuel:
                if self.collide_with_wall(obj):
                    self.fuel.remove(obj)
    
    def draw_shadow(self):
        """Draws Shadows to Screen at certain radius
        """
        for obj in self.shadow:
            if obj.radius(self.player)>self.player.hp:
                obj.show()

    def draw_walls(self):
        """Draws Walls and other obsticles
        """
        
        for obj in self.walls:
            obj.show()
        for obj in self.water:
            obj.show()
        for obj in self.tree:
            obj.show()

    def collide_with_wall(self, other):
        """Does Collision detection with outside 

        Args:
            other (list): Takes a list or single entities to be checked for obticle collision

        Returns:
            bool: True or False
        """

        obsticles = self.walls + self.water + self.tree
        for obsticle in obsticles:
            if obsticle.sprite.colliderect(other.sprite):
                
                return True
                
        return False

    def world_reset(self):
        """Resets all world info
        """

        self.player.sprite.x = self.player_start[0] 
        self.player.sprite.y = self.player_start[1] 
        self.enemy.sprite.x = self.enemy_start[0] 
        self.enemy.sprite.y = self.enemy_start[1] 
        self.player.hp = self.starting_hp
        self.fuel = []
    


def main():
    """Main program loop
    """

    world = World()
    clock = pygame.time.Clock()
    run = True
    playing = False

    while run:

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        if playing == False:
            world.draw_start()

            if pygame.mouse.get_pressed()[0]:
                
                world.world_reset()
                playing = True
        
        if playing == True:
            keys_pressed = pygame.key.get_pressed()
            world.player.player_movement(keys_pressed, world)
            world.enemy.enemy_movement(world.player, world)
            world.draw_game()
            world.collect_fuel()
            if world.player.hp <= 0:
                playing = False
            

if __name__== "__main__":
    main()