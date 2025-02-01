import pygame
from constants import *
from circleshape import CircleShape
from shot import Shot
from explosion import Explosion

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_timer = 0
        self.invulnerability = 0
        self.respawn_timer = 0

    # Calculate and return points for player triangle shape
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    # Overrides parent class
    def draw(self, screen):
        if self.respawn_timer <= 0:
            pygame.draw.polygon(screen, "white", self.triangle(), 2)
        else:
            pygame.draw.polygon(screen, "black", self.triangle(), 2)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    # Overrides parent class
    def update(self, dt):
        self.shot_timer -= dt
        self.respawn_timer -= dt
        if self.respawn_timer <= 0:
            self.invulnerability -= dt
            keys = pygame.key.get_pressed()

            if keys[pygame.K_a]: # rotate left
                self.rotate(-dt)
            if keys[pygame.K_d]: # rotate right
                self.rotate(dt)
            if keys[pygame.K_w]: # move forward
                self.move(dt)
            if keys[pygame.K_s]: # move backward
                self.move(-dt)
            if keys[pygame.K_LEFT]: # rotate left
                self.rotate(-dt)
            if keys[pygame.K_RIGHT]: # rotate right
                self.rotate(dt)
            if keys[pygame.K_UP]: # move forward
                self.move(dt)
            if keys[pygame.K_DOWN]: # move backward
                self.move(-dt)
            if keys[pygame.K_SPACE]: # shoot
                self.shoot()

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

        # Allows for screen wrap
        if self.position.x + self.radius < 0:
            self.position.x = SCREEN_WIDTH + self.radius
        if self.position.x - self.radius > SCREEN_WIDTH:
            self.position.x = 0 - self.radius
        if self.position.y + self.radius < 0:
            self.position.y = SCREEN_HEIGHT + self.radius
        if self.position.y - self.radius > SCREEN_HEIGHT:
            self.position.y = 0 - self.radius

    def shoot(self):
        # Enforces delay between shots
        if self.shot_timer > 0:
            return
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        self.shot_timer = PLAYER_SHOOT_COOLDOWN

    # When player colides with Asteroid
    def collided(self, lives, score, dt):
        lives -= 1
        if lives <=0:
            exit(f"Game over! Your score was {score}!")

        # Explosion effect
        for i in range(0, 360, 20):
            explode = Explosion(self.position.x, self.position.y)
            vect = pygame.Vector2(0, 1).rotate(i) * PLAYER_SPEED
            explode.velocity = vect

        # Player disappears from screen temporarily and becomes invulnerable
        self.invulnerability = RESPAWN_INVULNERABILITY
        self.respawn_timer = RESPAWN_TIMER
        
        return lives
