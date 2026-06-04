import pygame
from random import randint
start_time = 0
lifes = 3
obstacle_score = 0

# Initialize Pygame and create a window
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Intergalactic Earthquake Roller Rink Horse Bakery Bonanza")
clock = pygame.time.Clock()
running = True  # Pygame main loop, kills pygame when False

# Game state variables
is_playing = True  # Whether in game or in menu
menu = True
GROUND_Y = 300  # The Y-coordinate of the ground level
JUMP_GRAVITY_START_SPEED = -20  # The speed at which the player jumps
players_gravity_speed = 0  # The current speed at which the player falls

# Load level assets
sky_surf = pygame.image.load("graphics/level/sky.png").convert()
ground_surf = pygame.image.load("graphics/level/floor.png").convert()
end_surf = pygame.image.load("graphics/level/end.png")
start_surf = pygame.image.load("graphics/level/start.png")
game_font = pygame.font.Font(pygame.font.get_default_font(), 50)


# Load sprite assets
horse1 = pygame.image.load("graphics/player/horse1.png.png").convert_alpha()
horse2 = pygame.image.load("graphics/player/horse1.png-1.png.png").convert_alpha()
magic_horse1 = pygame.image.load("graphics/player/magichorse1.png").convert_alpha()
magic_horse2 = pygame.image.load("graphics/player/magichorse2.png").convert_alpha()
horse = [horse1, horse2, magic_horse1, magic_horse2]
horse_normal = True
horse_number = 0
player_surf = horse[horse_number]
player_rect = player_surf.get_rect(bottomleft=(25, GROUND_Y))
sugar_surf = pygame.image.load("graphics/egg/sugar.png").convert_alpha()
egg_surf = pygame.image.load("graphics/egg/egg.png").convert_alpha()
spoon_surf = pygame.image.load("graphics/egg/spoon.png").convert_alpha()
whisk_surf = pygame.image.load("graphics/egg/whisk.png").convert_alpha()
magic_surf = pygame.image.load("graphics/egg/magic.png").convert_alpha()

obstacle_rect_list = []
magic_rect_list = []

# timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1200)

magic_timer = pygame.USEREVENT + 2
spawn_time = 5000
combo = 0
pygame.time.set_timer(magic_timer, spawn_time)

horse_timer = pygame.USEREVENT + 3
pygame.time.set_timer(horse_timer, 100)

def score_display():
    global score
    score = (pygame.time.get_ticks() - start_time)//2000 + obstacle_score//540
    file = open("highscore.txt", "r")
    global current_hs
    current_hs = int(file.read())
    if score > current_hs:
        current_hs = score
        global highscore
        highscore = True
    else:
        highscore = False
    file.close()
    score_surf = game_font.render("SCORE:"+str(score)+" LIVES:"+str(lifes)+" COMBO:"+str(combo), False, "Cyan")
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)

def collisions(player, obstacles):
    for obstacle_rect in obstacles:
        if obstacle_rect.colliderect(player):
            global lifes, horse_normal
            lifes -= 1
            horse_normal = True
            obstacles.remove(obstacle_rect)
            if lifes <= 0:
                return False
    return True

def player_animation():
    global player_surf, horse_number, lifes, spawn_time

    if horse_normal == True:
        spawn_time = 5000
        if horse_number > 1:
            horse_number = 0
        horse_number += 0.6
        player_surf = horse[int(horse_number)]
    else:
        if horse_number > 3:
            horse_number = 2
        horse_number += 0.6
        player_surf = horse[int(horse_number)]

