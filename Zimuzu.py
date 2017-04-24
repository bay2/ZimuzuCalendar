from bs4 import BeautifulSoup
from Download import request
from pymongo import MongoClient
import re



class Zimuzu:

    def __init__(self):
        self.host = 'http://www.zmz2017.com'
        self.allUrl = self.host + '/tv/eschedule'
        self.calendarDic = {}

    def fectYear(self, html):

        Soup = BeautifulSoup(html, 'lxml')
        # 查找年月
        yearDivText = Soup.find('div', class_='middle-box') \
            .find('div', class_='corner') \
            .get_text()
        m = re.match(r'\d*月(\d*)年(\d*)月', yearDivText)
        return m.group(1)

    def fectMonth(self, html):

        Soup = BeautifulSoup(html, 'lxml')
        # 查找年月
        yearDivText = Soup.find('div', class_='middle-box') \
            .find('div', class_='corner') \
            .get_text()
        m = re.match(r'\d*月(\d*)年(\d*)月', yearDivText)
        return m.group(2)

    # 当月的HTML
    def getCurMonthHtml(self):
        start_html = request.get(self.allUrl)
        return start_html


    # 抓取解析数据
    def fecthData(self, html):

        Soup = BeautifulSoup(html, 'lxml')
        all_td = Soup.find_all('td', class_='ihbg ')

        monthDataCount = 0
        monthDic = {}

        for td in all_td:
            dayText = td.find('dt').text
            day = re.match(r'(\d*)号', dayText)
            all_dd = td.find_all('dd')
            ddArray = []
            for dd in all_dd:
                ddArray = ddArray + [dd.text]
                monthDataCount += 1
            monthDic[day.group(1)] = ddArray

        if monthDataCount == 0:
            return {}

        return monthDic


    # 下个月的HTML
    def getNextMonthHtml(self, html):
        Soup = BeautifulSoup(html, 'lxml')
        next_url = self.host + Soup.find('a', class_='r')['href']
        next_html = request.get(next_url)
        return next_html.text

    def getPreMonthHtml(self, html):
        Soup = BeautifulSoup(html, 'lxml')
        next_url = self.host + Soup.find('a', class_='l')['href']
        next_html = request.get(next_url)
        return next_html.text



    # 向后抓取数据
    def backwardFecth(self, html):

        nextHtml = html
        resultDic = self.fecthData(nextHtml)
        if len(resultDic) <= 0:
            return
        year = self.fectYear(nextHtml)
        month = self.fectMonth(nextHtml)
        if self.calendarDic.get(year) == None:
            self.calendarDic[self.fectYear(nextHtml)] = {
                self.fectMonth(nextHtml): self.fecthData(nextHtml)
            }
        else:
            yearDic = self.calendarDic[year]
            yearDic[month] = self.fecthData(nextHtml)

        nextHtml = self.getNextMonthHtml(nextHtml)
        self.backwardFecth(nextHtml)

    def forwardFecth(self, html):

        preHtml = html
        resultDic = self.fecthData(preHtml)
        if len(resultDic) <= 0:
            return
        year = self.fectYear(preHtml)
        month = self.fectMonth(preHtml)
        if self.calendarDic.get(year) == None:
            self.calendarDic[year] = {
                month: self.fecthData(preHtml)
            }
        else:
            yearDic = self.calendarDic[year]
            yearDic[month] = self.fecthData(preHtml)

        preHtml = self.getPreMonthHtml(preHtml)
        self.forwardFecth(preHtml)

zm = Zimuzu()
start_html = zm.getCurMonthHtml()
if start_html != None and start_html.text != None:
    zm.backwardFecth(start_html.text)
    zm.forwardFecth(zm.getPreMonthHtml(start_html.text))

print(zm.calendarDic)

client = MongoClient()
db = client['zimuzu']
meizitu_collection = db['calendar']
meizitu_collection.save(zm.calendarDic)


