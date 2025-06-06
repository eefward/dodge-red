import pygame
import sys
import random
import math

pygame.init()
pygame.display.set_caption("dodge red")

# init
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# variables
redRadius = 20
blueRadius = 15
blueSpeed = 2
blueCircles = []

def spawnBlue():
    x = random.randint(blueRadius, WIDTH - blueRadius)
    y = random.randint(blueRadius, HEIGHT - blueRadius)
    angle = random.uniform(0, 2 * math.pi)
    vx = blueSpeed * math.cos(angle)
    vy = blueSpeed * math.sin(angle)
    return {'pos': [x, y], 'vel': [vx, vy]}

def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def collideCircles(a, b):
    dx = b['pos'][0] - a['pos'][0]
    dy = b['pos'][1] - a['pos'][1]
    dist = math.hypot(dx, dy)
    if dist == 0 or dist > 2 * blueRadius:
        return  

    nx = dx / dist
    ny = dy / dist

    dvx = b['vel'][0] - a['vel'][0]
    dvy = b['vel'][1] - a['vel'][1]

    dot = dvx * nx + dvy * ny
    if dot > 0:
        return  

    a['vel'][0] += dot * nx
    a['vel'][1] += dot * ny
    b['vel'][0] -= dot * nx
    b['vel'][1] -= dot * ny

    overlap = 2 * blueRadius - dist
    a['pos'][0] -= nx * overlap / 2
    a['pos'][1] -= ny * overlap / 2
    b['pos'][0] += nx * overlap / 2
    b['pos'][1] += ny * overlap / 2

def resetGame():
    global blueCircles, ticks
    blueCircles = [spawnBlue()]
    ticks = pygame.time.get_ticks()

# game loop

resetGame()
while True:
    screen.fill((255, 255, 255))
    seconds = (pygame.time.get_ticks() - ticks) // 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    redPos = list(pygame.mouse.get_pos())

    if len(blueCircles) < 1 + (seconds // 3): # ball spawn time
        blueCircles.append(spawnBlue())

    for i in range(len(blueCircles)):
        for j in range(i + 1, len(blueCircles)):
            collideCircles(blueCircles[i], blueCircles[j])

    for blue in blueCircles:
        bx, by = blue['pos']
        vx, vy = blue['vel']

        dx = redPos[0] - bx
        dy = redPos[1] - by
        dist = math.hypot(dx, dy)
        if dist != 0:
            vx += 0.05 * dx / dist
            vy += 0.05 * dy / dist

        speed = math.hypot(vx, vy)
        max_speed = blueSpeed * 2
        if speed > max_speed:
            vx = (vx / speed) * max_speed
            vy = (vy / speed) * max_speed

        bx += vx
        by += vy

        if bx <= blueRadius or bx >= WIDTH - blueRadius:
            vx *= -1
            bx = max(blueRadius, min(WIDTH - blueRadius, bx))
        if by <= blueRadius or by >= HEIGHT - blueRadius:
            vy *= -1
            by = max(blueRadius, min(HEIGHT - blueRadius, by))

        blue['pos'] = [bx, by]
        blue['vel'] = [vx, vy]

        if distance(blue['pos'], redPos) < redRadius + blueRadius:
            resetGame()

    pygame.draw.circle(screen, (255, 0, 0), redPos, redRadius)

    for blue in blueCircles:
        pygame.draw.circle(screen, (0, 0, 255), (int(blue['pos'][0]), int(blue['pos'][1])), blueRadius)

    timer_text = font.render(f"Time: {seconds}s", True, (0, 0, 0))
    screen.blit(timer_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)