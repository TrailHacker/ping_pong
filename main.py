# See PyCharm help at https://www.jetbrains.com/help/pycharm/
import time
import os, pygame, sys
import random

"""
Game - 
    
Shape - 
    Ball - Location {x, y}, Size { width, height } 
    Paddle[] - Location {x, y}, Size {width, height}
State - 
    Speed - (0, 1), # timeout (in seconds)
    Delta - { x, y } 
"""
# configure game
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
bounceSound = pygame.mixer.Sound("bounce.ogg")
os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'
pygame.display.set_caption("Ping Pong - 1 Player Mode")
screenWidth = 500
screenHeight = 300
screen = pygame.display.set_mode([screenWidth, screenHeight], 0, 32)
background = pygame.Surface((screenWidth, screenHeight))
textSize = 36
scoreSurface = pygame.Surface((textSize, textSize))
font = pygame.font.Font(None, textSize)
pygame.event.set_allowed(None)
pygame.event.set_allowed([pygame.KEYDOWN, pygame.QUIT])

# setup game
background_color = (255, 255, 255)
background.fill(background_color)
ball_color = (0, 0, 0)
delta_choice = [[15, 1], [14, 1], [13, 1], [12, 1], [11, 1], [10, 1], [15, 2], [14, 2], [13, 2], [12, 2], [11, 2],
                [10, 2]]
max_delta = 11
text_color = (0, 0, 0)

box = [screenWidth - 10, screenHeight - 10]
delta = delta_choice[random.randint(0, max_delta)]
hw = screenWidth / 2
hh = screenHeight / 2
ball_position = [-hw, hh]
bat_margin = 30  # how far in from wall is the bat
bat_height = 48
bat_thick = 6
bat_increment = 20  # bat / key movement
bat_x = [bat_margin, screenWidth - bat_margin]
bat_y = [hh, hh]
limit = [0, 0, 0, 0, 0, 0]  # wall limits and bat limits
ball_radius = 8
rally = True
pause = True
score = 0
best = 0  # high score
balls = 3  # number of balls in a turn
balls_left = balls


def main():
    global ball_position, rally, balls, pause, score, best
    update_box(0, 0)  # setup wall limits
    update_score()
    screen.blit(background, [0, 0])
    while True:
        balls_left = balls
        if score > best:
            best = score
        score = 0
        update_score()
        while balls_left > 0:
            ball_position = wait_for_serve(ball_position)
            while rally:
                check_for_event()
                draw_screen(ball_position)
                ball_position = move_ball(ball_position)
            balls_left -= 1
        print("press space for", balls, "more balls")
        pause = True
        while pause:
            check_for_event()


def wait_for_serve(p):
    global bat_y, rally, delta
    computer_bat_delta = 2
    serve_time = time.time() + 2.0  # auto serve!
    while time.time() < serve_time:
        check_for_event()
        draw_screen(ball_position)
        bat_y[0] += computer_bat_delta

        # move bat up and down while waiting
        if bat_y[0] > limit[3] or bat_y[0] < limit[2]:
            computer_bat_delta = -computer_bat_delta

    p[0] = bat_x[0]
    p[1] = bat_y[0]
    delta = delta_choice[random.randint(0, max_delta)]
    rally = True
    return p


def move_ball(p):
    global delta, bat_y, rally, score, bat_thick

    # move ball
    p[0] += delta[0]
    p[1] += delta[1]

    # test top
    if p[1] <= limit[2]:
        bounceSound.play()
        delta[1] = -delta[1]  # move down
        p[1] = limit[2]  # position ball

    # test bottom
    elif p[1] >= limit[3]:
        bounceSound.play()
        delta[1] = -delta[1]  # move left
        p[1] = limit[3]  # move ball

    # player 1 miss?
    elif p[0] <= limit[0]:
        p[0] = limit[0]
        rally = False
        print("missed ball")

    # player 2 miss?
    elif p[0] >= limit[1]:
        p[0] = limit[1]
        rally = False
        print("missed ball")

    # test left bat collision
    elif is_bat_hit(p, 0): #
        bounceSound.play()
        p[0] = limit[4]
        delta[0] = random.randint(5, 15)
        if random.randint(1, 4) > 2:
            # random change in y direction
            delta[1] = 16 - delta[0]
        else:
            delta[1] = -(16 - delta[0])

    # test right bat collision
    # is_right_bat_hit(ball, bat_index)
    elif is_bat_hit(p, 1):
        bounceSound.play()
        delta[0] = -delta[0]
        p[0] = limit[5]
        score += 1
        update_score()

    bat_y[0] = p[1] - ball_radius  # make auto opponent follow bat
    # bat_y[1] = p[1] + ball_radius  # temporary test for auto player
    return p

