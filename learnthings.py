#!/usr/bin/python

import os, sys, pygame, random
from time import time
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
            soundpath = os.path.join("media", self.category, "sounds", self.name + ".ogg")
            self.sound = pygame.mixer.Sound(soundpath)

    def show(self):
        for y in range(-height, 1, 25):
            screen.blit(self.image, (0,y))
            pygame.display.flip()
        screen.blit(self.image, (0,0))
        pygame.display.flip()
        self.sound.play()

class Random:
    """Produce random numbers between 0-limit that do not repeat"""
    def __init__(self, limit):
        self.limit = limit-1;
        self.last = -1;

    def next(self):
        nextRandom = random.randint(0, self.limit)
        if nextRandom == self.last:
            return self.next()
        else:
            self.last = nextRandom
            return nextRandom
        
# Parse arguments
if len(sys.argv) < 2:
    print "Usage: ", sys.argv[0], "category"
    sys.exit()

category = sys.argv[1]
# At least how many seconds each image is showed
timeTreshold = 5
# How many times any key must be pressed after timeTreshold seconds
keypressTreshold = 5

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
rnd = Random(len(things))

# Show first random thing
things[rnd.next()].show()
thingShowTime = time()

keypresses = 0
thingsShown = 1
startTime = time()
# Exit sequence
exitSeq = [K_q, K_u, K_i, K_t]
exitIndex = 0

# Event loop
while exitIndex != len(exitSeq):
    if keypresses > keypressTreshold:
        keypresses = 0
        things[rnd.next()].show()
        thingsShown = thingsShown + 1
        thingShowTime = time()
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == KEYDOWN:
            if (time() - thingShowTime) > timeTreshold:
                keypresses = keypresses + 1
            if event.key == exitSeq[exitIndex]:
                exitIndex = exitIndex + 1
            else:
                exitIndex = 0

delta = time() - startTime
timePerThing = int(delta/thingsShown)
print thingsShown, "things shown in", int(delta), "seconds, ", timePerThing, "s/thing"
