import time, pandas as pd, matplotlib.pyplot as plt, numpy as np
from keras.layers import *
from keras.models import *
from keras.callbacks import EarlyStopping
from pprint import *

MAX_FEATURE = 4
TESTNUM = 100000

def main():
    data = pd.read_csv(r'womadSet_v3.csv', encoding='utf-8')
    data['from'] = data['from'].replace(['womad','joong'],[0,1])
    x_train, y_train = data[['from', 'w1', 'w2', 'w3', 'j1', 'j2', 'j3', 'run']][:TESTNUM].astype(int), data['from'][:TESTNUM]
    # print(x_train.values)

    numTrain = int(TESTNUM*0.8)
    numTest = len(x_train) - numTrain

    x_test = x_train.values[numTrain:]
    y_test = y_train.values[numTrain:]
    x_train = x_train.values[:numTrain]
    y_train = y_train.values[:numTrain]

    model = Sequential()
    # erStop = EarlyStopping(monitor='val_loss', patience=3, mode='min')

    model.add(Dense(16, input_dim=8, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    tHist = model.fit(x_train, y_train, epochs=30, batch_size=64, validation_data=(x_test, y_test))
    model.save('womad_freq_model_%d.h5'%TESTNUM, include_optimizer=True)

    fig, loss_ax = plt.subplots()

    acc_ax = loss_ax.twinx()

    loss_ax.plot(tHist.history['loss'], 'y', label='train loss')
    loss_ax.plot(tHist.history['val_loss'], 'r', label='val loss')

    acc_ax.plot(tHist.history['acc'], 'b', label='train acc')
    acc_ax.plot(tHist.history['val_acc'], 'g', label='val acc')

    loss_ax.set_xlabel('epoch')
    loss_ax.set_ylabel('loss')
    acc_ax.set_ylabel('accuray')

    loss_ax.legend(loc='upper left')
    acc_ax.legend(loc='lower left')

    plt.savefig('womad_freq_result_%d.png'%TESTNUM)
    plt.show()
    print("\n Accuracy: %.3f" % (model.evaluate(x_test, y_test)[1]))

if __name__ == '__main__':
    beg = time.time()
    main()
    print("--- %.6f sec(s) ---" % (time.time() - beg))
