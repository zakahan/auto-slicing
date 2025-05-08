
# For prerequisites running the following sample, visit https://help.aliyun.com/document_detail/xxxxx.html

import os
import requests
from http import HTTPStatus

import dashscope
from dashscope.audio.asr import *

# 若没有将API Key配置到环境变量中，需将your-api-key替换为自己的API Key
# dashscope.api_key = "your-api-key"

dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
r = requests.get(
    "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav"
)
with open("asr_example.wav", "wb") as f:
    f.write(r.content)

from http import HTTPStatus
from dashscope.audio.asr import Recognition


# https://help.aliyun.com/zh/model-studio/paraformer-real-time-speech-recognition-python-api
# 若没有将API Key配置到环境变量中，需将下面这行代码注释放开，并将apiKey替换为自己的API Key
# import dashscope
# dashscope.api_key = "apiKey"

recognition = Recognition(model='paraformer-realtime-v2',
                          format='wav',
                          sample_rate=16000,
                          # “language_hints”只支持paraformer-realtime-v2模型
                          language_hints=['zh', 'en'],
                          callback=None)
result = recognition.call('asr_example.wav')
if result.status_code == HTTPStatus.OK:
    print('识别结果：')
    print(result.get_sentence())
else:
    print('Error: ', result.message)
    
print(
    '[Metric] requestId: {}, first package delay ms: {}, last package delay ms: {}'
    .format(
        recognition.get_last_request_id(),
        recognition.get_first_package_delay(),
        recognition.get_last_package_delay(),
    ))