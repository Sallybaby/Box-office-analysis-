
import requests
from bs4 import BeautifulSoup
import re
import datetime


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36"}

#用于将一个列表平均分成多个列表
def list_of_groups(init_list, childern_list_len):
    list_of_groups = zip(*(iter(init_list),) *childern_list_len)
    end_list = [list(i) for i in list_of_groups]
    count = len(init_list) % childern_list_len
    end_list.append(init_list[-count:]) if count !=0 else end_list
    return end_list

#由于该网站可以查询指定日期的票房情况
#日期函数
def dateRange(beginDate, endDate):
    dates = []
    dt = datetime.datetime.strptime(beginDate, "%Y-%m-%d")
    date = beginDate[:]
    while date <= endDate:
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y-%m-%d")
    return dates
#爬取网页数据
def get_data(date):
    data={"riqi":date}
    url="http://www.piaofang168.com/index.php/Jinzhun"
    res=requests.post(url,headers=headers,data=data)
    res.encoding='utf-8'
    soup=BeautifulSoup(res.text,'html.parser')
    data=soup.select('.gross_table')[0].text.split()
    del data[0]
    Datetime=data[1]
    del data[0]
    newdata=list_of_groups(data,6)
    #print(newdata)
    dataFileName = 'piaofang168.txt'
    file_to_write = open(dataFileName,'a',encoding='utf-8')
    file_to_write.write("上映时间，当日票房，累计票房，当日排片，上座率，上映天数\n")
    for i in range(len(newdata)):
        #将列表转换成字符串
        text=",".join(newdata[i])
        file_to_write.write(text + '\n')
        print(text)
    file_to_write.close()

if __name__ == '__main__':
    beginDate = str(input("请输入要查询数据的开始时间（年-月-日）:"))
    endDate = str(input("请输入要查询数据的结束时间（年-月-日）:"))
    dates = dateRange(beginDate, endDate)
    for date in dates:
        get_data(date)
