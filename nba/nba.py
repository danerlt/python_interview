#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json

import pandas as pd
import requests
from matplotlib import pyplot as plt
from matplotlib.patches import Arc, Circle, Rectangle


class Point(object):
    # 坐标点位置
    def __init__(self, x, y):
        super(Point, self).__init__()
        self.x = x
        self.y = y


def draw_ball_field(made_shot, missed_shot, color='#20458C', lw=2, ):
    """
    绘制篮球场
    :param made_shot: 投中的坐标
    :param missed_shot: 未投中的坐标
    :param color: 颜色
    :param lw: 线条宽带
    :return:
    """
    # 新建一个大小为(6,6)的绘图窗口
    plt.figure(figsize=(6, 6))
    # 获得当前的Axes对象ax,进行绘图
    ax = plt.gca()
    # 对篮球场进行底色填充
    lines_outer_rec = Rectangle(xy=(-250, -47.5), width=500, height=470, linewidth=lw, color='#F0F0F0', fill=True)
    # 设置篮球场填充图层为最底层
    lines_outer_rec.set_zorder(0)
    # 将rec添加进ax
    ax.add_patch(lines_outer_rec)
    # 绘制篮筐,半径为7.5
    circle_ball = Circle(xy=(0, 0), radius=7.5, linewidth=lw, color=color, fill=False)
    # 将circle添加进ax
    ax.add_patch(circle_ball)
    # 绘制篮板,尺寸为(60,1)
    plate = Rectangle(xy=(-30, -7.5), width=60, height=-1, linewidth=lw, color=color, fill=False)
    # 将rec添加进ax
    ax.add_patch(plate)
    # 绘制2分区的外框线,尺寸为(160,190)
    outer_rec = Rectangle(xy=(-80, -47.5), width=160, height=190, linewidth=lw, color=color, fill=False)
    # 将rec添加进ax
    ax.add_patch(outer_rec)
    # 绘制2分区的内框线,尺寸为(120,190)
    inner_rec = Rectangle(xy=(-60, -47.5), width=120, height=190, linewidth=lw, color=color, fill=False)
    # 将rec添加进ax
    ax.add_patch(inner_rec)
    # 绘制罚球区域圆圈,半径为60
    circle_punish = Circle(xy=(0, 142.5), radius=60, linewidth=lw, color=color, fill=False)
    # 将circle添加进ax
    ax.add_patch(circle_punish)
    # 绘制三分线的左边线
    three_left_rec = Rectangle(xy=(-220, -47.5), width=0, height=140, linewidth=lw, color=color, fill=False)
    # 将rec添加进ax
    ax.add_patch(three_left_rec)
    # 绘制三分线的右边线
    three_right_rec = Rectangle(xy=(220, -47.5), width=0, height=140, linewidth=lw, color=color, fill=False)
    # 将rec添加进ax
    ax.add_patch(three_right_rec)
    # 绘制三分线的圆弧,圆心为(0,0),半径为238.66,起始角度为22.8,结束角度为157.2
    three_arc = Arc(xy=(0, 0), width=477.32, height=477.32, theta1=22.8, theta2=157.2, linewidth=lw, color=color,
                    fill=False)
    # 将arc添加进ax
    ax.add_patch(three_arc)
    # 绘制中场处的外半圆,半径为60
    center_outer_arc = Arc(xy=(0, 422.5), width=120, height=120, theta1=180, theta2=0, linewidth=lw, color=color,
                           fill=False)
    # 将arc添加进ax
    ax.add_patch(center_outer_arc)
    # 绘制中场处的内半圆,半径为20
    center_inner_arc = Arc(xy=(0, 422.5), width=40, height=40, theta1=180, theta2=0, linewidth=lw, color=color,
                           fill=False)
    # 将arc添加进ax
    ax.add_patch(center_inner_arc)
    # 绘制篮球场外框线,尺寸为(500,470)
    lines_outer_rec = Rectangle(xy=(-250, -47.5), width=500, height=470, linewidth=lw, color=color, fill=False)
    # 将rec添加进ax
    ax.add_patch(lines_outer_rec)
    # 设置坐标范围
    ax.set_xlim(-250, 250)
    ax.set_ylim(422.5, -47.5)
    # 消除坐标轴刻度
    ax.set_xticks([])
    ax.set_yticks([])
    # 绘制散点图
    # 未投中
    ax.scatter(x=missed_shot.x, y=missed_shot.y, s=30, marker='x', color='#A82B2B')
    # 投中
    ax.scatter(x=made_shot.x, y=made_shot.y, s=30, marker='o', edgecolors='#3A7711', color="#F0F0F0", linewidths=2)
    plt.show()


def crawl(player_id, start_year=2018, end_year=2019):
    """爬取数据

    :param player_id 球员ID
    :param start_year 开始年份
    :param end_year 结束年份
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    for i in range(start_year, end_year):
        # 赛季
        season = str(i) + '-' + str(i + 1)[-2:]
        # 请求网址
        url = 'https://stats.nba.com/stats/shotchartdetail?AheadBehind=&CFID=33&CFPARAMS=' + season + '&ClutchTime=&Conference=&ContextFilter=&ContextMeasure=FGA&DateFrom=&DateTo=&Division=&EndPeriod=10&EndRange=28800&GROUP_ID=&GameEventID=&GameID=&GameSegment=&GroupID=&GroupMode=&GroupQuantity=5&LastNGames=0&LeagueID=00&Location=&Month=0&OnOff=&OpponentTeamID=0&Outcome=&PORound=0&Period=0&PlayerID=' + player_id + '&PlayerID1=&PlayerID2=&PlayerID3=&PlayerID4=&PlayerID5=&PlayerPosition=&PointDiff=&Position=&RangeType=0&RookieYear=&Season=' + season + '&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StartPeriod=1&StartRange=0&StarterBench=&TeamID=0&VsConference=&VsDivision=&VsPlayerID1=&VsPlayerID2=&VsPlayerID3=&VsPlayerID4=&VsPlayerID5=&VsTeamID='
        # 请求结果
        response = requests.get(url=url, headers=headers)
        result = json.loads(response.text)
        # 获取数据
        datas = []
        for item in result['resultSets'][0]['rowSet']:
            # 是否进球得分
            flag = item[10]
            # 横坐标
            loc_x = str(item[17])
            # 纵坐标
            loc_y = str(item[18])
            datas.append(loc_x + ',' + loc_y + ',' + flag + '\n')

        with open(str(player_id) + ".csv", 'w') as f:
            f.write("".join(datas))


def analysis(player_id):
    """分析"""
    # 读取数据
    df = pd.read_csv(str(player_id) + ".csv", header=None, names=['width', 'height', 'type'])
    # 分类数据
    made_shot_df = df[df['type'] == 'Made Shot']
    missed_shot_df = df[df['type'] == 'Missed Shot']
    made_shot = Point(made_shot_df['width'], made_shot_df['height'])
    missed_shot = Point(missed_shot_df['width'], missed_shot_df['height'])
    return made_shot, missed_shot


def main():
    player_id = '201935'
    # crawl(player_id)
    print("crawl player_id:%s success" % player_id)
    made_shot, missed_shot = analysis(player_id)
    print("analysis player_id:%s success" % player_id)
    draw_ball_field(made_shot, missed_shot)
    print("draw_ball_field player_id:%s success" % player_id)


if __name__ == '__main__':
    main()
