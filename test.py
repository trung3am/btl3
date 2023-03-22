import sys
import pygame

# Configuration
pygame.init()
fps = 60
fpsClock = pygame.time.Clock()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

image = pygame.image.load('./bullet.png')
rotation = 0

# Game loop.
while True:
    screen.fill((20, 20, 20))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    rotated_image = pygame.transform.rotate(
        image,
        33
    )

    new_rect = rotated_image.get_rect(
        center = image.get_rect(
            center = (300, 300)
        ).center
    )

    screen.blit(rotated_image, new_rect)
    pygame.display.flip()
    fpsClock.tick(fps)