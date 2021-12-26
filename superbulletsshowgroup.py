import pygame
from pygame import image
from pygame.sprite import Sprite
class showsuperBullet(Sprite):
    def __init__(self,ai_game):
        """创建一个超级子弹对象"""
        super().__init__() #初始化父类构造方法
        self.screen=ai_game.screen  #获取游戏屏幕
        self.settings=ai_game.settings #获取设置类对象
        self.image=image.load('images/micro_super_bullet.bmp') #设置超级子弹图片
        self.rect=self.image.get_rect() #获得子弹矩形surface

    def draw_super_bullet(self):
        """在屏幕上绘制超级子弹"""
        #pygame.draw.rect(self.screen,self.color,self.rect)
        self.screen.blit(self.image,self.rect)
