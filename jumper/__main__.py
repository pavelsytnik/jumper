from enum import Enum, auto
import os

import pygame

from jumper.jump_physics import JumpPhysics


class JumpParameter(Enum):
    HEIGHT = auto()
    TIME = auto()

    def next(self) -> JumpParameter:
        members = list(JumpParameter)
        return members[(members.index(self) + 1) % len(members)]


def app_path(path: str) -> str:
    app_dir = os.path.join(os.path.dirname(__file__), "..")
    return os.path.join(app_dir, path)


pygame.init()

font = pygame.font.Font(app_path("fonts/fira-code-regular.ttf"), 24)

screen = pygame.display.set_mode((800, 800))
screen_rect = screen.get_rect()
pygame.display.set_caption("Jumper")

clock = pygame.time.Clock()
fps = pygame.display.get_current_refresh_rate()
dt = clock.tick(fps)

cube = pygame.Rect((0, 0), (100, 100))
cube.midbottom = screen_rect.midbottom
cube_bottom = float(cube.bottom)

jump = JumpPhysics()

selected_jump_param = JumpParameter.HEIGHT

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
                    velocity = jump.initial_velocity

            elif event.key == pygame.K_TAB:
                selected_jump_param = selected_jump_param.next()

            elif event.key in (pygame.K_UP, pygame.K_DOWN):
                if event.key == pygame.K_UP:
                    if selected_jump_param == JumpParameter.HEIGHT:
                        jump.height = min(700, jump.height + 5)
                    elif selected_jump_param == JumpParameter.TIME:
                        jump.time = min(10.0, jump.time + 0.1)
                elif event.key == pygame.K_DOWN:
                    if selected_jump_param == JumpParameter.HEIGHT:
                        jump.height = max(5, jump.height - 5)
                    elif selected_jump_param == JumpParameter.TIME:
                        jump.time = max(0.1, jump.time - 0.1)

    old_velocity = velocity
    velocity += jump.gravity * dt
    cube_bottom += (old_velocity + velocity) / 2 * dt
    cube.bottom = round(cube_bottom)

    if cube.bottom >= screen_rect.bottom:
        velocity = 0.0
        cube_bottom = float(screen_rect.bottom)
        cube.bottom = screen_rect.bottom

    screen.fill((25, 0, 50))

    jump_height_text = font.render(
        f"Jump Height: {jump.height}px", True, (255, 255, 255)
    )
    jump_height_text_rect = screen.blit(jump_height_text, (10, 10))

    jump_time_text = font.render(f"Jump Time: {jump.time:.1f}s", True, (255, 255, 255))
    jump_time_text_rect = screen.blit(jump_time_text, (10, 40))

    if selected_jump_param == JumpParameter.HEIGHT:
        selected_box = pygame.Surface(jump_height_text.size, pygame.SRCALPHA)
        selected_box.fill((255, 255, 255, 64))
        screen.blit(selected_box, jump_height_text_rect)
    elif selected_jump_param == JumpParameter.TIME:
        selected_box = pygame.Surface(jump_time_text.size, pygame.SRCALPHA)
        selected_box.fill((255, 255, 255, 64))
        screen.blit(selected_box, jump_time_text_rect)

    y_pos_text = font.render(
        f"Y: {screen_rect.h - cube.bottom}px", True, (255, 255, 255)
    )
    screen.blit(y_pos_text, (10, 70))

    pygame.draw.line(
        screen,
        (225, 255, 255),
        (0, screen_rect.h - jump.height),
        (screen_rect.w, screen_rect.h - jump.height),
    )
    pygame.draw.rect(screen, (225, 225, 175), cube)
    pygame.display.flip()
