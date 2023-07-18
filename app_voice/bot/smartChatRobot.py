import openai
from aip import AipSpeech


class SmartChatRobot(object):
    '''
    Baidu Speech API
    '''
    APP_ID = ''
    API_KEY = ''
    SECRET_KEY = ''

    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    url = 'http://fjx.com/api/test'

    # 设置 OpenAI 的 API 密钥
    openai.api_key = ''  # 将 YOUR_API_KEY 替换为您的实际 API 密钥


    '''
    将 SpeechRecognition 录制的音频格式为.wav文件使用Post方法上传上传至百度语音的服务，
    返回识别后的json数据并抽取result的文本进行输出
    '''
    def recogByBaiduApi(self):
        with open('wav_file/temp.wav', 'rb') as f:
            audio_data = f.read()
            # 参数'dev_pid'普通话(支持简单的英文识别)
        result = self.client.asr(audio_data, 'wav', 16000, {
            'dev_pid': 1536,
        })
        print(result)

        try:
            result_text = result["result"][0]
        except KeyError:
            # 处理键错误的逻辑
            result_text = None
        finally:
            if result_text is None:
                print("未检测到语音")
                return result_text
            else:
                print("you said: " + result_text)
        return result_text

    def chatgpt_dialog(self, my_text):

        # 目前需要设置代理才可以访问 api
        # os.environ["HTTP_PROXY"] = "127.0.0.1:7890"
        # os.environ["HTTPS_PROXY"] = "127.0.0.1:7890"

        # 调用 ChatGPT 接口
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一个养老院的智慧养老机器人，你乐于助人，现在你要为一个老人服务，你必须尊敬老人。请你的表达尽量口语化，不要长篇大论。"},
                {"role": "user", "content": my_text},
            ]
        )

        # 获取助手的回复
        assistant_response = response['choices'][0]['message']['content']
        print(assistant_response)
        return assistant_response


if __name__ == '__main__':
    test = SmartChatRobot()
    test.dialogue()
