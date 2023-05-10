import requests
from bs4 import BeautifulSoup
import re

url = 'http://quote.eastmoney.com/sh002174.html'

# 发送HTTP GET请求并获取响应
response = requests.get(url)

# 检查请求是否成功，如果不成功则抛出异常
response.raise_for_status()

# 使用BeautifulSoup解析响应HTML代码
# soup = BeautifulSoup(response.text, 'html.parser')
# print(soup)
# if soup.title.text == '':
#     print('None')
# 输出网页标题
# print(soup.title.text)
# target_list = soup.find('div', {'class': 'sider_brief'}).find_all('td')
# print(target_list)
# close = target_list[0].text
# high = target_list[8].text
# low = target_list[9].text
# open_ = target_list[10].text
# volume = target_list[4].text
# print(volume)
# data=[close,high,low,open_,volume]
# pattern = r'\d+\.?\d*'
# for i,num in enumerate(data):
#     data[i] = float(re.findall(pattern,data[i])[0])
#     if i == 4:
#         data[i] = data[i]*1000000

# print(data)