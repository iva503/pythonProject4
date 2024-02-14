# Example file showing a basic pygame "game loop"
import random

import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
running = True
def get_snake(length):
    snake=[]
    for x in range(length):
        position = (300, 300 + x*20)
        snake.append(position)
    return snake

def get_all_ship_sprites():
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
    sprites={
        "head_left"
    }



def draw_snake(snake):
    for index,position in enumerate(snake):
        if index == 0:
            color = "red"
        else:
            color = "green"
        rect = pygame.Rect((0, 0), (20, 20))
        rect.center = position
        pygame.draw.rect(screen, color, rect)

def move_snake(snake,direction,is_eating):
    if not is_eating:
        snake.pop(len(snake)-1)

    if direction == "up":
        head=snake[0]
        new_head=(head[0],head[1]-20)
        snake.insert(0,new_head)
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
        new_head = (head[0] - 20, head[1] )
        snake.insert(0, new_head)
fruits=[]
def spawn_fruit(fruits_list):
    x=random.randrange(0,600//20)
    y=random.randrange(0,600//20)
    fruits_list.append((x*20,y*20))

def draw_fruits(fruit_list):
    for index,position in enumerate(fruit_list):
        rect = pygame.Rect((0, 0), (20, 20))
        rect.center = position
        pygame.draw.rect(screen, "red", rect)

def is_head_hitting_body(snake):
    head=snake[0]
    for part in snake[1:]:
        if part==head:
            return True
    return False
def show_lost_message():
    font = pygame.font.Font('freesansbold.ttf', 20)
    text = font.render('game over, press enter to restart', True, 'red', 'black')
    textRect = text.get_rect()
    textRect.center = (screen.get_width() // 2, screen.get_height() // 2)
    screen.blit(text, textRect)

def is_snake_eating_food(snake,fruits_list):
    head=snake[0]
    for fruit in fruits_list:
        if fruit==head:
            fruits_list.remove(fruit)
            return True
    return False

our_snake=get_snake(4)
direction="up"
delay=0
lost=False
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    new_direction=direction

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and direction != "down":
        new_direction="up"
    if keys[pygame.K_s] and direction != "up":
        new_direction= "down"
    if keys[pygame.K_a] and direction != "right":
        new_direction= "left"
    if keys[pygame.K_d] and direction != "left":
        new_direction= "right"
    if keys[pygame.K_RETURN] and lost:
        our_snake=get_snake(4)
        lost=False
        direction="up"

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    if lost:
        show_lost_message()
        pygame.display.flip()
        continue


    if delay > 5:
        is_eating=is_snake_eating_food(our_snake,fruits)
        direction=new_direction
        move_snake(our_snake,direction,is_eating)
        delay=0
    else:
        delay += 1
    head=our_snake[0]
    head_x,head_y=head
    if head_x > screen.get_width() or head_x < 0:
        lost=True
    if head_y > screen.get_height() or head_y < 0:
        lost=True

    if len(fruits) < 1:
        spawn_fruit(fruits)

    if is_head_hitting_body(our_snake):
        lost=True

    draw_fruits(fruits)




    draw_snake(our_snake)

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # lim its FPS to 60

pygame.quit()