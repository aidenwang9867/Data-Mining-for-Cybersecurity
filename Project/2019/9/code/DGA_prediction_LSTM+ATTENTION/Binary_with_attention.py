from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers.core import Dense
from keras.layers.core import Dropout
from keras.layers.core import Activation
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM
from keras.models import load_model
from keras.layers import merge
from keras.layers.core import *
from keras.models import *
import numpy as np

def linear_attention_global(inputs,TIME_STEPS):
    # inputs.shape = (batch_size, time_steps, input_dim)
    a = Permute((2, 1))(inputs)                             # 128*75
    a = Dense(TIME_STEPS, activation='softmax')(a)          # 128*75
    a_probs = Permute((2, 1), name='attention_vec')(a)
    output_attention_mul = merge([inputs, a_probs], name='attention_mul', mode='mul')
    return output_attention_mul


def nonlinear_attention_relu(inputs,TIME_STEPS):
    a = Permute((2, 1))(inputs)
    a = Dense(TIME_STEPS, activation='softmax')(a)
    a = Dense(30, activation='relu')(a)
    a = Dense(TIME_STEPS, activation='softmax')(a)
    a_probs = Permute((2, 1), name='attention_vec')(a)
    output_attention_mul = merge([inputs, a_probs], name='attention_mul', mode='mul')
    return output_attention_mul

def nonlinear_attention_tanh(inputs,TIME_STEPS):
    a = Permute((2, 1))(inputs) 
    a = Dense(TIME_STEPS, activation='softmax')(a)
    a = Dense(30, activation='tanh')(a)
    a = Dense(TIME_STEPS, activation='softmax')(a)
    a_probs = Permute((2, 1), name='attention_vec')(a)
    output_attention_mul = merge([inputs, a_probs], name='attention_mul', mode='mul')
    return output_attention_mul

# 1/2维换维，用于连接RNN和全连接层

def model_attention_applied_after_lstm(shape, max_features):
    inputs = Input(shape=(shape,))
    a = Embedding(max_features, 128, input_length=shape)(inputs)
    lstm_out = LSTM(128, return_sequences=True)(a)  # 返回值 (time_steps, input_dim) = (75,128)

    # attention_mul = linear_attention_global(lstm_out, 75)
    # attention_mul = nonlinear_attention_relu(lstm_out, 75)
    attention_mul = nonlinear_attention_tanh(lstm_out, 75)

    attention_mul = Flatten()(attention_mul)    # 折叠成一维向量
    a = Dropout(0.5)(attention_mul)
    a = Dense(1)(a)
    outputs = Activation('sigmoid')(a)
    model = Model(input=[inputs], output=outputs)

    return model




def train(max_features, X_train, y_train, batch_size, epochs, modelPath):

    X_train = sequence.pad_sequences(X_train, maxlen=75)
    model = model_attention_applied_after_lstm(75, max_features)

    model.compile(loss='binary_crossentropy',optimizer='rmsprop')
    model.fit(X_train, y_train, batch_size=batch_size, epochs=epochs)

    model.save(modelPath)



def predict(X_test, batch_size, modelPath, resultPath):
    X_test = sequence.pad_sequences(X_test, maxlen=75)
    my_model = load_model(modelPath)
    y_test = my_model.predict(X_test, batch_size=batch_size).tolist()

    file = open(resultPath, 'w+')
    for index in y_test:
        y = float(str(index).strip('\n').strip('\r').strip(' ').strip('[').strip(']'))
        file.write(str(y) + '\n')
