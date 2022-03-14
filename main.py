import pygame

import random

WIDTH, HEIGHT = 800, 400

PAD_H = 90
PAD_W = 15

BALL_RAD = 10

BALL_VEL = 6
PAD_VEL = 6
COR_P = random.uniform(1.02, 1.06)
COR_O = random.uniform(0.9, 1.05)


class paddle:
    def __init__(self, x, y, width, height):
        self.rec = pygame.Rect(x, y, width, height)


class ball:
    def __init__(self, x, y, width, height):
        self.rec = pygame.Rect(x, y, width, height)


FPS = 60

pygame.init()
pygame.font.init()
pygame.mixer.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PONG")

FONT1 = pygame.font.SysFont("OCR A Extended", 50)

BG = pygame.transform.scale(pygame.image.load("background.jpg"), (WIDTH, HEIGHT))
sound = pygame.mixer.Sound("impact.mp3")


def draw(p1, p2, pong, p1_p, p2_p):
    WIN.fill((0, 0, 0))
    WIN.blit(BG, (0, 0))
    t1 = FONT1.render(str(p1_p), 1, (255, 255, 255))
    t2 = FONT1.render(str(p2_p), 1, (255, 255, 255))
    WIN.blit(t1, ((((WIDTH) / 2) - t1.get_width()) - 10, 20))
    WIN.blit(t2, ((((WIDTH) / 2) + t2.get_width()) + 7, 20))

    pygame.draw.rect(WIN, (255, 255, 255), p1.rec)
    pygame.draw.rect(WIN, (255, 255, 255), p2.rec)
    pygame.draw.circle(WIN, (255, 255, 255), (pong.rec.x, pong.rec.y), BALL_RAD)


def player_movement(p1, p2, KP):
    if KP[pygame.K_UP] and p1.rec.y > 0:
        p1.rec.y -= PAD_VEL
    if KP[pygame.K_DOWN] and p1.rec.y + PAD_H < HEIGHT:
        p1.rec.y += PAD_VEL
    if KP[pygame.K_w] and p2.rec.y > 0:
        p2.rec.y -= PAD_VEL
    if KP[pygame.K_s] and p2.rec.y + PAD_H < HEIGHT:
        p2.rec.y += PAD_VEL


def start(bxvel, byvel, pong):
    bxvel = byvel = random.choice((-1, 1)) * BALL_VEL
    pong.rec.x, pong.rec.y = (
        (WIDTH / 2) - BALL_RAD,
        (HEIGHT / 2) - BALL_RAD,
    )
    return False, bxvel, byvel


def ball_movement(pong, bxvel, byvel, p1_p, p2_p):
    if pong.rec.x >= 0 and pong.rec.x + (2 * BALL_RAD) <= WIDTH:
        if pong.rec.y <= 0 or pong.rec.y + (2 * BALL_RAD) >= HEIGHT:
            byvel = (-1) * byvel * COR_O
        pong.rec.x += bxvel
        pong.rec.y += byvel
        state = False
    else:
        if pong.rec.x < 0:
            p2_p += 1
        else:
            p1_p += 1
        state = True
    return bxvel, byvel, state, p1_p, p2_p


def collision(pong, p1, p2, bxvel):
    if pong.rec.colliderect(p1.rec) or pong.rec.colliderect(p2.rec):
        sound.play()
        bxvel = (-1) * bxvel * COR_P

    return bxvel


def main():

    run = True
    clock = pygame.time.Clock()
    p2 = paddle(0, (HEIGHT - PAD_H) / 2, PAD_W, PAD_H)
    p1 = paddle((WIDTH - PAD_W), (HEIGHT - PAD_H) / 2, PAD_W, PAD_H)
    pong = ball(
        (WIDTH / 2) - BALL_RAD, (HEIGHT / 2) - BALL_RAD, 2 * BALL_RAD, 2 * BALL_RAD
    )
    state = True
    bxvel = 0
    byvel = 0
    p1_p = 0
    p2_p = 0
    pygame.mixer.music.load("background.mp3")
    pygame.mixer.music.play(-1, 0, 0)

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        KP = pygame.key.get_pressed()

        if state:
            state, bxvel, byvel = start(bxvel, byvel, pong)

        player_movement(p1, p2, KP)
        bxvel = collision(pong, p1, p2, bxvel)
        bxvel, byvel, state, p1_p, p2_p = ball_movement(pong, bxvel, byvel, p1_p, p2_p)
        draw(p1, p2, pong, p1_p, p2_p)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
