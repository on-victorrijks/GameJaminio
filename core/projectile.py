import pygame as pg

class Projectile(pg.sprite.Sprite):

    #trouve un endroit où blit les bullets
    def __init__(self):
        super().__init__()
        self.speed = 5
        self.image = pg.image.load('../assets/player.png')
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + 100
        self.rect.y = player.rect.y + 40

    def move(self):
        self.rect.x += self.speed

    """   fout ça dans le while
    for projectile in player.bullet_pool:
        projectile.move()
    """