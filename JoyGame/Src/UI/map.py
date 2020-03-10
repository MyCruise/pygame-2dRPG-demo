import os
import pygame
from JoyGame.Src.Include.abspath import abspath_join
from JoyGame.Src.Include.glovar import GLOVAR
from JoyGame.Src.Tools.save2json import SAVE2CONFIG
from JoyGame.Src.System.picture import Picture
from JoyGame.Src.Character.sprite import MySprite


class Map:
    def __init__(self, screen):
        self.screen = screen
        self.width = self.screen.width
        self.height = self.screen.height
        self.maxBlockNum_w = 0
        self.maxBlockNum_h = 0

        self.map_group = pygame.sprite.Group()
        self.s2c = SAVE2CONFIG()
        self.glovar = GLOVAR()
        self.environment = self.glovar.MaterialsEnvironment
        self.label = 0
        self.start = (0, 0)
        self.loadFlag = False
        self.map_point = []
        self.map_block = []
        self.label_list = os.listdir(self.environment)
        self.block_list = os.listdir(abspath_join(self.environment, self.label_list[self.label]))

    def load_map_block(self, map_block, point):
        if map_block in self.block_list:
            path = abspath_join(self.environment, self.label_list[self.label])
            block = abspath_join(path, map_block)
            map_block = MySprite(self.screen.screen)
            map_block.position = point
            map_block.load(block, self.glovar.block_map[0], self.glovar.block_map[1], 1)
            return map_block
        else:
            print(str(map_block))

    def saveMap(self):
        index = 0
        map_dict = {}
        for i in range(len(self.map_block)):
            map_dict[str(index)] = [self.map_block[i], self.map_point[i]]
        self.s2c.save2map_dict(map_dict)

    def addMapBlock(self, map_block, point):
        point = tuple(map(lambda i, j: i * j, point, self.glovar.block_map))
        block = self.load_map_block(map_block, point)
        self.map_group.add(block)

    def mapping(self, map_point: tuple):
        map_dict = self.s2c.readFromMap()
        if not self.loadFlag:
            for i in range(len(map_dict)):
                point = tuple(map(lambda i, j: i + j, map_dict[str(i)][1], map_point))
                self.addMapBlock(map_dict[str(i)][0] + ".png", point)
            self.loadFlag = True

    def update(self, ticks):
        self.map_group.update(ticks)
        self.map_group.draw(self.screen.screen)


if __name__ == '__main__':
    glovar = GLOVAR()
