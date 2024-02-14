# Example file showing a basic pygame "game loop"
import random

import pygame
from pygame._sprite import Group

# pygame setup
pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
running = True


def get_snake(length):
    snake = []
    for x in range(length):
        position = (300, 300 + x * 20)
        snake.append(position)
    return snake


def get_all_snake_sprites():
    all_sprites = []
    sprite_base = pygame.image.load('img.png')
    sprite_width, sprite_height = sprite_base.get_width() // 5, sprite_base.get_height() // 4
    for row in range(1, 5):
        for column in range(5):
            subsprite_size = pygame.Rect(
                column * sprite_width,
                sprite_height * (row - 1),
                sprite_width,
                sprite_height
            )
            print(subsprite_size)
            print(sprite_base)
            subsprite = sprite_base.subsurface(subsprite_size)
            all_sprites.append(subsprite)
    sprites = {
        "right_up": all_sprites[0],
        "down_left": all_sprites[0],
        "left": all_sprites[1],
        "right": all_sprites[1],
        "left_up": all_sprites[2],
        "head_up": all_sprites[3],
        "head_right": all_sprites[4],
        "right_down": all_sprites[5],
        "up": all_sprites[7],
        "down": all_sprites[7],
        "head_left": all_sprites[8],
        "head_down": all_sprites[9],
        "left_down": all_sprites[12],
        "tail_up": all_sprites[13],
        "tail_right": all_sprites[14],
        "apple": all_sprites[15],
        "tail_left": all_sprites[18],
        "tail_down": all_sprites[19],
    }
    return sprites


sprite_map = get_all_snake_sprites()




def move_snake(snake, direction, is_eating):
    if not is_eating:
        snake.pop(len(snake) - 1)
    if direction == "up":
        head = snake[0]
        new_head = (head[0], head[1] - 20)
        snake.insert(0, new_head)
    if direction == "down":
        head = snake[0]
        new_head = (head[0], head[1] + 20)
        snake.insert(0, new_head)
    if direction == "right":
        head = snake[0]
        new_head = (head[0] + 20, head[1])
        snake.insert(0, new_head)
    if direction == "left":
        head = snake[0]
        new_head = (head[0] - 20, head[1])
        snake.insert(0, new_head)


fruits = []


def spawn_fruit(fruits_list):
    x = random.randrange(0, 600 // 20)
    y = random.randrange(0, 600 // 20)
    fruits_list.append((x * 20, y * 20))


def draw_image_at_position(image, position):
    sprite = pygame.transform.scale(image, (20, 20))
    rect = sprite.get_rect()
    rect.center = position
    screen.blit(sprite, rect)


def draw_fruits(fruit_list):
    for index, position in enumerate(fruit_list):
        draw_image_at_position(sprite_map['apple'], position)


def draw_snake(snake, direction):
    for index, position in enumerate(snake):
        if index == 0:
            # Drawing head
            draw_image_at_position(sprite_map[f'head_{direction}'], position)
        elif index == len(snake) - 1:
            # Drawing tail
            previous = snake[index - 1]
            if previous[0] < position[0]:
                tail_direction = 'left'
            elif previous[0] > position[0]:
                tail_direction = 'right'
            elif previous[1] < position[1]:
                tail_direction = 'up'
            else:
                tail_direction = 'down'
            draw_image_at_position(sprite_map[f'tail_{tail_direction}'], position)
        else:
            # Drawing body
            previous = snake[index - 1]
            next_pos = snake[index + 1]
            if previous[0] == next_pos[0]:
                # Vertical body
                draw_image_at_position(sprite_map['down'], position)
            elif previous[1] == next_pos[1]:
                # Horizontal body
                draw_image_at_position(sprite_map['right'], position)
            else:
                # Corner body
                if (previous[0] < position[0] and next_pos[1] < position[1]) or (previous[1] < position[1] and next_pos[0] < position[0]):
                    draw_image_at_position(sprite_map['left_down'], position)
                elif (previous[0] < position[0] and next_pos[1] > position[1]) or (previous[1] > position[1] and next_pos[0] < position[0]):
                    draw_image_at_position(sprite_map['left_up'], position)
                elif (previous[0] > position[0] and next_pos[1] < position[1]) or (previous[1] < position[1] and next_pos[0] > position[0]):
                    draw_image_at_position(sprite_map['right_down'], position)
                else:
                    draw_image_at_position(sprite_map['right_up'], position)


def is_head_hitting_body(snake):
    head = snake[0]
    for part in snake[1:]:
        if part == head:
            return True
    return False


def show_lost_message():
    font = pygame.font.Font('freesansbold.ttf', 20)
    text = font.render('game over, press enter to restart', True, 'red', 'black')
    textRect = text.get_rect()
    textRect.center = (screen.get_width() // 2, screen.get_height() // 2)
    screen.blit(text, textRect)


def is_snake_eating_food(snake, fruits_list):
    head = snake[0]
    for fruit in fruits_list:
        if fruit == head:
            fruits_list.remove(fruit)
            return True
    return False


our_snake = get_snake(4)
direction = "up"
delay = 0
lost = False
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    new_direction = direction

    print("Snake Extra Length", len(our_snake) - 4)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and direction != "down":
        new_direction = "up"
    if keys[pygame.K_s] and direction != "up":
        new_direction = "down"
    if keys[pygame.K_a] and direction != "right":
        new_direction = "left"
    if keys[pygame.K_d] and direction != "left":
        new_direction = "right"
    if keys[pygame.K_RETURN] and lost:
        our_snake = get_snake(4)
        lost = False
        direction = "up"

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    if lost:
        show_lost_message()
        pygame.display.flip()
        continue

    if delay > 5:
        is_eating = is_snake_eating_food(our_snake, fruits)
        direction = new_direction
        move_snake(our_snake, direction, is_eating)
        delay = 0
    else:
        delay += 1
    head = our_snake[0]
    head_x, head_y = head
    if head_x > screen.get_width() or head_x < 0:
        lost = True
    if head_y > screen.get_height() or head_y < 0:
        lost = True

    if len(fruits) < 1:
        spawn_fruit(fruits)

    if is_head_hitting_body(our_snake):
        lost = True

    draw_fruits(fruits)

    draw_snake(our_snake, direction)

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # lim its FPS to 60

pygame.quit()
