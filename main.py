import random
import sys, os
import pygame
from pygame.locals import *

pygame.init()

FPS = 32
SCREENWIDTH = 500 
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT 
GAME_SPRITES = {}
GAME_SOUNDS = {}


font_score = pygame.font.SysFont('kristenitc,consolas', 25, bold=False)
font_text = pygame.font.SysFont('kristenitc,consolas', 40, bold=False)
font_result = pygame.font.SysFont('kristenitc,consolas', 30, bold=False)

def resource_path(relative_path):
    # for PyInstaller
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# data    

player = 'images/bird.png'
background = 'images/bg.jpg'
pipe = 'images/pipe.png'
upper_pipe = 'images/rotated_pipe.png'

try:
    with open('best_score.txt', 'r') as file:
        best_score = int(file.read())
except OSError:
    best_score = 0

def finalexit():
    with open('best_score.txt', 'w') as file:
        file.write(str(best_score))
    pygame.quit()
    sys.exit()

def welcomeScreen():

    playerx = int(SCREENWIDTH / 5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height()) / 2)
    score = 0
    

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                finalexit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))

                start_game = font_text.render("Start Game", True, (255, 0, 0))
                SCREEN.blit(start_game, (SCREENWIDTH / 4, (SCREENHEIGHT)/5))
                
                start_text = font_text.render("Press Space to Start", True, (255, 0, 0))
                SCREEN.blit(start_text, (50, (3*SCREENHEIGHT)/4))

                score_text = font_score.render("Score: " f'{score}' , True, (255, 0, 0))
                SCREEN.blit(score_text, (10, 5))

                time_now = 0
                time_rendered = font_score.render("Time: " + str(time_now), True, (255, 0, 0))
                SCREEN.blit(time_rendered, (10, 35))

                pygame.display.update()
                FPSCLOCK.tick(FPS)


def mainGame():
    
    score = 0
    global best_score
    start_time = pygame.time.get_ticks()
    playerx = int(SCREENWIDTH / 6)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height()) / 2)

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperPipes = [
        {'x': SCREENWIDTH+110, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH+140+(SCREENWIDTH/2), 'y': newPipe2[0]['y']}
    ]

    lowerPipes = [
        {'x': SCREENWIDTH+110, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH+140+(SCREENWIDTH/2), 'y': newPipe2[1]['y']}
    ]

    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccy = 1

    playerFlapAccv = -8
    playerFlapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                finalexit()
                
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True    


        playerMidPos = playerx + GAME_SPRITES['player'].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                best_score = max(best_score, score)
                print(f"Your score is {score}")
                GAME_SOUNDS['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccy

        if playerFlapped:
            playerFlapped = False

        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)


        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX


        if 0 < upperPipes[0]['x'] < 5  :
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        
        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
            
        if crashTest:
            score_text = font_result.render("Score: " f'{score}' , True, (255, 0, 0))
            SCREEN.blit(score_text, (SCREENWIDTH/4 + 30, (SCREENHEIGHT)/4 + 10))

            time_now = (pygame.time.get_ticks() - start_time) // 1000
            time_rendered = font_result.render("Time: " + str(time_now), True, (255, 0, 0))
            SCREEN.blit(time_rendered, (SCREENWIDTH/4 + 30, (SCREENHEIGHT)/3 + 15)) 

            best_score_text = font_result.render("Best Score: " f'{best_score}' , True, (255, 0, 0))
            SCREEN.blit(best_score_text, (SCREENWIDTH/4 + 30, (SCREENHEIGHT)/3 + 70))

            return
        else:
            score_text = font_score.render("Score: " f'{score}' , True, (255, 0, 0))
            SCREEN.blit(score_text, (10, 5))

            time_now = (pygame.time.get_ticks() - start_time) // 1000
            time_rendered = font_score.render("Time: " + str(time_now), True, (255, 0, 0))
            SCREEN.blit(time_rendered, (10, 35)) 
    
        
        pygame.display.update()
        FPSCLOCK.tick(FPS) 
                                                


def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery <= 0 or playery > GROUNDY - 85:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] - 15 and abs(playerx - pipe['x'] - 10) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() -13 > pipe['y']) and abs(playerx - pipe['x'] - 10) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False

def getRandomPipe():

    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT / 3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - 1.2 * offset))
    pipeX = SCREENWIDTH  
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1},
        {'x': pipeX, 'y': y2}
    ]
    return pipe


def exitgame():

    while True:

        gameover_text = font_text.render("Game over!", True, (255, 0, 0))
        SCREEN.blit(gameover_text, (140, SCREENHEIGHT/10))

        start_text = font_text.render("Press Space to Start", True, (255, 0, 0))
        SCREEN.blit(start_text, (50, (2*SCREENHEIGHT)/3))

        escape_text = font_score.render("Escape - Quit", True, (255, 0, 0))
        SCREEN.blit(escape_text, (160, SCREENHEIGHT - 90))

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                finalexit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return

        pygame.display.update()
        FPSCLOCK.tick(FPS)  
    

if __name__ == "__main__":
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird Game')
    
    GAME_SPRITES['pipe'] = ( pygame.image.load(resource_path(upper_pipe)).convert_alpha() , pygame.image.load(resource_path(pipe)).convert_alpha())


    GAME_SOUNDS['hit'] = pygame.mixer.Sound(resource_path('sounds/sfx_hit.wav'))
    GAME_SOUNDS['point'] = pygame.mixer.Sound(resource_path('sounds/sfx_point.wav'))

    GAME_SPRITES['background'] = pygame.image.load(resource_path(background)).convert()
    GAME_SPRITES['player'] = pygame.image.load(resource_path(player)).convert_alpha()

    while True:
        welcomeScreen()
        mainGame()
        exitgame()
