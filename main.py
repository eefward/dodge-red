import pygame
import sys
import random
import math

pygame.init()
pygame.display.set_caption("dodge blue")

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

def distance(pos2, pos1):
    return math.sqrt((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2)

def collideCircles(circle1, circle2):
    dx = circle2['pos'][0] - circle1['pos'][0]
    dy = circle2['pos'][1] - circle1['pos'][1]
    dist = math.hypot(dx, dy)
    if dist == 0 or dist > 2 * blueRadius:
        return  

    nx = dx / dist
    ny = dy / dist

    dvx = circle2['vel'][0] - circle1['vel'][0]
    dvy = circle2['vel'][1] - circle1['vel'][1]

    dot = dvx * nx + dvy * ny
    if dot > 0:
        return  

    circle1['vel'][0] += dot * nx
    circle1['vel'][1] += dot * ny
    circle2['vel'][0] -= dot * nx
    circle2['vel'][1] -= dot * ny

    overlap = 2 * blueRadius - dist
    circle1['pos'][0] -= nx * overlap / 2
    circle1['pos'][1] -= ny * overlap / 2
    circle2['pos'][0] += nx * overlap / 2
    circle2['pos'][1] += ny * overlap / 2

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

        # bounce off left/right walls
        if bx <= blueRadius or bx >= WIDTH - blueRadius:
            vx *= -1
            bx = max(blueRadius, min(WIDTH - blueRadius, bx))
        # bounce off top/bottom walls
        elif by <= blueRadius or by >= HEIGHT - blueRadius:
            vy *= -1
            by = max(blueRadius, min(HEIGHT - blueRadius, by))

        blue['pos'] = [bx, by]
        blue['vel'] = [vx, vy]

        if distance(blue['pos'], redPos) < redRadius + blueRadius: # death
            resetGame()

    pygame.draw.circle(screen, (255, 0, 0), redPos, redRadius)

    for blue in blueCircles:
        pygame.draw.circle(screen, (0, 0, 255), (int(blue['pos'][0]), int(blue['pos'][1])), blueRadius)

    timer = font.render(f"Time: {seconds}s", True, (0, 0, 0))
    screen.blit(timer, (10, 10))

    pygame.display.flip()
    clock.tick(60) # frames per second