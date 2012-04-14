#!/opt/local/bin/python2.7

import os, sys, pygame
pygame.init()

black = 0, 0, 0

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)
info = pygame.display.Info()
width = info.current_w
height = info.current_h

class NoneSound:
    def play(self): pass

class Thing:
    """A thing that contains an image and a sound"""
    def __init__(self, category, name):
        self.name = name
        self.category = category
        self.load()
        
    def load(self):
        self.loadsound()
        self.loadimage()
    
    def loadimage(self):
        imagepath = os.path.join("media", self.category, "photos", self.name + ".jpg")
        try:
            self.image = pygame.image.load(imagepath)
        except pygame.error, message:
            raise SystemExit, message
        self.image = self.image.convert()
        self.pos = ( (width - self.image.get_width())/2, (height - self.image.get_height())/2 )

    def loadsound(self):
        if not pygame.mixer:
            self.sound = NoneSound()
        else:
            soundpath = os.path.join("media", self.category, "sounds", self.name     + ".ogg")
            self.sound = pygame.mixer.Sound(soundpath)

    def show(self):
        screen.fill(black)
        screen.blit(self.image, self.pos)
        pygame.display.flip()
        self.sound.play()

rooster = Thing("animals", "rooster")
sheep = Thing("animals", "sheep")

rooster.show()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_ESCAPE: 
                sys.exit()
            else:
                sheep.show()
