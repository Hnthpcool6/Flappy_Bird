from asyncio.windows_utils import pipe
from hashlib import new
from re import S, T
from shutil import move
from turtle import down
import pygame, sys, random
# def
def create_pipe():
    pipe_height = random.randint(300,550)
    bottom_pipe = pipe_surface.get_rect(midtop = (432,pipe_height))
    top_pipe = pipe_surface.get_rect(midtop = (432,pipe_height-650))
    return bottom_pipe, top_pipe
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -=5    
    return pipes
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False, True)
            screen.blit(flip_pipe,pipe)
        

    return pipes
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe) or bird_rect.top <= -75 or bird_rect.bottom >= 650:
            hit_sound.play()
            return False
    return True
def bird_animation():
    new_bird = bird_list[bird_idx]
    new_bird_rect = new_bird.get_rect(center = (bird_rect.centerx, bird_rect.centery))  
    return new_bird, new_bird_rect          
def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score)), True, (255,255,255))
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game over':
        hight_score_surface = game_font.render('Hight Score: '+str(int(hight_score)), True, (255,255,255))
        hight_score_rect = hight_score_surface.get_rect(center = (216,610))
        screen.blit(hight_score_surface, hight_score_rect)
        score_surface = game_font.render('Score: '+str(int(score)), True, (255,255,255))
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface, score_rect)
def update_score(score, hight_score):
    if score >= hight_score:
        hight_score = score
    return hight_score
pygame.mixer.pre_init(frequency=44100, size = -16, channels = 2, buffer =512)
pygame.init()
screen = pygame.display.set_mode((432,768))
clock = pygame.time.Clock()
pygame.display.set_caption('Flappy Bird')
icon = pygame.image.load('images/icon.ico')
pygame.display.set_icon(icon)
# font
game_font = pygame.font.Font('04B_19.ttf',40)
score = 0
hight_score = 0
score_sound_countdown = 100
#  bg
bg= pygame.image.load('images/background-night.png').convert()
bg = pygame.transform.scale2x(bg)
#  floor
floor= pygame.image.load('images/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_pos_x = 0
#  bird
bird_down = pygame.transform.scale2x(pygame.image.load('images/yellowbird-downflap.png').convert())
bird_mid = pygame.transform.scale2x(pygame.image.load('images/yellowbird-midflap.png').convert())
bird_up = pygame.transform.scale2x(pygame.image.load('images/yellowbird-upflap.png').convert())
bird_list = [bird_down, bird_mid, bird_up]
bird_idx=0
bird = bird_list[bird_idx]
# bird= pygame.image.load('images/yellowbird-midflap.png').convert()
# bird = pygame.transform.scale2x(bird)

bird_rect = bird.get_rect(center = (100,384))
# atv
gravity = 0.25
bird_movement = random.randint(200,300)
bird_movementx = 100
# pipe
pipe_surface = pygame.image.load('images/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
#  timer
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe,1200)
bird_flap = pygame.USEREVENT + 1
pygame.time.set_timer(bird_flap,200)
# if else 
running = True
game_active = True
#  game over
game_over_surface = pygame.transform.scale2x(pygame.image.load('images/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (216,384))
# sound
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')



# while loop
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and game_active == False:
                
                bird_rect = bird.get_rect(center = (100,384))
                bird_movement = random.randint(200,300)
                bird_movementx = 100
                score = 0
                game_active = True
                pipe_list.clear()
        if event.type == pygame.KEYDOWN:
            # if event.key == pygame.K_SPACE:
            #     bird_movement -=10  
            flap_sound.play()                  
            if event.key == pygame.K_w:
                bird_movement -= 50
            
            if event.key == pygame.K_s:
                bird_movement += 50
            if event.key == pygame.K_a:
                bird_movementx -= 50
            
            if event.key == pygame.K_d:
                bird_movementx += 50
            

        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())
        if event.type == bird_flap:
            if bird_idx < 2:
                bird_idx += 1
            else:
                bird_idx = 0
            bird, bird_rect = bird_animation()


    screen.blit(bg,(0,0))
    if game_active:

        # pipe
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        # bird
        # bird_movement += gravity
        bird_rect.centery = bird_movement
        bird_rect.centerx = bird_movementx
        
        screen.blit(bird, bird_rect)

        game_active=check_collision(pipe_list) 
        score +=0.01
        score_display('main game')
        score_sound_countdown -= 1
        if score_sound_countdown < 0:
            score_sound.play()
            score_sound_countdown = 100

    else:
        screen.blit(game_over_surface, game_over_rect)
        hight_score = update_score(score, hight_score)
        score_display('game over')

    # floor
    floor_pos_x -=1
    if floor_pos_x == -50:
        floor_pos_x = 0
    screen.blit(floor,(floor_pos_x,650))
    

    pygame.display.update()
    clock.tick(60)
pygame.quit()
sys.exit()

