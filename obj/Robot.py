import pygame as pg
from math import sin, cos, radians

class Robot :
    def __init__(self, maze : list, clock : pg.time.Clock) :
        for i in range(len(maze)) :
            for j in range(len(maze[i])) :
                if maze[i][j] == 2 :
                    self.arr_position = [i, j]
        self.maze = maze
        self.clock = clock
        self.angle = 0
        self.next_angle = 0
        self.original_image = pg.image.load("./assets/images/linebot.png").convert_alpha()
        self.action = -1
        self.action_queue = 0
        self.end = False
        for i in range(len(maze)) :
            for j in range(len(maze[0])) :
                if maze[i][j] == 3 :
                    self.maze_exit = [i, j]

    def update(self, start) :
        tick = self.clock.tick(60) / 250
        if start and self.action == -1 :
            if self.arr_position[0] == self.maze_exit[0] and\
            self.arr_position[1] == self.maze_exit[1] :
                self.end = True
            self.action = self.action_list[self.action_queue]
            if self.action == 0 :
                self.last_position = self.arr_position[:]
                if int(self.last_position[0] - sin(radians(self.angle)) in (-1, len(self.maze))) or \
                   int(self.last_position[1] + cos(radians(self.angle)) in (-1, len(self.maze[0]))) or \
                   self.maze[
                        int(self.last_position[0] - int(sin(radians(self.angle))))][
                        int(self.last_position[1] + int(cos(radians(self.angle))))] == 1 :
                    self.action = -1
            if self.action == 3 :
                self.next_angle = self.angle + 90
            if self.action == 2 :
                self.next_angle = self.angle - 90
        if self.action == 0 :
            self.move(tick)
        elif self.action == 3 :
            self.rotate(tick, 1)
        elif self.action == 2 :
            self.rotate(tick, -1)
        

    def move(self, tick) :
        sin_ang = int(sin(radians(self.angle)))
        cos_ang = int(cos(radians(self.angle)))

        self.arr_position[0] -= sin_ang * tick
        self.arr_position[1] += cos_ang * tick

        if sin_ang > 0 :
            if self.arr_position[0] <= self.last_position[0] - sin_ang :
                self.arr_position[0] = self.last_position[0] - sin_ang
                self.action = -1
                self.action_queue += 1

        elif sin_ang < 0 :
            if self.arr_position[0] >= self.last_position[0] - sin_ang :
                self.arr_position[0] = self.last_position[0] - sin_ang
                self.action = -1
                self.action_queue += 1

        elif cos_ang > 0 :
            if self.arr_position[1] >= self.last_position[1] + cos_ang :
                self.arr_position[1] = self.last_position[1] + cos_ang
                self.action = -1
                self.action_queue += 1

        elif cos_ang < 0 : 
            if self.arr_position[1] <= self.last_position[1] + cos_ang :
                self.arr_position[1] = self.last_position[1] + cos_ang
                self.action = -1
                self.action_queue += 1

            
    def rotate(self, tick, flag) :
        self.angle += 90 * tick * flag
        if flag > 0 and self.angle >= self.next_angle :
            self.angle = self.next_angle
            self.action = -1
            self.action_queue += 1
        if flag < 0 and self.angle <= self.next_angle :
            self.angle = self.next_angle
            self.action = -1
            self.action_queue += 1
