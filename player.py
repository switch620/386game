import sys, glob, pygame, math, projectile
from enum import Enum

ani_l = glob.glob("bun/bunl*")
ani_r = glob.glob("bun/bunr*")
ani_l.sort()
ani_r.sort()

class direction(Enum):
    LEFT = -1
    RIGHT = 1

class Player(pygame.sprite.Sprite):
    """ Player character code """

    width, height = 800, 800
    Scale = 2
    def __init__(self, screen):

        pygame.sprite.Sprite.__init__(self)
        self.reload_time = 0
        self.reload_speed = 30
        self.reloading = False
        self.screen = screen
        self.speed = [0,0]  # [X-axis, Y-axis]
        self.max_speed = 5
        self.scale = Player.Scale
        self.acceleration = .4
        self.direction = direction.RIGHT

        self.ani_l = ani_l
        self.ani_r = ani_r

        self.ani_max = len(self.ani_l) - 1
        self.ani_speed = 8
        self.ani_counter = 0
        self.ani_frame = 0

        self.image = self.loadFrame('l')
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 400

        # self.image = pygame.transform.scale(self.image, (self.width*self.scale, self.height*self.scale))
        # self.rect = self.rect.inflate((self.scale, self.scale))
    
    def loadFrame(self, dir: chr):
        if dir == 'r':
            img = pygame.image.load(self.ani_r[self.ani_frame])
        elif dir == 'l':
            img = pygame.image.load(self.ani_l[self.ani_frame])
        else:
            print("ERROR")
        width, height = img.get_size()
        return pygame.transform.scale(img, (width*self.scale, height*self.scale))


    def update(self):

        ##  Loop through frames depending on animation speed and animation frames
        self.ani_counter = (self.ani_counter + 1) % self.ani_speed
        if self.ani_counter == self.ani_max:
            self.ani_frame = (self.ani_frame + 1) % len(self.ani_l)

        ##  Set direction based off movement
        if self.speed[0] < 0:
            self.direction = direction.LEFT
        elif self.speed[0] > 0:
            self.direction = direction.RIGHT
        
        if self.speed[0] == 0 and self.speed[1] == 0:
            self.ani_frame = 0

        ##  Set frame based off direction
        if self.direction == direction.RIGHT:
            self.image = self.loadFrame('r')
        else:
            self.image = self.loadFrame('l')

        if self.reloading:
            self.reload_time = (self.reload_time+1) % self.reload_speed
            if self.reload_time == 0:
                self.reloading = False
        
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

    def processInput(self, keys):

        ## Check keys and calculate speed
        if keys[pygame.K_LEFT]:
            self.speed[0] -= self.acceleration
            if self.speed[0] < -self.max_speed:
                self.speed[0] = -self.max_speed
        if keys[pygame.K_RIGHT]:
            self.speed[0] += self.acceleration
            if self.speed[0] > self.max_speed:
                self.speed[0] = self.max_speed
        if not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.speed[0] *= .75
        if abs(self.speed[0]) < 0.1:
            self.speed[0] = 0

        if keys[pygame.K_DOWN]:
            self.speed[1] += self.acceleration
            if self.speed[1] > self.max_speed:
                self.speed[1] = self.max_speed
        if keys[pygame.K_UP]:
            self.speed[1] -= self.acceleration
            if self.speed[1] < -self.max_speed:
                self.speed[1] = -self.max_speed
        if not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            self.speed[1] *= .75
        if abs(self.speed[1]) < 0.1:
            self.speed[1] = 0

        bullet = None
        if keys[pygame.K_SPACE] and not self.reloading:
            print("Spacebar")
            self.reloading = True
            bullet = projectile.Projectile(self.rect, self.direction)

        ##  Move acording to speed
        # self.rect = self.rect.move(self.speed)

        ##  Checking bounds
        if self.rect.x < 0:
            self.rect.x = 0
            self.speed[0] = 0 
        if self.rect.x > (Player.width - self.rect.width): 
            self.rect.x = (Player.width - self.rect.width)
            self.speed[0] = 0 

        if self.rect.y < 0:
            self.rect.y = 0
            self.speed[1] = 0 
        if self.rect.y > (Player.height - self.rect.height): 
            self.rect.y = (Player.height - self.rect.height)
            self.speed[1] = 0 

        return bullet