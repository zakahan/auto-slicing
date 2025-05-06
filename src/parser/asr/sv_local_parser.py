# if __name__ == "__main__":
#     import os
#     import os.path as op
#     from dotenv import load_dotenv
#     load_dotenv(op.join(op.dirname(op.dirname(op.dirname(__file__))), ".env"))
#     pass

import os
from pydub import AudioSegment
from typing import Union
from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess
from parser.asr.base_parser import Parser


class SVLocalParser(Parser):
    def __init__(self):
        super().__init__()
        use_itn: bool = True
        device: str = 'cuda:0'  # ['cpu' ,'cuda:0']
        self.model_path = os.getenv("SENSE_VOICE_LOCAL_MODEL_PATH")
        self.vad_model_path = os.getenv("SENSE_VOICE_LOCAL_VAD_MODEL_PATH")
        self.model = AutoModel(model=self.model_path,
                               vad_model=self.vad_model_path,
                               vad_kwargs={"max_single_segment_time": 30000},
                               # trust_remote_code=True,
                               use_itn=use_itn,
                               device=device,  #,"cuda:0",
                               disable_update=True
                               )

        self.vad_model = AutoModel(
            model=self.vad_model_path,
            device=device,
            disable_update=True
        )

    def asr2str(self, input_audio: str, language: str = 'auto') -> str:
        # 解析音频,转为文字
        res = self.model.generate(
            input=input_audio,
            cache={},
            language=language,  # "zn", "en", "yue", "ja", "ko", "nospeech"
            use_itn=True,
            batch_size_s=60,
            # output_timestamp=True
            # merge_vad=True,  # 是否将 vad 模型切割的短音频碎片合成，合并后长度为merge_length_s，单位为秒s。
            # merge_length_s=15,    # 这俩开启之后会报错
        )
        text = rich_transcription_postprocess(res[0]["text"])
        return text

    def asr2dict(self, input_audio: str, task_id: str, language='auto') -> list[dict]:
        asr_list = []
        load_tmp_dir = os.path.join(self.kb_vad_path, task_id)
        if not os.path.exists(load_tmp_dir):
            os.makedirs(load_tmp_dir)

        clip_list = self.audio_split(input_audio, load_tmp_dir)
        for i, clip_dic in enumerate(clip_list):
            text = self.asr2str(input_audio=clip_dic['save_path'], language=language)
            asr_list.append(
                {
                    'slice_id': i,
                    'text': text,
                    'start_time': clip_list[i]['start_time'] // 1000,
                    'stop_time': clip_list[i]['stop_time'] // 1000,
                }
            )
        return asr_list  # 结果信息

    def vad_detect(self, input_audio: str) -> list[list]:
        res = self.vad_model.generate(input_audio)
        # the output as  [[beg1, end1], [beg2, end2], .., [begN, endN]]
        # 详情见 https://github.com/modelscope/FunASR/blob/main/examples/industrial_data_pretraining/fsmn_vad_streaming/demo.py
        return res[0]['value']

    def get_timestamps(self, input_audio, threshold_second: Union[float, int]):
        # 用于合并vad_detect之后的时间戳，直接输出使用的时间戳切的太碎了，开始的位置可能还行，结尾吃音了
        vad_timestamps = self.vad_detect(input_audio)  # vad检测timestamps
        if len(vad_timestamps) == 0:
            raise Exception('本段音频没有任何声音')

        duration = vad_timestamps[-1][1]  # 最后一位
        timestamps = []
        start_timestamps = [0]
        for item in vad_timestamps:
            start_timestamps.append(item[0])

        start = 0
        for i in range(0, len(start_timestamps)):
            if start_timestamps[i] - start < threshold_second * 1000:
                continue  # i 推至下一个
            else:
                timestamps.append([start, start_timestamps[i]])
                start = start_timestamps[i]
        # 肯定有一个收尾的
        if len(timestamps) > 0:
            timestamps.append([start, duration])
        # print(timestamps)
        return timestamps       # 这里的单位是毫秒，但实际上对我的应用场景来说秒就够了

    def audio_split(self, input_audio: str, save_dir: str):
        res_list = []
        # 加载音频文件
        input_format = input_audio.split('.')[-1]
        audio = AudioSegment.from_file(input_audio, format=input_format)
        # 获取时间戳
        # timestamps = self.get_timestamps(input_audio, threshold_second=1)       # 要求至少是一秒
        timestamps = self.vad_detect(input_audio)
        # 遍历时间戳并切割音频，输出到文件夹
        for i, (beg, end) in enumerate(timestamps):
            # 切割音频片段
            slice = audio[beg:end]
            # 保存音频片段到文件
            save_path = os.path.join(save_dir, f"clip_{i}.wav")
            res_list.append(
                {
                    'start_time': beg,
                    'stop_time': end,
                    'save_path': save_path
                })
            slice.export(save_path, format="wav")

        return res_list  # 返回这个，来确定文件位置



if __name__ == "__main__":
    print('hello world')
    kb_path = os.getenv("KB_BASE_PATH")
    test_file = os.path.join(kb_path, "raw", 'test.mp4')
    print(test_file)

    sv_loader = SVLocalParser()
    # res = sv_loader.asr2str(input_audio=test_file) #, task_id="001")
    res = sv_loader.asr2dict(input_audio=test_file, task_id="002")
    print(res)