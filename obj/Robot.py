import pygame as pg

class Robot :
    def __init__(self, maze : list, clock : pg.time.Clock) :
        for i in range(len(maze)) :
            for j in range(len(maze[i])) :
                if maze[i][j] == 2 :
                    self.arr_position = [i, j]
        self.clock = clock
        self.angle = 0
        self.original_image = pg.image.load("./assets/images/linebot.png").convert_alpha()
        self.action = -1

    def update(self) :
        tick = self.clock.tick(60) / 1000
        
        