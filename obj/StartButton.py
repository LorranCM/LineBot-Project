import pygame as pg
from obj.Button import Button

class StartButton(Button) :
    def __init__(self, surface : pg.surface.Surface) :
        image = pg.image.load("./assets/images/start-button-icon.png")
        size = surface.get_height() * 0.075 * image.get_width() / image.get_height(), surface.get_height() * 0.075 
        image = pg.transform.scale(image, size)
        super().__init__(image, surface)
        self.rect.bottomleft = surface.get_height() * 0.025, surface.get_height() * (1 - 0.025)
    
    def action(self) :
        pass