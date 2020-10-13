import pygame
import random

pygame.init()

WIN_WIDTH = 600
WIN_HEIGHT = 500

SNAKE_BLOCK = 10
SNAKE_SPEED = 15


def is_lost(snake_list, snake_head):
    for x in snake_list[:-1]:
        if x == snake_head:
            return True

    if snake_head[0] >= WIN_WIDTH or snake_head[0] < 0 or snake_head[1] >= WIN_HEIGHT or snake_head[1] < 0:
        return True

    return False


def display_window(win, score, snake_block, snake_list, foodx, foody):
    # score
    score_font = pygame.font.SysFont("comicsansms", 25)
    value = score_font.render("Your Score: " + str(score), True, (255, 255, 255))
    win.blit(value, [0, 0])

    # food
    pygame.draw.rect(win, (255, 255, 255), [foodx, foody, SNAKE_BLOCK, SNAKE_BLOCK])

    # snake
    for x in snake_list:
        pygame.draw.rect(win, (255, 255, 255), [x[0], x[1], snake_block, snake_block])

    pygame.display.update()


def play():
    dis = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    running = True

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -SNAKE_BLOCK
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = SNAKE_BLOCK
                    x1_change = 0

        # snake code
        if x1 >= WIN_WIDTH or x1 < 0 or y1 >= WIN_HEIGHT or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill((0, 0, 0))

        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        display_window(dis, length_of_snake - 1, SNAKE_BLOCK, snake_list, foodx, foody)

        if is_lost(snake_list, snake_head):
            running = False

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, WIN_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
            foody = round(random.randrange(0, WIN_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
            length_of_snake += 1

        clock.tick(SNAKE_SPEED)


if __name__ == "__main__":
    play()
