import logging
import cv2
import threading
import torch
# import dlib
import torchvision
from torchvision.utils import save_image

from algorithm.Dlib.face_reco_from_camera_ot import Face_Recognizer


def run(face_recognizer, url):
    # cap = cv2.VideoCapture("./Dlib/data/test/test.mp4")  # Get video stream from video file
    cap = cv2.VideoCapture(url)  # Get video stream from camera
    face_recognizer.process(cap)
    cap.release()
    cv2.destroyAllWindows()


def detect(url, Face_Recognizer_con):
    thread = threading.Thread(target=run, args=(Face_Recognizer_con, url))
    thread.start()
    # cv2.imshow("1", Face_Recognizer_con.detect_img)
    # run(Face_Recognizer_con, url)


def main():
    # logging.basicConfig(level=logging.DEBUG) # Set log level to 'logging.DEBUG' to print debug info of every frame
    logging.basicConfig(level=logging.INFO)
    Face_Recognizer_con = Face_Recognizer()
    run(Face_Recognizer_con)


if __name__ == '__main__':
    # main()
    # a = torch.Tensor([1, 2])
    # b = torch.Tensor([2, 3])
    # # c =  torch.pow(a - b, 2)
    # print(torch.cuda.is_available())
    # print(torch.backends.cudnn.is_available())
    # print(torch.cuda_version)
    # print(torch.backends.cudnn.version())
    # print(dlib.DLIB_USE_CUDA)

    import threading
    import time


    def run():
        print('run：当前的线程为', threading.current_thread())
        for i in range(5):
            print('跑')
            time.sleep(1)


    def eat():
        print('run：当前的线程为', threading.current_thread())
        for i in range(5):
            print('吃饭啦')
            time.sleep(1)


    # threading.Thread()的参数与进程类似
    # group: 线程组，目前只能使用None
    # target: 执行的目标任务名，一般是方法名
    # args: 以元组的方式给执行任务传参
    # kwargs: 以字典方式给执行任务传参
    # name: 线程名，一般不用设置
    # daemon：是否设置为守护主线程
    run_thread = threading.Thread(target=run)
    eat_thread = threading.Thread(target=eat)
    print('man：主线程为', threading.current_thread())
    '''
    第3步，开启线程
    '''
    run_thread.start()
    eat_thread.start()
    print("1")
