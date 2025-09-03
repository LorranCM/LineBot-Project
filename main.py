import pygame as pg
from pygame.locals import *
from tools.maze_surf_generation import get_maze_surface
from obj.Robot import Robot
from obj.HomeButton import HomeButton
from obj.StartButton import StartButton
from obj.TrashButton import TrashButton

class Game :
    def __init__(self) :
        self.screen = pg.display.set_mode((0, 0))
        self.clock = pg.time.Clock()
        self.running = True
        self.level = 1
        self.state = Gameplay(self, self.level)

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
        self.robot = Robot(self.maze_arr, game.clock)
        self.panel = Panel(game, self.robot)
        self.robot.action_list = self.panel.actionlist.action_list
        self.position = (self.game.screen.get_width() // 2, self.game.screen.get_height() // 2)
        self.resize_maze()
        self.homebutton = HomeButton(game.screen)
        self.startbutton = StartButton(game.screen)
        self.trashbutton = TrashButton(game.screen, self.panel.actionlist)
        self.trashbutton.rect.right = self.panel.actionlist.rect.left - game.screen.get_height() * 0.05
        self.zoom = 1.0
        self.screen_is_pressed = 0
        def action () : self.game.state = MainMenu(game)
        self.homebutton.action = action

    def draw(self) :
        self.game.screen.fill((139, 145, 150))
        self.surface_copy = self.surface.copy()
        self.draw_robot()
        self.game.screen.blit(self.surface_copy, self.rect)
        self.draw_panel()
        self.homebutton.draw()
        self.startbutton.draw()
        self.trashbutton.draw()
        pg.display.flip()

    def update(self) :
        if self.robot.end :
            self.game.level += 1 if not self.game.level == 20 else 0
            self.game.state = Gameplay(self.game, self.game.level)
        if self.startbutton.robot_moving :
            if self.robot.action_queue == len(self.robot.action_list) :
                self.startbutton.robot_moving = False
        self.robot.update(self.startbutton.robot_moving)
        self.panel.update()

    def handle_events(self) :
        for event in pg.event.get() :
            if event.type == QUIT :
                self.game.running = False
            
            if not self.screen_is_pressed :
                if not self.startbutton.running :
                    self.panel.actionbar.handle_events(event)
                if self.panel.actionbar.button_pressed == -1:
                    self.panel.actionlist.handle_events(event, self.startbutton.running)

            if event.type == MOUSEWHEEL :
                if not (self.panel.actionlist.rect.collidepoint(pg.mouse.get_pos()) or \
                    self.panel.actionbar.rect.collidepoint(pg.mouse.get_pos())) and \
                    self.panel.actionbar.button_pressed == -1  :
                    if event.y > 0 and self.zoom < 1.5 :
                        self.zoom += 0.05
                    elif event.y < 0 and self.zoom > 0.5 :
                        self.zoom -= 0.05
                    self.resize_maze(self.zoom)
                
                if self.panel.actionlist.rect.collidepoint(pg.mouse.get_pos()) and not self.startbutton.running :
                    self.panel.actionlist.scroll += 20 * event.y
                    if self.panel.actionlist.scroll > 0 : 
                        self.panel.actionlist.scroll = 0
                    if self.panel.actionlist.scroll_limit > self.panel.actionlist.scroll :
                        self.panel.actionlist.scroll = self.panel.actionlist.scroll_limit

                    self.panel.actionlist.update_action_list_rects()
            
            if event.type == MOUSEBUTTONDOWN and event.button == 1 :
                self.homebutton.get_pressed()
                if self.robot.action_list :
                    self.startbutton.get_pressed()
                    if not self.startbutton.running :
                        self.robot.__init__(self.maze_arr, self.game.clock)
                if not self.startbutton.running :
                    self.trashbutton.get_pressed()
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
                    if self.panel.actionlist.rect.collidepoint(pg.mouse.get_pos()) and not collide and \
                        not self.startbutton.running:
                        self.panel.actionlist.action_list.append(self.panel.actionbar.button_pressed)
                        self.panel.actionlist.update_action_list_rects()
                    self.panel.actionbar.__init__(self.game)

            if event.type == MOUSEMOTION and self.screen_is_pressed :
                dx, dy = event.rel
                self.position = (self.position[0] + dx, self.position[1] + dy)
                self.rect.center = self.position
            
            if event.type == KEYDOWN :
                if event.key == K_SPACE :
                    self.position = (self.game.screen.get_width() // 2, self.game.screen.get_height() // 2)
                    self.rect.center = self.position
    
    def resize_maze(self, resize_factor : int = 1) :
        height = int(self.game.screen.get_height() * resize_factor)
        width = height * self.initial_surface.get_width() / self.initial_surface.get_height()
        self.surface = pg.transform.scale(self.initial_surface, (int(width), int(height)))
        self.surface_copy = self.surface.copy()
        self.rect = self.surface.get_rect(
            center = (self.position)
        )
    
    def draw_robot(self) :
        robot_image = pg.transform.scale(
            self.robot.original_image, ([self.surface_copy.get_height() / (len(self.maze_arr) + 2) + 1] * 2)
        )
        robot_image = pg.transform.rotate(robot_image, self.robot.angle)
        robot_rect = robot_image.get_rect(center = (
                (self.robot.arr_position[1] + 1) * (self.surface_copy.get_height() / (len(self.maze_arr) + 2)) +
                self.surface_copy.get_height() / (len(self.maze_arr) + 2) / 2,
                (self.robot.arr_position[0] + 1) * (self.surface_copy.get_height() / (len(self.maze_arr) + 2)) +
                self.surface_copy.get_height() / (len(self.maze_arr) + 2) / 2,
            )
        )
        self.surface_copy.blit(robot_image, robot_rect)
    
    def draw_panel(self) :
        self.panel.actionbar.rect.topright = (self.game.screen.get_width(), self.panel.actionlist.rect.bottom)
        if self.startbutton.running :
            self.panel.actionlist.draw_queue_cursor()
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
    def __init__(self, game : Game, robot : Robot) :
        self.actionlist = ActionList(game, robot)
        self.actionbar = ActionBar(game)
    
    def update(self) :
        self.actionbar.update()
        self.actionlist.update()

class ActionList :
    def __init__(self, game : Game, robot : Robot) :
        self.surface = pg.Surface(
            (game.screen.get_width() * 0.15, game.screen.get_height() - game.screen.get_width() * 0.15), SRCALPHA
        )
        self.surface.fill((200, 200, 200, 240))
        self.rect = self.surface.get_rect()
        self.rect.topright = (game.screen.get_width(), 0)
        self.action_list = []
        self.action_list_rects = []
        self.action_buttons_imgs = [
            pg.image.load("assets/images/move-act.png").convert_alpha(),
            pg.image.load("assets/images/use-act.png").convert_alpha(),
            pg.image.load("assets/images/turn-right-act.png").convert_alpha(), 
            pg.image.load("assets/images/turn-left-act.png").convert_alpha()
        ]
        self.queue_cursor_image = pg.transform.scale(
            pg.image.load("assets/images/queue-cursor.png").convert_alpha(),
            [self.surface.get_width() * 0.1] * 2
        )
        self.robot = robot
        self.scroll_limit = 0
        self.scroll = 0
    
    def update(self) :
        self.surface.fill((200, 200, 200, 240))
        self.action_queue = self.robot.action_queue
        if self.action_queue >= len(self.robot.action_list) :
            self.action_queue = len(self.robot.action_list) - 1
    
    def draw_queue_cursor(self) :
        position = [0, 0]
        rect = self.queue_cursor_image.get_rect()
        self.scroll = (self.action_queue) // 3 + 1 - (self.surface.get_height() // (self.surface.get_width() * 0.3))
        if self.scroll < 0 :
            self.scroll = 0
        self.scroll *= self.surface.get_width() * -0.3
        self.update_action_list_rects()
        position[0] = self.surface.get_width() * 0.1 + \
            (self.action_queue % 3) * self.surface.get_width() * 0.3
        position[1] = self.surface.get_width() * 0.1 + \
            (self.action_queue // 3) * self.surface.get_width() * 0.3 + self.scroll
        rect.center = position
        self.surface.blit(self.queue_cursor_image, rect)

    def update_action_list_rects(self) :
        self.action_list_rects = []
        for i in range(len(self.action_list)) :
            rect = pg.rect.Rect(
                self.surface.get_width() * 0.1 * (i % 3 + 1) + self.surface.get_width() * 0.2 * (i % 3) + \
                    self.surface.get_width() * 8.5 / 1.5,
                self.surface.get_width() * 0.1 * (i // 3 + 1) + self.surface.get_width() * 0.2 * (i // 3) + \
                    self.scroll,
                self.surface.get_width() * 0.2,
                self.surface.get_width() * 0.2
            )
            self.action_list_rects.append(rect)
        self.scroll_limit = (
            len(self.action_list) - 1) // 3 - (self.surface.get_height() // (self.surface.get_width() * 0.3) - 1
        )
        if self.scroll_limit < 0 :
            self.scroll_limit = 0
        self.scroll_limit *= self.surface.get_width() * -0.3
    
    def handle_events(self, event : pg.event.Event, running) :
        if event.type == MOUSEBUTTONDOWN and event.button == 3 :
            for i in range(len(self.action_list_rects)) :
                if self.action_list_rects[i].collidepoint(pg.mouse.get_pos()) and not running :
                    self.action_list.pop(i)
                    self.update_action_list_rects()
                    if self.scroll <= self.scroll_limit :
                        self.scroll = self.scroll_limit
                    self.update_action_list_rects()
                    self.surface.fill((200, 200, 200, 240))
                    break

class ActionBar :
    def __init__(self, game : Game) :
        self.surface = pg.Surface((game.screen.get_width() * 0.15, game.screen.get_width() * 0.15))
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
    
    def handle_events(self, event : pg.event.Event) :
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
