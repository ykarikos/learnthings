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
        self.screensize = (width, height)
        self.lang = lang
        self.sound = False
        self.namesound = False
        self.load()    
        
    def load(self):
        self.loadsounds()
        self.loadimage()
    
    def loadimage(self):
        imagepath = os.path.join("media", self.category, "photos", self.name + ".jpg")
        try:
            image = pygame.image.load(imagepath).convert()
            self.image = pygame.transform.smoothscale(image, self.targetsize(image.get_size()))
        except pygame.error, message:
            raise SystemExit, message

    def loadsounds(self):
        if not mixer:
            self.sound = NoneSound()
        else:
            soundpath = os.path.join("media", self.category, "sounds", self.name + ".ogg")
            if (os.path.isfile(soundpath)):
                self.sound = mixer.Sound(soundpath)
            if self.lang != "":
                namepath = os.path.join("media", self.category, "names", self.lang, self.name + ".ogg")
                if (os.path.isfile(namepath)):
                    self.namesound = mixer.Sound(namepath)

    def show(self, screen):
        imagesize = self.image.get_size()
        center = ((self.screensize[0] - imagesize[0]) / 2, (self.screensize[1] - imagesize[1]) / 2)
        
        for y in range(-self.screensize[1], center[1], 25):
            screen.fill((0,0,0), (0, 0, self.screensize[0], imagesize[1] + y))
            screen.blit(self.image, (center[0],y))
            pygame.display.flip()
        screen.blit(self.image, (center[0],center[1]))
        pygame.display.flip()

        # clear space below photo
        for y in range(center[1] + imagesize[1], self.screensize[1]+1, 25):
            screen.fill((0,0,0), (0, y, self.screensize[0], y + 25))
            pygame.display.flip()
        
        # play sounds
        if self.namesound:
            self.namesound.play()
            time.sleep(self.namesound.get_length() - 0.5)
        if self.sound:
            self.sound.play()

    def targetsize(self, size):
        if ((size[0] / size[1]) > (self.screensize[0] / self.screensize[1])):
            return (self.screensize[0], size[1] * self.screensize[0] / size[0])
        else:
            return (size[0] * self.screensize[1] / size[1], self.screensize[1])


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
