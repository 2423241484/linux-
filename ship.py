import pygame
from pygame.sprite import Sprite
class Ship(Sprite):
    def __init__(self,ai_game): #ai_game为传入的游戏窗口对象
        super().__init__()
        self.screen=ai_game.screen #获取窗口屏幕
        self.settings=ai_game.settings
        self.screen_rect=ai_game.screen.get_rect() #获取屏幕surface，便于设置飞船位置
        self.image=pygame.image.load('images/ship.bmp') #加载飞船图像
        self.rect=self.image.get_rect() #创建图像的外接矩形便于操控飞船的移动
        self.rect.midbottom=self.screen_rect.midbottom #将飞船放在游戏屏幕的底部中间
        self.moving_right=False #设置初始向右移动位
        self.moving_left=False #设置初始向左移动位
        self.x=float(self.rect.x)
    def blitme(self):
        self.screen.blit(self.image,self.rect) #绘制飞船
    
    def update(self):
        if self.moving_right and self.rect.right< self.screen_rect.right : #检测飞船是否想向右移动并且判断飞船是否超过游戏屏幕右边界
            self.x+=self.settings.ship_speed  #增加移动距离（以浮点值增加）
        elif self.moving_left and self.rect.left>0:#检测飞船是否想向左移动并且判断飞船是否超过游戏屏幕左边界
            self.x-=self.settings.ship_speed  #减少移动距离（以浮点值减少）
        self.rect.x=self.x #把更新后的移动距离化为整数后赋给飞船的矩形surface水平坐标，表示飞船平滑移动

    def center_ship(self):
        """让飞船在屏幕底部居中"""
        self.rect.midbottom=self.screen_rect.midbottom  #设置飞船在屏幕底部居中
        self.x=float(self.rect.x) #重置用于跟踪飞船位置的属性