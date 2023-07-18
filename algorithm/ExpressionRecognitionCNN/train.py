import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
# import utils
import os

from keras.layers import MaxPooling2D
from keras_preprocessing.image import load_img
from livelossplot.inputs.tf_keras import PlotLossesCallback
import tensorflow as tf
from keras import regularizers
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Dense, Input, Dropout, Flatten, Conv2D
from keras.layers import BatchNormalization, Activation, MaxPooling2D
from keras.models import Model, Sequential
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
from keras.utils import plot_model

from IPython.display import SVG, Image

# from livelossplot import PlotLossesTensorFlowKeras
print("Tensorflow version:", tf.__version__)

i = 1
plt.figure(figsize=(8, 8))
for expression in os.listdir('./img/test/'):
    img = load_img(('./img/test/' + expression + '/'
                    + os.listdir('./img/test/' + expression)[1]))
    plt.subplot(1, 7, i)
    plt.imshow(img)
    plt.title(expression)
    plt.axis('off')
    i += 1

plt.show()

# check the amount of data in each folder in training dataset
for expression in os.listdir('./img/train/'):
    print(expression, "folder contains\t\t", len(os.listdir('./img/train/' +
                                                            expression)), "images")

# check the amount of data in each folder in testing dataset
for expression in os.listdir('./img/test/'):
    print(expression, "folder contains\t\t", len(os.listdir('./img/train/' +
                                                            expression)), "images")

# Data Augmentation

datagen_train = ImageDataGenerator(rescale=1. / 255,
                                   zoom_range=0.3,
                                   horizontal_flip=True)

train_generator = datagen_train.flow_from_directory('./img/train/',
                                                    batch_size=16,
                                                    target_size=(48, 48),
                                                    shuffle=True,
                                                    color_mode='grayscale',
                                                    class_mode='categorical')

datagen_test = ImageDataGenerator(rescale=1. / 255,
                                  zoom_range=0.3,
                                  horizontal_flip=True)

test_generator = datagen_test.flow_from_directory('./img/test/',
                                                  batch_size=16,
                                                  target_size=(48, 48),
                                                  shuffle=True,
                                                  color_mode='grayscale',
                                                  class_mode='categorical')

model = tf.keras.models.Sequential()

model.add(Conv2D(64, kernel_size=(3, 3), padding='same', activation='relu', input_shape=(48, 48, 1)))
model.add(BatchNormalization())
model.add(MaxPooling2D(2, 2))
model.add(Dropout(0.25))

model.add(Conv2D(128, kernel_size=(5, 5), activation='relu', padding='same', kernel_regularizer=regularizers.l2(0.01)))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(512, kernel_size=(3, 3), activation='relu', padding='same', kernel_regularizer=regularizers.l2(0.01)))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(512, kernel_size=(3, 3), activation='relu', padding='same', kernel_regularizer=regularizers.l2(0.01)))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(512, activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.25))

model.add(Dense(7, activation='softmax'))

model.compile(optimizer=Adam(learning_rate=0.0005, decay=1e-6),
              loss='categorical_crossentropy',
              metrics=['accuracy'])
model.summary()

epochs = 50
steps_per_epoch = train_generator.n / train_generator.batch_size
testing_steps = test_generator.n / test_generator.batch_size

checkpoint = ModelCheckpoint("model_weights.h5", monitor="val_accuracy", save_weights_only=False, mode='max', verbose=1)

reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=2, min_lr=0.00001, model='auto')

callbacks = [PlotLossesCallback(), checkpoint, reduce_lr]

history = model.fit(
    x=train_generator,
    steps_per_epoch=steps_per_epoch,
    epochs=epochs,
    validation_data=test_generator,
    validation_steps=testing_steps,
    callbacks=callbacks
)
