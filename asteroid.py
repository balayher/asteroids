import pygame
import random
from constants import *
from circleshape import CircleShape
from explosion import Explosion

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    # Overrides parent class
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    # Overrides parent class
    def update(self, dt):
        self.position += (self.velocity * dt)
        if self.position.x + self.radius < 0:
            self.position.x = SCREEN_WIDTH + self.radius
        if self.position.x - self.radius > SCREEN_WIDTH:
            self.position.x = 0 - self.radius
        if self.position.y + self.radius < 0:
            self.position.y = SCREEN_HEIGHT + self.radius
        if self.position.y - self.radius > SCREEN_HEIGHT:
            self.position.y = 0 - self.radius

    def split(self, score):
        score += 1
        self.kill()

        #Explosion effect
        for i in range(0, 360, 20):
            explode = Explosion(self.position.x, self.position.y)
            vect = self.velocity.rotate(i)
            explode.velocity = vect

        if self.radius <= ASTEROID_MIN_RADIUS:
            return score
        angle = random.uniform(20, 50)
        vect_a = self.velocity.rotate(angle)
        vect_b = self.velocity.rotate(-angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        asteroid_a = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid_a.velocity = vect_a * 1.2
        asteroid_b = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid_b.velocity = vect_b * 1.2 
        return score       