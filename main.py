# See PyCharm help at https://www.jetbrains.com/help/pycharm/
import time
import os, pygame, sys

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
pygame.display.set_caption("Bounce2")
screenWidth = 400
screenHeight = 400
screen = pygame.display.set_mode([screenWidth, screenHeight], 0, 32)
background = pygame.Surface((screenWidth, screenHeight))

# define colors
cBackground = (255, 255, 255)
cBlock = (0, 0, 0)
background.fill(cBackground)

# define areas
box = [screenWidth - 80, screenHeight - 80]
delta = [5, 10]
hw = screenWidth / 2
hh = screenHeight / 2
position = [hw, hh]
limit = [0, 0, 0, 0]
ballRadius = 8


def main():
    global position
    update_box(0, 0)  # setup wall limits
    screen.blit(background, [0, 0])
    while True:
        check_for_event()
        time.sleep(0.05)
        draw_screen(position)
        position = move_ball(position)


def move_ball(p):
    global delta

    # move ball
    p[0] += delta[0]
    p[1] += delta[1]

    # left wall hit?
    if p[0] <= limit[0]:
        bounceSound.play()
        delta[0] = -delta[0]  # move right
        p[0] = limit[0]  # move ball

    # right wall hit?
    if p[0] >= limit[1]:
        bounceSound.play()
        delta[0] = -delta[0]  # move left
        p[0] = limit[1]  # move ball

    # top wall hit?
    if p[1] <= limit[2]:
        bounceSound.play()
        delta[1] = -delta[1]  # move down
        p[1] = limit[2]  # move ball

    # bottom wall hit?
    if p[1] >= limit[3]:
        bounceSound.play()
        delta[1] = -delta[1]  # move up
        p[1] = limit[3]  # move ball

    # position updated
    return p


def draw_screen(p):
    screen.blit(background, [0, 0])

    pygame.draw.rect(screen, (255, 0, 0),
                     (hw - (box[0] / 2), hh - (box[1] / 2), box[0], box[1]),
                     2)
    pygame.draw.circle(screen, cBlock, (p[0], p[1]), ballRadius, 2)
    pygame.display.update()


def update_box(d, amount):
    global box, limit
    box[d] += amount
    limit[0] = hw - (box[0] / 2) + ballRadius  # left limit
    limit[1] = hw + (box[0] / 2) - ballRadius  # right limit
    limit[2] = hh - (box[1] / 2) + ballRadius  # top limit
    limit[3] = hh + (box[1] / 2) - ballRadius  # bottom limit


def terminate():
    print("Closing down please wait")
    pygame.quit()
    sys.exit()


def check_for_event():
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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
