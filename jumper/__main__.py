import pygame

from jumper.physics import JumpPhysics
from jumper.menu import JumpMenu, JumpParameter
from jumper.particle import PointParticle

from jumper.utils import app_path


pygame.init()

pygame.key.set_repeat(250, 50)

font = pygame.font.Font(app_path("fonts/fira-code-regular.ttf"), 24)

screen = pygame.display.set_mode((800, 800))
screen_rect = screen.get_rect()
pygame.display.set_caption("Jumper")

clock = pygame.time.Clock()
fps = pygame.display.get_current_refresh_rate()
dt = clock.tick(fps)

jump = JumpPhysics()

cube = PointParticle(jump)
cube_side = 100

menu = JumpMenu(
    [
        JumpParameter(
            name="Jump Height",
            get_value=lambda: jump.height,
            set_value=lambda v: setattr(jump, "height", v),
            min=5,
            max=screen_rect.height - cube_side,
            step=5,
            unit="px",
        ),
        JumpParameter(
            name="Jump Time",
            get_value=lambda: int(jump.time * 1000),
            set_value=lambda v: setattr(jump, "time", v / 1000),
            min=100,
            max=10000,
            step=100,
            unit="ms",
        ),
    ],
)

running = True

while running:
    dt = clock.tick(fps) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                cube.jump()

            elif event.key == pygame.K_UP:
                menu.next()
            elif event.key == pygame.K_DOWN:
                menu.prev()

            elif event.key == pygame.K_RIGHT:
                menu.selected.up()
            elif event.key == pygame.K_LEFT:
                menu.selected.down()

    cube.update(dt)

    screen.fill((25, 0, 50))

    menu.draw(screen, font)

    velocity_text = font.render(
        f"Velocity: {cube.velocity:.0f}px/s", True, (255, 255, 255)
    )
    velocity_text_rect = velocity_text.get_rect()
    velocity_text_rect.bottomleft = (10, screen_rect.bottom - 40)
    screen.blit(velocity_text, velocity_text_rect)

    y_pos_text = font.render(
        f"Y: {cube.height:.0f}px", True, (255, 255, 255)
    )
    y_pos_text_rect = y_pos_text.get_rect()
    y_pos_text_rect.bottomleft = (10, screen_rect.bottom - 10)
    screen.blit(y_pos_text, y_pos_text_rect)

    pygame.draw.line(
        screen,
        (225, 255, 255),
        (0, screen_rect.h - jump.height),
        (screen_rect.w, screen_rect.h - jump.height),
    )
    cube.draw(screen, (225, 225, 175), cube_side)
    pygame.display.flip()
