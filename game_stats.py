class GameStats:
    """跟踪游戏的统计信息"""
    def __init__(self,ai_game):
        """初始化统计信息"""
        self.settings=ai_game.settings  #获取游戏设置类对象
        self.reset_stats() #执行统计信息方法
        self.game_active=False #让游戏一开始处于非活动状态
        self.high_score = 0 #任何情况下都不重置最高得分
        

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ships_left=self.settings.ship_limit  #飞船初始数量
        self.bullets_left=self.settings.bullet_allowed #子弹数量限制
        self.score = 0 #初始化得分
        self.level = 1 #初始化等级
        self.settings.super_bullet_num=1#初始化超级子弹显示图片
