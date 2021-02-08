#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date: 2021/01/29 Fri
# @Author: ShayXU
# @Filename: captcha_classifier.py


"""
    keras 搭个cnn应该就行了吧


    可以到95？
    60 * 95 = 57%

    # to_do

"""


import tensorflow as tf
import tensorboard
from tensorflow import keras

import numpy as np

def train_model():
    print('\n'*10)
    # 读取图片 tf.data.Dataset 默认双线性插值 bilinear
    train_ds = keras.preprocessing.image_dataset_from_directory(
        "img_output/", image_size=(40, 40), subset="training", validation_split=0.2,
        seed=123
    )

    val_ds  = keras.preprocessing.image_dataset_from_directory(
        "img_output/", labels='inferred', image_size=(40, 40), subset="validation", validation_split=0.2,
        seed=123
    )
    # train_ds.class_names

    model = keras.models.Sequential()
    model.add(keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(40, 40, 3)))
    model.add(keras.layers.MaxPooling2D((2, 2)))
    model.add(keras.layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(keras.layers.MaxPooling2D((2, 2)))
    model.add(keras.layers.Conv2D(64, (3, 3), activation='relu'))

    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(64, activation='relu'))
    model.add(keras.layers.Dense(len(train_ds.class_names)))

    # model.summary()

    model.compile(optimizer='adam', 
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    model.fit(train_ds, validation_data=val_ds, epochs=1)
    tf.saved_model.save(model, 'saved_model/')
    # pretrained_model = tf.saved_model.load('saved_model/')


def predict(img_path='img_output/2/6.gif'):
    # 类别
    class_names = list('23456789abcdefghjkmnopqrstuvwxyz')

    # 读取模型
    model = tf.saved_model.load('saved_model/')

    # 读取图片
    img = keras.preprocessing.image.load_img(
        img_path, target_size=(40, 40), color_mode='rgb', interpolation='bilinear'
    )
    img_array = keras.preprocessing.image.img_to_array(img)     # 转成数组
    img_array = tf.expand_dims(img_array, 0)                    # Create a batch

    # 预测
    predictions = model(img_array)          # (1, 32) 每一类有个预测值
    score = tf.nn.softmax(predictions[0])   # (32,)   通过softmax转换成概率

    print(
        "This image most likely belongs to {} with a {:.2f} percent confidence."
        .format(class_names[np.argmax(score)], 100 * np.max(score))
    )

if __name__ == "__main__":
    # train_model()
    predict()


