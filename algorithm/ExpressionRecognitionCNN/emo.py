import cv2
import numpy as np
import tensorflow as tf
from keras.models import load_model
from keras_preprocessing.image import load_img, img_to_array

model = load_model('algorithm/ExpressionRecognitionCNN/model_weights.h5')
# model = load_model('model_weights.h5')
labelDict = {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'neutral', 5: 'sad', 6: 'surprise'}


def emo(img):
    # 调整图像大小为 (256, 256)
    image = cv2.resize(img, (48, 48))

    # 转换为灰度图像
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # image_array=
    # image_array = np.expand_dims(gray_image, axis=0)  # 添加一个维度，因为模型期望输入是批量的图像
    input_data = gray_image / 255.0  # 对图像进行归一化处理，将像素值缩放到 [0, 1] 的范围

    # 增加维度，从 (height, width) 变为 (1, height, width, 1)
    input_data = np.expand_dims(input_data, axis=0)
    input_data = np.expand_dims(input_data, axis=-1)

    # 进行模型预测
    predictions = model.predict(input_data)

    # 查找最大概率的预测结果
    max_index = np.argmax(predictions[0])
    label = labelDict[max_index]
    return label


if __name__ == '__main__':
    img = cv2.imread("image.jpg")
    l = emo(img)
    print(l)
