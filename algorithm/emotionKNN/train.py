import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
import pickle
import sklearn
import seaborn

from skimage.feature import hog
from sklearn.tree import DecisionTreeClassifier
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from skimage import io
from PIL import Image
from sklearn.naive_bayes import GaussianNB


def extract_hog_features(X):
    image_descriptors = []
    for i in range(len(X)):  # 此处的X为之前训练部分所有图像的矩阵形式拼接而来，所以len(X)实为X中矩阵的个数，即训练部分图像的个数
        print(i)  # 方便了解程序进程
        fd, _ = hog(X[i], orientations=9, pixels_per_cell=(16, 16), cells_per_block=(16, 16),
                    block_norm='L2-Hys', visualize=True)  # 此处的参数细节详见其他文章
        image_descriptors.append(fd)  # 拼接得到所有图像的hog特征
    return image_descriptors  # 返回的是训练部分所有图像的hog特征


def extract_hog_features_single(X):
    image_descriptors_single = []
    fd, _ = hog(X, orientations=9, pixels_per_cell=(16, 16), cells_per_block=(16, 16),
                block_norm='L2-Hys', visualize=True)
    image_descriptors_single.append(fd)
    return image_descriptors_single


def read_data(label2id):  # label2id为定义的标签
    X = []
    Y = []
    path = r'.\dataset'
    for label in os.listdir(path):  # os.listdir用于返回指定的文件夹包含的文件或文件夹的名字的列表，此处遍历每个文件夹
        for img_file in os.listdir(os.path.join(path, label)):  # 遍历每个表情文件夹下的图像
            image = cv2.imread(os.path.join(path, label, img_file))  # 读取图像
            gray_img = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            result = gray_img / 255.0  # 图像归一化
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            X.append(result)  # 将读取到的所有图像的矩阵形式拼接在一起
            Y.append(label2id[label])  # 将读取到的所有图像的标签拼接在一起
    return X, Y  # 返回的X,Y分别是图像的矩阵表达和图像的标签


label2id = {'angry': 0, 'disgust': 1, 'fearful': 2, 'happy': 3, 'neutral': 4, 'sad': 5, 'surprise': 6}
X, Y = read_data(label2id)
X_features = extract_hog_features(X)
X_train, X_test, Y_train, Y_test = train_test_split(X_features, Y, test_size=0.25, random_state=42)

'''
#svm算法
#svm = sklearn.svm.SVC(C = 10, kernel='linear') # acc = 0.9
svm =sklearn.svm.SVC(C=2, kernel='rbf', gamma=10, decision_function_shape='ovr')      #acc=0.9534
svm.fit(X_train, Y_train)
Y_predict = svm.predict(X_test)
'''


#knn算法
knn = KNeighborsClassifier(n_neighbors=1)     #0.93
knn.fit(X_train,Y_train)
print(knn)
print('测试数据集得分：{:.2f}'.format(knn.score(X_test,Y_test)))
Y_predict = knn.predict(X_test)
output = open('.\\model\\knn.pkl', 'wb')
# input = open('./model', 'rb')
s = pickle.dump(knn, output)
output.close()
# knn2 = pickle.load(input)
# input.close()


'''
#决策树算法   0.3+
tree_D = DecisionTreeClassifier()
tree_D.fit(X_train, Y_train)
Y_predict = tree_D.predict(X_test)
'''
'''
#朴素贝叶斯分类   0.67+
mlt=GaussianNB()
mlt.fit(X_train, Y_train)
Y_predict = mlt.predict(X_test)
'''
'''
#逻辑回归分类  0.488
logistic = LogisticRegression()
logistic.fit(X_train, Y_train)
Y_predict = logistic.predict(X_test)
'''

# # 随机森林    0.87
# Forest = RandomForestClassifier(n_estimators=180, random_state=0)
# Forest.fit(X_train, Y_train)
# Y_predict = Forest.predict(X_test)
#
# acc = accuracy_score(Y_test, Y_predict)
# precision = precision_score(Y_test, Y_predict, average='macro')
# recall = recall_score(Y_test, Y_predict, average='macro')
# cm = confusion_matrix(Y_test, Y_predict)
# print(cm)
# print('Acc: ', acc)
# print('Precision: ', precision)
# print('Recall: ', recall)
#
# xtick = ['angry', 'disgust', 'fearful', 'happy', 'neutral', 'sad', 'surprise']
# ytick = xtick
#
# f, ax = plt.subplots(figsize=(7, 5))
# ax.tick_params(axis='y', labelsize=15)
# ax.tick_params(axis='x', labelsize=15)
#
# seaborn.set(font_scale=1.2)
# plt.rc('font', family='Times New Roman', size=15)
#
# seaborn.heatmap(cm, fmt='g', cmap='Blues', annot=True, cbar=True, xticklabels=xtick, yticklabels=ytick, ax=ax)
#
# plt.title('Confusion Matrix', fontsize='x-large')
#
# plt.show()

