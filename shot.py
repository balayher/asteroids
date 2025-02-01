import pygame
from constants import *
from circleshape import CircleShape

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)
        self.duration = SHOT_DURATION

    # Overrides parent class
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    # Overrides parent class
    def update(self, dt):
        self.position += (self.velocity * dt)

        # Allows for screen wrap
        if self.position.x + self.radius < 0:
            self.position.x = SCREEN_WIDTH + self.radius
        if self.position.x - self.radius > SCREEN_WIDTH:
            self.position.x = 0 - self.radius
        if self.position.y + self.radius < 0:
            self.position.y = SCREEN_HEIGHT + self.radius
        if self.position.y - self.radius > SCREEN_HEIGHT:
            self.position.y = 0 - self.radius
        
        # Removes shot after some time
        self.duration -= dt
        if self.duration <= 0:
            self.kill()