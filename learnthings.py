#!/usr/bin/python
#
# learnthings.py (C) 2012 Yrjo Kari-Koskinen <ykk@peruna.fi>
#
# Program for small kids to learn recognizing e.g. animals
#
# See README and LICENSE.txt

import os, sys, pygame, random, time
from pygame import mixer
from pygame.locals import *

class NoneSound:
    def play(self): pass

class Thing:
    """A thing that contains an image and a sound"""
    def __init__(self, category, name, width, height, lang):
        self.name = name
        self.category = category
        self.size = (width, height)
        self.lang = lang
        self.load()
        
    def load(self):
        self.loadsounds()
        self.loadimage()
    
    def loadimage(self):
        imagepath = os.path.join("media", self.category, "photos", self.name + ".jpg")
        try:
            self.image = pygame.image.load(imagepath)
        except pygame.error, message:
            raise SystemExit, message
        self.image = self.image.convert()
        self.image = pygame.transform.smoothscale(self.image, self.size)

    def loadsounds(self):
        if not mixer:
            self.sound = NoneSound()
        else:
            soundpath = os.path.join("media", self.category, "sounds", self.name + ".ogg")
            self.sound = mixer.Sound(soundpath)
            if self.lang != "":
                namepath = os.path.join("media", self.category, "names", self.lang, self.name + ".ogg")
                self.namesound = mixer.Sound(namepath)

    def show(self, screen):
        for y in range(-self.size[1], 1, 25):
            screen.blit(self.image, (0,y))
            pygame.display.flip()
        screen.blit(self.image, (0,0))
        pygame.display.flip()
        if self.lang != "":
            self.namesound.play()
            time.sleep(self.namesound.get_length() - 0.5)
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

def mainLoop(things, screen):
    rnd = Random(len(things))
    # Show first random thing
    things[rnd.next()].show(screen)
    thingShowTime = time.time()
    
    keypresses = 0
    thingsShown = 1
    # Exit sequence: q, u, i,t
    exitSeq = [K_q, K_u, K_i, K_t]
    exitIndex = 0
    
    # Event loop
    while exitIndex != len(exitSeq):
        if keypresses > keypressTreshold:
            keypresses = 0
            things[rnd.next()].show(screen)
            thingsShown = thingsShown + 1
            thingShowTime = time.time()
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if (time.time() - thingShowTime) > timeTreshold:
                    keypresses = keypresses + 1
                if event.key == exitSeq[exitIndex]:
                    exitIndex = exitIndex + 1
                else:
                    exitIndex = 0

    return thingsShown


def main(timeTreshold, keypressTreshold):
    # Parse arguments
    if len(sys.argv) < 2:
        print "Usage: ", sys.argv[0], "category", "[language]"
        sys.exit()

    category = sys.argv[1]
    lang = ""
    if len(sys.argv) > 2:
        lang = sys.argv[2]
        if not os.access(os.path.join("media", category, "names", lang), os.R_OK):
            print lang, "language not found"
            sys.exit()

    if not os.access(os.path.join("media", category), os.R_OK):
        print category, "category not found"
        sys.exit()

    # Init pygame display
    print >> sys.stderr, "Loading", category, "..."
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
    things = map(lambda n: Thing(category, n, width, height, lang), thingNames)

    startTime = time.time()
    thingsShown = mainLoop(things, screen)

    delta = time.time() - startTime
    timePerThing = int(delta/thingsShown)
    print >> sys.stderr, thingsShown, "things shown in", int(delta), "seconds, ", timePerThing, "s/thing"

if __name__ == "__main__":
    # At least how many seconds each image is showed
    timeTreshold = 2
    # How many times any key must be pressed after timeTreshold seconds
    keypressTreshold = 3
    
    main(timeTreshold, keypressTreshold)
