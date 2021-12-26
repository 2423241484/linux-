import random
import pygame
from pygame.sprite import Sprite
from time import sleep
class Alien(Sprite):
    """表示单个外星人的类"""
    def __init__(self,ai_game):
        """初始化外星人并设置其起始位置"""
        super().__init__()  #初始化父类构造方法 
        self.screen=ai_game.screen #获取游戏屏幕surface
        self.settings=ai_game.settings #获取游戏设置对象
        """加载外星人图像并设置其rect属性"""
        self.image=pygame.image.load('images/alien.bmp') #载入外星人图像
        self.rect=self.image.get_rect() #获取外星人矩形surface
        """每个外星人最初都在屏幕左上角附近"""
        self.x_range=list(range(self.screen.get_rect().width)) #获得屏幕上的x坐标的范围数组
        self.y_range=list(range((self.screen.get_rect().height)//3))#获得屏幕上上三分之一的y坐标的范围数组
        #self.rect.x=self.rect.width  #将外星人的左边距设置为外星人的宽度 
        #self.rect.y=self.rect.height  #将外星人的上边距设置为外星人的高度
        self.rect.x=random.choice(self.x_range) #设置外星人的左边距
        self.rect.y=random.choice(self.y_range) #设置外星人的上边距
        self.x=float(self.rect.x)  #存储外星人的精确水平位置
        self.y=float(self.rect.y)  #存储外星人的精确水平位置
        self.movetime=5#初始化持续移动次数
    
    """更新外星人移动"""
    def update(self):
        """向左或者向右移动外星人"""
        if self.movetime==0:
            self.movetime=5
        if self.movetime==5:
           self.select_direction_leftandright=random.choice(list(range(2))) #代表左右2个方向
        
        if self.select_direction_leftandright==0 and self.rect.left>self.screen.get_rect().left:
            self.x-=self.settings.alien_speed*6 #外星人向左移动
            self.movetime-=1 #次数减一
        elif self.select_direction_leftandright==0 and self.rect.left<=self.screen.get_rect().left:
            self.x=random.choice(list(range(100,self.screen.get_rect().width-100)))
            self.movetime-=1 #次数减一
        if self.select_direction_leftandright==1 and self.rect.right<self.screen.get_rect().right:
            self.x+=self.settings.alien_speed*6#外星人向右移动
            self.movetime-=1 #次数减一
        elif self.select_direction_leftandright==1 and self.rect.right>=self.screen.get_rect().right:
            self.x=random.choice(list(range(100,self.screen.get_rect().width-100)))
            self.movetime-=1 #次数减一
        #self.x+=(self.settings.alien_speed*self.settings.fleet_direction) #设置外星人移动距离
        self.rect.x=self.x #让外星人水平移动
        self.y+=self.settings.fleet_drop_speed #精确存储外星人垂直移动距离
        self.rect.y=self.y #存储外星人垂直移动
    """判断外星人是否触及边缘"""
    def check_edges(self):
        """如果外星人位于屏幕边缘，就返回True"""
        screen_rect=self.screen.get_rect() #获得游戏屏幕矩形surface
        if self.rect.right >= screen_rect.right or self.rect.left <= 0: #判断外星人矩形surface是否触及游戏屏幕边缘
            return True  #返回True表示触及边缘
