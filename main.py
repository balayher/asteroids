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
    # game setup
    pygame.init()
    print("Starting asteroids!")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    score = 0
    lives = PLAYER_LIVES
    
    # sprite setup
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
        # Exit the game with browser x box
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Update objects
        updatable.update(dt)

        # Checking for Asteroid collision
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

        # Draw sprites
        for obj in drawable:
            obj.draw(screen)

        # Displays text in top left
        TextDisplay(screen, 'Score: {0}'.format(score), 0, 0)
        TextDisplay(screen, 'Lives: {0}'.format(lives), 0, 20)

        # Update game display
        pygame.display.flip()

        # calculates delta time for next game frame (60 fps)
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