def is_bat_hit(p, bat_index):
    if bat_index == 0:  # left bat
        if p[0] <= limit[4]: # is ball to the left of bat's right side?
            if p[1] >= bat_y[bat_index] - ball_radius: # is bat below the top of the bat?
                if p[1] <= bat_y[bat_index] + ball_radius + bat_height:
                    return True

    elif bat_index == 1:  # right bat
        # is ball to the right of the bat
        if p[0] >= limit[5]:
            # is ball below top of bat
            if p[1] >= bat_y[bat_index] - ball_radius:
                # is ball above bottom of bat
                if p[1] <= bat_y[bat_index] + ball_radius + bat_height:
                    return True
    return False

def update_score():
    global score, best, score_rect, scoreSurface
    scoreSurface = font.render(str(best) + " : " + str(score), True, text_color, background_color)
    score_rect = scoreSurface.get_rect()
    score_rect.centerx = hw
    score_rect.centery = 24


def draw_screen(p):
    global rally
    time.sleep(0.05)
    screen.blit(background, [0, 0])

    # game board
    pygame.draw.rect(screen, (255, 0, 0),
                     (hw - (box[0] / 2), hh - (box[1] / 2), box[0], box[1]),
                     4)
    # left bat
    pygame.draw.line(screen, (0, 255, 0),
                     (bat_x[0], bat_y[0]), (bat_x[0], bat_y[0] + bat_height), bat_thick)

    # right bat
    pygame.draw.line(screen, (0, 255, 0),
                     (bat_x[1], bat_y[1]), (bat_x[1], bat_y[1] + bat_height), bat_thick)

    # update score display
    screen.blit(scoreSurface, score_rect)

    # only draw ball if we are in a rally
    if rally:
        pygame.draw.circle(screen, ball_color, (p[0], p[1]), ball_radius, 2)

    pygame.display.update()


def update_box(d, amount):
    global box, limit
    box[d] += amount
    limit[0] = hw - (box[0] / 2) + ball_radius  # left limit
    limit[1] = hw + (box[0] / 2) - ball_radius  # right limit
    limit[2] = hh - (box[1] / 2) + ball_radius  # top limit
    limit[3] = hh + (box[1] / 2) - ball_radius  # bottom limit
    limit[4] = bat_x[0] + ball_radius + bat_thick / 2  # x limit ball from right
    limit[5] = bat_x[1] - ball_radius - bat_thick / 2  # x limit ball from left


def terminate():
    print("Closing down please wait")
    pygame.quit()
    sys.exit()


def check_for_event():
    global bat_y, rally, pause
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        terminate()

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            terminate()

        # expand / contract ball
        if event.key == pygame.K_DOWN:
            update_box(1, -2)

        if event.key == pygame.K_UP:
            update_box(1, 2)

        if event.key == pygame.K_LEFT:
            update_box(0, -2)

        if event.key == pygame.K_RIGHT:
            update_box(0, 2)

        if event.key == pygame.K_s:
            rally = True

        if event.key == pygame.K_SPACE:
            pause = False

        if event.key == pygame.K_PAGEDOWN:
            if bat_y[1] < screenHeight - bat_increment:
                bat_y[1] += bat_increment

        if event.key == pygame.K_PAGEUP:
            if bat_y[1] > bat_increment:
                bat_y[1] -= bat_increment


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
