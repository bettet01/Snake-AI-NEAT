import pygame
import random
import neat
import os

pygame.init()

WIN_WIDTH = 600
WIN_HEIGHT = 500

SNAKE_BLOCK = 10
SNAKE_SPEED = 500

GENERATION_COUNT = 1


def is_lost(snake_list, snake_head):
    for x in snake_list[:-1]:
        if x == snake_head:
            return True

    if snake_head[0] >= WIN_WIDTH or snake_head[0] < 0 or snake_head[1] >= WIN_HEIGHT or snake_head[1] < 0:
        return True

    return False


def display_window(win, score, snake_block, snake_list, foodx, foody):
    global GENERATION_COUNT
    win.fill((0, 0, 0))
    # score
    font = pygame.font.SysFont("comicsansms", 25)
    value = font.render("Your Score: " + str(score), True, (255, 255, 255))
    win.blit(value, [0, 0])

    gen_display = font.render("Generation: " + str(GENERATION_COUNT), True, (255, 255, 255))
    win.blit(gen_display, [410, 0])

    # food
    pygame.draw.rect(win, (255, 255, 255), [foodx, foody, SNAKE_BLOCK, SNAKE_BLOCK])

    # snake
    for x in snake_list:
        pygame.draw.rect(win, (255, 255, 255), [x[0], x[1], snake_block, snake_block])

    pygame.display.update()


def main(genomes, config):
    global GENERATION_COUNT
    global SNAKE_SPEED

    nets = []
    ge = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0
        ge.append(g)

    # loop through each snake
    for index, net in enumerate(nets):
        current_direction = ""
        head_history = []
        running = True
        timer = 0
        got_apple = False
        dis = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        clock = pygame.time.Clock()

        # food items
        foodx = round(random.randrange(0, WIN_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
        foody = round(random.randrange(0, WIN_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0

        # snake items
        x1 = WIN_WIDTH / 2
        y1 = WIN_HEIGHT / 2
        x1_change = 0
        y1_change = 0
        snake_list = []
        length_of_snake = 1

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    quit()

            if snake_list:
                dis_to_food_x = snake_list[len(snake_list) - 1][0] - foodx
                dis_to_food_y = snake_list[len(snake_list) - 1][1] - foody
                var1 = snake_list[len(snake_list) - 1][1]
                var2 = abs(snake_list[len(snake_list) - 1][1] - WIN_HEIGHT)
                var3 = snake_list[len(snake_list) - 1][0]
                var4 = abs(snake_list[len(snake_list) - 1][0] - WIN_WIDTH)
            else:
                dis_to_food_x = 0
                dis_to_food_y = 0
                var1 = 0
                var2 = 0
                var3 = 0
                var4 = 0

            # output
            output = net.activate((dis_to_food_x, dis_to_food_y, var1, var2, var3, var4))

            if output[0] > .5:
                if current_direction != "RIGHT":
                    x1_change = -SNAKE_BLOCK
                    y1_change = 0
                    current_direction = "LEFT"
            elif output[1] > .5:
                if current_direction != "LEFT":
                    x1_change = SNAKE_BLOCK
                    y1_change = 0
                    current_direction = "RIGHT"
            elif output[2] > .5:
                if current_direction != "DOWN":
                    y1_change = -SNAKE_BLOCK
                    x1_change = 0
                    current_direction = "UP"
            elif output[3] > .5:
                if current_direction != "UP":
                    y1_change = SNAKE_BLOCK
                    x1_change = 0
                    current_direction = "DOWN"

            x1 += x1_change
            y1 += y1_change

            snake_head = [x1, y1]
            snake_list.append(snake_head)
            if len(snake_list) > length_of_snake:
                del snake_list[0]

            if GENERATION_COUNT % 200 == 0:
                SNAKE_SPEED = 50
                display_window(dis, length_of_snake - 1, SNAKE_BLOCK, snake_list, foodx, foody)
            else:
                SNAKE_SPEED = 2000

            if is_lost(snake_list, snake_head):
                ge[index].fitness -= 50
                running = False

            if x1 == foodx and y1 == foody:
                timer = 0
                ge[index].fitness += 1000
                foodx = round(random.randrange(0, WIN_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
                foody = round(random.randrange(0, WIN_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
                length_of_snake += 1

            if timer < 500:
                timer += 1
            else:
                ge[index].fitness -= 100
                running = False

            if head_history:
                if abs(head_history[0] - foodx) < abs(snake_head[0] - foodx):
                    ge[index].fitness += (600 - abs(snake_head[0] - foodx)) / 100
                if abs(head_history[1] - foody) < abs(snake_head[1] - foody):
                    ge[index].fitness += (500 - abs(snake_head[1] - foody)) / 100
            head_history = snake_head
            clock.tick(SNAKE_SPEED)

    GENERATION_COUNT += 1


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 1000)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
