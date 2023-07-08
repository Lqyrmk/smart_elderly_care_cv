from time import sleep

import cv2
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from algorithm import integrate
from algorithm.Dlib.face_reco_from_camera_ot import Face_Recognizer

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


# video_url请求参数设置视频流地址

def detect_iter(Face_Recognizer_con):
    while(True):
        img = Face_Recognizer_con.detect_img
        # cv2.imshow("camera", img)
        frame = cv2.imencode('.jpg', img)[1].tobytes()
        yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'


@app.get('/cv')
async def video_feed():
    video_url = 'rtmp://43.143.247.127:1935/hls/lym'
    # video_url = 0
    Face_Recognizer_con = Face_Recognizer()
    integrate.detect(video_url, Face_Recognizer_con)
    return StreamingResponse(detect_iter(Face_Recognizer_con),
                             media_type='multipart/x-mixed-replace; boundary=frame')
