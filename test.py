from collections import defaultdict
import requests
import time
from bs4 import BeautifulSoup

def get_weather(st):
    url = 'https://www.cwb.gov.tw/V7/forecast/taiwan/'+record[1]+'.htm'
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'lxml')
    rowsss = soup.find('table', attrs={'class':'FcstBoxTable01'})
    roe = rowsss.find_next('tbody')
    rows = roe.find_all('tr')
    content=[]
    aa= a+"天氣:"
    content.append(aa)
    for row in rows:
        times = row.find_next('th')
        temperatures = times.find_next('td')
        temperature = "溫度:"+temperatures.text
        re = temperatures.find_next('td')
        weather = re.find_next('img')
        weather = weather.get('title')
        weather = "天氣狀況:"+weather
        comforts = re.find_next('td')
        comfort = "舒適度:"+comforts.text
        rain = comforts.find_next('td')
        rain = "降雨機率:"+rain.text
        
        content.append(times.text)
        content.append(temperature)
        content.append(weather)
        content.append(comfort)
        content.append(rain)
        content.append("=========")
    return content
print('請輸入縣市名稱:')
a = input()
tracks = [["台北", "Taipei_City"],["新北", "New_Taipei_City"],
          ["基隆","Keelung_City"],["台中","Taichung_City"],
          ["台南","Tainan_City"],["高雄","Kaohsiung_City"],
          ["新竹","Hsinchu_City"],["桃園","Taoyuan_City"],
          ["屏東","Pingtung_County"],["花蓮","Hualien_County"],
          ["台東","Taitung_County"],["苗栗","Miaoli_County"],
          ["彰化","Changhua_County"],["南投","Nantou_County"],
          ["雲林","Yunlin_County"],["嘉義","Chiayi_County"],
          ["宜蘭","Yilan_County"],["澎湖","Penghu_County"]]

for record in tracks:
    for data in record:
        if data == a:
            gg = get_weather(a)
            b ='\n'.join(gg)
            print(b)

                    
            