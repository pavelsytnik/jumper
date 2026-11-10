import pygame

from jumper.physics import JumpPhysics


class PointParticle:
    GROUND = 0.0

    def __init__(self, physics: JumpPhysics) -> None:
        self.physics = physics
        self.ground = PointParticle.GROUND
        self.height = PointParticle.GROUND
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
        self.velocity += self.physics.acceleration * dt
        self.height += (old_velocity + self.velocity) / 2 * dt

        if self.height <= self.ground:
            self.velocity = 0.0
            self.height = self.ground
            self.grounded = True

    def draw(
        self,
        surface: pygame.surface.Surface,
        color: pygame.color.ColorLike,
        side: int,
    ) -> None:
        cube = pygame.rect.Rect(0, 0, side, side)
        cube.midbottom = surface.get_rect().midbottom
        cube.bottom -= self.height

        pygame.draw.rect(surface, color, cube)
