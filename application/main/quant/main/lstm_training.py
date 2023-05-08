import tensorflow as tf
import pandas as pd
# pip install scikit-learn
from sklearn.preprocessing import StandardScaler    #标准化
import joblib
import matplotlib.pyplot as plt
from matplotlib import rc
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import os
datadir = os.path.join(os.path.dirname(__file__), '..', 'data')
modeldir = os.path.join(os.path.dirname(__file__), '..', 'model')

plt.rcParams['font.sans-serif']= ['SimHei']
plt.rcParams['axes.unicode_minus']= False
rc('mathtext', default='regular')
sns.set_style('whitegrid') 

def execute():
    df = pd.read_excel(os.path.join(datadir, 'new特征数据.xlsx'),index_col=0)
    del df['date']
    del df['code']
    del df['id']
    del df['jdqs10']
    X = df.values[:,:-1]
    transfer = StandardScaler()
    X = transfer.fit_transform(X)
    joblib.dump(transfer,os.path.join(datadir, '标准化器.pkl'))
    X_3d = X.reshape((-1, 10, 5)) 
    y = df['result'].values+1
    y[y==0]=1
    y=y-1
    y=y.reshape(-1,10).mean(axis=1)
    X_3d=X_3d[:,-5:,:]
    X1, X2, y1, y2 = train_test_split(X_3d, y, random_state=6666,
                                  train_size=0.8)
    # 定义超参数和模型结构
    num_units = 13
    num_layers = 2
    batch_size = 20
    learning_rate = 0.0003
    # 创建RNN模型
    model = tf.keras.Sequential()
    #model.add(tf.keras.layers.LSTM(22, dropout=0.3,recurrent_activation='leaky_relu',return_sequences=True)),
    model.add(tf.keras.layers.LSTM(22, dropout=0.4,recurrent_activation='leaky_relu',kernel_regularizer=tf.keras.regularizers.l2(0.001)))
    #model.add(tf.keras.layers.SimpleRNN(units=num_units, return_sequences=False, input_shape=(3, 4)))
    model.add(tf.keras.layers.Dense(units=10, activation='leaky_relu',kernel_regularizer=tf.keras.regularizers.l2(0.001)))
    model.add(tf.keras.layers.Dropout(0.3))
    model.add(tf.keras.layers.Dense(units=1, activation=tf.nn.sigmoid))
    # 定义损失函数和优化器
    loss_fn = tf.keras.losses.BinaryCrossentropy()
    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
    # 编译模型
    model.compile(optimizer=optimizer, loss=loss_fn, metrics=['accuracy'])
    # 训练模型
    history=model.fit(X1, y1, batch_size=batch_size, epochs=200,validation_data=(X2,y2))
    plt.plot(history.epoch,history.history['accuracy'],linestyle ="-",linewidth=2,label="训练准确率")
    plt.plot(history.epoch,history.history['val_accuracy'],linewidth=2,label="测试准确率")
    plt.xlabel("迭代次数",fontsize=16)
    plt.ylabel("模型准确率",fontsize=16)
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    plt.legend(fontsize=13)
    plt.title('赔率拦截器训练过程')
    plt.savefig(os.path.join(datadir, '赔率拦截器训练过程.png'),dpi = 300)
    #model.save(os.path.join(modeldir, '二分类模型.h5')
    y2_model=(model.predict(X2)>0.5)[:,0]
    print(confusion_matrix(y2, y2_model))

if __name__ == '__main__':
    execute()
    