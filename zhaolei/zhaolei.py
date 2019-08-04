#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author: danerlt
@file: zhaolei.py
@time: 2019/8/4 0004 13:21
@desc:
"""

import os
import codecs
import requests
import json
import re
import logging
import jieba
import jieba.analyse
import matplotlib.pyplot as plt
from wordcloud import WordCloud


logging.basicConfig(level=logging.DEBUG,
                    filename='output.log',
                    datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')
logger = logging.getLogger(__name__)

s_headers = """
Host: music.fooor.cn
Proxy-Connection: keep-alive
Content-Length: 56
Pragma: no-cache
Cache-Control: no-cache
Accept: text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01
Origin: http://music.fooor.cn
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Referer: http://music.fooor.cn/
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7"""

path_name = "lyric"
abs_path = os.path.abspath(".")
lyric_path = os.path.join(abs_path, path_name)  # 存放歌词的路径
if not os.path.exists(lyric_path):
    os.mkdir(lyric_path)


def str_to_dict(s=""):
    """Chrome请求view source字符串转成字典"""
    if not s:
        return {}
    else:
        return dict([[h.partition(':')[0], h.partition(':')[2].strip()] for h in s.strip().split('\n')])


def get_all_song_by_singer(singer):
    """获取歌手所有的歌曲名，歌词ID"""
    url = "http://music.fooor.cn/api.php?callback=jQuery111307859797521650602_1564816950440"
    headers = str_to_dict(s_headers)
    s_params = f"""
        types: search
        count: 100
        source: netease
        pages: 1
        name: {singer}
    """
    params = str_to_dict(s_params)
    logger.debug(f'get_all_song_by_singer url:{url}, params:{params}, headers:{headers}')
    res = requests.post(url, data=params, headers=headers)
    logger.debug(f'get_all_song_by_singer res:{res}')
    text = res.text
    logger.debug(f'get_all_song_by_singer text:{text}')
    regex = '(\{.*?\})'
    logger.debug(f'get_all_song_by_singer regex:{regex}')
    s = re.findall(regex, text)
    datas = [json.loads(i) for i in s]
    logger.debug(f'get_all_song_by_singer result:{datas}')
    return datas


def get_lyric_content(lyric_id):
    """根据歌词Id提取歌词"""
    url = "http://music.fooor.cn/api.php?callback=jQuery111307859797521650602_1564816950440"
    headers = str_to_dict(s_headers)
    s_params = f"""
        types: lyric
        id: {lyric_id}
        source: netease
    """
    params = str_to_dict(s_params)
    logger.debug(f'get_lyric_content url:{url}, params:{params}, headers:{headers}')
    res = requests.post(url, data=params, headers=headers)
    logger.debug(f'get_lyric_content res:{res}')
    text = res.text
    logger.debug(f'get_lyric_content text:{text}')
    regex = '(\{.*?\})'
    logger.debug(f'get_lyric_content regex:{regex}')
    s = re.findall(regex,
                   text)  # ['{"lyric":"[00:00.000] \\u4f5c\\u66f2 : \\u8d75\\u96f7\\n[00:26.340]\\u4e3a\\u5bc2\\u5bde\\u7684\\u591c\\u7a7a\\u753b\\u4e0a\\u4e00\\u4e2a\\u6708\\u4eae\\n[00:31.650]\\u628a\\u6211\\u753b\\u5728\\u90a3\\u6708\\u4eae\\u4e0b\\u9762\\u6b4c\\u5531\\n[00:36.790]\\u4e3a\\u51b7\\u6e05\\u7684\\u623f\\u5b50\\u753b\\u4e0a\\u4e00\\u6247\\u5927\\u7a97\\n[00:42.140]\\u518d\\u753b\\u4e0a\\u4e00\\u5f20\\u5e8a\\n[00:47.120]\\u753b\\u4e00\\u4e2a\\u59d1\\u5a18\\u966a\\u7740\\u6211\\n[00:52.580]\\u518d\\u753b\\u4e2a\\u82b1\\u8fb9\\u7684\\u88ab\\u7a9d\\n[00:57.840]\\u753b\\u4e0a\\u7076\\u7089\\u4e0e\\u67f4\\u706b\\n[01:03.020]\\u6211\\u4eec\\u4e00\\u8d77\\u751f\\u6765\\u4e00\\u8d77\\u6d3b\\n[01:09.320]\\n[01:29.110]\\u753b\\u4e00\\u7fa4\\u9e1f\\u513f\\u56f4\\u7740\\u6211\\n[01:34.300]\\u518d\\u753b\\u4e0a\\u7eff\\u5cad\\u548c\\u9752\\u5761\\n[01:39.550]\\u753b\\u4e0a\\u5b81\\u9759\\u4e0e\\u7965\\u548c\\n[01:44.690]\\u96e8\\u70b9\\u513f\\u5728\\u7a3b\\u7530\\u4e0a\\u98d8\\u843d\\n[01:49.970]\\u753b\\u4e0a\\u6709\\u4f60\\u80fd\\u7528\\u624b\\u89e6\\u5230\\u7684\\u5f69\\u8679\\n[01:55.090]\\u753b\\u4e2d\\u6709\\u6211\\u51b3\\u5b9a\\u4e0d\\u706d\\u7684\\u661f\\u7a7a\\n[02:00.090]\\u753b\\u4e0a\\u5f2f\\u66f2\\u65e0\\u5c3d\\u5e73\\u5766\\u7684\\u5c0f\\u8def\\n[02:05.320]\\u5c3d\\u5934\\u7684\\u4eba\\u5bb6\\u68a6\\u5df2\\u5165\\n[02:11.010]\\u753b\\u4e0a\\u6bcd\\u4eb2\\u5b89\\u8be6\\u7684\\u59ff\\u52bf\\n[02:15.960]\\u8fd8\\u6709\\u6a61\\u76ae\\u80fd\\u64e6\\u53bb\\u7684\\u4e89\\u6267\\n[02:21.140]\\u753b\\u4e0a\\u56db\\u5b63\\u90fd\\u4e0d\\u6101\\u7684\\u7cae\\u98df\\n[02:26.260]\\u60a0\\u95f2\\u7684\\u4eba\\u4ece\\u6ca1\\u5fc3\\u4e8b\\n[02:31.660]\\n[03:13.290]\\u6211\\u6ca1\\u6709\\u64e6\\u53bb\\u4e89\\u5435\\u7684\\u6a61\\u76ae\\n[03:18.450]\\u53ea\\u6709\\u4e00\\u652f\\u753b\\u7740\\u5b64\\u72ec\\u7684\\u7b14\\n[03:23.720]\\u90a3\\u591c\\u7a7a\\u7684\\u6708\\u4e5f\\u4e0d\\u518d\\u4eae\\n[03:28.990]\\u53ea\\u6709\\u4e2a\\u5fe7\\u90c1\\u7684\\u5b69\\u5b50\\u5728\\u5531\\n[03:34.170]\\u4e3a\\u5bc2\\u5bde\\u7684\\u591c\\u7a7a\\u753b\\u4e0a\\u4e00\\u4e2a\\u6708\\u4eae\\n","tlyric":""}']
    logger.debug(f'get_lyric_content s:{s}')
    lyric_dict = json.loads(s[0])
    logger.debug(f'get_lyric_content lyric_dict:{lyric_dict}')
    lyric_text = lyric_dict.get(
        "lyric")  # {'lyric': '[00:00.000] 作曲 : 赵雷\n[00:26.340]为寂寞的夜空画上一个月亮\n[00:31.650]把我画在那月亮下面歌唱\n[00:36.790]为冷清的房子画上一扇大窗\n[00:42.140]再画上一张床\n[00:47.120]画一个姑娘陪着我\n[00:52.580]再画个花边的被窝\n[00:57.840]画上灶炉与柴火\n[01:03.020]我们一起生来一起活\n[01:09.320]\n[01:29.110]画一群鸟儿围着我\n[01:34.300]再画上绿岭和青坡\n[01:39.550]画上宁静与祥和\n[01:44.690]雨点儿在稻田上飘落\n[01:49.970]画上有你能用手触到的彩虹\n[01:55.090]画中有我决定不灭的星空\n[02:00.090]画上弯曲无尽平坦的小路\n[02:05.320]尽头的人家梦已入\n[02:11.010]画上母亲安详的姿势\n[02:15.960]还有橡皮能擦去的争执\n[02:21.140]画上四季都不愁的粮食\n[02:26.260]悠闲的人从没心事\n[02:31.660]\n[03:13.290]我没有擦去争吵的橡皮\n[03:18.450]只有一支画着孤独的笔\n[03:23.720]那夜空的月也不再亮\n[03:28.990]只有个忧郁的孩子在唱\n[03:34.170]为寂寞的夜空画上一个月亮\n', 'tlyric': ''}
    clean_lyric_text = re.sub("\[.*\]", "", lyric_text)  # 去掉[00:00.000]这种
    logger.debug(f'get_lyric_content result:{clean_lyric_text}')
    return clean_lyric_text


def write_lyric(file_name, content, path=lyric_path, ):
    """将歌词写入到文件中"""
    file_path_name = os.path.join(path, file_name)
    with codecs.open(file_path_name + ".txt", "w", encoding='utf-8') as f:
        f.write(content)


def crawl(singer):
    # 爬取歌词
    songs = get_all_song_by_singer(singer=singer)
    for song in songs:
        try:
            # song_id = song.get("id", 0)  # 歌曲Id
            name = song.get("name", "未知")  # 歌曲名
            artist = song.get("artist", [])  # 歌手列表
            lyric_id = song.get("lyric_id")
            if singer not in artist:
                # 歌手没有在歌手列表
                logger.warning("singer is not in artist")
            else:
                if lyric_id is None:
                    logger.warning("lyric_id is None")
                else:
                    lyric_content = get_lyric_content(lyric_id)
                    write_lyric(name, lyric_content)
        except Exception as e:
            logger.error("crawl song error:%s" % e)


def read_all_lyric():
    lyric_files = os.listdir(lyric_path)
    all_lyric_arr = []
    for lyric_file in lyric_files:
        with codecs.open(os.path.join(lyric_path, lyric_file), 'r', encoding='utf-8') as f:
            all_lyric_arr.append(f.read())
    return "".join(all_lyric_arr)


def analysis():
    all_lyric_str = read_all_lyric()
    tags = jieba.analyse.extract_tags(all_lyric_str, topK=50, withWeight=True)
    tf = dict((tag[0], tag[1]) for tag in tags)
    logger.debug("tags", tags)
    wordcloud = WordCloud(font_path="SimHei.ttf").generate_from_frequencies(tf)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()


def main(singer):
    # 爬取歌词
    crawl(singer)
    # 分析歌词
    analysis()


if __name__ == '__main__':
    singer = "赵雷"
    main(singer=singer)
