# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from gtts import gTTS

import os


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    os.environ["HTTP_PROXY"] = "127.0.0.1:7890"
    os.environ["HTTPS_PROXY"] = "127.0.0.1:7890"
    tts = gTTS('嗨，叔叔，北京今天的天气很好呢！天空晴朗，阳光明媚，适合出门活动哦！',lang='zh')
    tts.save('ret1.wav')


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
