"""Dino Game in Python

A game similar to the famous Chrome Dino Game, built using pygame-ce.
Made by intern: @bassemfarid, no one or nothing else. 🤖
"""

import pygame
from random import randint

def score():
    time = pygame.time.get_ticks()
    score_surf = game_font.render("SCORE:"+str(int(time/5000)), False, "Cyan")
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 320:
                screen.blit(sugar_surf,obstacle_rect)
            elif obstacle_rect.bottom == 310:
                screen.blit(egg_surf,obstacle_rect)
            elif obstacle_rect.bottom == 300:
                screen.blit(spoon_surf, obstacle_rect)
            else:
                screen.blit(whisk_surf, obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -120]
        return obstacle_list
    else:
        return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
            else:
                return True

lifes = 3

# Initialize Pygame and create a window
pygame.init()
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
running = True  # Pygame main loop, kills pygame when False

# Game state variables
is_playing = True  # Whether in game or in menu
GROUND_Y = 300  # The Y-coordinate of the ground level
JUMP_GRAVITY_START_SPEED = -20  # The speed at which the player jumps
players_gravity_speed = 0  # The current speed at which the player falls

# Load level assets
SKY_SURF = pygame.image.load("graphics/level/sky.png").convert()
GROUND_SURF = pygame.image.load("graphics/level/floor.png").convert()
end_surf = pygame.image.load("graphics/level/end.png")
game_font = pygame.font.Font(pygame.font.get_default_font(), 50)


# Load sprite assets
player_surf = pygame.image.load("graphics/player/horse1.png.png").convert_alpha()
player_rect = player_surf.get_rect(bottomleft=(25, GROUND_Y))
sugar_surf = pygame.image.load("graphics/egg/sugar.png").convert_alpha()
egg_surf = pygame.image.load("graphics/egg/egg.png").convert_alpha()
spoon_surf = pygame.image.load("graphics/egg/spoon.png").convert_alpha()
whisk_surf = pygame.image.load("graphics/egg/whisk.png").convert_alpha()

obstacle_rect_list = []

# timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 2000)

while running:
    # Poll for events
    for event in pygame.event.get():
        # pygame.QUIT --> user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False

        elif is_playing:
            # When player wants to jump by pressing SPACE
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
                or event.type == pygame.MOUSEBUTTONDOWN
            ) and player_rect.bottom >= GROUND_Y:
                players_gravity_speed = JUMP_GRAVITY_START_SPEED
        else:
            # When player wants to play again by pressing SPACE
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                is_playing = True
       
        #enemy spawn
        if event.type == obstacle_timer:
            egg_type = randint(0,4)
            if egg_type == 0:
                obstacle_rect_list.append(sugar_surf.get_rect(bottomleft=(randint(8,11)*100, 320)))
            elif egg_type == 1:
                obstacle_rect_list.append(egg_surf.get_rect(bottomleft=(randint(8,11)*100, 310)))
            if egg_type == 2:
                obstacle_rect_list.append(spoon_surf.get_rect(bottomleft=(randint(8,11)*100, 300)))
            if egg_type == 3:
                obstacle_rect_list.append(whisk_surf.get_rect(bottomleft=(randint(8,11)*100, 290)))


    if is_playing:
        screen.fill("purple")  # Wipe the screen

        # Blit the level assets
        screen.blit(SKY_SURF, (0, 0))
        screen.blit(GROUND_SURF, (0, GROUND_Y))
        score()

        # Adjust player's vertical location then blit it
        players_gravity_speed += 1
        player_rect.y += players_gravity_speed
        if player_rect.bottom > GROUND_Y:
            player_rect.bottom = GROUND_Y
        screen.blit(player_surf, player_rect)

        #obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # When player collides with enemy, game ends
        is_playing = collisions(player_rect, obstacle_rect_list)

    # When game is over, display game over message
    else:
        screen.blit(end_surf, (0,0))
        if (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_SPACE):
            is_playing = True
            obstacle_rect_list.clear()


    # flip the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # Limits game loop to 60 FPS

pygame.quit()
