# -*- coding:utf-8 -*-

import urllib
import re
import MySQLdb
import logging

global count
count = 0


#######################################################################################
# get a html page based on the url
def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html


#######################################################################################
# get the song list of a singer

def getSongList(html):
    pattern = re.compile('<span.*?songlist__songname_txt"><a.*?>(.*?)</a></span>')
    songs = re.findall(pattern, html)
    print "I have get the songs of this album:"
    logging.info("I have get the songs of this album")
    print len(songs)
    for i in range(0, len(songs)):
        print songs[i]


#######################################################################################
# get a singer's detail
def getSinger(html):
    reg_3 = '<h1.*?class="data__name_txt js_index".*?title=.*?>(.*?)</h1>.*?<span.*?class="data_statistic__tit">(.*?)</span>.*?<strong.*?class="data_statistic__number">(.*?)</strong>'
    reg_2 = '<h1.*?class="data__name_txt js_index".*?title=.*?>(.*?)</h1>.*?<span.*?class="data_statistic__tit">(.*?)</span>.*?<strong.*?class="data_statistic__number">(.*?)</strong>.*?<span.*?class="data_statistic__tit">(.*?)</span><strong.*?class="data_statistic__number">(.*?)</strong>'
    reg_1 = '<h1.*?class="data__name_txt js_index".*?title=.*?>(.*?)</h1>.*?<span.*?class="data_statistic__tit">(.*?)</span>.*?<strong.*?class="data_statistic__number">(.*?)</strong>.*?<span.*?class="data_statistic__tit">(.*?)</span><strong.*?class="data_statistic__number">(.*?)</strong>.*?<span.*?class="data_statistic__tit">(.*?)</span><strong.*?class="data_statistic__number">(.*?)</strong>'
    pattern_1 = re.compile(reg_1, re.S)
    pattern_2 = re.compile(reg_2, re.S)
    pattern_3 = re.compile(reg_3, re.S)

    data = re.findall(pattern_1, html)
    if len(data) == 1:
        return data[0]

    print "No MV information!"
    data = re.findall(pattern_2, html)
    if len(data) == 1:
        singer = data[0] + ("MV", "0")
        return singer

    print "No Album Information!"
    data = re.findall(pattern_3, html)
    if len(data) == 1:
        singer = data[0] + ("专辑", "0", "MV", "0")
        return singer
    else:
        return None


def getAuthor(id):
    url = "https://y.qq.com/portal/singer/" + id + ".html"
    print url
    html = getHtml(url)
    author = getSinger(html)
    return author


#######################################################################################
# The following codes will query the front page, and get the singer list.

def getSingerList(url):
    html = getHtml(url)
    reg = '<li.*?class="singer_list_txt__item"><a.*?href=.*?class="singer_list_txt__link js_singer".*?data-singermid="(.*?)".*?data-singerid=.*?title=.*?>(.*?)</a></li>'
    pattern = re.compile(reg, re.S)
    singerIDList = re.findall(pattern, html)
    return singerIDList


#######################################################################################
# THe following codes will do insertion operation
# open database and connect
def insertSingerList(singers):
    db = MySQLdb.connect(host='localhost', user='root', passwd='zhangjie', db='QQSpider', charset='utf8')
    # get operation cursor
    cursor = db.cursor()

    # SQL 插入语句

    state = "china"
    vals = []
    for singer in singers:
        val = (singer[0], state, int(singer[2]), int(singer[4]), int(singer[6]), '100')
        vals.append(val)

    # # SQL 插入语句,不论数据是什么类型,都使用%s作为占位符号
    sql = "INSERT INTO singers(name,state,songs,albums,mvs,followers) VALUES (%s, %s, %s,%s,%s,%s)"
    print sql
    try:
        # execute sql
        # 数据可以是tuple或者list
        cursor.executemany(sql, vals)
        db.commit()
    except Exception as e:
        print e
        print("Error:unable to query the database!")
    # close the connection
    db.close()
    print "Ennnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnd\n"


def getPage(pageURL):
    idNameList = getSingerList(pageURL)
    print "The ID and Name list on this page: ", idNameList
    singers = []
    for singer in idNameList:
        print "URL : ", singer[0], "      NAME ： ", singer[1]
        author = getAuthor(singer[0])
        if author is not None:
            singers += [author]
    print "Insertion starteeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeed"
    # logging("Insertion starteeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeed")
    insertSingerList(singers)


for i in range(1,50):
    i = 1
    pageURL = "https://y.qq.com/portal/singerlist.html#t4="+str(i)+"&t3=all&t2=all&t1=all&"
    getPage(pageURL)
