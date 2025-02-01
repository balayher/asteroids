import pygame
from constants import *
from circleshape import CircleShape

class Explosion(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, EXPLOSION_RADIUS)
        self.duration = EXPLOSION_DURATION

    # Overrides parent class
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    # Overrides parent class
    def update(self, dt):
        self.position += (self.velocity * dt)
        self.duration -= dt
        if self.duration <= 0:
            self.kill()