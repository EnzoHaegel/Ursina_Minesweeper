#!/usr/bin/env python3

##
## PROJECT, 2021
## Ursina_Minesweeper
## File description:
## minesweeper
##

from ursina import *
import os.path
from os import path
import random

SEED = 42

random.seed(SEED)

app = Ursina()

NB_CELLS_X = 16*2
NB_CELLS_Y = 9*2
DENSITY = 5
OPEN_DELAY = 2

SKIN = ""

Play = True

file_types = '.png'
textureless = False

load_texture("Assets/{SKIN}base", path=None)
load_texture("Assets/{SKIN}flag", path=None)
load_texture("Assets/{SKIN}0", path=None)
load_texture("Assets/{SKIN}1", path=None)
load_texture("Assets/{SKIN}2", path=None)
load_texture("Assets/{SKIN}3", path=None)
load_texture("Assets/{SKIN}4", path=None)
load_texture("Assets/{SKIN}5", path=None)
load_texture("Assets/{SKIN}6", path=None)
load_texture("Assets/{SKIN}7", path=None)
load_texture("Assets/{SKIN}8", path=None)
load_texture("Assets/{SKIN}9", path=None)

window.borderless = False

camera.orthographic = True
camera.fov = (NB_CELLS_X+3)//2
camera.position = (NB_CELLS_X / 2 - 0.5, NB_CELLS_Y / 2 - 1)

class Core():
    def __init__(self):
        self.firstHit = True
        self.density = DENSITY
        self.debug = False

class Map():
    def __init__(self, size=(NB_CELLS_X, NB_CELLS_Y), density=0.3):
        self.width = size[0]
        self.height = size[1]
        self.voxels = [[Voxel(position=(x,y,0)) for x in range(self.width)] for y in range(self.height)]

class Voxel(Button):
    def __init__(self, position=(0,0,0), voxelType="Cell", amount=0):
        if voxelType == "Number":
            super().__init__(
                parent = scene,
                position = position,
                model = 'cube',
                origin_y = .5,
                texture = 'white_cube',
                color = color.color(0, 0, random.uniform(.9, 1.0)),
                highlight_color = color.lime,
                bomb = False,
                flaged = False,
                bombsNearby = 0,
                destroyed = False,
                destroyable = False,
                a = Audio('Assets/pop.wav', pitch=1, loop=False, autoplay=False, volume=1),
            )
        else:
            super().__init__(
                parent = scene,
                position = position,
                model = 'cube',
                origin_y = .5,
                texture = SKIN + "base",
                color = color.white, #color.color(0, 0, random.uniform(.9, 1.0)),
                highlight_color = color.lime,
                bomb = False,
                flaged = False,
                bombsNearby = 0,
                destroyed = False,
                destroyable = True,
                openMe = -1,
                a = Audio('Assets/pop.wav', pitch=1, loop=False, autoplay=False, volume=1),
            )

    def openCell(self):
        calculTexture(self)
        self.destroyed = True
        if self.bombsNearby == 0:
            for voxel_row in board.voxels:
                for voxel in voxel_row:
                    if voxel.position[0] >= self.position[0] - 1 and voxel.position[0] <= self.position[0] + 1:
                        if voxel.position[1] >= self.position[1] - 1 and voxel.position[1] <= self.position[1] + 1:
                            if voxel.destroyed == False and voxel.openMe == -1:
                                voxel.openMe = OPEN_DELAY
        if checkWin() == True:
            print("GAGNE")
            exit(0)

    def openCellNext(self):
        count = 0
        for voxel_row in board.voxels:
            for voxel in voxel_row:
                if voxel.position[0] >= self.position[0] - 1 and voxel.position[0] <= self.position[0] + 1:
                    if voxel.position[1] >= self.position[1] - 1 and voxel.position[1] <= self.position[1] + 1:
                        if voxel.flaged == True:
                            count += 1
        if self.bombsNearby <= count:
            for voxel_row in board.voxels:
                for voxel in voxel_row:
                    if voxel.position[0] >= self.position[0] - 1 and voxel.position[0] <= self.position[0] + 1:
                        if voxel.position[1] >= self.position[1] - 1 and voxel.position[1] <= self.position[1] + 1:
                            if voxel.flaged == False and voxel.destroyed == False and voxel.openMe == -1:
                                voxel.openMe = OPEN_DELAY

    def flagCellNext(self):
        count = 0
        for voxel_row in board.voxels:
            for voxel in voxel_row:
                if voxel.position[0] >= self.position[0] - 1 and voxel.position[0] <= self.position[0] + 1:
                    if voxel.position[1] >= self.position[1] - 1 and voxel.position[1] <= self.position[1] + 1:
                        if not voxel.destroyed:
                            count += 1
        if self.bombsNearby == count:
            for voxel_row in board.voxels:
                for voxel in voxel_row:
                    if voxel.position[0] >= self.position[0] - 1 and voxel.position[0] <= self.position[0] + 1:
                        if voxel.position[1] >= self.position[1] - 1 and voxel.position[1] <= self.position[1] + 1:
                            if not voxel.destroyed:
                                voxel.flaged = True
                                voxel.texture = "flag"

    def input(self, key):
        if self.hovered and self.destroyable:
            if key == "left mouse down" and self.flaged == False:
                if core.firstHit:
                    addMines(position=self.position, density=core.density)
                    core.firstHit = False
                if self.bomb:
                    self.color = color.rgb(255, 0, 0)
                    # if core.debug == False:
                    #     print("PERDU")
                    #     exit(1)
                elif self.destroyed:
                    self.openCellNext()
                else:
                    # destroy(self)
                    self.openMe = OPEN_DELAY
            if key == "right mouse down":
                if self.flaged:
                    self.flaged = False
                    if self.bomb or self.destroyed == False:
                        self.texture = "base"
                    else:
                        calculTexture(self)
                elif not self.flaged and not self.destroyed:
                    self.flaged = True
                    self.texture = "flag"
                elif not self.flaged and self.destroyed:
                    self.flagCellNext()
            if key == 'd':
                debug()

