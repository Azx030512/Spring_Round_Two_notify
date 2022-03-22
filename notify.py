#!python3

#This script can download html file from multiple websites of zju
#the website urls include:
#[学工部]url1_1="http://www.xgb.zju.edu.cn"
#[校团委]url1_2="http://www.youth.zju.edu.cn"
#[综合服务网]url1_3="https://zhfw.zju.edu.cn"
#[资讯中心]url2="https://service.zju.edu.cn/_s2/students_zxzx/main.psp"
#[校车路线]url3="http://car.zju.edu.cn/index.php?c=Wei&a=car"

#spider part
import requests
import bs4
import logging
import re
import pprint
from selenium import webdriver
import time
from fake_useragent import UserAgent
import pymysql
logging.disable(logging.CRITICAL)  #取消注释关闭日志记录
debugInfo=open(r"debugInfo.txt","w+")
debugInfo.close()
logging.basicConfig(filename=r'C:/Users/艾/Desktop/debugInfo.txt',level=logging.DEBUG,format=' %(asctime)s - %(levelname)s - %(message)s')


url1_list=[r"http://www.xgb.zju.edu.cn",r"http://www.youth.zju.edu.cn",r"https://zhfw.zju.edu.cn"]

url2=r"https://service.zju.edu.cn/_s2/students_zxzx/main.psp"

url3=r"http://car.zju.edu.cn/index.php?c=Wei&a=car"
#请求头随机设置
fake_user_agent=UserAgent()
headers={}
headers["User-Agent"]=fake_user_agent.random
formdata={"username":"3210105952","password":"*********"}
#-------------------很遗憾，尽管前三个网站下载部分可以通用，但内容提取部分得分开，以下只适用于学工部------------
#全局变量保存内容 新闻链接 news_title
def url_spider1():
    """Here to make choice for the target website"""
    option_index=0

    res=requests.get(url1_list[option_index],headers=headers)
    res.encoding=res.apparent_encoding
    logging.critical(res.encoding.replace("\xa9","")) #gbk cannot solve '@' in unicode
    #handle the Chinese encoding problem
    logging.debug(res.text.replace('\xa9',''))    #checking if the problem is solved
    soup=bs4.BeautifulSoup(res.text.replace('\xa9',''),"html.parser")
    logging.debug(soup) #find what are we need
    division_content=soup.findAll("div",attrs={"news_title"})
    span_content=soup.findAll("span",attrs={"news_title"})
    news_content={}

    logging.debug(division_content)
    #.contents[0]
    for item in division_content:
        news_content[item.contents[0].text]=item.contents[0].attrs['href']
        logging.error(item.contents)
        if len(item.contents[0].text)<4:
            news_content.pop(item.contents[0].text)
            continue
        if not news_content[item.contents[0].text].startswith(r"http"):
            news_content[item.contents[0].text]=url1_list[option_index]+news_content[item.contents[0].text]
    for item in span_content:
        news_content[item.contents[0].text]=item.contents[0].attrs['href']
        logging.error(item.contents)
        if len(item.contents[0].text)<4:
            news_content.pop(item.contents[0].text)
            continue
        if not news_content[item.contents[0].text].startswith(r"http"):
            news_content[item.contents[0].text]=url1_list[option_index]+news_content[item.contents[0].text]
    
    #Here the news titles and urls are stored in dictionary form: news_content
    pprint.pprint(news_content)
    #全局变量保存内容 学院链接 link-item
    list_content=soup.findAll('li',attrs={"link-item"})
    school_content={}
    for item in list_content:
        for thing in item.contents:
            try:
                school_content[item.text]=thing.attrs['href']
                logging.error(item.contents)
            except:
                continue
        if not school_content[item.text].startswith(r"http"):
            school_content[item.text]=url1_list[option_index]+school_content[item.text]
    #Here the institute website are stored in dictionary form: school_content
    pprint.pprint(school_content)

    #注意到学工部图片内容放在名为 w11imgJsons 的数据结构中，使用BeautifulSoup无法直接提取，所以用上正则表达式
    model_regex=re.compile(r"(w11imgJsons)(.){1,40}(\[(.){1,100000}\])", re.DOTALL|re.VERBOSE)
    match=model_regex.search(res.text.replace('\xa9',''))
    img_content_code=match.group(3).replace('\t','').replace('\n','')
    #这里我们不需要图片，只要其中的text和url
    img_soup=bs4.BeautifulSoup(img_content_code,'html.parser')
    a_content=img_soup.select('a')
    img_content={}
    for item in a_content:
        img_content[item.text]=item.get('href')
        if len(item.text)<4:
            img_content.pop(item.text)
            continue
        if not img_content[item.text].startswith(r"http"):
            img_content[item.text]=url1_list[option_index]+img_content[item.text]
    pprint.pprint(img_content)
    #写入mysql部分,这里只导入一部分url
    """mysql_database=pymysql.Connect(host="localhost",user="root",password="*********",database="mysql",port=3306)
    cursor=mysql_database.cursor(cursor=pymysql.cursors.DictCursor)    
    table="news_information"
    news_information = [(k, v) for k, v in img_content.items()]
    sentence = 'INSERT %s (' % table + ';'.join([i[0] for i in news_information]) +') VALUES (' + ';'.join(repr(i[1]) for i in news_information) + ');'
    print(sentence)
    cursor.execute(sentence)
    mysql_database.commit()"""
    
    return None
    #这几个pprint主要方便展示结果，实际使用时可注释掉
url_spider1()
#-----------------------------学工部主要内容如上----------------------------


#------------------下面部分用于咨询中心网站-------------------------------------
def url_spider2():
    browser=webdriver.Firefox()
    target_URL=r"https://service.zju.edu.cn/_s2/students_zxzx/main.psp"
    browser.get(target_URL)
    #browser.fullscreen_window()
    #账号密码处理
    id_element=browser.find_element(by='id',value='username')
    id_element.click()
    id_element.send_keys("3210105952")#[1]这里填写您的账号
    password_element=browser.find_element(by='id',value='password')
    password_element.click()
    password_element.send_keys("*********\n")#[2]这里填写您的密码
    time.sleep(5)
    html_source=browser.page_source.replace('\u271a','').replace('\xa9','')
    logging.debug(html_source)
    browser.close()
    soup=bs4.BeautifulSoup(html_source,"html.parser")
    news_content=soup.findAll("div",attrs={"info-flex jump-dom"})
    news_data={} #用于存储新闻及其网址链接
    for item in news_content:
        news_data[item.text]=item.get("data-link")
        if len(item.text)<4:
                news_data.pop(item.text)
                continue
        if not news_data[item.text].startswith(r"http"):
            news_data[item.text]=r"http:"+news_data[item.text]
    pprint.pprint(news_data)
    #写入mysql部分
    """mysql_database=pymysql.Connect(host="localhost",user="root",password="******",database="mysql",port=3306)
    cursor=mysql_database.cursor(cursor=pymysql.cursors.DictCursor)    
    table="news_information"
    news_information = [(k, v) for k, v in news_data.items()]
    sentence = 'INSERT %s (' % table + ';'.join([i[0] for i in news_information]) +') VALUES (' + ';'.join(repr(i[1]) for i in news_information) + ');'
    print(sentence)
    cursor.execute(sentence)
    mysql_database.commit()"""
    
    return None
url_spider2()
#-----------------咨询中心主要内容如上------------------------------------
