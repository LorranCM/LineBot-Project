import pygame as pg
from obj.Button import Button

class TrashButton(Button) :
    def __init__(self, surface : pg.surface.Surface, actionlist) :
        size = [surface.get_height() * 0.075] * 2
        image = pg.image.load("./assets/images/trash-button-icon.png")
        image = pg.transform.scale(image, size)
        super().__init__(image, surface)
        self.actionlist = actionlist
        self.rect.topleft = [surface.get_height() * 0.05] * 2
    
    def action(self) :
        self.actionlist.action_list.clear()
        self.actionlist.update_action_list_rects()
        