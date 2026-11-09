import pygame

from jumper.jump_physics import JumpPhysics


class PointParticle:
    def __init__(self, physics: JumpPhysics, ground: int) -> None:
        self.physics = physics
        self.ground = ground
        self.y = float(ground)
        self.velocity = 0.0
        self.grounded = True

    def handle(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_SPACE and self.grounded:
            self.velocity = self.physics.initial_velocity
            self.grounded = False

    def update(self, dt: float) -> None:
        if self.grounded:
            return

        old_velocity = self.velocity
        self.velocity += self.physics.gravity * dt
        self.y += (old_velocity + self.velocity) / 2 * dt

        if self.y >= self.ground:
            self.velocity = 0.0
            self.y = float(self.ground)
            self.grounded = True

    def draw(
        self,
        surface: pygame.surface.Surface,
        color: pygame.color.ColorLike,
        side: int,
    ) -> None:
        cube = pygame.rect.Rect(0, 0, side, side)
        cube.midbottom = surface.get_rect().midbottom
        cube.bottom = self.y

        pygame.draw.rect(surface, color, cube)
