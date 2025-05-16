# auto-slicing

[English](README_en.md) | [简体中文](README.md)

### Summarize in One Sentence
Automated Slicing: This is a project that realizes the automated slicing of recorded videos through ASR + LLM Agent.

### 👐Recommend Oneself

- One day, while you're livestreaming, on a whim, you start fantasizing. You fantasize about becoming one of those "super slicing guys" and making video clips for your beloved streamer or the VTuber you adore. What should you do?
- You have the intention, but you don't have the time to edit. What's more, you haven't even learned how to edit. What should you do?
- You think it over, gather your courage to obtain the recorded broadcast and prepare to edit. But then you realize that this is just the starting point.🙂‍↕️
- Screening, aligning the timeline ⌚️, coming up with an appropriate title 🙋, it's all too complicated. 😩 If there's a day when you haven't watched the live stream 🏃‍♂️ and you have to watch the entire recorded broadcast before slicing, what should you do? 😭
- You say that your love is charming and you're really determined, but it still requires a lot of operation. So, is there any simple yet powerful way to slice the video?
- Yes, there is, bro.
- Take a look at "auto-slicing". You take care of the recorded broadcast, and it takes care of the slicing.  



## 👀Quick Start

### 1. Install Dependencies

#### 1.1 Clone the project or download the zip package directly

Prerequisites:
- Video memory >= 8GB. I haven't tried with less.
- Memory >= 32GB.

#### 1.2 Configure the Python environment

Python version: Theoretically, Python `3.11 - 3.12` can be used. There were some problems with `3.13` before, and it's not clear if they have been fixed now.

1. It is recommended to use uv to install

```bash
cd vedit - mcp
uv pip install - r requirements.txt
```

2. Or directly use pip to install

```bash
pip install - r requirements.txt
```

#### 1.3 Configure ffmpeg

The video edit parts depends on [`zakahan/vedit-mcp`](https://github.com/zakahan/vedit-mcp), which depends on `ffmpeg` to work, so please configure ffmpeg.

```bash
# Ubuntu
sudo apt update
sudo apt install ffmpeg
```

#### 1.4 Download ASR model weights

- For audio analysis, including speech recognition and speech interruption detection. Please refer to:
  - https://github.com/FunAudioLLM/SenseVoice
  - [modelscope - iic/SenseVoiceSmall](https://www.modelscope.cn/models/iic/SenseVoiceSmall) - corresponding to SENSE_VOICE_MODEL_PATH
  - [modelscope - icc/vad_fsmmn](https://www.modelscope.cn/models/iic/speech_fsmn_vad_zh - cn - 16k - common - pytorch/summary) - corresponding to SENSE_VOICE_VAD_MODEL_PATH

Note: This part currently only supports local inference, and the API method may be supported in the future.

#### 1.5 Configure environment variables

```bash
cd auto - slicing/src
cp .env.example .env
```

Edit the `.env` file and modify some configurations according to the actual situation.

Note: Currently, this script uses the API of the [Volcano Ark Platform](https://www.volcengine.com/product/ark), so both API_BASE and API_KEY are from this platform.
1. `OPENAI_API_BASE`: Currently, it is the api - base of the Volcano Ark Platform.
2. `OPENAI_API_KEY`: It is recommended to configure it directly using environment variables to prevent leakage. Of course, it can also be configured directly here.
3. `OPENAI_MODEL` and `OPENAI_MODEL_THINKING`: Model names, please adjust according to the actual situation.
4. `SENSE_VOICE_LOCAL_MODEL_PATH`: Modify it to the address of the sense_voice model weights you downloaded.
5. `SENSE_VOICE_LOCAL_VAD_MODEL_PATH`: Modify it to the address of the vad_model weights you downloaded.
6. `KB_BASE_PATH`: The basic path for slice processing. All files will be relative to this path.

Note: Absolute paths are recommended for the above paths.

### 2. Start the project

(Choose either 2.1 or 2.2)

### 2.1 Script Startup

Please modify the `query` section in `src/main.py` according to your requirements.

Note: `raw_video` must be a path relative to `KB_BASE_PATH`. This design is to reduce the possibility of path errors when the large model is being invoked.

```bash
cd src
python main.py
```

### 2.2 Web UI

```bash
bash start_up.sh
```

Then you can access the Web UI. 

## 🫡Introduction to the Implementation

The overall architecture diagram is as follows.

![](./assert/images/stream_en.png)

For the specific implementation, you can directly refer to the `src/processor` part of the code. This is the entry point of each module, and the overall idea is very clear in the diagram.

## ✅Todo List
- [x] Graphical user interface: Consider using Streamlit to create a graphical user interface.
- [ ] Implement support for the ASR API to break free from local inference limitations.
- [ ] Expand `vedit - mcp`. Currently, it only supports basic editing functions, and further support needs to be provided.
- [ ] Add the subtitle - adding function.
- [ ] Add the API calling method for speech recognition.
- [ ] Add the cover generation function. First, create a simple version.
- [ ] Consider support for singing livestreams.
- [ ] Consider using speaker separation to support scenarios with non - single sound signals, such as game livestreams and video - watching livestreams. 

## 🔥Latest News

- 2025-05-08, a simple web UI interface was implemented using Streamlit.