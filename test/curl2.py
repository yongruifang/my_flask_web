import threading
import requests
from bs4 import BeautifulSoup

# 定义要尝试的股票代码
stock_code = '002362'

# 定义请求函数
def request_url(prefix):
    url = f'http://quote.eastmoney.com/{prefix}{stock_code}.html'
    response = requests.get(url,timeout=1000)
    if response.status_code == 200:
        html = response.text  # 获取HTML代码
        print(f"成功访问 {url}")
        return html
    else:
        print(f"访问 {url} 失败")

# 创建线程
threads = []
prefixes = ['sh', 'sz']

results = []  # 存储请求结果

for prefix in prefixes:
    thread = threading.Thread(target=lambda: results.append(request_url(prefix)))
    threads.append(thread)

# 启动线程
for thread in threads:
    thread.start()

# 等待所有线程完成
for thread in threads:
    thread.join()

# 输出请求结果
for result in results:
    if result:
        print("返回的HTML代码:", result)
        soup = BeautifulSoup(result, 'html.parser')
        target_list = soup.find('div', {'class': 'sider_brief'}).find_all('td')
        close = target_list[0].text
        high = target_list[8].text
        low = target_list[9].text
        open_ = target_list[10].text
        volume = target_list[4].text
        data=[close,high,low,open_,volume]
        print(data)


print("所有尝试完成")
