# -*- codeing = utf-8 -*-
# import bs4 # 网页解析，获取数据

from bs4 import BeautifulSoup
import re  # 正则表达,进行文字匹配
import urllib.request, urllib.error  # 制定URL，获取网页数据
import xlwt  # 进行excel操作
import sqlite3  # 进行SQLite数据库操作


def main():
    baseurl = "https://movie.douban.com/top250?start="
    # 1、爬去网页
    datalist = getData(baseurl)
    # savepath = "豆瓣电影Top250.xls"  # 当前文件路径下
    dbpath = "movie.db"
    # 3、保存数据
    # saveDate(datalist, savepath)\
    saveDateDB(datalist, dbpath)

# 正则规则
findLink = re.compile(r'<a href="(.*?)">')  # 创建正则表达式对象，表示规则（字符串模式）
findImgSrc = re.compile(r'<img alt=".*" class="" src="(.*?)"', re.S)  # re.S 让换行符包含在字符中
findTitle = re.compile(r'<span class="title">(.*?)</span>')
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findJudge = re.compile(r'<span>(\d*)人评价</span>')
findInq = re.compile(r'<span class="inq">(.*?)</span>')
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)


# 爬取网页
def getData(baseurl):
    datalist = []
    for i in range(0, 10):
        url = baseurl + str(i * 25)
        html = askUrl(url)
        # 2、逐一解析数据
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="item"):
            data = []
            item = str(item)
            print(item)
            # 获取影片详情的超链接
            link = re.findall(findLink, item)[0]
            imgSrc = re.findall(findImgSrc, item)[0]
            titles = re.findall(findTitle, item)
            ctitle = titles[0]
            if (len(titles) == 2):
                otitle = titles[1].replace("/", "")
            else:
                otitle = " "
            print(ctitle)
            print(otitle)
            rating = re.findall(findRating, item)[0]
            judgeNum = re.findall(findJudge, item)[0]
            inq = re.findall(findInq, item)
            print(inq)
            if (len(inq) != 0):
                inq = inq[0].replace("。", "")
            else:
                inq = " "
            bd = re.findall(findBd, item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?', "", bd)
            bd = re.sub('/', " ", bd)
            bd = bd.strip()
            data.append(link)
            data.append(imgSrc)
            data.append(ctitle)
            data.append(otitle)
            data.append(rating)
            data.append(judgeNum)
            data.append(inq)
            data.append(bd)
            datalist.append(data)
    return datalist


# 保存数据到excel
def saveDate(datalist, savepath):
    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet('豆瓣电影Top250')
    col = ("电影详情", "图片链接", "中文名", "外文名", "评分", "评价数", "概况", "相关信息")
    for i in range(0, 8):
        sheet.write(0, i, col[i])
    for i in range(0, len(datalist)):
        print("第%d条成功写入"%i)
        data = datalist[i]
        for j in range(0, 8):
            sheet.write(i+1, j, data[j])
    book.save(savepath)
    print("文件写入完毕")
# 保存数据（DB）
def saveDateDB(datalist, dbpath):
    init_db(dbpath)  # 初始化
    conn = sqlite3.connect(dbpath)  # 路径存在，则连接；路径不存在，则创建
    cursor = conn.cursor()

    for data in datalist:
        for index in range(len(data)):
            if index == 4 or index == 5:
                continue
            data[index] = '"'+data[index]+'"'
        sql = '''
            insert into movie251(
            info_link,pic_link,cname,oname,score,rated,instroduction,info)
            values(%s)''' % ",".join(data)

        cursor.execute(sql)  # 执行sql
        conn.commit() # 提交sql
    cursor.close()
    conn.close()
    print("文件写入SQLite完毕")

# 建表方法
def init_db(dbpath):
    # 创建数据表
    sql = '''
        create table movie251
        (
        id integer primary key autoincrement,
        info_link text,
        pic_link text,
        cname varchar,
        oname varchar,
        score numeric,
        rated numeric,
        instroduction text,
        info text
        )
    '''
    conn = sqlite3.connect(dbpath)  # 路径存在，则连接；路径不存在，则创建
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()

# 请求URL
def askUrl(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/87.0.4280.88 Safari/537.36 "
    }

    request = urllib.request.Request(url=url, headers=head)  # 封装
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


if __name__ == "__main__":  # 当程序执行时
    # 调用函数
    main()
    # init_db("movie.db")
