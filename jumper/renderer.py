import pygame

from jumper.menu import JumpMenu
from jumper.particle import PointParticle
from jumper.physics import JumpPhysics


class JumpRenderer:
    def __init__(self, surface: pygame.Surface, font: pygame.Font) -> None:
        self.surface = surface
        self.surface_rect = surface.get_rect()
        self.font = font

    def draw(
        self,
        cube: PointParticle,
        menu: JumpMenu,
        jump: JumpPhysics,
    ) -> None:
        self.surface.fill((25, 0, 50))

        self._draw_cube(cube)
        self._draw_menu(menu)

        velocity_text = self.font.render(
            f"Velocity: {cube.velocity:.0f}px/s", True, (255, 255, 255)
        )
        velocity_text_rect = velocity_text.get_rect()
        velocity_text_rect.bottomleft = (10, self.surface_rect.bottom - 40)
        self.surface.blit(velocity_text, velocity_text_rect)

        y_pos_text = self.font.render(
            f"Y: {cube.height:.0f}px", True, (255, 255, 255)
        )
        y_pos_text_rect = y_pos_text.get_rect()
        y_pos_text_rect.bottomleft = (10, self.surface_rect.bottom - 10)
        self.surface.blit(y_pos_text, y_pos_text_rect)

        pygame.draw.line(
            self.surface,
            (225, 255, 255),
            (0, self.surface_rect.h - jump.height),
            (self.surface_rect.w, self.surface_rect.h - jump.height),
        )

    def _draw_cube(self, cube: PointParticle) -> None:
        cube_rect = pygame.rect.Rect(0, 0, 100, 100)
        cube_rect.midbottom = self.surface_rect.midbottom
        cube_rect.bottom -= cube.height

        pygame.draw.rect(self.surface, (225, 225, 175), cube_rect)

    def _draw_menu(self, menu: JumpMenu) -> None:
        for i, param in enumerate(menu.params):
            text = self.font.render(param.format(), True, (255, 255, 255))
            text_rect = self.surface.blit(text, (10, 10 + i * 30))

            if param == menu.selected:
                box = pygame.Surface(text.size, pygame.SRCALPHA)
                box.fill((255, 255, 255))
                box.set_alpha(64)
                self.surface.blit(box, text_rect)
