import pygame

pygame.init()

screen = pygame.display.set_mode((800, 800))
screen_rect = screen.get_rect()
pygame.display.set_caption("Jumper")

clock = pygame.time.Clock()
fps = pygame.display.get_current_refresh_rate()
dt = clock.tick(fps)

cube = pygame.Rect((0, 0), (100, 100))
cube.midbottom = screen_rect.midbottom
cube_bottom = float(cube.bottom)

JUMP_HEIGHT = 100
JUMP_TIME = 0.5

GRAVITY = (8 * JUMP_HEIGHT) / (JUMP_TIME**2)
JUMP = -GRAVITY * JUMP_TIME / 2

velocity = 0.0
running = True

while running:
    dt = clock.tick(fps) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if cube.bottom >= screen_rect.bottom:
                    velocity = JUMP

    old_velocity = velocity
    velocity += GRAVITY * dt
    cube_bottom += (old_velocity + velocity) / 2 * dt
    cube.bottom = round(cube_bottom)

    if cube.bottom >= screen_rect.bottom:
        velocity = 0.0
        cube_bottom = float(screen_rect.bottom)
        cube.bottom = screen_rect.bottom

    screen.fill((25, 0, 50))
    pygame.draw.line(
        screen,
        (225, 255, 255),
        (0, screen_rect.h - JUMP_HEIGHT),
        (screen_rect.w, screen_rect.h - JUMP_HEIGHT),
    )
    pygame.draw.rect(screen, (225, 225, 175), cube)
    pygame.display.flip()
