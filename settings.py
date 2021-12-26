import pygame
from pygame import image
from pygame import mixer

class settings:
    def __init__(self):
        """初始化游戏静态设置"""
        """屏幕设置"""
        self.screen_width=1200 #设置屏幕宽
        self.screen_height=800 #设置屏幕高
        self.bg_color=(230,230,230)  #设置屏幕背景颜色
        self.bg=image.load('images/back.bmp') #设置背景图片
        """飞船设置"""
        self.ship_speed=25 #设置飞船速度
        self.ship_limit=3 #设置飞船初始数量
        """子弹设置"""
        self.bullet_speed=1.2 #设置子弹速度
        self.bullet_width=40 #设置子弹宽度
        self.bullet_height=23 #设置子弹高度
        #self.bullet_color=(60,60,60) #设置子弹颜色
        self.bullet_allowed=8 #最大子弹数
        """爆炸设置"""
        self.boom=image.load('images/boom2.bmp') #爆炸效果图片
        self.boom_rect=self.boom.get_rect()  #获得爆炸图片矩形surface
        """外星人设置"""
        self.alien_speed=1.2 #设置外星人水平移动距离
        self.fleet_drop_speed=1.5 #当外星人撞到屏幕边缘时，设置外星人向下移动的距离
        self.fleet_drop_speeds=1.5
        """游戏节奏设置"""
        self.speedup_scale=1.3 #加快游戏的速度 2表示玩家每提高一个等级，游戏的节奏就翻一倍；1表示游戏节奏始终不变
        self.score_scale=1.5 #外星人的分数提高速度
        self.drop_speedup_scale=1.15 #外星人下落加速速度
        self.initialize_dynamic_settings()  #初始化随游戏进行而变化的属性
        """游戏音效设置"""
        self.bullet_ready=mixer.Sound('sounds/bullet_ready.mp3') #游戏子弹备弹音效
        self.bullet_fire=mixer.Sound('sounds/bullet_fire.mp3') #游戏飞船开火音效
        self.bullet_fire.set_volume(0.1)#设置开火音效音量大小
        self.Boom=mixer.Sound('sounds/Boom.mp3') #游戏碰撞爆炸音效
        self.Boom.set_volume(0.5)#设置爆炸音效音量大小
        self.super_bullet_fire_music=mixer.Sound('sounds/rocket_fire.mp3')#超级子弹开火音效
        """随机宝箱设置"""
        self.baoxiangimage=image.load('images/baoxiang.bmp')#设置随机宝箱图片
        self.baoxiangrect=self.baoxiangimage.get_rect()#获得宝箱rect矩形surface
        self.baoxiangdakaiimage=image.load('images/baoxiangdakai.bmp')#设置宝箱打开的图片
        self.baoxiangdakairect=self.baoxiangdakaiimage.get_rect()#获得宝箱rect矩形surface
        """超级子弹设置"""
        self.super_bullet_num=1#初始化超级子弹数量
        
        

    """初始化随游戏进行而变化的设置"""
    def initialize_dynamic_settings(self):
        self.ship_speed=25 #设置飞船初始速度
        self.bullet_speed=20  #设置子弹初始速度
        self.alien_speed=1.3 #设置外星人初始速度
        self.fleet_direction=1 #设置外星人初始移动方向
        self.alien_points=50 #设置一个外星人初始所值得分数
        self.clock_speed=100  #初始游戏时钟频率

    
    """提高速度设置和外星人分数"""
    def increase_speed(self):
        self.ship_speed *= self.speedup_scale #提高飞船速度
        self.bullet_speed *= self.speedup_scale #提高子弹速度
        self.alien_speed *= self.speedup_scale #提高外星人水平速度
        self.fleet_drop_speeds *=self.drop_speedup_scale
        self.fleet_drop_speed=self.fleet_drop_speeds #提高外星人下落速度
        self.alien_points = int(self.alien_points * self.score_scale) #提高外星人分数
      

        
