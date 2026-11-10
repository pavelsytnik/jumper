class JumpPhysics:
    def __init__(self, height: int = 100, time: float = 0.5) -> None:
        self.height = height
        self.time = time

    @property
    def acceleration(self) -> float:
        """Calculate the acceleration due to gravity, given the height to
        which an object jumps and the duration of the jump."""
        return -(8 * self.height / self.time**2)

    @property
    def initial_velocity(self) -> float:
        """Calculate the initial velocity of a jump"""
        return -self.acceleration * self.time / 2
