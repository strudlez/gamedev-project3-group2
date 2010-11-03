import random
import weakref

from pandac.PandaModules import *
from direct.actor.Actor import Actor

import Globals
import LevelConstants
from LevelWalker import LevelWalker

class Partier(object):

    # walking speed of partier, in cells per second
    WANDER_SPEED = 3

    # how quickly partier rotates, in degrees per second
    TURN_SPEED = 270

    all = [] # list of all Partiers in existence

    def __init__(self, spawnLocation):
        # create a walker at current position
        self._walker = LevelWalker(Globals.currentLevel, spawnLocation, set = False)
        self._nextWalker = LevelWalker(Globals.currentLevel, spawnLocation, set = False)

        # register self to be updated
        self._updateTask = taskMgr.add(self.move, 'partier moving')

        # used to calculate time deltas each frame
        self._lastTime = 0

        # actor for partier
        self._actor = Actor("models/player", {"walk": "models/conga"})

        self._actor.loop('walk')

        self._actor.reparentTo(render)
        self._actor.setShaderOff()

        self._dir = None
        self._dirVec = (0, 0, 0)

        self._inbetweenAmount = 0
        # number from 0 to 1, how far from _walker to _nextWalker the partier
        # has moved

        # add self to the dict of all partiers
        Partier.all.append(self)
    
    def move(self, task):
        # get the time delta from last frame
        dt = task.time - self._lastTime
        self._lastTime = task.time
        
        # how far we should walk this frame
        wanderDistance = 0 if self._dir == None else self.WANDER_SPEED * dt
        self._inbetweenAmount += wanderDistance
        # if we walked a whole space or we're not walking at all
        if self._inbetweenAmount >= 1 or self._dir == None:
            # we've reached the next grid space, must pick a new direction
            # move the walker up to current position
            if self._dir != None:
                if self._walker.getCell() == LevelConstants.PARTIER:
                    self._walker.setCell(LevelConstants.EMPTY)
                self._walker.walk(self._dir, 1)
            # pick a new direction
            self._dir = self.chooseDirection()

            if self._dir == None:
                self._inbetweenAmount = 0
            else:
                self._inbetweenAmount -= 1
                self._nextWalker.setCell(LevelConstants.PARTIER)
            self._dirVec = {'U':(0, -1, 0), 'D':(0, 1, 0), 'R':(1, 0, 0), 'L':(-1, 0, 0), None:(0, 0, 0)}[self._dir]

        # set new position of walker
        oldPos = self._walker.getModelPos()
        currPos = [oldPos[i] + (self._dirVec[i] * self._inbetweenAmount * Globals.TILESIZE) for i in xrange(0, 3)]
        self._actor.setPos(currPos[0], currPos[1], currPos[2])
        
        # move walker's heading closer to target heading
        h = self._actor.getH()
        self._actor.setH(Globals.turnAngle(h, {'U':0, 'D':180, 'L':270, 'R':90, None:0}[self._dir], self.TURN_SPEED * dt))

        return task.cont
        
    def chooseDirection(self):
        '''returns a string specifying the next direction to walk in, or None if
        partier can't walk anywhere.  As a side effect, self._nextWalker is
        moved to the next position
        Return value is one of 'U', 'D', 'L', 'R', None'''
        
        # try a random direction
        dirs = ['U', 'D', 'L', 'R']
        dirI = startDirI = random.randint(0, 3)
        #dirI = startDirI = 3
        while True:
            # walk ahead one unit in random direction, check for collision
            self._nextWalker.walk(dirs[dirI], 1)
            c = self._nextWalker.getCell()
            if c == LevelConstants.BLANK or c == LevelConstants.EMPTY or c == LevelConstants.SPAWN:
                # we can walk in this direction!
                break
            
            # can't walk this way, go back
            self._nextWalker.walk(dirs[dirI], -1)
            
            # try next direction
            dirI += 1
            if dirI > 3:
                dirI = 0
            if dirI == startDirI:
                dirI = None
                break

        if dirI == None:
            return None
        return dirs[dirI]

    def collidesWith(self, location):
        return (self._walker.colocated(location) or self._nextWalker.colocated(location))


    def destroy(self):
        taskMgr.remove(self._updateTask)
        Partier.all.remove(self)
        for i in [self._nextWalker, self._walker]:
            if i.getCell() == LevelConstants.PARTIER:
                i.setCell(LevelConstants.EMPTY)
        self._actor.cleanup()
        self._actor.removeNode()
