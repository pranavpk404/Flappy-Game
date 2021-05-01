import random  # For generating random numbers
import sys  # We will use sys.exit to exit the program
import pygame
from pygame.locals import *  # Basic pygame imports

# Global Variables for the game
FPS = 32
SCR_WIDTH = 289
SCR_HEIGHT = 511
DISPLAY_SCREEN_WINDOW = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
PLAY_GROUND = SCR_HEIGHT * 0.8
GAME_IMAGE = {}
GAME_AUDIO = {}
PLAYER = 'images/bird.png'
BG_IMAGE = 'images/background.png'
PIPE_IMAGE = 'images/pipe.png'


def welcome_main_screen():
    p_x = int(SCR_WIDTH / 5)
    p_y = int((SCR_HEIGHT - GAME_IMAGE['PLAYER'].get_height()) / 2)
    msgx = int((SCR_WIDTH - GAME_IMAGE['message'].get_width()) / 2)
    msgy = int(SCR_HEIGHT * 0.13)
    b_x = 0
    while True:
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # If the user presses space or up key, start the game for them
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                DISPLAY_SCREEN_WINDOW.blit(GAME_IMAGE['background'], (0, 0))
                DISPLAY_SCREEN_WINDOW.blit(GAME_IMAGE['PLAYER'], (p_x, p_y))
                DISPLAY_SCREEN_WINDOW.blit(GAME_IMAGE['message'], (msgx, msgy))
                DISPLAY_SCREEN_WINDOW.blit(GAME_IMAGE['base'], (b_x, PLAY_GROUND))
                pygame.display.update()
                time_clock.tick(FPS)


def main_gameplay():
    score = 0
    p_x = int(SCR_WIDTH / 5)
    p_y = int(SCR_WIDTH / 2)
    b_x = 0

    n_pip1 = get_Random_Pipes()
    n_pip2 = get_Random_Pipes()

    up_pips = [
        {'x': SCR_WIDTH + 200, 'y': n_pip1[0]['y']},
        {'x': SCR_WIDTH + 200 + (SCR_WIDTH / 2), 'y': n_pip2[0]['y']},
    ]

    low_pips = [
        {'x': SCR_WIDTH + 200, 'y': n_pip1[1]['y']},
        {'x': SCR_WIDTH + 200 + (SCR_WIDTH / 2), 'y': n_pip2[1]['y']},
    ]

    pip_Vx = -4

    p_vx = -9
    p_mvx = 10

    p_accuracy = 1

    p_flap_accuracy = -8
    p_flap = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if p_y > 0:
                    p_vx = p_flap_accuracy
                    p_flap = True
                    GAME_AUDIO['wing'].play()

        cr_tst = is_Colliding(p_x, p_y, up_pips,
                              low_pips)
        if cr_tst:
            return

        p_middle_positions = p_x + GAME_IMAGE['PLAYER'].get_width() / 2
        for pipe in up_pips:
            pip_middle_positions = pipe['x'] + GAME_IMAGE['pipe'][0].get_width() / 2
            if pip_middle_positions <= p_middle_positions < pip_middle_positions + 4:
                score += 1
                print(f"Your score is {score}")
                GAME_AUDIO['point'].play()

        if p_vx < p_mvx and not p_flap:
            p_vx += p_accuracy

        if p_flap:
            p_flap = False
        p_height = GAME_IMAGE['PLAYER'].get_height()
        p_y = p_y + min(p_vx, PLAY_GROUND - p_y - p_height)

        for pip_upper, pip_lower in zip(up_pips, low_pips):
            pip_upper['x'] += pip_Vx
            pip_lower['x'] += pip_Vx

        if 0 < up_pips[0]['x'] < 5:
            new_pip = get_Random_Pipes()
            up_pips.append(new_pip[0])
            low_pips.append(new_pip[1])

        if up_pips[0]['x'] < -GAME_IMAGE['pipe'][0].get_width():
            up_pips.pop(0)
            low_pips.pop(0)

        DISPLAY_SCREEN_WINDOW.blit(GAME_IMAGE['background'], (0, 0))
        for pip_upper, pip_lower in zip(up_pips, low_pips):
            DISPLAY_SCREEN_WINDOW.blit(GAME_IMAGE['pipe'][0], (pip_upper['x'], pip_upper['y']))
            DISPLAY_SCREEN_WINDOW.blit(GAME_IMAGE['pipe'][1], (pip_lower['x'], pip_lower['y']))

        DISPLAY_SCREEN_WINDOW.blit(GAME_IMAGE['base'], (b_x, PLAY_GROUND))
        DISPLAY_SCREEN_WINDOW.blit(GAME_IMAGE['PLAYER'], (p_x, p_y))
        d = [int(x) for x in list(str(score))]
        w = 0
        for digit in d:
            w += GAME_IMAGE['numbers'][digit].get_width()
        Xoffset = (SCR_WIDTH - w) / 2

        for digit in d:
            DISPLAY_SCREEN_WINDOW.blit(GAME_IMAGE['numbers'][digit], (Xoffset, SCR_HEIGHT * 0.12))
            Xoffset += GAME_IMAGE['numbers'][digit].get_width()
        pygame.display.update()
        time_clock.tick(FPS)


