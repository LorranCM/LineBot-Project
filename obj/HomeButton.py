import pygame as pg
from obj.Button import Button

class HomeButton(Button) :
    def __init__(self, surface : pg.surface.Surface) :
        size = [surface.get_height() * 0.075] * 2
        image = pg.image.load("./assets/images/home-button-icon.png")
        image = pg.transform.scale(image, size)
        super().__init__(image, surface)
        self.rect.topleft = [surface.get_height() * 0.05] * 2
        