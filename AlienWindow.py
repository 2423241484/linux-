from super_bullet import SuperBullet
import time
import random
import pygame
from pygame import image #游戏组件工具包
from pygame import mixer #游戏音乐组件包
from randombaoxiang import BaoXiang 
from settings import settings #导入设置类
from ship import Ship #导入飞船类
from bullet import Bullet #导入子弹类
from alien import Alien #导入外星人类
from time import sleep #导入时间类
from game_stats import GameStats #导入初始化统计信息类
from button import Button #导入按钮类
from scoreboard import Scoreboard #导入计分类
class Alienview: #主类
    """初始化游戏配置信息"""
    def __init__(self): #主类构造方法
        pygame.init() #初始化游戏组件
        pygame.mixer.init() #初始化游戏音乐组件
        self.settings=settings() #引用设置类对象
        self.bulletnum=8 #标记已发射子弹数
        self.clock=pygame.time.Clock() #创建时钟对象
        self.baoxiangs=pygame.sprite.Group() #创建随机宝箱编组
        self.screen=pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height)) #创造一个显示窗口并把它赋给自己的成员变量
        """self.screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN) #全屏模式下屏幕
        #self.settings.screen_width=self.screen.get_rect().width  #修改设置类的屏幕属性值为全屏模式下的屏幕宽
        #self.settings.screen_height=self.get_rect().height   #修改设置类的屏幕属性值为全屏模式下的屏幕高"""
        pygame.display.set_caption("疯狂外星人") #设置窗口标题
        self.stats=GameStats(self) #创建初始化游戏统计信息对象
        self.sb=Scoreboard(self) #创建记分牌
        self.ship=Ship(self)  #创建飞船对象
        self.bullets=pygame.sprite.Group() #创建存储子弹的编组，便于后续控制所有发射出去的有效子弹
        self.aliens=pygame.sprite.Group() #创建存储外星人的编组，便于后续控制所有产生的有效的外星人
        self.super_bullets=pygame.sprite.Group()#创建存储超级子弹的编组，便于后续控制所有产生的有效的超级子弹
        self._create_fleet() #创建外星人群
        self.play_button = Button(self,"Play") #创建play按钮
        self.bulletreadysoundsign=False #子弹备弹声音播放次数标记

    """响应飞船被外星人撞到"""
    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1 #当飞船与外星人发生碰撞时将飞船个数减一
            rect=self.settings.boom.get_rect() #获得爆炸图片矩形surface
            rect.centerx=self.ship.rect.centerx #获得飞船与外星人发生碰撞的位置x坐标
            rect.centery=self.ship.rect.centery #获得飞船与外星人发生碰撞的位置y坐标
            self.screen.blit(self.settings.boom,rect) #绘制爆炸效果
            pygame.display.update() #更新屏幕
            mixer.Sound.play(self.settings.Boom)
            self.sb.prep_ships() #更新飞船数量
            self.aliens.empty() #清空余下的外星人
            self.bullets.empty() #清空余下的子弹
            self._create_fleet() #创建一群新的外星人
            self.ship.center_ship() #将飞船放到屏幕底部中央
            sleep(0.5) #暂停一会儿
        else:
            self.stats.game_active = False #飞船已用完，标志字段为False，表示游戏结束
            rect=self.settings.boom.get_rect() #获得爆炸图片矩形surface
            rect.centerx=self.ship.rect.centerx #获得飞船与外星人发生碰撞的位置x坐标
            rect.centery=self.ship.rect.centery #获得飞船与外星人发生碰撞的位置y坐标
            self.screen.blit(self.settings.boom,rect) #绘制爆炸效果
            pygame.display.update() #更新屏幕
            sleep(0.5)
            pygame.mouse.set_visible(True) #游戏结束，重新让鼠标光标可见
            self.sign=False #标记变量
            mixer.music.load('sounds/game_qianzhou.mp3') #设置游戏前奏音效

    """运行游戏"""
    def run_game(self): #游戏运行函数
        self.sign=False #标记变量
        mixer.music.load('sounds/game_qianzhou.mp3') #设置游戏前奏音效
        pygame.mixer.music.play(0,-1) #开启背景音乐播放
        while True: #持续监听游戏变化及用户输入
            self.clock.tick(40)#时钟频率，帧率随游戏进行逐渐变大  self.settings.clock_speed
            if pygame.mixer.music.get_busy()==False and self.sign==False:#检测当前是否在播放，若已经播放完则重新播放
                 pygame.mixer.music.play(0,-1)
            self._check_events() #监听用户输入
            if self.stats.game_active: #stats.game_active为True表示飞船还有剩余数量，游戏未结束，反之游戏结束
                if pygame.mixer.music.get_busy()==True and self.sign==False:#检测当前是否在播放前奏乐，若有则停止当前前奏乐，播放背景音乐
                    pygame.mixer.music.stop()
                    mixer.music.load('sounds/backgroundmusic.wav') #设置游戏背景音效
                    pygame.mixer.music.play(0,-1)
                    self.sign=True #更换标记变量值
                elif pygame.mixer.music.get_busy()==False and self.sign==True:#检测当前背景音乐是否播放完毕，若是则重新播放
                    pygame.mixer.music.play(0,-1)
                self.ship.update()  #实时更新飞船行为
                self._update_bullets() #更新子弹行为
                self._update_super_bullets()#更新超级子弹行为
                sleep(0.06) #让爆炸效果体现出来，太快了会导致爆炸效果被掩盖
                self._update_aliens() #更新外星人行为
            self._update_screen() #实时更新屏幕状态

    """事件监听"""
    def _check_events(self):
        for event in pygame.event.get(): #事件监听，监听用户的键盘或者鼠标事件
            if event.type == pygame.QUIT:  #判断用户是否点击了窗口关闭按钮
                exit()   #关闭窗口退出游戏
            elif event.type == pygame.KEYDOWN:  #判断用户是否按下了键盘某个按键
               self._check_keydown_events(event) #处理按下键盘按键事件
            elif event.type == pygame.KEYUP:  #判断用户是否松开了键盘某个按键
               self._check_keyup_events(event) #处理松开键盘按键事件
            elif event.type == pygame.MOUSEBUTTONDOWN: #判断是否发生了鼠标点击事件
                mouse_pos = pygame.mouse.get_pos()  #获取鼠标单击屏幕上位置的横纵坐标，值为元组
                self._check_play_button(mouse_pos) #执行play按钮事件处理函数

    """在玩家单击play按钮时开始新游戏"""
    def _check_play_button(self,mouse_pos):
        button_clicked=self.play_button.rect.collidepoint(mouse_pos)#检查鼠标单击位置是否在play按钮的rect内
        if button_clicked and not self.stats.game_active:#如果鼠标单击位置在play按钮的rect内并且游戏为非活动状态
            self.settings.initialize_dynamic_settings() #重置游戏设置
            self.stats.reset_stats() #重置游戏统计信息
            self.stats.game_active=True  #设置游戏为活动状态，游戏开始！
            self.sb.prep_score() #重置游戏信息再显示得分
            self.sb.prep_level() #更新等级图像
            self.sb.prep_ships() #更新飞船数量
            self.sb.prep_super_bullets() #更新编组
            self.aliens.empty() #清空余下的外星人
            self.bullets.empty() #清空余下的子弹
            self._create_fleet() #创建新的外星人群
            self.ship.center_ship() #让飞船居中
            pygame.mouse.set_visible(False) #当游戏运行时让鼠标光标不可见



    """屏幕更新"""
    def _update_screen(self):  
        #self.screen.fill(self.settings.bg_color)#给游戏屏幕填充颜色
        self.screen.blit(self.settings.bg,(0,0))
        self.ship.blitme() #绘制飞船
        for baoxiang in self.baoxiangs.sprites():
            if baoxiang.disappear==False:
               baoxiang.blitimage()
            elif baoxiang.disappear==True:
                baoxiang.kill()
        for bullet in self.bullets.sprites(): #sprites()返回值是一个列表，返回编组中的所有子弹对象
            bullet.draw_bullet() #将每个子弹对象绘制在屏幕上
        for superbullet in self.super_bullets.sprites():
            superbullet.draw_super_bullet()          #将每个超级子弹对象绘制在屏幕上
        self.aliens.draw(self.screen) #将每个外星人对象绘制在屏幕上
        self.sb.show_score() #显示得分
        if not self.stats.game_active: #如果游戏处于非活动状态就绘制按钮
            self.play_button.draw_button()  #绘制按钮
        pygame.display.flip() #更新屏幕新状态

    """键盘监听按下某一键事件"""
    def _check_keydown_events(self,event):
         if event.key == pygame.K_RIGHT: #判断用户按下的按键是否是→方向键
                self.ship.moving_right = True  #确定用户按下的是→方向键，将飞船的“向右移动”状态变量改为true
         elif event.key == pygame.K_LEFT:  #判断用户按下的按键是否是←方向键
                self.ship.moving_left = True  #确定用户按下的是←方向键，将飞船的“向左移动”状态变量改为true
         elif event.key == pygame.K_ESCAPE:  #检测用户按下的键是否为ESC键
                exit()  #退出游戏
         elif event.key == pygame.K_SPACE: #检测用户是否按下开火键(空格)
                if self.bulletnum!=0:
                   self._fire_bullet() #调用射击方法开火！
                   self.bulletnum-=1
                   self.lastfiretime=time.gmtime().tm_sec
                elif self.bulletnum==0:
                    if self.bulletreadysoundsign==False:
                       mixer.Sound.play(self.settings.bullet_ready)#备弹音效
                    self.bulletreadysoundsign=True
                    if abs(time.gmtime().tm_sec-self.lastfiretime)>=1:
                        self._fire_bullet()
                        self.bulletnum=8
                        self.bulletreadysoundsign=False
         elif event.key == pygame.K_c:#检查用户是否按下c键
             if self.settings.super_bullet_num!=0:
                 self._fire_super_bullet()#调用超级子弹方法开火!
                 self.settings.super_bullet_num-=1
                 self.sb.prep_super_bullets()#更新编组
                    

    """键盘监听松开某一键事件"""
    def _check_keyup_events(self,event):
         if event.key == pygame.K_RIGHT:  #判断用户松开的按键是否是→方向键
                self.ship.moving_right = False #确定用户松开的是→方向键，将飞船的“向右移动”状态变量改为false
         elif event.key == pygame.K_LEFT:  #判断用户松开的按键是否是←方向键
                self.ship.moving_left = False#确定用户松开的是←方向键，将飞船的“向左移动”状态变量改为false
    
    """飞船使用超级子弹开火射击"""
    def _fire_super_bullet(self):
        """"创建超级子弹，并将其加入编组superbullets"""
        new_super_bullet=SuperBullet(self)#创建一颗超级子弹
        mixer.Sound.play(self.settings.super_bullet_fire_music)#超级子弹开火音效
        self.super_bullets.add(new_super_bullet)#将创建的超级子弹加入编组中
        

    """飞船开火射击"""
    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets中"""
        if len(self.bullets)<self.settings.bullet_allowed: #如果当前编组里的子弹数小于最大子弹数8则执行以下操作
            new_bullet=Bullet(self) #创建一颗子弹
            mixer.Sound.play(self.settings.bullet_fire) #开火音效
            self.bullets.add(new_bullet) #将创建的子弹加入编组中

        if self.stats.bullets_left>0:
            self.stats.bullets_left-=1
            self.sb.prep_bullets()
        elif self.stats.bullets_left==0:
             self.stats.bullets_left=8
             self.sb.prep_bullets()
    
    """更新子弹位置及删除消失子弹"""
    def _update_bullets(self):
        """更新子弹的位置"""
        self.bullets.update() #更新子弹的位置
        """删除消失的子弹"""
        for bullet in self.bullets.copy(): #获取子弹编组的副本
                if bullet.rect.bottom <= 0:  #判断编组下所有子弹是否已经飞过屏幕顶端
                    self.bullets.remove(bullet)  #删除飞过屏幕顶端的子弹
        self._check_bullet_alien_collisions() #检查碰撞和判断外星人是否全部被射杀，若外星人全部被射杀则新建一群外星人
        self._check_bullet_baoxiang_collisions()#检查子弹和宝箱碰撞
    
    """更新超级子弹位置及删除消失的超级子弹"""
    def _update_super_bullets(self):
        """更新超级子弹位置"""
        self.super_bullets.update()#更新超级子弹位置
        """删除消失的超级子弹"""
        for superbullet in self.super_bullets.copy():
            if superbullet.rect.bottom <=0:
                self.super_bullets.remove(superbullet)
        self._check_superbullet_baoxiang_collisions()#检查超级子弹与宝箱的碰撞
        self._check_superbullet_alien_collisions()#检查超级子弹与外星人的碰撞
    
    """响应超级子弹和宝箱碰撞"""
    def _check_superbullet_baoxiang_collisions(self):
        collisions=pygame.sprite.groupcollide(self.super_bullets,self.baoxiangs,False,True)
        if collisions:
             for baoxiangs in collisions.values():
                for baoxiang in baoxiangs:
                    self.settings.super_bullet_num+=1#超级子弹个数加一
                    self.sb.prep_super_bullets()#更新编组
                    rect=self.settings.baoxiangdakairect #获得宝箱打开图片矩形surface
                    rect.centerx=baoxiang.rect.centerx #获得随机宝箱的位置x坐标
                    rect.centery=baoxiang.rect.centery #获得随机宝箱的位置y坐标
                    self.screen.blit(self.settings.baoxiangdakaiimage,rect) #绘制爆炸效果
                    pygame.display.update() #更新屏幕
                    mixer.Sound.play(self.settings.Boom)#爆炸音效
    
    

    """响应子弹和宝箱碰撞"""
    def _check_bullet_baoxiang_collisions(self):
        collisions=pygame.sprite.groupcollide(self.bullets,self.baoxiangs,True,True)
        if collisions:
            for baoxiangs in collisions.values():
                for baoxiang in baoxiangs:
                    self.settings.super_bullet_num+=1#超级子弹个数加一
                    self.sb.prep_super_bullets()#更新编组
                    rect=self.settings.baoxiangdakairect #获得宝箱打开图片矩形surface
                    rect.centerx=baoxiang.rect.centerx #获得随机宝箱的位置x坐标
                    rect.centery=baoxiang.rect.centery #获得随机宝箱的位置y坐标
                    self.screen.blit(self.settings.baoxiangdakaiimage,rect) #绘制爆炸效果
                    pygame.display.update() #更新屏幕
                    mixer.Sound.play(self.settings.Boom)#爆炸音效
                    
    """响应超级子弹和外星人碰撞"""
    def _check_superbullet_alien_collisions(self):
        collisions=pygame.sprite.groupcollide(self.super_bullets,self.aliens,False,True)
        if collisions:
            for aliens in collisions.values():
                for alien in aliens:
                    rdm=random.choice(list(range(20)))
                    rect=self.settings.boom.get_rect() #获得爆炸图片矩形surface
                    rect.centerx=alien.rect.centerx #获得外星人的位置x坐标
                    rect.centery=alien.rect.centery #获得外星人的位置y坐标
                    self.screen.blit(self.settings.boom,rect) #绘制爆炸效果
                    pygame.display.update() #更新屏幕
                    mixer.Sound.play(self.settings.Boom)#爆炸音效
                    if rdm==19:#指定一个随机数，这样出现宝箱的概率为5%
                        baoxiangnum=BaoXiang(self,alien.rect.centerx,alien.rect.centery)#创建宝箱对象
                        self.baoxiangs.add(baoxiangnum)#加入编组

                self.stats.score += self.settings.alien_points * len(aliens) #增加射杀外星人所得分
                self.sb.prep_score() #创建包含最新得分的新图像
                self.sb.check_high_score() #检查当前得分是否超过了最高分
        if not self.aliens: #判断外星人是否全部被射杀
            self._create_fleet() #新建一群外星人
            self.settings.increase_speed() #加快游戏节奏
            self.stats.level += 1 #消灭了整群外星人，等级加一
            self.sb.prep_level()  #将等级重新绘制表示
  

    """响应子弹和外星人碰撞"""
    def _check_bullet_alien_collisions(self):
        collisions=pygame.sprite.groupcollide(self.bullets,self.aliens,True,True) #检查是否有子弹击中了外星人，如果是，就删除相应的子弹和外星人
        if collisions:
            for aliens in collisions.values():
                for alien in aliens:
                    rdm=random.choice(list(range(20)))
                    rect=self.settings.boom.get_rect() #获得爆炸图片矩形surface
                    rect.centerx=alien.rect.centerx #获得外星人的位置x坐标
                    rect.centery=alien.rect.centery #获得外星人的位置y坐标
                    self.screen.blit(self.settings.boom,rect) #绘制爆炸效果
                    pygame.display.update() #更新屏幕
                    mixer.Sound.play(self.settings.Boom)#爆炸音效
                    if rdm==19:#指定一个随机数，这样出现宝箱的概率为5%
                        baoxiangnum=BaoXiang(self,alien.rect.centerx,alien.rect.centery)#创建宝箱对象
                        self.baoxiangs.add(baoxiangnum)#加入编组

                self.stats.score += self.settings.alien_points * len(aliens) #增加射杀外星人所得分
                self.sb.prep_score() #创建包含最新得分的新图像
                self.sb.check_high_score() #检查当前得分是否超过了最高分
        if not self.aliens: #判断外星人是否全部被射杀
            self.bullets.empty() #删除现有的子弹
            self._create_fleet() #新建一群外星人
            self.settings.increase_speed() #加快游戏节奏
            self.stats.level += 1 #消灭了整群外星人，等级加一
            self.sb.prep_level()  #将等级重新绘制表示


    """创建外星人群"""
    def _create_fleet(self):
        alien=Alien(self) #创建一个外星人
        alien_width,alien_height=alien.rect.size #获取外星人surface的宽度和高度，size属性值是一个元组（width，height）
       # available_space_x=self.settings.screen_width-(3*alien_width) #计算一行下的可用空间，可用空间为屏幕宽度减去两倍的外星人surface宽度
        #number_aliens_x=available_space_x // (2*alien_width) #计算一行下的可用空间可容纳多少个外星人，其中//为整除,舍弃余数
        #ship_height=self.ship.rect.height #获取飞船的高度
        #available_space_y=(self.settings.screen_height-(3*alien_height)-ship_height) #计算屏幕可容纳多少外星人
        #number_rows=available_space_y // (2*alien_height) #计算可用空间下可容纳外星人的行数
        """创建外星人群"""
        #for row_number in range(number_rows):
         #   for alien_number in range(number_aliens_x): #对第row_number行的0~number_aliens_x序号的外星人执行以下操作
          #     self._create_alien(alien_number,row_number) #创建第row_number行的第alien_number序号的外星人，设置好边距并加入编组中
        for alien_number in range(20):
            self._create_alien(alien_number)

    """创建外星人设置边距并加入编组"""
    def _create_alien(self,alien_number):#,row_number
        """创建一个外星人并将其放在当前行"""
        alien=Alien(self) #创建一个外星人
        #alien_width,alien_height=alien.rect.size #获取外星人surface的宽度和高度，size属性值是一个元组（width，height）
        #alien.x=alien_width+2*alien_width*alien_number #设置第alien_number个外星人的x坐标为前面的所有外星人x坐标加上一个外星人宽度
        #alien.rect.x=alien.x #设置第alien_number个外星人的矩形surface左边距
        #alien.rect.y=alien.rect.height+2*alien.rect.height*row_number #设置外星人的上边距
        self.aliens.add(alien) #将创建的外星人加入编组中
    
    """检查是否有外星人到达屏幕边缘，并更新外星人群中所有外星人的位置"""
    def _update_aliens(self):
        self._check_fleet_edges() #检查是否有外星人触及屏幕边缘，若有则让所有外星人下移
        self.aliens.update() #更新所有外星人的位置，让所有外星人移动起来
        if pygame.sprite.spritecollideany(self.ship,self.aliens):  #判断飞船是否与外星人群中的某个外星人发生碰撞，若有则返回发生碰撞的外星人
            self._ship_hit() #执行飞船撞到外星人后的操作
        self._check_aliens_bottom() #检查是否有外星人到达了屏幕底端
    
    """外星人是否触及边缘判断"""
    def _check_fleet_edges(self):
        """有外星人到达边缘时采取相应的措施"""
        for alien in self.aliens.sprites(): #获取外星人编组中的每个外星人
            if alien.check_edges(): #判断外星人编组中的所有外星人是否有外星人触及屏幕边缘
                self._change_fleet_direction() #对触及屏幕边缘的外星人让它们向下移动并且向左水平移动
                break #退出循环
    
    """外星人方向改变及位置下移"""
    def _change_fleet_direction(self):
        """将所有外星人下移，并改变它的方向"""
        for alien in self.aliens.sprites(): #获取外星人编组中的每个外星人
           #alien.rect.x=self.screen.get_rect().width/2
           alien.rect.y+=self.settings.fleet_drop_speed #让外星人下移
           #alien.rect.x=random.choice(list(range(self.screen.get_rect().width//4,self.screen.get_rect().width//2)))#获得随机偏移距离 self.settings.fleet_direction *= -1 #改变外星人的水平移动方向


    """检查是否有外星人到达了屏幕底端"""
    def _check_aliens_bottom(self):
        screen_rect=self.screen.get_rect() #获取游戏屏幕矩形surface
        for alien in self.aliens.sprites(): #获取外星人编组里的所有外星人并且对它们一一进行操作
            if alien.rect.bottom >= screen_rect.bottom:  #如果外星人矩形surface底部触及游戏屏幕底部即外星人到达了底部
                self._ship_hit() #执行响应外星人与飞船碰撞的方法
                break #退出循环
            

if __name__ == '__main__':
    alien=Alienview()
    alien.run_game()
