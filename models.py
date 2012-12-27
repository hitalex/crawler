# -*- coding: utf-8 -*-

#! /usr/bin/env python

import re
from datetime import datetime
from lxml import etree # use XPath from lxml

"""
在这里，我将定义会用到的类和数据结构，包括小组、topic和评论。它们之间的关系为：
一个小组包括一些topic，每个评论包括一些评论
注意：
所有的文本全部用UTF-8来编码
"""

class Comment(object):
    """评论的类
    """
    def __init__(self, cid, user_id, pubdate, content, quote_id, topic_id, group_id):
        self.cid = cid              # 评论id
        self.user_id = user_id      # 发评论的人的id
        self.pubdate = pubdate      # 发布时间
        self.content = content      # 评论内容，不包括引用评论的内容
        self.quote_id = quote_id    # 引用他人评论的id
        
        self.topic_id = topic_id    # 所在topic的id
        self.group_id = group_id    # 所在小组的id
        
        
        
class Topic(object):
    """小组中的某个话题
    """
    def __init__(self, topic_id, group_id, first_page, nonfirst_page):
        self.topic_id = topic_id    # 该topic的id
        self.user_id = ""           # 发布topic的人的id
        self.user_name = ""         # 用户的昵称
        self.pubdate = ""           # 该topic发布的时间
        self.title = ""             # 该topic的标题
        self.content = ""          # topic的内容
        self.comment_list = []    # 所有评论的id列表
        
        self.group_id = group_id    # 所在小组的id
        
        self.first_page = first_page        # 测试用，首页
        self.nonfirst_page = nonfirst_page  # 测试用，非首页
        
        # 用户匹配用户id
        self.pattern = re.compile("^http://www.douban.com/people/([0-9, a-z, A-Z]+)/$")
        
        # 抽取信息
        self.extract_info()
        
    def extract_info(self):
        """ 从网页中抽取信息，填写类中的字段
        @param strformat 字符串格式的数据
        """
        # 抽取topic首页的内容
        self.extract_first_page()
        # 抽取topic非首页的内容
        self.extract_nonfirst_page()
        
    def extract_first_page(self):
        # 抽取topic首页的内容
        url = "http://www.douban.com/group/topic/" + self.topic_id + "/"
        print "Reading webpage: " + url
        page = etree.HTML(self.first_page.decode('utf-8'))
        content = page.xpath(u"/html/body/div[@id='wrapper']/div[@id='content']")[0]
        self.title = content.xpath(u"h1")[0].text.strip()
        
        lz = page.xpath(u"//div[@class='topic-doc']/h3/span[@class='from']/a")[0]
        self.user_name = lz.text.strip()
        url = lz.attrib['href']
        print url
        match_obj = self.pattern.match(url)
        assert(match_obj is not None)
        self.user_id = match_obj.group(1)
        strtime = content.xpath(u"//div[@class='topic-doc']/h3/span[@class='color-green']")[0].text
        self.pubdate = datetime.strptime(strtime, "%Y-%m-%d %H:%M:%S")
        
        
    def extract_nonfirst_page(self):
        # 抽取topic非首页的内容
        
        return ""
        
        
class Group(object):
    """小组类
    """
    def __init__(self, group_id, user_id, pubdate, desc, topic_list):
        self.group_id = group_id    # 小组的id
        self.user_id = user_id      # 创建小组的user id
        self.pubdate = pubdate      # 小组创建的时间
        self.desc = desc            # 小组的介绍
        self.topic_list = topic_list    # 小组中的topic id列表
        
if __name__ == "__main__":
    f = open("./testpage/求掀你的英语怎样从烂到无底洞到变强人的！！！.html")
    strfile = f.read()
    topic = Topic('31195872', 'insidestory', strfile, u"")
    
    print "Topic id: ", topic.topic_id
    print "Group id: ", topic.group_id
    print "Title: ", topic.title
    print "User id: ", topic.user_id
    print "User name: ", topic.user_name
    print "Time: ", topic.pubdate