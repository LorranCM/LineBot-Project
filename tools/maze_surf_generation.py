import json, pygame

def get_maze_surface(maze_n : int) :
    with open("./mazes.json", "r") as file :
        mazes_dict = json.loads(file.read())

    maze_name = "maze-" + str(maze_n)
    c_maze = mazes_dict[maze_name]

    maze_wall_imgs = [
        pygame.image.load("./assets/images/wall1.png").convert_alpha(),
        pygame.image.load("./assets/images/wall2-1.png").convert_alpha(),
        pygame.image.load("./assets/images/wall3.png").convert_alpha(),
        pygame.image.load("./assets/images/wall4.png").convert_alpha(),
        pygame.image.load("./assets/images/wall2-2.png").convert_alpha(),
    ]

    wall_dim = maze_wall_imgs[0].get_size()
    maze_surface = pygame.Surface(
        (wall_dim[0] * len(c_maze[0]) + wall_dim[0] * 2, wall_dim[1] * len(c_maze) + wall_dim[1] * 2), pygame.SRCALPHA
    )
    maze_surface.fill((35, 38, 41, 50))

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
                        if c_maze[i + d[0]][j + d[1]] == 1 :
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
                                if search_dir[d - 1] and c_maze[i + search_dir[d-1][0]][j + search_dir[d-1][1]] == 1:
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
                maze_surface.blit(wall_img, ((j + 1) * wall_dim[0], (i + 1) * wall_dim[1]))

    return maze_surface, c_maze