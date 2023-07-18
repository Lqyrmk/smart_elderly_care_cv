import cv2
import httpx
import threading
import utils.file_cos_utils.cos_loader as cos

from app_nia.dec_area import yoloDetect as yoloDetectArea
from app_nia.dec_fall import yoloDetect as yoloDetectFall
from app_nia.dec_fire import yoloDetect as yoloDetectFire
from app_nia.dec_water import yoloDetect as yoloDetectWater
from app_nia.dec_seepage import yoloDetect as yoloDetectSeepage

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from utils.mysql_utils.database import engine, Base, SessionLocal
from utils.mysql_utils.models import Elderly, Event, Algorithm, Camera
from datetime import datetime

from algorithm import integrate
from algorithm.Dlib.face_reco_from_camera_ot import Face_Recognizer

nia_app = APIRouter()

Base.metadata.create_all(bind=engine)

# @nia_app.get("/test")
# async def add_face():
#     # 开启session
#     session = SessionLocal()
#
#     # 人脸录入，数据库生成
#     face_type = 1
#     face_name = "毛景辉"
#
#     # 录入类型
#     if face_type == 1:
#         # 老人
#         face_obj = session.query(Elderly).filter(Elderly.elderly_name == face_name).first()
#     elif face_type == 2:
#         # 义工
#         face_obj = session.query(Volunteer).filter(Volunteer.volunteer_name == face_name).first()
#     elif face_type == 3:
#         # 工作人员
#         face_obj = session.query(Employee).filter(Employee.employee_name == face_name).first()
#
#
#     # 提交
#     session.commit()
#     # 关闭session
#     session.close()
#     return {"data": None, "msg": "已添加！", "code": "1"}

# 添加事件

flag = True


@nia_app.get("/event")
async def add_event():
    # 开启session
    session = SessionLocal()

    # 检测异常，生成事件

    algorithm_name = "人脸识别"
    algorithm = session.query(Algorithm).filter(Algorithm.algorithm_name == algorithm_name).first()
    event_type = algorithm.algorithm_id  # 事件类型

    event_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 发生日期
    event_location = '307门口'  # 发生地点
    event_desc = '测试1'  # 事件描述
    elderly_name = '毛景辉'
    # elderly_id = 1676623591240806402  # 老人id

    # 根据姓名搜索老人
    elderly = session.query(Event).filter(Elderly.elderly_name == elderly_name).first()
    elderly_id = elderly.elderly_id

    # 检测到后保存的文件
    file_name = "image_" + str(elderly_id) + "_" + event_date + ".jpg"

    # 上传样例
    # 要上传图片所在的文件夹
    local_dir_path = 'utils/file_cos_utils/img'
    # 老人图片对应的path，对应上传到的文件夹
    elderly_path = "/cv/" + str(elderly_id)
    # 最终路径为 local_dir_path +
    cos.upload_file_to_cos(local_dir_path=local_dir_path, elderly_path=elderly_path)

    # 向数据库插入数据
    cv_event = Event(event_type=event_type,
                     event_date=event_date,
                     event_location=event_location,
                     event_desc=event_desc,
                     elderly_id=elderly_id)
    session.add(cv_event)

    # 提交
    session.commit()
    # 关闭session
    session.close()
    return {"data": None, "msg": "已添加！", "code": "1"}


@nia_app.get("/")
async def root():
    return {"message": "Hello World"}


@nia_app.get("/close_cv")
async def close():
    # 这里写关闭算法检测的逻辑
    global flag
    flag = False
    return {"message": "Hello World"}


# video_url请求参数设置视频流地址
async def detect_iter_face(Face_Recognizer_con):
    while (True):
        cv2.destroyAllWindows()
        img = Face_Recognizer_con.detect_img
        if Face_Recognizer_con.hasUnknown:
            async with httpx.AsyncClient() as client:
                url = "http://43.143.247.127:8090/api/v1/alert"
                # 将需要发送的消息字典作为payload
                payload = {"message": "这是一条预警消息", "alert_type": "检测到陌生人"}
                # json格式发送
                await client.post(url, json=payload)
            Face_Recognizer_con.hasUnknown = 0
        Face_Recognizer_con.flag = flag
        frame = cv2.imencode('.jpg', img)[1].tobytes()
        yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'


