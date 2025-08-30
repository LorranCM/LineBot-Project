import json, pygame
from pygame.locals import *

def main() :
    with open("./mazes.json", "r") as file :
        mazes_dict = json.loads(file.read())

    maze_name = "maze-" + input()
    c_maze = mazes_dict[maze_name]
    screen = pygame.display.set_mode((500,500))
    pygame.display.set_caption("Maze Generation Test")

    maze_wall_imgs = [
        pygame.image.load("./assets/images/wall1.png").convert_alpha(),
        pygame.image.load("./assets/images/wall2-1.png").convert_alpha(),
        pygame.image.load("./assets/images/wall3.png").convert_alpha(),
        pygame.image.load("./assets/images/wall4.png").convert_alpha(),
        pygame.image.load("./assets/images/wall2-2.png").convert_alpha(),
    ]

    wall_dim = maze_wall_imgs[0].get_size()
    maze_surface = pygame.Surface(
        (wall_dim[0] * len(c_maze[0]), wall_dim[1] * len(c_maze)), pygame.SRCALPHA
    )

    for i in range(len(c_maze)) :
        for j in range(len(c_maze[i])) :
            if c_maze[i][j] == 1 :
                search_dir = [(0, -1), (1, 0), (0, 1), (-1, 0)]
                wall_type = -1
                image_angle = 0

                if i == 0 :
                    search_dir[search_dir.index((-1, 0))] = 0
                if i == len(c_maze) - 1 :
                    search_dir[search_dir.index((1, 0))] = 0
                if j == 0 :
                    search_dir[search_dir.index((0, -1))] = 0
                if j == len(c_maze[i]) - 1 :
                    search_dir[search_dir.index((0, 1))] = 0
                for d in search_dir :
                    if d :
                        if c_maze[i + d[0]][j + d[1]] :
                            wall_type += 1


                if wall_type == 0 :
                    for d in search_dir :
                        if d :
                            if c_maze[i + d[0]][j + d[1]] == 1 :
                                break
                        image_angle += 90 

                if wall_type == 1 :
                    count = 0
                    step = 0
                    for d in range(len(search_dir)) :
                        if count == 1 :
                            step += 1
                        if search_dir[d] :
                            if c_maze[i + search_dir[d][0]][j + search_dir[d][1]] == 1 :
                                if search_dir[d - 1] and c_maze[i + search_dir[d-1][0]][j + search_dir[d-1][1]] :
                                    wall_type = 4
                                    break
                                if count == 1 :
                                    if not step == 2 :
                                        wall_type = 4
                                    break
                                count += 1
                        image_angle += 90 

                if wall_type == 2 :
                    for d in search_dir :
                        if d :
                            if c_maze[i + d[0]][j + d[1]] == 0 :
                                image_angle += 180
                                break
                        else :
                            image_angle += 180
                            break
                        image_angle += 90 
                
                wall_img = pygame.transform.rotate(maze_wall_imgs[wall_type], image_angle)
                maze_surface.blit(wall_img, (j * wall_dim[0], i * wall_dim[1]))

    running = True

    while running :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                running = False

        screen.fill((106, 155, 195))
        screen.blit(maze_surface, (250 - maze_surface.get_width()//2, 250 - maze_surface.get_height()//2))
        pygame.display.flip()   

if __name__ == "__main__" :
    main()