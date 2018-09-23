import numpy as np
import pandas as pd
import json
import glob
from PIL import Image
from keras.models import Sequential
from keras.layers.core import Dense, Flatten
from keras.layers import Conv2D, MaxPool2D, Dropout
from keras.utils import to_categorical
from keras.optimizers import SGD
from sklearn.preprocessing import LabelBinarizer
from keras.regularizers import l1

SERIE_INDEX = ['img', 'steering', 'throttle', 'brake']

def load_data():
    records = glob.glob('log/record_*.json')
    X = []
    Y = []
    for rec in records:
        rec = load_record(rec)
        X.append(load_image(rec['cam/image_array']))
        Y.append([rec['user/throttle'], rec['user/brake'], rec['user/steering']])
    return np.array(X), np.array(Y)
    

def load_record(filename):
    with open(filename) as f:
        return json.load(f)
        
        

def load_image( infilename ) :
    img = Image.open( 'log/' + infilename )
    img.load()
    data = np.asarray( img, dtype="int32" )
    return data

def read_record(record_dict):
        data = {}
        for key, val in record_dict.items():
            typ = self.get_input_type(key)

            # load objects that were saved as separate files
            if typ == 'image_array':
                img = Image.open((val))
                val = np.array(img)

            data[key] = val
        return data

X, Y = load_data()

model = Sequential()

model.add(Conv2D(filters=32,
                 kernel_size=(3, 3),
                 activation='relu',
                 padding='same',
                 kernel_regularizer=l1(0.01),
                 input_shape=(120, 160, 3))),


model.add(Conv2D(filters=32,
                 kernel_size=(3, 3),
                 padding='same',
                 kernel_regularizer=l1(0.01),
                 activation='relu'))

model.add(MaxPool2D(2, 2))

model.add(Conv2D(filters=32,
                 kernel_size=(3, 3),
                 padding='same',
                 kernel_regularizer=l1(0.01),
                 activation='relu'))

model.add(Conv2D(filters=32,
                 kernel_size=(3, 3),
                 padding='same',
                 kernel_regularizer=l1(0.01),
                 activation='relu'))

model.add(MaxPool2D(2, 2))

model.add(Conv2D(filters=32,
                 kernel_size=(3, 3),
                 padding='same',
                 kernel_regularizer=l1(0.01),
                 activation='relu'))

model.add(Conv2D(filters=32,
                 kernel_size=(3, 3),
                 padding='same',
                 kernel_regularizer=l1(0.01),
                 activation='relu'))

model.add(MaxPool2D(2, 2))

model.add(Flatten())

model.add(Dense(128, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(128, activation='relu'))

model.add(Dense(3, activation='softmax'))

model.summary()

model.compile(optimizer="SGD", loss="categorical_crossentropy", metrics=["accuracy"])

model.fit(X, Y, epochs=100)
