import os
import random
import pilk

from gtts import gTTS

from fastapi import Request, APIRouter, UploadFile, Body
from app_voice.bot.smartChatRobot import SmartChatRobot
import utils.file_cos_utils.cos_loader as cos

voice_app = APIRouter()


# @voice_app.get("/chat", summary="语音接口", description="调用此接口可以对语音输入文件进行处理")
# async def process_voice():
#     return "ok"


@voice_app.post("/chat", summary="语音接口", description="调用此接口可以对语音输入文件进行处理")
async def process_voice1(file: UploadFile):
    # 可以在这里进行文件的处理逻辑，比如保存到服务器或进行语音识别等操作
    # file 是上传的文件对象，可以根据需要进行处理

    # 从上传的文件对象中读取内容，并保存到服务器上
    contents = await file.read()
    directory = "./wav_file/"
    # os.makedirs(directory, exist_ok=True)
    with open(directory + 'temp.silk', "wb") as f:
        f.write(contents)

    pilk.silk_to_wav(silk=directory + 'temp.silk', wav=directory + 'temp.wav')

    os.environ["HTTP_PROXY"] = "127.0.0.1:7890"
    os.environ["HTTPS_PROXY"] = "127.0.0.1:7890"

    ad_bot = SmartChatRobot()
    my_text = ad_bot.recogByBaiduApi()
    result_text = ''
    wav_url = ''
    if my_text is None:
        result_text = "我没有听清，您能再说一遍吗？"
    else:
        # result_text = "hhhhhhhhhhhhhhh"
        result_text = ad_bot.chatgpt_dialog(my_text)
    # 要上传语音所在的文件夹
    local_dir_path = 'wav_file/my_wav/'
    # 上传到的文件夹
    elderly_path = "/wav_file"

    tts = gTTS(result_text, lang='zh')
    tts.save(local_dir_path + 'result_wav.wav')

    # 最终路径为 local_dir_path +
    cos.upload_file_to_cos(local_dir_path=local_dir_path, elderly_path=elderly_path)

    # # 清空本地
    for root, dirs, files in os.walk(local_dir_path):
        # 删除每个文件
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)
    wav_url = 'http://lqyrmk.online/resources/smart_elderly_care/cv_file/wav_file/result_wav.wav'
    # 返回相应的处理结果
    return {"message": "录音文件已接收并处理成功",
            "my_text": my_text,
            "result_text": result_text,
            "wav_url": wav_url + '?t=' + str(random.random())}

@voice_app.post("/input", summary="文字接口", description="调用此接口可以对文字输入进行处理")
async def process_voice2(data=Body(None)):
    my_text = data["my_text"]

    os.environ["HTTP_PROXY"] = "127.0.0.1:7890"
    os.environ["HTTPS_PROXY"] = "127.0.0.1:7890"

    ad_bot = SmartChatRobot()
    result_text = ad_bot.chatgpt_dialog(str(my_text))
    wav_url = ''
    # 要上传语音所在的文件夹
    local_dir_path = 'wav_file/my_wav/'
    # 上传到的文件夹
    elderly_path = "/wav_file"

    tts = gTTS(result_text, lang='zh')
    tts.save(local_dir_path + 'result_wav.wav')

    # 最终路径为 local_dir_path +
    cos.upload_file_to_cos(local_dir_path=local_dir_path, elderly_path=elderly_path)

    # # 清空本地
    for root, dirs, files in os.walk(local_dir_path):
        # 删除每个文件
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)
    wav_url = 'http://lqyrmk.online/resources/smart_elderly_care/cv_file/wav_file/result_wav.wav'
    # 返回相应的处理结果
    return {"message": "处理成功",
            "my_text": my_text,
            "result_text": result_text,
            "wav_url": wav_url + '?t=' + str(random.random())}

