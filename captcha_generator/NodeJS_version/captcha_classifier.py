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
    保存训练完的参数
    predict

"""


import tensorflow as tf
import tensorboard
from tensorflow import keras

if __name__ == "__main__":
    print('\n'*10)
    # 读取图片 tf.data.Dataset
    train_ds = keras.preprocessing.image_dataset_from_directory(
        "img_output/", image_size=(40, 40), subset="training", validation_split=0.2,
        seed=123
    )

    val_ds  = keras.preprocessing.image_dataset_from_directory(
        "img_output/", labels='inferred', image_size=(40, 40), subset="validation", validation_split=0.2,
        seed=123
    )
    # train_ds.class_names

    # train_images = list()
    # train_labels = list()
    # for gif_name in os.listdir("img_output/"):    
    #     im = Image.open("img_output/" + gif_name)
    #     im = numpy.array(im.getdata()).reshape(40, 40)
    #     train_images.append(im)
    #     train_labels.append(gif_name.split('.')[0].split('_')[1].lower())

    # class_names = [str(i) for i in range(10)]
    # class_names.extend(list('abcdefghijklmnopqrstuvwxyz'))
    # # 除外0o1itILl
    # for item in '0o1itILl':
    #     if item in class_names:
    #         class_names.remove(item)
    # # 30个类别
    # print(len(class_names))

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

    history = model.fit(train_ds, validation_data=val_ds, epochs=10)



