import uvicorn
import socketio
from fastapi import FastAPI, Body
from fastapi_socketio import SocketManager
from fastapi.responses import Response, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware


from app_nia import nia_app
from app_voice import voice_app
from app_info import info_app

app = FastAPI(
    title='FastAPI后端接口文档',
    description='使用Fastapi构建智慧养老系统的算法接口',
    version='1.0.0',
    docs_url='/api/v2/docs',
    redoc_url='/api/v2/redocs',
)

origins = [
    "http://localhost"
    # "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(nia_app, prefix='/api/v1/cv', tags=['cv应用'])
app.include_router(voice_app, prefix='/api/v1/voice', tags=['voice应用'])
app.include_router(info_app, prefix='/api/v1/info', tags=['info应用'])

# sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins=[])
# app.mount("/ws", socketio.ASGIApp(sio))

# fastapi_socketio挂载路径
# 默认挂载 /ws
socket_manager = SocketManager(app)


# 检测是否连接
@socket_manager.on("connect", namespace="/ws")
async def connect(sid, environ):
    await socket_manager.emit("connect_response", {"message": f"客户端{sid}已连接到服务端"}, room=sid, namespace='/ws')


# 检测是否断开连接
@socket_manager.on("disconnect", namespace="/ws")
async def disconnect(sid):
    await socket_manager.emit("connect_response", {"message": f"客户端{sid}已断开连接"}, room=sid, namespace='/ws')


@app.post("/api/v1/alert",
          summary="报警信息推送接口",
          description="调用此接口即可使用Websocket向前端推送消息",
          tags=['socket应用'])
async def alert_test2(msg=Body(None)):
    print(msg)
    # 发送预警消息
    await socket_manager.emit("alarm_message", msg, namespace='/ws')
    return "预警信息发送成功"


# 这个暂时没啥用
# 定义事件处理函数
# @socket_manager.on("chat", namespace="/ws")
# async def handle_chat_event(sid, data):
#     message = data.get('message')
#     print(f"接收到来自客户端的信息: {message}")
#     # 向指定客户端发送消息
#     await socket_manager.emit("chat_message", {"message": "你好，客户端"}, room=sid, namespace='/ws')


if __name__ == '__main__':
    uvicorn.run('run:app', port=8090, reload=True, workers=1)
