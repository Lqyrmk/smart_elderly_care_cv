"""
:Description: 
:Author: lym
:Date: 2023/07/15/14:08
:Version: 1.0
"""
import os
import openai

# 目前需要设置代理才可以访问 api
os.environ["HTTP_PROXY"] = "127.0.0.1:7890"
os.environ["HTTPS_PROXY"] = "127.0.0.1:7890"

# 设置 OpenAI 的 API 密钥
openai.api_key = ''  # 将 YOUR_API_KEY 替换为您的实际 API 密钥

# 调用 ChatGPT 接口
response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
    ]
)

# 获取助手的回复
assistant_response = response['choices'][0]['message']['content']
print(assistant_response)
