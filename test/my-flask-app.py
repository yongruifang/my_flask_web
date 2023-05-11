from flask import Flask,request,jsonify
import jqdatasdk as jq
import datetime
import pandas as pd
app = Flask(__name__)

@app.route('/acquire_data', methods=['POST'])
def acquire_data():
    # data = request.get_json()
    code = request.json.get('code')
    count = request.json.get('count')
    end_day = datetime.datetime.strptime(request.json.get('end_day'),'%Y-%m-%d %H:%M:%S')
    result = jq.get_bars(jq.normalize_code(code),count = count,\
            unit='1d',fields=['date', 'open', 'close', 'high', 'low', 'volume'],include_now=True,end_dt=end_day)
    print(result)
    # return result.to_json()
    # 可以使用jsonify(df)方法将Pandas DataFrame对象转换为JSON格式的响应。jsonify()函数是Flask框架中的一个内置函数，用于将Python对象转换为JSON格式的响应，可以直接返回JSON响应。因此，使用jsonify()方法比使用df.to_json()方法更方便。
    # return jsonify(result)
    return jsonify(data=result.to_json())


@app.route('/')
def index():
    return '<h1>Hello World</h1>'

if __name__ == '__main__':
    jq.auth('13192921466','A123456a')
    app.run(port=8888,debug=True)