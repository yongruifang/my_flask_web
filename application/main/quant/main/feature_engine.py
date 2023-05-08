import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
import jqdatasdk as jq
import re
from bs4 import BeautifulSoup
jq.auth('13192921466','A123456a')
import os
datadir = os.path.join(os.path.dirname(__file__), '..', 'data')

class GetInterceptorFeature:
    def __init__(self,code,end_day,max_window,afternoon,result):
        '''max_window should larger than any the maximun of T'''
        self.code = code
        self.end_day = end_day
        self.max_window = max_window
        self.afternoon = afternoon
        data = jq.get_bars(jq.normalize_code(self.code),count = self.max_window+1,\
            unit='1d',fields=['date', 'open', 'close', 'high', 'low', 'volume'],include_now=True,end_dt=self.end_day)
        self.result = result
        self.data=data
        self.date = data.date.values
        self.close = data.close.values
        self.volume = data.volume.values
        self.open = data.open.values
        self.low = data.low.values
        self.high = data.high.values
    def get_feature(self):
        '''R1是日收益率  zf是振幅   R2是收盘价/开盘价-1  deltaV是量的变化'''
        # 通过计算'close'的后一天/前一天-1得到日收益率
        R1 = self.close[1:]/self.close[:-1]-1 # [1:]是第二天到最后一天,[:-1]是第一天到倒数第二天
        # 通过计算'high'/'low'-1得到振幅 
        zf = self.high[1:]/self.low[1:]-1
        # 通过计算'close'/'open'-1得到收盘价/开盘价-1
        R2 = self.close[1:]/self.open[1:]-1
        # 通过计算'volume'的后一天/前一天-1得到量的变化
        deltaV = self.volume[1:]/self.volume[:-1]-1
        # 将以上数据转化为dataframe
        df = pd.DataFrame({'id':range(self.max_window),'R1':R1,'振幅':zf,'R2':R2,'deltaV':deltaV})
        df['date'] = self.date[1:]
        df['code'] = self.code
        return df


def execute():
    a = GetInterceptorFeature('601360',datetime(2023,4,24,0,0,0)+timedelta(hours=16),3,1,1)
    a = a.get_feature()
    df = pd.read_excel(os.path.join(datadir, '训练数据.xlsx'))
    df.date[0].date() # date[0]是一个datetime.datetime对象, 转化为date对象，不要时分秒
    feature_df=pd.DataFrame(columns=a.columns) # 创建一个空的dataframe
    for i in df.index: # 遍历行索引
        try:
            b=GetInterceptorFeature(df.code[i][-6:],df['date'][i]+timedelta(hours=16),10,df['afternoon'][i],df['胜负'][i])
            b=b.get_feature()
            # 列是一样的，所以可以新的一行b直接拼接到旧的dataframe上
            feature_df=pd.concat([feature_df,b],axis=0,ignore_index=True)
        except:
            print('bad>>>>>>>>')
    feature_df['code'] = 'code'+feature_df['code']
    feature_df.to_excel(os.path.join(datadir, '特征数据.xlsx'),columns=feature_df.columns,index=True)


def get_today_data(code,driver):
    # driver.quit()
    # 打开目标网页
    url = r'http://quote.eastmoney.com/{}.html'.format(code)
    driver.get(url)
    html = driver.page_source
    # 解析HTML代码
    soup = BeautifulSoup(html, 'html.parser')
    target_list = soup.find('div', {'class': 'sider_brief'}).find_all('td')
    close = target_list[0].text
    high = target_list[8].text
    low = target_list[9].text
    open_ = target_list[10].text
    volume = target_list[4].text
    data=[close,high,low,open_,volume]
    pattern = r'\d+\.?\d*'
    for i,num in enumerate(data):
        data[i] = float(re.findall(pattern,data[i])[0])
        if i == 4:
            data[i] = data[i]*1000000
    return data 

class GetInterceptorFeature_for_buy:
    driver = None
    def __init__(self,code,end_day,max_window,afternoon,driver):
        '''max_window should larger than any the maximun of T'''
        self.code = code
        self.end_day = end_day
        self.max_window = max_window
        self.afternoon = afternoon
        data = jq.get_bars(jq.normalize_code(self.code),count = self.max_window,\
            unit='1d',fields=['date', 'open', 'close', 'high', 'low', 'volume'],include_now=True,end_dt=self.end_day)
        self.data=data
        self.date = data.date.values
        self.close = data.close.values
        self.volume = data.volume.values
        self.open = data.open.values
        self.low = data.low.values
        self.high = data.high.values
        self.driver = driver
    def get_feature(self):
        '''R1是日收益率  zf是振幅   R2是收盘价/开盘价-1  deltaV是量的变化'''
        today_data =  get_today_data(self.code,self.driver)
        self.close = np.append(self.close,today_data[0])
        self.high = np.append(self.high,today_data[1])
        self.low = np.append(self.low,today_data[2])
        self.open = np.append(self.open,today_data[3])
        self.volume = np.append(self.volume,today_data[4])

        R1 = self.close[1:]/self.close[:-1]-1
        zf = self.high[1:]/self.low[1:]-1
        R2 = self.close[1:]/self.open[1:]-1
        deltaV = self.volume[1:]/self.volume[:-1]-1
        df = pd.DataFrame({'R1':R1,'振幅':zf,'R2':R2,'deltaV':deltaV})
        df['afternoon'] = self.afternoon
        return df

if __name__ == '__main__':
    execute()
