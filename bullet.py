import pygame
from pygame import image
from pygame.sprite import Sprite
class Bullet(Sprite):
    """管理飞船所发射子弹的类"""
    def __init__(self,ai_game):
        """在飞船当前位置创建一个子弹对象"""
        super().__init__() #初始化父类构造方法
        self.screen=ai_game.screen  #获取游戏屏幕
        self.settings=ai_game.settings #获取设置类对象
        #self.color=self.settings.bullet_color #获取子弹颜色
        self.bullet_image=image.load('images/bullet.bmp') #设置子弹图片
        self.rect=self.bullet_image.get_rect() #获得子弹矩形surface
        #self.rect=pygame.Rect(0,0,self.settings.bullet_width,self.settings.bullet_height) #在（0,0）处创建一个表示子弹的矩形，在设置正确的位置。
        self.rect.midtop=ai_game.ship.rect.midtop #改变子弹的初始位置，将子弹初始位置设置在飞船的头部中间位置
        self.y=float(self.rect.y)  #存储用浮点数表示的子弹位置(纵坐标，因为子弹是垂直向上)

    def update(self):
        """向上移动子弹"""
        self.y-=self.settings.bullet_speed #更新表示子弹位置的浮点值
        self.rect.y=self.y #更新表示子弹rect的位置（真正子弹的位置）

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        #pygame.draw.rect(self.screen,self.color,self.rect)
        self.screen.blit(self.bullet_image,self.rect)
