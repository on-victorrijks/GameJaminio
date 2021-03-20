
import pygame
from game import Game

pygame.init()

#fenetre de jeu
pygame.display.set_caption("alpha_game")
screen = pygame.display.set_mode((1080, 720))
arnaque = pygame.image.load('assets/onEnEstLa.jfif')

game = Game()

running = True

#boucle ouverture fenetre
while running:

    #appliquer le bg
    screen.blit(arnaque, (0, 0))
    #appliquer player
    screen.blit(game.player.image, game.player.rect)

    #check gauche droite
    if game.pressed.get(pygame.K_RIGHT):
        game.player.move_right()
    elif game.pressed.get(pygame.K_LEFT):
        game.player.move_left()
    #maj screen
    pygame.display.flip()

    #events
    for event in pygame.event.get():
        #si event = fermer la fenetre
        if event == pygame.QUIT:
            running = False
            pygame.quit()
        #touche relachée
        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True
        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False



###############################
#############################

import pygame
from player import Player

class Game:
    def __init__(self):
        #génerer le joueur
        self.player = Player()
        self.pressed = {}




########################
########################

import pygame
class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.maxHealth = 200
        self.health = 200
        self.attack = 20
        self.armor = 0
        self.speed = 5
        self.accelerate = 0
        self.jump = 1.5
        self.image = pygame.image.load('assets/trump.png')
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 500

    def move_right(self):
        self.rect.x += self.speed
    def move_left(self):
        self.rect.x -= self.speed
    def Jump(self):
        self.rect.y -= self.jump