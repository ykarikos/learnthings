#!/usr/bin/python

import os, sys, pygame, random
from pygame.locals import *

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
        self.image = pygame.transform.smoothscale(self.image, (width, height))

    def loadsound(self):
        if not pygame.mixer:
            self.sound = NoneSound()
        else:
            soundpath = os.path.join("media", self.category, "sounds", self.name     + ".ogg")
            self.sound = pygame.mixer.Sound(soundpath)

    def show(self):
        screen.fill(black)
        screen.blit(self.image, (0,0))
        pygame.display.flip()
        self.sound.play()

# Parse arguments
if len(sys.argv) < 2:
    print "Usage: ", sys.argv[0], "category"
    sys.exit()
category = sys.argv[1]
if not os.access(os.path.join("media", category), os.R_OK):
    print category, "category not found"
    sys.exit()

# Init pygame display
print "Loading", category, "..."
pygame.init()
black = 0, 0, 0
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)
info = pygame.display.Info()
width = info.current_w
height = info.current_h

# Load things
thingNames = map(
    lambda s: s[:s.rindex(".jpg")], 
    os.listdir(os.path.join("media", category, "photos")))
things = map(lambda n: Thing(category, n), thingNames)

# Show first random thing
things[random.randint(0, len(things)-1)].show()

keypresses = 0

# Event loop
while 1:
    if keypresses > 5:
        keypresses = 0
        things[random.randint(0, len(things)-1)].show()
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == KEYDOWN:
            if event.mod & KMOD_CTRL and event.key == K_q:
                sys.exit()
            else:
                keypresses = keypresses + 1
