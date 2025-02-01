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

    # in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        if self.respawn_timer <= 0:
            pygame.draw.polygon(screen, "white", self.triangle(), 2)
        else:
            pygame.draw.polygon(screen, "black", self.triangle(), 2)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        self.shot_timer -= dt
        self.respawn_timer -= dt
        if self.respawn_timer <= 0:
            self.invulnerability -= dt
            keys = pygame.key.get_pressed()

            if keys[pygame.K_a]:
                self.rotate(-dt)
            if keys[pygame.K_d]:
                self.rotate(dt)
            if keys[pygame.K_w]:
                self.move(dt)
            if keys[pygame.K_s]:
                self.move(-dt)
            if keys[pygame.K_LEFT]:
                self.rotate(-dt)
            if keys[pygame.K_RIGHT]:
                self.rotate(dt)
            if keys[pygame.K_UP]:
                self.move(dt)
            if keys[pygame.K_DOWN]:
                self.move(-dt)
            if keys[pygame.K_SPACE]:
                self.shoot()

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
        if self.position.x + self.radius < 0:
            self.position.x = SCREEN_WIDTH + self.radius
        if self.position.x - self.radius > SCREEN_WIDTH:
            self.position.x = 0 - self.radius
        if self.position.y + self.radius < 0:
            self.position.y = SCREEN_HEIGHT + self.radius
        if self.position.y - self.radius > SCREEN_HEIGHT:
            self.position.y = 0 - self.radius

    def shoot(self):
        if self.shot_timer > 0:
            return
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        self.shot_timer = PLAYER_SHOOT_COOLDOWN

    def collided(self, lives, score, dt):
        lives -= 1
        if lives <=0:
            exit(f"Game over! Your score was {score}!")

        #Explosion effect
        for i in range(0, 360, 20):
            explode = Explosion(self.position.x, self.position.y)
            vect = pygame.Vector2(0, 1).rotate(i) * PLAYER_SPEED
            explode.velocity = vect

        self.invulnerability = RESPAWN_INVULNERABILITY
        self.respawn_timer = RESPAWN_TIMER
        
        return lives


        