# 人脸识别、情绪识别、交互检测
@nia_app.get('/face')
async def cv_face(video_url):
    # 开启session
    session = SessionLocal()
    # video_url = 'rtmp://43.143.247.127:1935/hls/lym'
    video_url = 0
    Face_Recognizer_con = Face_Recognizer()
    # 拿到对应的摄像头
    camera = session.query(Camera).filter(Camera.stream_address == str(video_url)).first()
    Face_Recognizer_con.stream_address = camera.stream_address
    Face_Recognizer_con.event_location = camera.camera_name
    # 关闭session
    session.close()
    integrate.detect(video_url, Face_Recognizer_con)
    return StreamingResponse(detect_iter_face(Face_Recognizer_con),
                             media_type='multipart/x-mixed-replace; boundary=frame')


def run(yolo, url):
    # cap = cv2.VideoCapture("./Dlib/data/test/test.mp4")  # Get video stream from video file
    # cap = cv2.VideoCapture(url)  # Get video stream from camera
    yolo.detect(url)
    # cap.release()
    # cv2.destroyAllWindows()


# 禁区入侵检测
async def detect_iter_area(yolo):
    while True:
        img = yolo.img_det
        # cv2.imshow("camera", img)
        # im = img.numpy()
        if yolo.warn:
            async with httpx.AsyncClient() as client:
                url = "http://43.143.247.127:8090/api/v1/alert"
                # 将需要发送的消息字典作为payload
                payload = {"message": "这是一条预警消息", "alert_type": "检测到禁区有人闯入"}
                # json格式发送
                await client.post(url, json=payload)
            yolo.warn = False
        yolo.flag = flag
        frame = cv2.imencode('.jpg', img)[1].tobytes()
        yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'


@nia_app.get('/area')
async def cv_area(video_url, px1, px2, px3, px4, py1, py2, py3, py4):
    # video_url = 'rtmp://43.143.247.127:1935/hls/lym'
    # video_url = "rtmp://43.143.247.127:1935/hls/wz"
    # loc = [0.3, 0.363,
    #        0.65, 0.386,
    #        0.69, 0.586,
    #        0.317, 0.693]
    print(type(px1))
    print(type(0.317))
    print(float(px1))
    print(type(float(px1)))
    print(px2)
    print(px3)
    print(px4)
    print(py1)
    print(py2)
    print(py3)
    print(py4)
    loc = [float(px1), float(py1), float(px2), float(py2), float(px3), float(py3), float(px4), float(py4)]
    yl = yoloDetectArea(video_url, loc)

    # 开启session
    session = SessionLocal()
    # 拿到对应的摄像头
    camera = session.query(Camera).filter(Camera.stream_address == str(video_url)).first()
    yl.stream_address = camera.stream_address
    yl.event_location = camera.camera_name
    # 关闭session
    session.close()

    thread = threading.Thread(target=run, args=(yl, video_url))
    thread.start()
    # integrate.detect(video_url, Face_Recognizer_con)
    return StreamingResponse(detect_iter_area(yl),
                             media_type='multipart/x-mixed-replace; boundary=frame')


# 摔倒检测
async def detect_iter_fall(yolo):
    while True:
        img = yolo.img_det
        # cv2.imshow("camera", img)
        # im = img.numpy()
        if yolo.warn:
            async with httpx.AsyncClient() as client:
                url = "http://43.143.247.127:8090/api/v1/alert"
                # 将需要发送的消息字典作为payload
                payload = {"message": "这是一条预警消息", "alert_type": "检测到有老人跌倒"}
                # json格式发送
                await client.post(url, json=payload)
        yolo.warn = False
        frame = cv2.imencode('.jpg', img)[1].tobytes()
        yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'


@nia_app.get('/fall')
async def cv_fall(video_url):
    # video_url = 'rtmp://43.143.247.127:1935/hls/lym'
    # video_url = "rtmp://43.143.247.127:1935/hls/wz"
    # loc = [-10 / 900, -10 / 1280,
    #        -10 / 900, 1300 / 1280,
    #        950 / 900, 1300 / 1280,
    #        950 / 900, -10 / 1280]
    yl = yoloDetectFall(video_url)

    # 开启session
    session = SessionLocal()
    # 拿到对应的摄像头
    camera = session.query(Camera).filter(Camera.stream_address == str(video_url)).first()
    yl.stream_address = camera.stream_address
    yl.event_location = camera.camera_name
    # 关闭session
    session.close()

    thread = threading.Thread(target=run, args=(yl, video_url))
    thread.start()
    # integrate.detect(video_url, Face_Recognizer_con)
    return StreamingResponse(detect_iter_fall(yl),
                             media_type='multipart/x-mixed-replace; boundary=frame')


