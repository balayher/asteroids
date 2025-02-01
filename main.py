# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from text_display import TextDisplay
from explosion import Explosion

def main():
    pygame.init()
    print("Starting asteroids!")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    score = 0
    lives = PLAYER_LIVES
    
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    asteroid_field = AsteroidField()

    Shot.containers = (shots, updatable, drawable)

    Explosion.containers = (updatable, drawable)

    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)

        for asteroid in asteroids:
            if asteroid.collision(player):
                if player.invulnerability <= 0:
                    asteroid.kill()
                    lives = player.collided(lives, score, dt)
                #exit(f"Game over! Your score was {score}!")

            for shot in shots:
                if asteroid.collision(shot):
                    score = asteroid.split(score)
                    shot.kill()

        screen.fill("black")

        for obj in drawable:
            obj.draw(screen)

        TextDisplay(screen, 'Score: {0}'.format(score), 0, 0)
        TextDisplay(screen, 'Lives: {0}'.format(lives), 0, 20)

        pygame.display.flip()

        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
