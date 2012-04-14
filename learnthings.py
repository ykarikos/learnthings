#!/opt/local/bin/python2.7

import sys, pygame
pygame.init()

black = 0, 0, 0

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)
info = pygame.display.Info()
width = info.current_w
height = info.current_h

roosterSound = pygame.mixer.Sound("media/animals/sounds/rooster.ogg")

rooster = pygame.image.load("media/animals/photos/rooster.jpg")
rooster = rooster.convert()
pos = ( (width - rooster.get_width())/2, (height - rooster.get_height())/2 )

screen.fill(black)
screen.blit(rooster, pos)
pygame.display.flip()
roosterSound.play()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN: sys.exit()