# fire明火烟雾
async def detect_iter_fire(yolo):
    while True:
        img = yolo.img_det
        # cv2.imshow("camera", img)
        # im = img.numpy()
        if yolo.warn:
            async with httpx.AsyncClient() as client:
                url = "http://43.143.247.127:8090/api/v1/alert"
                # 将需要发送的消息字典作为payload
                payload = {"message": "这是一条预警消息", "alert_type": "检测到有明火或烟雾，请及时处理"}
                # json格式发送
                await client.post(url, json=payload)
            yolo.warn = False
        frame = cv2.imencode('.jpg', img)[1].tobytes()
        yolo.warn = False
        yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'


@nia_app.get('/fire')
async def cv_fire(video_url):
    # video_url = 'rtmp://43.143.247.127:1935/hls/lym'
    # video_url = "rtmp://43.143.247.127:1935/hls/wz"
    yl = yoloDetectFire(video_url)

    # 开启session
    session = SessionLocal()
    # 拿到对应的摄像头
    camera = session.query(Camera).filter(Camera.stream_address == str(video_url)).first()
    yl.stream_address = camera.stream_address
    yl.event_location = camera.camera_name
    # 关闭session
    session.close()

    thread = threading.Thread(target=run, args=(yl, video_url))
    thread.start()
    # integrate.detect(video_url, Face_Recognizer_con)
    return StreamingResponse(detect_iter_fire(yl),
                             media_type='multipart/x-mixed-replace; boundary=frame')


# 积水检测
async def detect_iter_water(yolo):
    while True:
        img = yolo.img_det
        # cv2.imshow("camera", img)
        # im = img.numpy()
        if yolo.warn:
            async with httpx.AsyncClient() as client:
                url = "http://43.143.247.127:8090/api/v1/alert"
                # 将需要发送的消息字典作为payload
                payload = {"message": "这是一条预警消息", "alert_type": "检测到有积水，请及时处理"}
                # json格式发送
                await client.post(url, json=payload)
            yolo.warn = False
        yolo.flag = flag
        frame = cv2.imencode('.jpg', img)[1].tobytes()
        yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'


@nia_app.get('/water')
async def cv_water(video_url):
    # video_url = 'rtmp://43.143.247.127:1935/hls/lym'
    # video_url = "rtmp://43.143.247.127:1935/hls/wz"
    yl = yoloDetectWater(video_url)

    # 开启session
    session = SessionLocal()
    # 拿到对应的摄像头
    camera = session.query(Camera).filter(Camera.stream_address == str(video_url)).first()
    yl.stream_address = camera.stream_address
    yl.event_location = camera.camera_name
    # 关闭session
    session.close()

    thread = threading.Thread(target=run, args=(yl, video_url))
    thread.start()
    # integrate.detect(video_url, Face_Recognizer_con)
    return StreamingResponse(detect_iter_water(yl),
                             media_type='multipart/x-mixed-replace; boundary=frame')


# 房屋渗水检测
async def detect_iter_seepage(yolo):
    while True:
        img = yolo.img_det
        # cv2.imshow("camera", img)
        # im = img.numpy()
        if yolo.warn:
            async with httpx.AsyncClient() as client:
                url = "http://43.143.247.127:8090/api/v1/alert"
                # 将需要发送的消息字典作为payload
                payload = {"message": "这是一条预警消息", "alert_type": "检测到有房屋渗水，请及时处理"}
                # json格式发送
                await client.post(url, json=payload)
            yolo.warn = False
        yolo.flag = flag
        frame = cv2.imencode('.jpg', img)[1].tobytes()
        yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'


@nia_app.get('/seepage')
async def cv_seepage(video_url):
    # video_url = 'rtmp://43.143.247.127:1935/hls/lym'
    # video_url = "rtmp://43.143.247.127:1935/hls/wz"
    yl = yoloDetectSeepage(video_url)

    # 开启session
    session = SessionLocal()
    # 拿到对应的摄像头
    camera = session.query(Camera).filter(Camera.stream_address == str(video_url)).first()
    yl.stream_address = camera.stream_address
    yl.event_location = camera.camera_name
    # 关闭session
    session.close()

    thread = threading.Thread(target=run, args=(yl, video_url))
    thread.start()
    # integrate.detect(video_url, Face_Recognizer_con)
    return StreamingResponse(detect_iter_seepage(yl),
                             media_type='multipart/x-mixed-replace; boundary=frame')