def calculTexture(voxel: Voxel):
    if voxel.bomb == True:
        voxel.color = color.rgb(255, 0, 0)
        Play = False
        print("PERDU")
        return
    # if voxel.bombsNearby == 0:
    #     destroy(voxel)
    # else:
    voxel.a.play()
    voxel.a.fade_out(value=0, duration=.5, delay=0, resolution=None, interrupt='finish')
    voxel.texture = SKIN + str(voxel.bombsNearby)

def debug():
    if core.debug == False:
        core.debug = True
        for voxel_row in board.voxels:
            for voxel in voxel_row:
                # if voxel:
                    # print(f"#{voxel.position}, #{voxel.bombsNearby}")
                if voxel.bomb:
                    voxel.color = color.rgb(255, 0, 0)
    elif core.debug == True:
        core.debug = False
        for voxel_row in board.voxels:
            for voxel in voxel_row:
                if voxel.bomb:
                    voxel.color = color.color(0, 0, random.uniform(.9, 1.0))

def update():
    for voxel_row in board.voxels:
        for voxel in voxel_row:
            if voxel.openMe == 0:
                voxel.openMe = -1
                voxel.openCell()
            if voxel.openMe > 0:
                voxel.openMe -= 1

def checkWin():
    for voxel_row in board.voxels:
        for voxel in voxel_row:
            if voxel.bomb == False and voxel.destroyed == False:
                return False
    return True    

def addMines(position=(0, 0), density = 3):
    for voxel_row in board.voxels:
        for voxel in voxel_row:
            if voxel.position[0] >= position[0] - 1 and voxel.position[0] <= position[0] + 1:
                if voxel.position[1] >= position[1] - 1 and voxel.position[1] <= position[1] + 1:
                    random.randint(0, density - 1)
                    continue
            if random.randint(0, density - 1) == 0:
                voxel.bomb = True
                addBombCounter(voxel.position, 1)
                # voxel.color = color.rgb(255, 0, 0)
#    addText()

#def addText():
#    for voxel_row in board.voxels:
#        for voxel in voxel_row:
#            Voxel(position=(voxel.position[0], voxel.position[1], 1), voxelType="Number", amount=voxel.bombsNearby)

def addBombCounter(position, amount):
    for voxel_row in board.voxels:
        for voxel in voxel_row:
            if voxel.position[0] >= position[0] - 1 and voxel.position[0] <= position[0] + 1:
                if voxel.position[1] >= position[1] - 1 and voxel.position[1] <= position[1] + 1:
                    voxel.bombsNearby += 1

if len(sys.argv) > 1 and path.exists("Assets/"+sys.argv[1]+"_1.png"):
    SKIN = sys.argv[1]+"_"
    print("Skin: "+SKIN)
core = Core()
EditorCamera()
board = Map(size=(NB_CELLS_X, NB_CELLS_Y), density=0.3)
app.run()