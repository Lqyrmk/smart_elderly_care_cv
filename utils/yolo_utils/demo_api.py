import cv2
import multiprocessing as mp
# import detect
import time
import detect_api


def image_put(q, ip, port, name):
    cap = cv2.VideoCapture("rtmp://43.143.247.127:1935/hls/wz")
    if cap.isOpened():
        print(name)

    while True:
        q.put(cap.read()[1])
        q.get() if q.qsize() > 1 else time.sleep(0.01)
        # print("555" * 25) if cap.read()[0] == False else print(" ")


def get_frames():
    camera_ip, camera_port, camera_name = "192.168.2.119", "554", "stream0"

    mp.set_start_method(method='spawn')  # init
    queue = mp.Queue(maxsize=2)
    processes = mp.Process(target=image_put, args=(queue, camera_ip, camera_port, camera_name)),
    [process.start() for process in processes]
    while True:
        yield queue.get()


def main():
    a = detect_api.detectapi(weights=r'F:\yolov5-5.0\runs\train\exp3\weights\best.pt')
    frames = get_frames()
    for frame in frames:
        result, names = a.detect([frame])
        img = result[0][0]  # 第一张图片的处理结果图片
        '''
        for cls,(x1,y1,x2,y2),conf in result[0][1]: #第一张图片的处理结果标签。
            print(cls,x1,y1,x2,y2,conf)
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0))
            cv2.putText(img,names[cls],(x1,y1-20),cv2.FONT_HERSHEY_DUPLEX,1.5,(255,0,0))
        '''
        cv2.namedWindow("video", cv2.WINDOW_NORMAL)
        cv2.imshow("video", img)
        cv2.waitKey(1)


if __name__ == '__main__':
    main()
