import requests
import json
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
import pymysql

# db = pymysql.connect(host='localhost',user='root',password='0000',db='sheepyeeee_news',charset='utf8')
# cur = db.cursor()

#聯合內文
def t_udn(url):

    resp = requests.get(url)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'lxml')
    ros = soup.find('div', attrs={'id':'story_body_content'})
    title = ros.find_next('h1')#標題
    timewho = title.find_next('div',attrs={'class':'story_bady_info_author'})#發布時間 記者
    # rows = ros.find_all('p')
    content=[]
    content.append(url)
    content.append(title.text)
    content.append(timewho.text)
    detail = soup.select("#story_body_content > p")
    content.append(detail)

    return content

#自由內文
def t_free(url):

    resp = requests.get(url)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'lxml')
    ros = soup.find('div', attrs={'class':'whitecon'})
    title = ros.find_next('h1')#標題
    content=[]
    content.append(url)
    content.append(title.text)
    detail = soup.select(".text")
    content.append(detail)

    return content


#tvbs內文
def t_tvbs(url):

    resp = requests.get(url)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'lxml')
    ros = soup.find('div', attrs={'class':'title'})
    title = ros.find_next('h1',attrs={'class':'margin_b20'})#標題
    who = title.find_next('h4',attrs={'class':'font_color5'})#報導者
    time = who.find_next('div')#發布時間
    content=[]
    content.append(url)
    content.append(title.text)
    content.append(who.text)
    content.append(time.text)

    detail = soup.select(".newsdetail_content > .contxt")
    content.append(detail)
    
    return content

#中時內文
def t_ct(url):
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'lxml')
    re = soup.find('header',attrs={'class':'article-header'})
    title = re.find_next('h1',attrs={'class':'article-title'})#標題
    content=[]
    content.append(url)
    content.append(title.text)

    about = title.find_next('div',attrs={'class':'meta-info'})
    times = about.find_next('time')
    time = times.get('datetime')
    content.append(time)
    who = times.find_next('div',attrs={'class':'author'})
    content.append(who.text)

    pic = soup.select(".main-figure")
    content.append(pic)

    detail = soup.select(".article-body")
    content.append(detail)
    
    return content

# print(t_ct('https://www.chinatimes.com/realtimenews/20190502002477-260405?chdtv'))


def mail_news(url,usermail):
    tilte=" "
    if "https://udn.com/" in url:
        a = t_udn(url)
        href = a[0]
        title = a[1]
        time = a[2]
        detail = a[3]
        # detail=[i.replace('li','') for i in detail]

        details=" ".join('%s' %i for i in detail)
        details = details.replace('分享','') 
        details = details.replace('facebook','')
        details = details.replace('<ul> <li class=""><a href="#" title=""></a></li> </ul>','')
        mail_msg = """
                <!DOCTYPE html>
                <html lang="zh-Hant-TW">
                <head>
                    <meta charset="utf-8">
                    <title></title>
                    
                </head>
                <body style="color:#000;width:90%;margin-left:5px;">
                    <div style="color:#000;margin:0 auto;">
                        <h1 style="color:#000;">{title}</h1>
                        <div style="width:85%;position: relative;">
                            <span style="color:dimgrey;float:left;">{time}</span>
                            <span><a href="{href}" style="float:right;">原文連結</a></span>
                        </div>
                        <div style="width:90%;margin-top: 40px; float:left;font-size:14px;">{details}</div>
                    </div>
                </body>
                </html>
                """.format(**locals())

    elif "https://news.ltn.com.tw/" in url:
        a = t_free(url)
        href = a[0]
        title = a[1]
        detail = a[2]
        details=" ".join('%s' %i for i in detail)
        details = details.replace('<li>','')
        details = details.replace('</li>','')
        mail_msg = """
                <!DOCTYPE html>
                <html lang="zh-Hant-TW">
                <head>
                    <meta charset="utf-8">
                    <title></title>
                    
                </head>
                <body style="color:#000;width:90%;margin-left:5px;">
                    <div style="color:#000;margin:0 auto;">
                        <h1 style="color:#000;">{title}</h1>
                        <div style="width:85%;position: relative;">
                            <span><a href="{href}" style="float:left;">原文連結</a></span>
                        </div>
                        <div style="width:90%;margin-top: 40px; float:left;font-size:14px;">{details}</div>
                    </div>
                </body>
                </html>
                """.format(**locals())
    elif "https://news.tvbs.com.tw" in url:
        a = t_tvbs(url)
        href = a[0]
        title = a[1]
        who = a[2]
        time = a[3]
        detail = a[4]
        details=" ".join('%s' %i for i in detail)
        mail_msg = """
                <!DOCTYPE html>
                <html lang="zh-Hant-TW">
                <head>
                    <meta charset="utf-8">
                    <title></title>
                    
                </head>
                <body style="color:#000;width:90%;margin-left:5px;">
                    <div style="color:#000;margin:0 auto;">
                        <h1 style="color:#000;">{title}</h1>
                        <div style="width:90%;position: relative;">
                            <span style="color:dimgrey;float:left;margin-right:5px;">{who}</span>
                            <span style="color:dimgrey;float:left;">{time}</span>
                            <span><a href="{href}" style="float:right;">原文連結</a></span>
                        </div>
                        <div style="width:90%;margin-top: 40px; float:left;font-size:14px;">{details}</div>
                    </div>
                </body>
                </html>
                """.format(**locals())
    elif "https://www.chinatimes.com" in url:
        a = t_ct(url)
        href = a[0]
        title = a[1]
        time = a[2]
        who = a[3]
        pic = a[4]
        pic=" ".join('%s' %i for i in pic)
        detail = a[5]
        details=" ".join('%s' %i for i in detail)
        mail_msg = """
                <!DOCTYPE html>
                <html lang="zh-Hant-TW">
                <head>
                    <meta charset="utf-8">
                    <title></title>
                    
                </head>
                <body style="color:#000;width:90%;margin-left:5px;">
                    <div style="color:#000;margin:0 auto;">
                        <h1 style="color:#000;">{title}</h1><br>
                        <div style="width:85%;padding-bottom:25px;">
                            <span style="color:dimgrey;float:left;margin-right:5px;">{who}</span>
                            <span style="color:dimgrey;float:left;">{time}</span>
                            <span><a href="{href}" style="float:right;">原文連結</a></span>
                        </div>
                        <div style="width:90%;">{pic}</div>
                        <div style="width:90%;margin-top: 40px; float:left;font-size:14px;">{details}</div>
                    </div>
                </body>
                </html>
                """.format(**locals())

    sender = 'xiaoxuanlai233@gmail.com'
    passwd = 'lili23070'
    receivers = usermail



    msg = MIMEText(mail_msg, 'html', 'utf-8')
    subject = "SheepYeeee幫你把新聞寄過來了喔"
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = sender
    msg['To'] = receivers

    smtp = smtplib.SMTP("smtp.gmail.com:587")
    smtp.ehlo()
    smtp.starttls()
    smtp.login(sender, passwd)
    smtp.sendmail(sender, receivers, msg.as_string())

    return print('Send mails to',msg['To'])


# mail_news('https://www.chinatimes.com/realtimenews/20190502001899-260402?chdtv')


