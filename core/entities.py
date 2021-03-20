import pygame as pg

class Player(pg.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.maxHealth = 200
        self.health = 200
        self.attack = 20
        self.armor = 0
        self.speed = 5
        self.accelerate = 0
        self.jump = 1.5
        self.image = pg.image.load('../assets/trump.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 500

    def move_right(self):
        self.rect.x += self.speed

    def move_left(self):
        self.rect.x -= self.speed

    def Jump(self):
        self.rect.y -= self.jump