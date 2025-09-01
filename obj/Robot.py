import pygame as pg

class Robot :
    def __init__(self, maze : list) :
        for i in range(len(maze)) :
            for j in range(len(maze[i])) :
                if maze[i][j] == 2 :
                    self.arr_position = [i, j]
        self.angle = 0
        self.original_image = pg.image.load("./assets/images/linebot.png").convert_alpha()
    
    def move(self, distance : float) :
        ...
    
    def rotate(self, angle : float) :
        ...