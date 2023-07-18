import os
import pickle
import time
import cv2
from skimage.feature import hog

model = open('algorithm\\emotionKNN\\model\\knn.pkl', 'rb')
knn = pickle.load(model)
model.close()
labelDict = {0: 'angry', 1: 'disgust', 2: 'fearful', 3: 'happy', 4: 'neutral', 5: 'sad', 6: 'surprise'}

def extract_hog_features_single(X):
    image_descriptors_single = []
    fd, _ = hog(X, orientations=9, pixels_per_cell=(16, 16), cells_per_block=(16, 16),
                block_norm='L2-Hys', visualize=True)
    image_descriptors_single.append(fd)
    return image_descriptors_single


def emotion(img):
    # 下面为同一文件夹下多张图片的表情识别
    # i = 1
    t1=time.time()
    gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # resize图像，满足HOG特征提取标准
    resize_img = cv2.resize(gray_img, (256, 256))

    result = resize_img / 255.0
    # cv2.imshow("face_", result)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    X_Single = extract_hog_features_single(result)
    t2=time.time()
    predict = knn.predict(X_Single)  # 可以在这里选择分类器的类别
    print(t2-t1)
    # i += 1
    return labelDict[predict[0]]
