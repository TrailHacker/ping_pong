# See PyCharm help at https://www.jetbrains.com/help/pycharm/
import time
import os, pygame, sys

# configure game
pygame.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'
pygame.display.set_caption("Bounce")
screenWidth = 400
screenHeight = 400
screen = pygame.display.set_mode([screenWidth, screenHeight], 0, 32)
background = pygame.Surface((screenWidth, screenHeight))

# define colors
cBackground = (255, 255, 255)
cBlock = (0, 0, 0)
background.fill(cBackground)
dx = 5
dy = 10


def main():
    X = screenWidth / 2
    Y = screenHeight / 2

    screen.blit(background, [0, 0])
    while True:
        check_for_event()

        time.sleep(0.05)
        draw_screen(X, Y)
        X += dx
        Y += dy
        check_bounds(X, Y)


def check_bounds(px, py):
    global dx, dy
    if px > screenWidth - 10 or px < 0:
        dx = -dx
    if py > screenHeight - 10 or py < 0:
        dy = -dy


def draw_screen(px, py):
    screen.blit(background, [0, 0])
    pygame.draw.rect(screen, cBlock, (px, py, 10, 10), 0)
    pygame.display.update()


def terminate():
    print("Closing down please wait")
    pygame.quit()
    sys.exit()


def check_for_event():
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        terminate()
    if event.type == pygame.K_ESCAPE:
        terminate()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
