import joblib
from .feature_engine import GetInterceptorFeature_for_buy
import tensorflow as tf
from datetime import datetime
from msedge.selenium_tools import Edge, EdgeOptions
import math
# 如果是直接 import datetime ，那么就要用 datetime.datetime.today() 来获取当前时间
import os
datadir = os.path.join(os.path.dirname(__file__), '..', 'data')
modeldir = os.path.join(os.path.dirname(__file__), '..', 'model')

def execute(morning_stock,afternoon_stock):
    result = []
    # 创建webDriver对象
    options = EdgeOptions()
    options.use_chromium = True
    options.add_argument('--headless')  # 隐藏浏览器窗口
    driver = Edge(executable_path="msedgedriver.exe", options=options)
    transfer = joblib.load(os.path.join(datadir, '标准化器.pkl'))
    wr_model = tf.keras.models.load_model(os.path.join(modeldir, 'model.h5'))
    for code in morning_stock:
        class_GIF=GetInterceptorFeature_for_buy(code,datetime.today(),10,0,driver)
        a=class_GIF.get_feature()
        a = transfer.transform(a)
        a = a.reshape(-1,10,5)
        result.append(math.ceil(wr_model.predict(a)[0][0]*100))
    for code in afternoon_stock:
        class_GIF=GetInterceptorFeature_for_buy(code,datetime.today(),10,1,driver)
        a=class_GIF.get_feature()
        a = transfer.transform(a)
        a = a.reshape(-1,10,5)
        result.append(math.ceil(wr_model.predict(a)[0][0]*100))
    driver.quit()
    return result


if __name__ == '__main__':
    # print(datetime.today())
    execute(morning_stock=['002174','601858'],afternoon_stock=['600661','002517'])

