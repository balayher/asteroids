import pygame
from constants import *

def TextDisplay(screen, text, x, y):

    text = str(text)
    font = pygame.font.Font(None, TEXT_SIZE)
    text = font.render(text, True, TEXT_COLOR)
    screen.blit(text, (x, y))
