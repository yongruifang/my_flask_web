
from msedge.selenium_tools import Edge, EdgeOptions
from bs4 import BeautifulSoup

code = '600705'
# 创建webDriver对象
options = EdgeOptions()
options.use_chromium = True
options.add_argument('--headless')  # 隐藏浏览器窗口
driver = Edge(executable_path="msedgedriver.exe", options=options)

# 打开目标网页
url = r'http://quote.eastmoney.com/{}.html'.format(code)
driver.get(url)
html = driver.page_source
# 解析HTML代码
soup = BeautifulSoup(html, 'html.parser')
# print(soup)
# 输出到文件
# with open('output.html', 'w', encoding='utf-8') as f:
#     f.write(str(soup))

texts = soup.title.text.split(' ')
name = texts[0]
print(name)
driver.quit()