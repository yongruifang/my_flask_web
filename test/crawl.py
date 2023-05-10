import requests
from bs4 import BeautifulSoup
import re
import time

url = 'http://quote.eastmoney.com/sz002362.html'

# 发送HTTP GET请求并获取响应
response = requests.get(url,timeout=1000)

time.sleep(5)

# 检查请求是否成功，如果不成功则抛出异常
response.raise_for_status()


# 使用BeautifulSoup解析响应HTML代码
soup = BeautifulSoup(response.text, 'html.parser')
# if soup.title.text == '':
#     print('None')
# 输出网页标题
print(soup.title.text)
target_list = soup.find('div', {'class': 'sider_brief'}).find_all('td')
print(target_list)
# [<td>最新：-</td>, <td>均价：-</td>, <td>涨幅：-</td>, <td>涨跌：-</td>, <td>总手：-</td>, <td>金额：-</td>, <td> 换手：-</td>, <td>量比：-</td>, <td>最高：-</td>, <td>最低：-</td>, <td>今开：-</td>, <td>昨收：-</td>, <td>涨停 -</td>, <td>跌停：-</td>, <td>外盘：-</td>, <td>内盘：-</td>]
close = target_list[0].text
high = target_list[8].text
low = target_list[9].text
open_ = target_list[10].text
volume = target_list[4].text
data=[close,high,low,open_,volume]
# print(data)
# pattern = r'\d+\.?\d*'
# for i,num in enumerate(data):
#     data[i] = float(re.findall(pattern,data[i])[0])
#     if i == 4:
#         data[i] = data[i]*1000000

# print(data)