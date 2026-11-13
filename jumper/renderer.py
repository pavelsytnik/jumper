import pygame

from jumper.menu import JumpMenu
from jumper.particle import PointParticle
from jumper.physics import JumpPhysics


class JumpRenderer:
    def __init__(
        self,
        surface: pygame.Surface,
        font: pygame.Font,
        cube_size: int
    ) -> None:
        self.surface = surface
        self.surface_rect = surface.get_rect()

        self.font = font

        self.cube_rect = pygame.Rect(0, 0, cube_size, cube_size)
        self.cube_rect.midbottom = self.surface_rect.midbottom

    def draw(
        self,
        cube: PointParticle,
        menu: JumpMenu,
        jump: JumpPhysics,
    ) -> None:
        self.surface.fill((25, 0, 50))

        self._draw_cube(cube)
        self._draw_menu(menu)

        self._draw_info(f"Velocity: {cube.velocity:.0f}px/s", row=1)
        self._draw_info(f"Y: {cube.height:.0f}px", row=2)

        pygame.draw.line(
            self.surface,
            (225, 255, 255),
            (0, self.surface_rect.h - jump.height),
            (self.surface_rect.w, self.surface_rect.h - jump.height),
        )

    def _draw_cube(self, cube: PointParticle) -> None:
        self.cube_rect.bottom = self.surface_rect.h - cube.height

        pygame.draw.rect(self.surface, (225, 225, 175), self.cube_rect)

    def _draw_menu(self, menu: JumpMenu) -> None:
        for i, param in enumerate(menu.params):
            text = self.font.render(param.format(), True, (255, 255, 255))
            text_rect = self.surface.blit(text, (10, 10 + i * 30))

            if param == menu.selected:
                box = pygame.Surface(text.size, pygame.SRCALPHA)
                box.fill((255, 255, 255))
                box.set_alpha(64)
                self.surface.blit(box, text_rect)

    def _draw_info(self, text: str, row: int) -> None:
        info = self.font.render(text, True, (255, 255, 255))
        info_rect = info.get_rect()

        padding = 30 * (row - 1) + 10
        info_rect.bottomleft = (10, self.surface_rect.bottom - padding)

        self.surface.blit(info, info_rect)
