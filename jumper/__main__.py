from enum import Enum, auto
import os

import pygame


class JumpParameter(Enum):
    HEIGHT = auto()
    TIME = auto()

    def next(self) -> JumpParameter:
        members = list(JumpParameter)
        return members[(members.index(self) + 1) % len(members)]


def app_path(path: str) -> str:
    app_dir = os.path.join(os.path.dirname(__file__), "..")
    return os.path.join(app_dir, path)


def calc_gravity(height: float, time: float) -> float:
    """Calculate the acceleration due to gravity, given the height to which an
    object jumps and the duration of the jump."""
    return 8 * height / time**2


def calc_initial_velocity(gravity: float, time: float) -> float:
    """Calculate the initial velocity of a jump"""
    return -gravity * time / 2


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

jump_height = 100
jump_time = 0.5

gravity = calc_gravity(jump_height, jump_time)
jump = calc_initial_velocity(gravity, jump_time)

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
                    velocity = jump

            elif event.key == pygame.K_TAB:
                selected_jump_param = selected_jump_param.next()

            elif event.key in (pygame.K_UP, pygame.K_DOWN):
                if event.key == pygame.K_UP:
                    if selected_jump_param == JumpParameter.HEIGHT:
                        jump_height = min(700, jump_height + 5)
                    elif selected_jump_param == JumpParameter.TIME:
                        jump_time = min(10.0, jump_time + 0.1)
                elif event.key == pygame.K_DOWN:
                    if selected_jump_param == JumpParameter.HEIGHT:
                        jump_height = max(5, jump_height - 5)
                    elif selected_jump_param == JumpParameter.TIME:
                        jump_time = max(0.1, jump_time - 0.1)

                gravity = calc_gravity(jump_height, jump_time)
                jump = calc_initial_velocity(gravity, jump_time)

    old_velocity = velocity
    velocity += gravity * dt
    cube_bottom += (old_velocity + velocity) / 2 * dt
    cube.bottom = round(cube_bottom)

    if cube.bottom >= screen_rect.bottom:
        velocity = 0.0
        cube_bottom = float(screen_rect.bottom)
        cube.bottom = screen_rect.bottom

    screen.fill((25, 0, 50))

    jump_height_text = font.render(
        f"Jump Height: {jump_height}px", True, (255, 255, 255)
    )
    jump_height_text_rect = screen.blit(jump_height_text, (10, 10))

    jump_time_text = font.render(f"Jump Time: {jump_time:.1f}s", True, (255, 255, 255))
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
        (0, screen_rect.h - jump_height),
        (screen_rect.w, screen_rect.h - jump_height),
    )
    pygame.draw.rect(screen, (225, 225, 175), cube)
    pygame.display.flip()
