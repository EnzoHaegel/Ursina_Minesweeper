#!/usr/bin/env python3

##
## PROJECT, 2021
## Ursina_Minesweeper
## File description:
## minesweeper
##

from ursina import *
import random

app = Ursina()

NB_CELLS_X = 16
NB_CELLS_Y = 9
DENSITY = 5

file_types = '.png'
textureless = False

load_texture("Assets/base", path=None)
load_texture("Assets/flag", path=None)
load_texture("Assets/0", path=None)
load_texture("Assets/1", path=None)
load_texture("Assets/2", path=None)
load_texture("Assets/3", path=None)
load_texture("Assets/4", path=None)
load_texture("Assets/5", path=None)
load_texture("Assets/6", path=None)
load_texture("Assets/7", path=None)
load_texture("Assets/8", path=None)
load_texture("Assets/9", path=None)

window.borderless = False

camera.orthographic = True
camera.fov = 16
camera.position = (NB_CELLS_X / 2 - 1, NB_CELLS_Y / 2 - 1)

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
            )
        else:
            super().__init__(
                parent = scene,
                position = position,
                model = 'cube',
                origin_y = .5,
                texture = 'base',
                color = color.color(0, 0, random.uniform(.9, 1.0)),
                highlight_color = color.lime,
                bomb = False,
                flaged = False,
                bombsNearby = 0,
                destroyed = False,
                destroyable = True,
            )

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
                else:
                    # destroy(self)
                    calculTexture(self)
                    self.destroyed = True
                    if checkWin() == True:
                        print("GAGNE")
                        exit(0)
            if key == "right mouse down":
                if self.flaged:
                    self.flaged = False
                    self.texture = "base"
                elif not self.flaged:
                    self.flaged = True
                    self.texture = "flag"
            if key == 'd':
                debug()

def calculTexture(voxel: Voxel):
    if voxel.bomb == True:
        return
    # if voxel.bombsNearby == 0:
    #     destroy(voxel)
    # else:
    voxel.texture = str(voxel.bombsNearby)

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
                    continue
            if random.randint(0, density - 1) == 0:
                voxel.bomb = True
                addBombCounter(voxel.position, 1)
                # voxel.color = color.rgb(255, 0, 0)
    addText()

def addText():
    for voxel_row in board.voxels:
        for voxel in voxel_row:
            Voxel(position=(voxel.position[0], voxel.position[1], 1), voxelType="Number", amount=voxel.bombsNearby)

def addBombCounter(position, amount):
    for voxel_row in board.voxels:
        for voxel in voxel_row:
            if voxel.position[0] >= position[0] - 1 and voxel.position[0] <= position[0] + 1:
                if voxel.position[1] >= position[1] - 1 and voxel.position[1] <= position[1] + 1:
                    voxel.bombsNearby += 1

core = Core()
EditorCamera()
board = Map(size=(NB_CELLS_X, NB_CELLS_Y), density=0.3)
app.run()