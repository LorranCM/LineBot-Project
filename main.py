import pygame as pg
from pygame.locals import *
from tools.maze_surf_generation import get_maze_surface
from obj.Robot import Robot

class Game :
    def __init__(self) :
        self.screen = pg.display.set_mode((1200, 800), NOFRAME)
        self.clock = pg.time.Clock()
        self.running = True
        self.state = Gameplay(self, 8)

        pg.display.set_caption("LineBot")
        pg.display.set_icon(pg.image.load("assets/images/gameicon.png"))

    def run(self) :
        while self.running :
            self.state.handle_events()
            self.state.update()
            self.state.draw()  
            self.clock.tick(60)

class MainMenu : 
    def __init__(self, game : Game) :
        self.game = game

    def draw(self) :
        self.game.screen.fill((0, 0, 0))
        pg.display.flip()

    def update(self) : ...

    def handle_events(self) :
        for event in pg.event.get() :
            if event.type == QUIT :
                self.game.running = False

class Gameplay :
    def __init__(self, game : Game, level : int) :
        self.game = game
        self.initial_surface, self.maze_arr = get_maze_surface(level)
        self.robot = Robot(self.maze_arr)
        self.panel = Panel(game)
        self.posiion = (self.game.screen.get_width() // 2, self.game.screen.get_height() // 2)
        self.resize_maze()

        self.zoom = 1.0
        self.screen_is_pressed = 0

    def draw(self) :
        self.game.screen.fill((139, 145, 150))
        self.draw_robot()
        self.game.screen.blit(self.surface, self.rect)
        self.draw_panel()
        pg.display.flip()

    def update(self) :
        self.panel.update()

    def handle_events(self) :
        for event in pg.event.get() :
            if event.type == QUIT :
                self.game.running = False
            
            if not self.screen_is_pressed :
                self.panel.actionbar.handle_events(event)
                if not self.panel.actionbar.button_pressed != -1:
                    self.panel.actionlist.handle_events(event)

            if event.type == MOUSEWHEEL and not (self.panel.actionlist.rect.collidepoint(pg.mouse.get_pos()) or \
                self.panel.actionbar.rect.collidepoint(pg.mouse.get_pos())) \
                    and self.panel.actionbar.button_pressed == -1 :
                if event.y > 0 and self.zoom < 1.5 :
                    self.zoom += 0.05
                elif event.y < 0 and self.zoom > 0.5 :
                    self.zoom -= 0.05
                self.resize_maze(self.zoom)
            
            if event.type == MOUSEBUTTONDOWN and event.button == 1 :
                if not (self.panel.actionlist.rect.collidepoint(pg.mouse.get_pos()) or\
                    self.panel.actionbar.rect.collidepoint(pg.mouse.get_pos())) :
                    self.screen_is_pressed = 1

            if event.type == MOUSEBUTTONUP and event.button == 1 :
                self.screen_is_pressed = 0
                if self.panel.actionbar.button_pressed != -1 :
                    collide = False
                    for i in range(len(self.panel.actionlist.action_list_rects)) :
                        if self.panel.actionlist.action_list_rects[i].collidepoint(pg.mouse.get_pos()) :
                            self.panel.actionlist.action_list.insert(i, self.panel.actionbar.button_pressed)
                            self.panel.actionlist.update_action_list_rects()
                            collide = True
                            break
                    if self.panel.actionlist.rect.collidepoint(pg.mouse.get_pos()) and not collide:
                        self.panel.actionlist.action_list.append(self.panel.actionbar.button_pressed)
                        self.panel.actionlist.update_action_list_rects()
                    self.panel.actionbar.__init__(self.game)

            if event.type == MOUSEMOTION and self.screen_is_pressed :
                dx, dy = event.rel
                self.posiion = (self.posiion[0] + dx, self.posiion[1] + dy)
                self.rect.center = self.posiion
            
            if event.type == KEYDOWN :
                if event.key == K_SPACE :
                    self.posiion = (self.game.screen.get_width() // 2, self.game.screen.get_height() // 2)
                    self.rect.center = self.posiion
    
    def resize_maze(self, resize_factor : int = 1) :
        height = int(self.game.screen.get_height() * resize_factor)
        width = height * self.initial_surface.get_width() / self.initial_surface.get_height()
        self.surface = pg.transform.scale(self.initial_surface, (int(width), int(height)))
        self.rect = self.surface.get_rect(
            center = (self.posiion)
        )
    
    def draw_robot(self) :
        robot_image = pg.transform.scale(
            self.robot.original_image, ([self.surface.get_height() / (len(self.maze_arr) + 2)] * 2)
        )
        robot_image = pg.transform.rotate(robot_image, self.robot.angle)
        robot_rect = robot_image.get_rect(center = (
                (self.robot.arr_position[1] + 1) * (self.surface.get_height() / (len(self.maze_arr) + 2)) +
                self.surface.get_height() / (len(self.maze_arr) + 2) / 2,
                (self.robot.arr_position[0] + 1) * (self.surface.get_height() / (len(self.maze_arr) + 2)) +
                self.surface.get_height() / (len(self.maze_arr) + 2) / 2,
            )
        )
        self.surface.blit(robot_image, robot_rect)
    
    def draw_panel(self) :
        self.panel.actionlist.rect.topright = (self.game.screen.get_width(), 0)
        self.panel.actionbar.rect.topright = (self.game.screen.get_width(), self.panel.actionlist.rect.bottom)
        self.game.screen.blit(self.panel.actionlist.surface, self.panel.actionlist.rect)
        for i in range(len(self.panel.actionlist.action_list)) : 
            action_img = pg.transform.scale(
                self.panel.actionlist.action_buttons_imgs[self.panel.actionlist.action_list[i]], 
                (self.panel.actionlist.surface.get_width() * 0.2, self.panel.actionlist.surface.get_width() * 0.2)
            )
            self.game.screen.blit(action_img, self.panel.actionlist.action_list_rects[i])
        self.game.screen.blit(self.panel.actionbar.surface, self.panel.actionbar.rect)
        for i in range(len(self.panel.actionbar.action_buttons_imgs)) :
            self.game.screen.blit(
                self.panel.actionbar.action_buttons_imgs[i], self.panel.actionbar.action_buttons_rects[i]
            )

class Panel :
    def __init__(self, game : Game) :
        self.actionlist = ActionList(game)
        self.actionbar = ActionBar(game)
    
    def update(self) :
        self.actionbar.update()
        self.actionlist.update()

class ActionList :
    def __init__(self, game : Game) :
        self.surface = pg.Surface(
            (game.screen.get_width() * 0.2, game.screen.get_height() - game.screen.get_width() * 0.2), SRCALPHA
        )
        self.surface.fill((200, 200, 200, 240))
        self.rect = self.surface.get_rect()
        self.action_list = []
        self.action_list_rects = []

        self.action_buttons_imgs = [
            pg.image.load("assets/images/move-act.png").convert_alpha(),
            pg.image.load("assets/images/use-act.png").convert_alpha(),
            pg.image.load("assets/images/turn-right-act.png").convert_alpha(), 
            pg.image.load("assets/images/turn-left-act.png").convert_alpha()
        ]
    
    def update(self) : ...
    
    def update_action_list_rects(self) :
        self.action_list_rects = []
        for i in range(len(self.action_list)) :
            rect = pg.rect.Rect(
                self.surface.get_width() * 0.1 * (i % 3 + 1) + self.surface.get_width() * 0.2 * (i % 3) + \
                    self.surface.get_width() * 4,
                self.surface.get_width() * 0.1 * (i // 3 + 1) + self.surface.get_width() * 0.2 * (i // 3),
                self.surface.get_width() * 0.2,
                self.surface.get_width() * 0.2
            )
            self.action_list_rects.append(rect)
    
    def handle_events(self, event) :
        if event.type == MOUSEBUTTONDOWN and event.button == 3 :
            for i in range(len(self.action_list_rects)) :
                if self.action_list_rects[i].collidepoint(pg.mouse.get_pos()) :
                    self.action_list.pop(i)
                    self.update_action_list_rects()
                    self.surface.fill((200, 200, 200, 240))
                    break

class ActionBar :
    def __init__(self, game : Game) :
        self.surface = pg.Surface((game.screen.get_width() * 0.2, game.screen.get_width() * 0.2))
        self.surface.fill((35, 38, 41))
        self.rect = self.surface.get_rect()
        self.button_pressed = -1
        button_size = self.surface.get_width() * 0.25

        self.action_buttons_imgs = [
            pg.transform.scale(pg.image.load("assets/images/move-act.png").convert_alpha(), [button_size] * 2),
            pg.transform.scale(pg.image.load("assets/images/use-act.png").convert_alpha(), [button_size] * 2),
            pg.transform.scale(pg.image.load("assets/images/turn-right-act.png").convert_alpha(), [button_size] * 2),
            pg.transform.scale(pg.image.load("assets/images/turn-left-act.png").convert_alpha(), [button_size] * 2)
        ]
        self.action_buttons_rects = []
        for i in range(2) :
            for j in range(2) :
                button_rect = self.action_buttons_imgs[i * 2 + j].get_rect(
                    topleft = (
                        game.screen.get_width() - self.surface.get_width() +\
                            self.surface.get_width() * 0.5 / 3 * (j + 1) + button_size * j,
                        game.screen.get_height() - self.surface.get_height() +\
                        self.rect.top + self.surface.get_height() * 0.5 / 3 * (i + 1) + button_size * i
                    )
                )
                self.action_buttons_rects.append(button_rect)
    
    def handle_events(self, event) :
        if event.type == MOUSEBUTTONDOWN and event.button == 1 :
            for i in range(len(self.action_buttons_rects)) :
                if self.action_buttons_rects[i].collidepoint(pg.mouse.get_pos()) :
                    self.button_pressed = i
        
    def update(self) : 
        if self.button_pressed != -1 :
            self.action_buttons_rects[self.button_pressed].center = pg.mouse.get_pos()

def main () :
    game = Game()
    game.run()

if __name__ == "__main__":
    game = Game()
    game.run()
