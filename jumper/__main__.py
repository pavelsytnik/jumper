import os

import pygame

from jumper.jump_physics import JumpPhysics
from jumper.jump_menu import JumpMenu, JumpParameter
from jumper.point_particle import PointParticle


def app_path(path: str) -> str:
    app_dir = os.path.join(os.path.dirname(__file__), "..")
    return os.path.join(app_dir, path)


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

cube = PointParticle(jump, screen_rect.bottom)

menu = JumpMenu(
    [
        JumpParameter(
            name="Jump Height",
            get_value=lambda: jump.height,
            set_value=lambda v: setattr(jump, "height", v),
            min=5,
            max=700,
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

        menu.handle(event)
        cube.handle(event)

    cube.update(dt)

    screen.fill((25, 0, 50))

    menu.draw(screen, font)

    y_pos_text = font.render(
        f"Y: {screen_rect.h - cube.y:.0f}px", True, (255, 255, 255)
    )
    screen.blit(y_pos_text, (10, 70))

    pygame.draw.line(
        screen,
        (225, 255, 255),
        (0, screen_rect.h - jump.height),
        (screen_rect.w, screen_rect.h - jump.height),
    )
    cube.draw(screen, (225, 225, 175), 100)
    pygame.display.flip()
