from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from qcloud_cos.cos_exception import CosClientError, CosServiceError

from datetime import datetime

import sys
import os
import logging

# 配置COS区域和密钥信息
secret_id = 'AKIDfFrRuCIG3MURAeKq9E7qLgokW7UefZKb'
secret_key = 'AJJI9vXxLgtvmV2NTRGtjMo6C5j8LNHz'
bucket = 'cos-lqyrmk-1312783534'
region = 'ap-beijing'         # 指定的 COS 地域
token = None            # 如果使用永久密钥建议设置 Token
scheme = 'https'        # 指定使用 https 协议来访问 COS
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
client = CosS3Client(config)


def upload_file_to_cos(local_dir_path, elderly_path):

    # 获取指定文件夹下的所有文件名
    files = os.listdir(local_dir_path)
    # 使用列表推导式和字符串操作
    # 筛选出所有的jpg png图片文件
    images = [f for f in files if f.endswith('.jpg') or f.endswith('.png')]

    # 将文件上传到指定存储桶中
    # 使用高级接口断点续传，失败重试时不会上传已成功的分块(这里重试 10 次)
    for image in images:
        for i in range(0, 10):
            try:
                # 无后缀名
                base_image = os.path.splitext(os.path.basename(image))[0]
                response = client.upload_file(
                    Bucket=bucket,  # 存储桶名称
                    Key='resources/smart_elderly_care/cv_file' + elderly_path
                        + "/" + image,  # 文件在 COS 中的名称
                    LocalFilePath=local_dir_path + "/" + image
                )
                break
            except (CosClientError, CosServiceError) as e:
                print(e)
        # 输出上传结果
        # print(response['ETag'])
    print('文件上传完毕！！！')

def download_file_from_cos(file_path_key, save_path):
    try:
        # 执行下载操作
        response = client.get_object(Bucket=bucket, Key=file_path_key)
        response['Body'].get_stream_to_file(save_path)
        print(f"图片下载成功：{file_path_key}")
    except Exception as e:
        print(f"图片下载失败：{e}")

if __name__ == '__main__':
    # 上传样例：
    # 要上传图片所在的文件夹
    local_dir_path = 'img'
    # 老人图片对应的path，对应上传到的文件夹
    elderly_path = "/nia"
    # 最终路径为 local_dir_path +
    upload_file_to_cos(local_dir_path=local_dir_path, elderly_path=elderly_path)

    # 下载样例
    # 要下载文件的cos全路径
    file_path_key = 'resources/smart_elderly_care/cv_file/img' + elderly_path + "/" + "丁真.jpg"
    # 下载到的文件夹全路径
    save_path = './download_file/' + "丁真.jpg"
    download_file_from_cos(file_path_key=file_path_key, save_path=save_path)



