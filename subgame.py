
from pygame.constants import K_RCTRL
import pygame
import os
pygame.font.init()


width, height = 1000, 700
wid, hei = 55, 40

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("SpaceFighters")

white = (255, 255, 255)
black = (0, 0, 0,)
red_shoot = (255, 0, 0)
yellow_shoot = (255, 255, 0)

border = pygame.Rect(495, 0, 10, height)

fps = 60
velocity = 5
bullet_vel = 7
max_bullets = 5

yellow_hit = pygame.USEREVENT + 1
red_hit = pygame.USEREVENT + 2

health_font = pygame.font.SysFont('calibri', 40)
win_font = pygame.font.SysFont('cosmicsans', 100)

red_spaceship_image = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
red_spaceship = pygame.transform.rotate(
    pygame.transform.scale(red_spaceship_image, (wid, hei)), (90))
yellow_spaceship_image = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
yellow_spaceship = pygame.transform.rotate(
    pygame.transform.scale(yellow_spaceship_image, (wid, hei)), (270))
space = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), (width, height))


def window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    # win.fill(white)
    win.blit(space, (0, 0))
    pygame.draw.rect(win, black, border)
    red_health_text = health_font.render("HEALTH:" + str(red_health), 1, white)
    win.blit(red_health_text, (5, 10))
    yellow_health_text = health_font.render(
        "HEALTH:" + str(yellow_health), 1, white)
    win.blit(yellow_health_text, (820, 10))
    win.blit(red_spaceship, (red.x, red.y))
    win.blit(yellow_spaceship, (yellow.x, yellow.y))

    for bullet in red_bullets:
        pygame.draw.rect(win, red_shoot, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(win, yellow_shoot, bullet)
    pygame.display.update()


def spaceship_movement(red, yellow):
    key_press = pygame.key.get_pressed()
    if key_press[pygame.K_a] and red.x - velocity > 0:  # left
        red.x -= velocity
    if key_press[pygame.K_d] and red.x + velocity < 460:  # right
        red.x += velocity
    if key_press[pygame.K_w] and red.y - velocity > 0:  # up
        red.y -= velocity
    if key_press[pygame.K_s] and red.y + velocity < 640:  # down
        red.y += velocity
    if key_press[pygame.K_LEFT] and yellow.x - velocity > 500:  # left
        yellow.x -= velocity
    if key_press[pygame.K_RIGHT] and yellow.x + velocity < 960:  # right
        yellow.x += velocity
    if key_press[pygame.K_UP] and yellow.y - velocity > 0:  # up
        yellow.y -= velocity
    if key_press[pygame.K_DOWN] and yellow.y + velocity < 640:  # down
        yellow.y += velocity


def handle_bullets(red_bullets, yellow_bullets, red, yellow):
    for bullet in red_bullets:
        bullet.x += bullet_vel
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(yellow_hit))
            red_bullets.remove(bullet)
        elif bullet.x > 960:
            red_bullets.remove(bullet)

    for bullet in yellow_bullets:
        bullet.x -= bullet_vel
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(red_hit))
            yellow_bullets.remove(bullet)
        elif bullet.x < 10:
            yellow_bullets.remove(bullet)


def Win(winner):
    draw_winner = win_font.render(winner, 1, white)
    win.blit(draw_winner, (500 - draw_winner.get_width() /
             2, 350-draw_winner.get_height()/2))
    pygame.display.update()
    pygame.time.delay(2000)


def main():
    red = pygame.Rect(150, 300, wid, hei)
    yellow = pygame.Rect(800, 300, wid, hei)
    run = True
    red_bullets = []
    yellow_bullets = []
    red_health = 10
    yellow_health = 10
    clock = pygame.time.Clock()
    while(run):
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(red_bullets) < max_bullets:
                    red_bullet = pygame.Rect(
                        red.x + red.width, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(red_bullet)

                if event.key == pygame.K_RCTRL and len(yellow_bullets) < max_bullets:
                    yellow_bullet = pygame.Rect(
                        yellow.x, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(yellow_bullet)

            if event.type == yellow_hit:
                yellow_health -= 1

            if event.type == red_hit:
                red_health -= 1

        winner = ""
        if yellow_health <= 0:
            winner = "RED WINS!"
        if red_health <= 0:
            winner = "YELLOW WINS!"
        if winner != "":
            Win(winner)
            break

        spaceship_movement(red, yellow)
        handle_bullets(red_bullets, yellow_bullets, red, yellow)

        print(red_bullets, " ", yellow_bullets, end="")
        window(red, yellow, red_bullets, yellow_bullets,
               red_health, yellow_health)

    pygame.quit()


if __name__ == "__main__":
    main()
