import math
import time
import random
import pygame
from pygame import image #游戏组件工具包
from pygame import mixer
from pygame import display
from pygame.sprite import Group, Sprite #游戏组件包
from settings import settings #导入设置类
class BaoXiang(Sprite):
    def __init__(self,ai_game,centerx,centery):
        super().__init__()
        self.screen=ai_game.screen
        self.settings=ai_game.settings
        self.image=self.settings.baoxiangimage
        self.rect=self.settings.baoxiangrect
        self.firstappeartime=time.gmtime().tm_sec
        self.disappear=False
        self.rect.centerx=centerx
        self.rect.centery=centery
        
    def blitimage(self):
        self.screen.blit(self.image,self.rect)
        if time.gmtime().tm_sec-self.firstappeartime>=10:
            self.disappear=True    
