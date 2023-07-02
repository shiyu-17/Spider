# -*- codeing = utf-8 -*-


from bs4 import BeautifulSoup     # 网页解析，获取数据
import re       # 正则表达式，进行文字匹配
import urllib.request, urllib.error      # 制定URL，获取网页数据
import xlwt     # 进行excel操作
import sqlite3  # 进行SQLite数据库操作


def main():
    baseurl = "https://weibo.com/u/page/follow/1776448504?relate=fans"
    # 1.爬取网页
    userid = getData(baseurl)
    print(userid)
    # savepath = "电影Top250.xls"
    # dbpath = "movie.db"
    # 3.保存数据
    # saveData(datalist, savepath)
    # saveData2DB(datalist, dbpath)


    # askURL("https://movie.douban.com/top250?start=")
findid = re.compile(r'<span usercard="(.*?)">')
findfans = re.compile(r'<span> 粉丝 (.*?) </span>')

#爬取网页
def getData(baseurl):
    userid = []
    html = askURL(baseurl)      #保存获取到的网页源码

    soup = BeautifulSoup(html, "html.parser")
    for item in soup.find_all('div', class_="vue-recycle-scroller__item-view"):   # 查找符合要求的字符串，形成列表
        # print(item)   #测试：查看电影item全部信息
        fans = re.findall(findfans, item)

        uid = re.findall(findid, item)
        print(uid)
        if fans > 10:
            userid.append(uid)

    return userid


#得到指定一个URL的网页内容
def askURL(url):
    head = {
        'authority': 'weibo.com',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://weibo.com/1192329374/KnnG78Yf3?filter=hot&root_comment_id=0&type=comment',
        'accept-language': 'zh-CN,zh;q=0.9,en-CN;q=0.8,en;q=0.7,es-MX;q=0.6,es;q=0.5',
        'cookie': 'SINAGLOBAL=4945420457337.851.1687757054834; ULV=1687783573979:2:2:2:4484271402463.207.1687783573938:1687757054879; ALF=1690376071; SUB=_2A25JnfrXDeRhGeFK71cR8C3KwzyIHXVrYYafrDV8PUJbkNAGLVfkkW1NQ0JvEEY9SrsfJRjBmxnGao7QKaJXXaK1; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFTjbqqYaFYv30HRPYsfwDi5JpX5oz75NHD95QNShBfeh50Son7Ws4Dqcj-i--ciKLFiKLhi--NiKnpi-zfMN.t; XSRF-TOKEN=3wXZ3Udcf5PS1NibWJIkYAsy; WBPSESS=UrLW89wrdUSfYyBqvsO571XABSPBMZ50sC7VUf1twclrUpozKM59pcOrr6shrDF9RGHUUQipvQYQnBs90fWmPH4dYnWJDd508b3_3UfO8aZG2mdK3-SNragyhGd2Hkz5WQB26U54IWn6HTakTkxPVw=='
    }
                            #用户代理，表示告诉豆瓣服务器，我们是什么类型的机器、浏览器（本质上是告诉浏览器，我们可以接收什么水平的文件内容）

    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


#保存数据
def saveData(datalist, savepath):
    print("save....")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  #创建workbook对象
    sheet = book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True)    #创建工作表
    col = ("电影详情链接", "图片链接", "影片中文名", "影片外国名", "评分", "评价数", "概况", "相关信息")
    for i in range(0, 8):
        sheet.write(0, i, col[i]) #列名
    for i in range(0, 250):
        print("第%d条" %(i+1))
        data = datalist[i]
        for j in range(0, 8):
            sheet.write(i+1, j, data[j])      #数据

    book.save(savepath)       #保存


def saveData2DB(datalist, dbpath):
    init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    for data in datalist:
        for index in range(len(data)):
            if index == 4 or index == 5:
                continue
            data[index] = '"'+data[index]+'"'
        sql = '''
                insert into movie250 (
                info_link,pic_link,cname,ename,score,rated,instroduction,info) 
                values(%s)'''%",".join(data)
        print(sql)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()


def init_db(dbpath):
    sql = '''
        create table movie250 
        (
        id integer primary key autoincrement,
        info_link text,
        pic_link text,
        cname varchar,
        ename varchar,
        score numeric ,
        rated numeric ,
        instroduction text,
        info text
        )
    
    '''  #创建数据表
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()


if __name__ == "__main__":          #当程序执行时
#调用函数
    main()
    print("爬取完毕！")