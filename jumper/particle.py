from jumper.physics import JumpPhysics


class PointParticle:
    GROUND = 0.0

    def __init__(self, physics: JumpPhysics) -> None:
        self.physics = physics
        self.ground = PointParticle.GROUND
        self.height = PointParticle.GROUND
        self.velocity = 0.0
        self.grounded = True

    def jump(self) -> None:
        if self.grounded:
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
