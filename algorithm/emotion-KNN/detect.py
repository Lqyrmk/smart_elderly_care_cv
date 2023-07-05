import os
import pickle
import cv2
from skimage.feature import hog


def extract_hog_features_single(X):
    image_descriptors_single = []
    fd, _ = hog(X, orientations=9, pixels_per_cell=(16, 16), cells_per_block=(16, 16),
                block_norm='L2-Hys', visualize=True)
    image_descriptors_single.append(fd)
    return image_descriptors_single


# 下面为同一文件夹下多张图片的表情识别
labelDict = {0: 'angry', 1: 'disgust', 2: 'fearful', 3: 'happy', 4: 'neutral', 5: 'sad', 6: 'surprise'}
path = r'./test'
model = open('.\\model\\knn.pkl', 'rb')
knn = pickle.load(model)
model.close()
i = 1
for image_file in os.listdir(path):
    image = cv2.imread(os.path.join(path, image_file))
    gray_img = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    result = gray_img / 255.0
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    X_Single = extract_hog_features_single(result)
    predict = knn.predict(X_Single)  # 可以在这里选择分类器的类别
    print(i)
    i += 1
    print(labelDict[predict[0]])
