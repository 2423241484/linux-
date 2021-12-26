import pygame
import pygame.font
class Button:
    def __init__(self,ai_game,msg):
        """初始化按钮的属性"""
        self.screen=ai_game.screen #获取游戏屏幕对象
        self.screen_rect=self.screen.get_rect()  #获取游戏屏幕对象surface矩形
        self.width,self.height=200,50 #设置初始化按钮宽度和高度
        self.button_color=(0,255,0)  #设置按钮背景颜色
        self.text_color=(255,255,255) #设置按钮内文本颜色
        self.font=pygame.font.SysFont(None,48)  #设置字体样式并渲染在屏幕上
        self.rect=pygame.Rect(0,0,self.width,self.height)  #绘制矩形按钮
        self.rect.center=self.screen_rect.center #设置按钮的位置为屏幕居中
        self._prep_msg(msg)  #将文本渲染成图像显示

    
    """将msg渲染成图像，并使其在按钮上居中"""
    def _prep_msg(self,msg):
        self.msg_image=self.font.render(msg,True,self.text_color,self.button_color) #将msg表示的文本转换为图像，开启反锯齿，渲染字体色，背景色
        self.msg_image_rect=self.msg_image.get_rect() #获取文本图像的矩形surface
        self.msg_image_rect.center=self.rect.center #让文本图像在按钮上居中显示

    """绘制按钮"""
    def draw_button(self):
        self.screen.fill(self.button_color,self.rect) #绘制一个用颜色填充的按钮
        self.screen.blit(self.msg_image,self.msg_image_rect) #绘制文本图像