def is_Colliding(p_x, p_y, up_pipes, low_pipes):
    if p_y > PLAY_GROUND - 25 or p_y < 0:
        GAME_AUDIO['hit'].play()
        return True

    for pipe in up_pipes:
        pip_h = GAME_IMAGE['pipe'][0].get_height()
        if p_y < pip_h + pipe['y'] and abs(p_x - pipe['x']) < GAME_IMAGE['pipe'][0].get_width():
            GAME_AUDIO['hit'].play()
            return True

    for pipe in low_pipes:
        if (p_y + GAME_IMAGE['PLAYER'].get_height() > pipe['y']) and abs(p_x - pipe['x']) < \
                GAME_IMAGE['pipe'][0].get_width():
            GAME_AUDIO['hit'].play()
            return True

    return False


def get_Random_Pipes():
    """
    Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    """
    pip_h = GAME_IMAGE['pipe'][0].get_height()
    off_s = SCR_HEIGHT / 3
    yes2 = off_s + random.randrange(0, int(SCR_HEIGHT - GAME_IMAGE['base'].get_height() - 1.2 * off_s))
    pipeX = SCR_WIDTH + 10
    y1 = pip_h - yes2 + off_s
    pipe = [
        {'x': pipeX, 'y': -y1},  # upper Pipe
        {'x': pipeX, 'y': yes2}  # lower Pipe
    ]
    return pipe


if __name__ == "__main__":

    pygame.init()
    time_clock = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird Game')
    GAME_IMAGE['numbers'] = (
        pygame.image.load('images/0.png').convert_alpha(),
        pygame.image.load('images/1.png').convert_alpha(),
        pygame.image.load('images/2.png').convert_alpha(),
        pygame.image.load('images/3.png').convert_alpha(),
        pygame.image.load('images/4.png').convert_alpha(),
        pygame.image.load('images/5.png').convert_alpha(),
        pygame.image.load('images/6.png').convert_alpha(),
        pygame.image.load('images/7.png').convert_alpha(),
        pygame.image.load('images/8.png').convert_alpha(),
        pygame.image.load('images/9.png').convert_alpha(),
    )

    GAME_IMAGE['message'] = pygame.image.load('images/message.png').convert_alpha()
    GAME_IMAGE['base'] = pygame.image.load('images/base.png').convert_alpha()
    GAME_IMAGE['pipe'] = (pygame.transform.rotate(pygame.image.load(PIPE_IMAGE).convert_alpha(), 180),
                          pygame.image.load(PIPE_IMAGE).convert_alpha()
                          )

    # Game sounds
    GAME_AUDIO['die'] = pygame.mixer.Sound('sounds/die.wav')
    GAME_AUDIO['hit'] = pygame.mixer.Sound('sounds/hit.wav')
    GAME_AUDIO['point'] = pygame.mixer.Sound('sounds/point.wav')
    GAME_AUDIO['swoosh'] = pygame.mixer.Sound('sounds/swoosh.wav')
    GAME_AUDIO['wing'] = pygame.mixer.Sound('sounds/wing.wav')

    GAME_IMAGE['background'] = pygame.image.load(BG_IMAGE).convert()
    GAME_IMAGE['PLAYER'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcome_main_screen()  # Shows welcome screen to the user until he presses a button
        main_gameplay()  # This is the main game function
