import pygame
import os

window_x = 100
window_y = 50
display_x = pygame.display.Info().current_w
display_y = pygame.display.Info().current_h

x = display_x - window_x
y = display_y - window_y

os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x},{y}"

pygame.init()

windoww, windowh = 400, 300

screen = pygame.display.set_mode((windoww, windowh), pygame.NOFRAME)

pygame.display.set_caption("Deskpet")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255,255,255))
    pygame.display.flip()

pygame.quit()