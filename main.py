import pygame
from random import randint
start_time = 0
lifes = 3
obstacle_score = 0
music_number = 0

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
shape_surf = pygame.image.load("graphics/level/shapeland.png")
where_surf = pygame.image.load("graphics/level/warehouse.png")
sunset_surf = pygame.image.load("graphics/level/sunset.png")
sky = [sky_surf, where_surf, sunset_surf]
sky_mode = 0
game_font = pygame.font.Font("font/ugly.ttf", 30)

bakery_music = pygame.mixer.Sound("audio/french.mp3")
unicorn_music = pygame.mixer.Sound("audio/fairy.mp3")
intergalactic_music = pygame.mixer.Sound("audio/space.mp3")
magic_sf = pygame.mixer.Sound("audio/unicorn.mp3")
whisk_sf = pygame.mixer.Sound("audio/whisk.mp3")
lifelost_sf = pygame.mixer.Sound("audio/fail.mp3")
rock_music = pygame.mixer.Sound("audio/cool.mp3")
fantasy_music = pygame.mixer.Sound("audio/epic.mp3")
cat_music = pygame.mixer.Sound("audio/fatcat.mp3")
groovy_music = pygame.mixer.Sound("audio/groovy.mp3")
fresh_music = pygame.mixer.Sound("audio/guitar.mp3")
kahoot_music = pygame.mixer.Sound("audio/kahoot.mp3")
music_list = [bakery_music, unicorn_music, intergalactic_music, rock_music, fantasy_music, groovy_music, fresh_music, kahoot_music]

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
obstacle_time = 1200
pygame.time.set_timer(obstacle_timer, obstacle_time)

magic_timer = pygame.USEREVENT + 2
spawn_time = 6000
combo = 0
pygame.time.set_timer(magic_timer, spawn_time)

horse_timer = pygame.USEREVENT + 3
pygame.time.set_timer(horse_timer, 100)

music_timer = pygame.USEREVENT + 4
pygame.time.set_timer(music_timer, 50000)

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
    score_surf = game_font.render("SCORE:"+str(score)+" LIVES:"+str(lifes)+" COMBO:"+str(combo), False, "Blue")
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)

def choose_music():
    global music_number
    music_number = randint(0,7)
    music_list[music_number].play(loops = -1)


def collisions(player, obstacles):
    for obstacle_rect in obstacles:
        if obstacle_rect.colliderect(player):
            lifelost_sf.play()
            global lifes, horse_normal
            lifes -= 1
            if lifes > 4:
                lifes = 5
            horse_normal = True
            obstacles.remove(obstacle_rect)
            if lifes <= 0:
                return False
    return True

def player_animation():
    global player_surf, horse_number, lifes, spawn_time, combo

    if horse_normal == True:
        spawn_time = 6000
        combo = 0
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
                choose_music()
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
                    obstacle_rect_list.append(egg_surf.get_rect(bottomleft=(randint(8,10)*100, 190)))
                if egg_type == 2:
                    obstacle_rect_list.append(spoon_surf.get_rect(bottomleft=(randint(8,10)*100, 300)))
                if egg_type == 3:
                    obstacle_rect_list.append(whisk_surf.get_rect(bottomleft=(randint(8,10)*100, 290)))
                    whisk_sf.play()
            
            if event.type == magic_timer:
                magic_rect_list.append(magic_surf.get_rect(bottomleft = (randint(8,10)*100, 312)))
            
            if event.type == music_timer:
                pygame.mixer.pause()
                choose_music()
        
        else:
            screen.blit(start_surf, (0, 0))
            # When player wants to play again by pressing SPACE
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                choose_music()
                is_playing = True
       
    if menu:
        screen.blit(start_surf, (0,0))

    elif is_playing:
        screen.fill("purple")  # Wipe the screen

        score_display()

        if score > 50 and score < 100 and horse_normal == False:
            sky_mode = 2
        elif horse_normal == True and score < 30:
            sky_mode = 0
        elif score > 30 and score < 50 and horse_normal == False:
            sky_mode = 1
        elif score > 50 and horse_normal == False:
            sky_mode = 0

        sky[sky_mode].scroll(randint(-4, 0), randint(-1, 1), pygame.SCROLL_REPEAT)
        ground_surf.scroll(int(-5-(combo*3)), 0, pygame.SCROLL_REPEAT)

        # Blit the level assets
        screen.blit(sky[sky_mode], (0, 0))
        screen.blit(ground_surf, (0, GROUND_Y))

        score_display()
        obstacle_time -= score*10


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
                    obstacle_rect.x -= int(15+combo*2+score/5)
                elif obstacle_rect.bottom == 190:
                    #egg_surf = pygame.transform.rotate(egg_surf, 15)
                    screen.blit(egg_surf,obstacle_rect)
                    obstacle_rect.x -= int(23+combo*2+score/5)
                elif obstacle_rect.bottom == 300:
                    #spoon_surf = pygame.transform.rotate(spoon_surf, 10)
                    screen.blit(spoon_surf, obstacle_rect)
                    obstacle_rect.x -= int(7+combo*2+score/5)
                else:
                    #whisk_surf = pygame.transform.rotate(whisk_surf, randint(-1, 5)*5)
                    screen.blit(whisk_surf, obstacle_rect)
                    obstacle_rect.x -= int(randint(-1, 6)*4+combo*2+score/int(randint(1,4)))
            obstacle_rect_list = [obstacle for obstacle in obstacle_rect_list if obstacle.x > -100]
        else:
            obstacle_rect_list = []
        obstacle_score += len(obstacle_rect_list)

        
        

        if magic_rect_list:
            for magic_rect in magic_rect_list:
                screen.blit(magic_surf, magic_rect)
                magic_rect.x -= 10
                magic_rect_list = [magic for magic in magic_rect_list if magic.x > -100]
        else: magic_rect_list = []

        # When player collides with enemy, game ends
        is_playing = collisions(player_rect, obstacle_rect_list)
        

        for magic_rect in magic_rect_list:
            if player_rect.colliderect(magic_rect):
                magic_sf.play()
                horse_normal = False
                spawn_time -= 999
                if spawn_time < 200:
                    spawn_time = 0
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
        obstacle_time = 1200
        start_time = pygame.time.get_ticks()
        pygame.mixer.pause()
        file = open("highscore.txt", "w")
        file.write(str(current_hs))
        file.close()
        obstacle_score = 0

    
    # flip the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # Limits game loop to 60 FPS

pygame.quit()