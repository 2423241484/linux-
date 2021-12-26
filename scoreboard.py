from bulletshowgroup import showBullet
from superbulletsshowgroup import showsuperBullet
from pygame import image
import pygame.font
from pygame.mixer import stop
from pygame.sprite import Group
from ship import Ship
from bullet import Bullet
class Scoreboard:
    """显示得分信息的类"""
    def __init__(self,ai_game):
        """初始化显示得分涉及的属性"""
        self.ai_game=ai_game #获取游戏对象
        self.screen=ai_game.screen #获取游戏屏幕对象
        self.screen_rect=self.screen.get_rect()  #获取游戏屏幕对象矩形surface
        self.settings=ai_game.settings #获取游戏设置类对象
        self.stats=ai_game.stats  #获取游戏统计属性
        self.text_color=(30,30,30,0.25) #设置文本颜色
        self.font=pygame.font.SysFont(None,48)  #设置文本样式并绘制在屏幕上显示
        self.prep_score() #将显示的文本转换为图像
        self.prep_high_score() #准备包含最高得分的图像
        self.prep_level() #显示当前等级
        self.prep_ships() #显示余下的飞船
        self.prep_bullets()#显示剩余子弹数
        self.prep_super_bullets()#显示现有的超级子弹数
        

    
    """将得分渲染为一幅图像"""
    def prep_score(self):
        rounded_score=round(self.stats.score,-1)
        score_str="{:,}".format(rounded_score) #将数值score格式化表示
        self.score_image=self.font.render(score_str,True,self.text_color,self.settings.bg_color) #将字符串绘制成图像并设置文本色和背景色
        self.score_rect=self.score_image.get_rect() #获取绘制的图像的矩形surface
        self.score_rect.right=self.screen_rect.right-20 #分数字符串放置在距离屏幕右边20像素位置
        self.score_rect.top=20  #分数字符串距离屏幕上部20像素

    
    """在屏幕上显示得分和等级"""
    def show_score(self):
        self.screen.blit(self.score_image,self.score_rect) #将得分绘制出来显示在屏幕上
        self.screen.blit(self.high_score_image,self.high_score_rect) #将最高得分绘制出来显示在屏幕上
        self.screen.blit(self.level_image,self.level_rect) #将等级绘制出来显示在屏幕上
        self.ships.draw(self.screen) #将剩余飞船绘制出来显示在屏幕上
        self.bullets.draw(self.screen) #将剩余子弹绘制出来显示在屏幕上
        self.super_bullets.draw(self.screen)#将剩余超级子弹数绘制出来显示在屏幕上

    
    """将最高分转换为渲染的图像并放置在屏幕中央顶上"""
    def prep_high_score(self):
        high_score=round(self.stats.high_score,-1) #获取最高得分
        high_score_str="{:,}".format(high_score) #对最高得分执行格式化
        self.high_score_image=self.font.render(high_score_str,True,self.text_color,self.settings.bg_color) #绘制表示最高得分的图像
        self.high_score_rect=self.high_score_image.get_rect()  #获得表示最高得分的图像的矩形surface
        self.high_score_rect.centerx=self.screen_rect.centerx #设置图像的位置
        self.high_score_rect.top=self.score_rect.top #设置图像的位置

    
    """检查是否诞生了新的最高分"""
    def check_high_score(self):
        if self.stats.score > self.stats.high_score: #如果新的得分超过了最高分
            self.stats.high_score = self.stats.score  #将最高分设置为当前得分
            self.prep_high_score()  #更新包含最高得分的图像

    
    """显示当前等级，将等级转换为渲染的图像"""
    def prep_level(self):
        level_str=str(self.stats.level)  #将当前等级转换为字符串表示
        self.level_image=self.font.render(level_str,True,self.text_color,self.settings.bg_color) #绘制表示当前等级的图像
        self.level_rect=self.level_image.get_rect() #获取图像的矩形surface
        self.level_rect.right=self.score_rect.right #设置图像位置
        self.level_rect.top=self.score_rect.bottom+10 #设置图像位置

    
    """显示还余下多少艘飞船"""
    def prep_ships(self):
        self.ships=Group() #创建显示飞船的空编组
        for ship_number in range(self.stats.ships_left): #对剩下的飞船数进行以下操作
            ship = Ship(self.ai_game)  #获取飞船对象
            ship.rect.x=10+ship_number * ship.rect.width  #设置飞船的位置
            ship.rect.y=10  #设置飞船的位置
            self.ships.add(ship)  #将飞船加入编组
    
    def prep_bullets(self):
        self.bullets=Group() #创建显示子弹数的空编组
        for bullet_number in range(self.stats.bullets_left):
            bullet=showBullet(self.ai_game)
            bullet.rect.x=130+bullet_number*bullet.rect.width #设置子弹水平显示位置
            bullet.rect.y=10 #设置子弹垂直显示位置
            self.bullets.add(bullet) #将子弹加入编组

    def prep_super_bullets(self):
        self.super_bullets=Group()#创建显示现有超级子弹数的空编组
        if self.settings.super_bullet_num!=0:
            for super_bullet_number in range(self.settings.super_bullet_num):
                 super_bullet=showsuperBullet(self.ai_game)
                 super_bullet.rect.x=10+super_bullet_number*super_bullet.rect.width #设置超级子弹水平显示位置
                 super_bullet.rect.y=90 #设置子弹垂直显示位置
                 self.super_bullets.add(super_bullet)#将子弹加入编组




        