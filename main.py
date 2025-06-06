import pygame
import sys
import random
import math

pygame.init()
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("dodge red")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

RED = (255, 0, 0)
BLUE = (0, 0, 255)
BG = (255, 255, 255)

red_radius = 20
blue_radius = 15
blue_speed = 2
blue_circles = []

def spawn_blue():
    x = random.randint(blue_radius, WIDTH - blue_radius)
    y = random.randint(blue_radius, HEIGHT - blue_radius)
    angle = random.uniform(0, 2 * math.pi)
    vx = blue_speed * math.cos(angle)
    vy = blue_speed * math.sin(angle)
    return {'pos': [x, y], 'vel': [vx, vy]}

def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def collide_circles(a, b):
    dx = b['pos'][0] - a['pos'][0]
    dy = b['pos'][1] - a['pos'][1]
    dist = math.hypot(dx, dy)
    if dist == 0 or dist > 2 * blue_radius:
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

    overlap = 2 * blue_radius - dist
    a['pos'][0] -= nx * overlap / 2
    a['pos'][1] -= ny * overlap / 2
    b['pos'][0] += nx * overlap / 2
    b['pos'][1] += ny * overlap / 2

def reset_game():
    global blue_circles, start_ticks
    blue_circles = [spawn_blue()]
    start_ticks = pygame.time.get_ticks()

reset_game()

while True:
    screen.fill(BG)
    seconds = (pygame.time.get_ticks() - start_ticks) // 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    red_pos = list(pygame.mouse.get_pos())

    if len(blue_circles) < 1 + (seconds // 4):
        blue_circles.append(spawn_blue())

    for i in range(len(blue_circles)):
        for j in range(i + 1, len(blue_circles)):
            collide_circles(blue_circles[i], blue_circles[j])

    for blue in blue_circles:
        bx, by = blue['pos']
        vx, vy = blue['vel']

        dx = red_pos[0] - bx
        dy = red_pos[1] - by
        dist = math.hypot(dx, dy)
        if dist != 0:
            vx += 0.05 * dx / dist
            vy += 0.05 * dy / dist

        speed = math.hypot(vx, vy)
        max_speed = blue_speed * 2
        if speed > max_speed:
            vx = (vx / speed) * max_speed
            vy = (vy / speed) * max_speed

        bx += vx
        by += vy

        if bx <= blue_radius or bx >= WIDTH - blue_radius:
            vx *= -1
            bx = max(blue_radius, min(WIDTH - blue_radius, bx))
        if by <= blue_radius or by >= HEIGHT - blue_radius:
            vy *= -1
            by = max(blue_radius, min(HEIGHT - blue_radius, by))

        blue['pos'] = [bx, by]
        blue['vel'] = [vx, vy]

        if distance(blue['pos'], red_pos) < red_radius + blue_radius:
            reset_game()

    pygame.draw.circle(screen, RED, red_pos, red_radius)

    for blue in blue_circles:
        pygame.draw.circle(screen, BLUE, (int(blue['pos'][0]), int(blue['pos'][1])), blue_radius)

    timer_text = font.render(f"Time: {seconds}s", True, (0, 0, 0))
    screen.blit(timer_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)
