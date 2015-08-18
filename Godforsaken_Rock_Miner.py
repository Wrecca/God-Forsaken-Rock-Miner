import pygame
from pygame.locals import *
from math import *
import pygame, math
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DKRED = (102, 10, 0)
BROWN = (150, 50, 0)
DKBROWN = (102, 51, 0)
BLUE = (204, 255, 255)
GREY = (160, 160, 160)

class Ship(pygame.sprite.Sprite):

    def __init__(self, angle, screen_width, screen_height, shell):
        super().__init__()

        self.shell = shell
        self.imageThrust = pygame.image.load("shipThrust.png")
        self.imageCruise = pygame.image.load("shipCruise.png")
        self.imageLeft = pygame.image.load("shipLeft.png")
        self.imageRight = pygame.image.load("shipRight.png")
        self.imageThrust.set_colorkey(BLACK)
        self.imageCruise.set_colorkey(BLACK)
        self.imageLeft.set_colorkey(BLACK)
        self.imageRight.set_colorkey(BLACK)
        self.imageMaster = self.imageCruise
        self.image = self.imageMaster
        self.rect = self.imageCruise.get_rect()
        self.rect.x = screen_width / 2
        self.rect.y = screen_height / 2

        self.x = 100
        self.y = 100
        self.dx = 0
        self.dy = 0
        self.angle = angle
        self.turnRate = 5
        self.thrust = 0
        self.charge = 5
        self.mass = 1
        self.speed = 0


    def update(self):

        self.checkKeys()
        self.rotate()
        self.calcVector()
        self.setPos()
        self.rect.center = (self.x, self.y)

    def rotate(self):
        oldCenter = self.rect.center
        self.image = pygame.transform.rotate(self.imageMaster, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = oldCenter

    def calcVector(self):
        radians = self.angle * math.pi / 180

        thrustDx = self.thrust * math.cos(radians)
        thrustDy = self.thrust * math.sin(radians)
        thrustDy *= -1

        self.dx += thrustDx
        self.dy += thrustDy
        self.speed = math.sqrt((self.dx * self.dx) + (self.dy * self.dy))
        print(self.speed)

    def setPos(self):
        self.x += self.dx
        self.y += self.dy

    def checkKeys(self):
        keys = pygame.key.get_pressed()
        self.imageMaster = self.imageCruise
        if keys[pygame.K_d]:
            self.angle -= self.turnRate
            if self.angle < 0:
                self.angle = 360 - self.turnRate
            self.imageMaster = self.imageRight

        if keys[pygame.K_a]:
            self.angle += self.turnRate
            if self.angle > 360:
                self.angle = self.turnRate
            self.imageMaster = self.imageLeft

        if keys[pygame.K_w]:
            self.thrust = .1
            self.imageMaster = self.imageThrust

        elif keys[pygame.K_SPACE]:
            self.shell.x = self.rect.centerx
            self.shell.y = self.rect.centery
            self.shell.speed = self.charge
            self.shell.dir = self.angle

        else:
            self.thrust = 0


class Shell(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((7, 7))
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        pygame.draw.circle(self.image, (250, 250, 250), (5, 5), 5)
        self.rect = self.image.get_rect()
        self.rect.center = (-100, -100)
        self.speed = 0
        self.dir = 0
        self.mass = 1
        self.dx = 0
        self.dy = 0
        self.reset()

    def update(self):
        self.calcVector()
        self.calcPos()
        self.rect.center = (self.x, self.y)

    def calcVector(self):
        radians = self.dir * math.pi / 180

        self.dx = self.speed * math.cos(radians)
        self.dy = self.speed * math.sin(radians)
        self.dy *= -1


    def calcPos(self):
        self.x += self.dx
        self.y += self.dy

    def reset(self):
        """ move off stage and stop"""
        self.x = 0
        self.y = 0
        self.speed = 0


class Planet(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("pluto.gif")
        self.image = self.image.convert()
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.rect = self.image.get_rect()
        self.mass = 100
        self.x = screen_width / 2
        self.y = screen_height / 2
        self.rect.center = (self.x, self.y)

    def gravitate(self, body):
        """ calculates gravitational pull on
            object """
        (self.x, self.y) = self.rect.center

        #get dx, dy, distance
        dx = self.x - body.x
        dy = self.y - body.y

        distance = math.sqrt((dx * dx) + (dy * dy))
        #normalize dx and dy
        dx /= distance
        dy /= distance

        force = (body.mass * self.mass)/(math.pow(distance, 2))

        dx *= force
        dy *= force

        body.dx += dx
        body.dy += dy


class Game(object):

    def __init__(self, screen_width, screen_height):

        self.game_over = False

        self.all_sprites_list = pygame.sprite.Group()

        self.planet = Planet(screen_width, screen_height)
        self.shell = Shell()
        self.ship = Ship(270, screen_width, screen_height, self.shell)
        self.all_sprites_list.add(self.ship, self.shell, self.planet)







    def process_events(self):         ## This is the where we process stuff done on the keyboard and
                                                    ## refresh our Shoot functions.


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == KEYDOWN:
                if event.key == K_w:
                    print("Do something")




                else:
                    print("Unrecognized key")

            if event.type == KEYUP:
                print("botton off")








        return False



    def run_logic(self):                            ## This is where the game decides stuff. The logical brain is here.
                                                    ## The Sprite lists are checked for collisions and it checks for game states.
        if not self.game_over:
            self.planet.gravitate(self.ship)
            #self.planet.gravitate(self.shell)
            print("Game is Running")






    def display_frame(self, screen):            ## This is where the frames are processed and movement is illusioned
                                                ##  onto the screen. In fact <screen> is passed here so it knows how to process your screen.
        SCREEN_WIDTH = 1700
        SCREEN_HEIGHT = 800

        screen.fill(BLACK)
        self.all_sprites_list.update()
        self.all_sprites_list.draw(screen)
        pygame.display.flip()



def main():

    pygame.init()


    clock = pygame.time.Clock()

    screen_width = 1700
    screen_height = 850

    screen = pygame.display.set_mode([screen_width, screen_height])



    done = False

    game = Game(screen_width, screen_height)


    while not done:



        done = game.process_events()

        game.run_logic()

        game.display_frame(screen)


        clock.tick(30)


    pygame.quit()



if __name__ == "__main__":
    main()