while running:
    screen.blit(start_surf, (0,0))
    # Poll for events
    for event in pygame.event.get():
        # pygame.QUIT --> user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False

        elif menu == True:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or event.type == pygame.MOUSEBUTTONDOWN:
                menu = False
                playing = True

        elif is_playing:
            if event.type == horse_timer:
                player_animation()
            # When player wants to jump by pressing SPACE
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
                or event.type == pygame.MOUSEBUTTONDOWN
            ) and player_rect.bottom > 200:
                players_gravity_speed = JUMP_GRAVITY_START_SPEED
            #enemy spawn
            if event.type == obstacle_timer:
                egg_type = randint(0,4)
                if egg_type == 0:
                    obstacle_rect_list.append(sugar_surf.get_rect(bottomleft=(randint(8,10)*100, 320)))
                if egg_type == 1:
                    obstacle_rect_list.append(egg_surf.get_rect(bottomleft=(randint(8,10)*100, 310)))
                if egg_type == 2:
                    obstacle_rect_list.append(spoon_surf.get_rect(bottomleft=(randint(8,10)*100, 300)))
                if egg_type == 3:
                    obstacle_rect_list.append(whisk_surf.get_rect(bottomleft=(randint(8,10)*100, 290)))
            
            if event.type == magic_timer:
                magic_rect_list.append(magic_surf.get_rect(bottomleft = (randint(8,10)*100, 312)))
        
        else:
            screen.blit(start_surf, (0, 0))
            # When player wants to play again by pressing SPACE
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                is_playing = True
       
    if menu:
        screen.blit(start_surf, (0,0))

    elif is_playing:
        screen.fill("purple")  # Wipe the screen


        sky_surf.scroll(randint(-1, 1), randint(-4, 0), pygame.SCROLL_REPEAT)
        ground_surf.scroll(-9, 0, pygame.SCROLL_REPEAT)

        # Blit the level assets
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, GROUND_Y))

        # Adjust player's vertical location then blit it
        players_gravity_speed += 0.75
        player_rect.y += players_gravity_speed
        if player_rect.bottom > GROUND_Y:
            player_rect.bottom = GROUND_Y
        screen.blit(player_surf, player_rect)

        #obstacle movement
        # obstacle_rect_list = obstacle_movement(obstacle_rect_list, sugar_surf)
        if obstacle_rect_list:
            for obstacle_rect in obstacle_rect_list:
                if obstacle_rect.bottom == 320:
                    #sugar_surf = pygame.transform.rotate(sugar_surf, 5)
                    screen.blit(sugar_surf,obstacle_rect)
                    obstacle_rect.x -= 15
                elif obstacle_rect.bottom == 310:
                    #egg_surf = pygame.transform.rotate(egg_surf, 15)
                    screen.blit(egg_surf,obstacle_rect)
                    obstacle_rect.x -= 12
                elif obstacle_rect.bottom == 300:
                    #spoon_surf = pygame.transform.rotate(spoon_surf, 10)
                    screen.blit(spoon_surf, obstacle_rect)
                    obstacle_rect.x -= 7
                else:
                    #whisk_surf = pygame.transform.rotate(whisk_surf, randint(-1, 5)*5)
                    screen.blit(whisk_surf, obstacle_rect)
                    obstacle_rect.x -= randint(-1, 4)*4
            obstacle_rect_list = [obstacle for obstacle in obstacle_rect_list if obstacle.x > -100]
        else:
            obstacle_rect_list = []
        obstacle_score += len(obstacle_rect_list)
        score_display()

        if magic_rect_list:
            for magic_rect in magic_rect_list:
                screen.blit(magic_surf, magic_rect)
                magic_rect.x -= 12
                magic_rect_list = [magic for magic in magic_rect_list if magic.x > -100]
        else: magic_rect_list = []

        # When player collides with enemy, game ends
        is_playing = collisions(player_rect, obstacle_rect_list)
        

        for magic_rect in magic_rect_list:
            if player_rect.colliderect(magic_rect):
                horse_normal = False
                spawn_time -= 1000
                combo += 1
                horse_number = 2
                lifes += 1
                magic_rect_list.remove(magic_rect)

    # When game is over, display game over message
    else:
        screen.blit(end_surf, (0,0))
        if highscore == True:
            wow_surf = game_font.render("HIGH SCORE! ", False, "Purple")
            wow_rect = wow_surf.get_rect(center = (300, 280))
            screen.blit(wow_surf, wow_rect)
        highscore_surf = game_font.render("HIGHSCORE:"+str(current_hs)+" SCORE:"+str(score), False, "Orange")
        highscore_rect = highscore_surf.get_rect(center=(400, 50))
        screen.blit(highscore_surf, highscore_rect)
        obstacle_rect_list.clear()
        lifes = 3
        start_time = pygame.time.get_ticks()
        file = open("highscore.txt", "w")
        file.write(str(current_hs))
        file.close()
        obstacle_score = 0

    
    # flip the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # Limits game loop to 60 FPS

pygame.quit()