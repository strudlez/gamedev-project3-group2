from ModelLoader import ModelLoader
from ModelMetadataCache import ModelMetadataCache

globalModelLoader = ModelLoader(ModelMetadataCache())

GRIDSIZE = 2
CONGASPEED=0.1
TURNSPEED=12
TILESIZE=1
SCALE=1

def turnAngle(angle,angleTo,amt):
    if abs(angle-360-angleTo)<abs(angle-angleTo):angle-=360
    elif abs(angle+360-angleTo)<abs(angle-angleTo):angle+=360
    return moveInc(angle,angleTo,amt)%360

def moveInc(move,moveTo,inc):
    if moveTo>move:
        move+=inc
        if move>moveTo:move=move
    elif moveTo<move:
        move-=inc
        if move<moveTo:move=moveTo
    return move
