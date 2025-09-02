import pygame as pg

class Button :
    def __init__(self, image : pg.surface.Surface, surface : pg.surface.Surface) :
        self.surface = surface
        self.image = image
        self.rect = self.image.get_rect()
    
    def draw(self) :
        self.surface.blit(self.image, self.rect)
    
    def get_pressed(self) :
        if self.rect.collidepoint(pg.mouse.get_pos()) :
            self.action()
        