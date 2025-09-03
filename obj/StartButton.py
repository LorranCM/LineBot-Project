import pygame as pg
from obj.Button import Button

class StartButton(Button) :
    def __init__(self, surface : pg.surface.Surface) :
        image = pg.image.load("./assets/images/start-button-icon.png")
        size = surface.get_height() * 0.075 * image.get_width() / image.get_height(), surface.get_height() * 0.075 
        self.images = [
            pg.transform.scale(image, size),
            pg.transform.scale(pg.image.load("./assets/images/stop-button-icon.png"), size)
        ]
        super().__init__(self.images[0], surface)
        self.rect.bottomleft = surface.get_height() * 0.05, surface.get_height() * (1 - 0.05)
        self.robot_moving = False
        self.running = False
    
    def action(self) :
        self.running = not self.running
        if self.running :
            self.image = self.images[1]
            self.robot_moving = True
        else :
            self.robot_moving = False
            self.image = self.images[0]