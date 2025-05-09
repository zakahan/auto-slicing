import os
import json
import secrets
import requests
import streamlit as st
from streamlit_option_menu import option_menu
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()
from parser.json_parser import json2dict, dict2json

st.set_page_config(
    page_title="☝️🤓💡切片神器（简陋版）",
    layout="wide",
)

# content
options_dict = json2dict("introduction.json")
options = list(options_dict.keys())

# 在代码开头初始化 session_state
if "submit" not in st.session_state:
    st.session_state.submit = False
if "item_list" not in st.session_state:
    st.session_state.item_list = None
if "introduction" not in st.session_state:
    st.session_state.introduction = options_dict[options[0]]
if "kb_base_path" not in st.session_state:
    st.session_state.kb_base_path = os.getenv("KB_BASE_PATH")
if "raw_path" not in st.session_state:
    st.session_state.raw_path = None


def upload_file_in_chunks(file_path, chunk_size=1024 * 1024 * 5):  # 5MB 每块
    API_URL = "http://127.0.0.1:8090/uploadfile/"
    file_name = os.path.basename(file_path)
    total_size = os.path.getsize(file_path)
    total_chunks = (total_size + chunk_size - 1) // chunk_size

    progress_bar = st.progress(0)

    with open(file_path, "rb") as file:
        for chunk_number in range(1, total_chunks + 1):
            chunk = file.read(chunk_size)
            files = {"file": (file_name, chunk)}
            data = {
                "file_name": file_name,
                "chunk_number": chunk_number,
                "total_chunks": total_chunks
            }
            response = requests.post(API_URL, files=files, data=data)
            if response.status_code != 200:
                st.error(f"Error uploading chunk {chunk_number}: {response.text}")
                return
            progress = chunk_number / total_chunks
            progress_bar.progress(progress)
    raw_path = response.json()['path']
    return raw_path

def list_existing_file_list():
    API_URL = "http://127.0.0.1:8090/list-files"
    response = requests.get(API_URL)
    if response.status_code == 200:
        # st.success(response.json())
        return list(response.json())
    

def submit_root_processor():
    API_URL =  "http://127.0.0.1:8090/submit"
    response = requests.post(
        API_URL,
        json={
            'task_id': secrets.token_hex(4),
            'raw_path': st.session_state.raw_path,
            'introduction': st.session_state.introduction
        }
        )
    if response.status_code == 200:
        return response.json()
    else:
        return {}

def get_video_mime_type(path):
    """根据文件路径获取视频MIME类型（常见格式映射）"""
    if not path:
        return "video/mp4"  # 默认格式
    ext = os.path.splitext(path)[1].lower().lstrip('.')  # 获取扩展名并去除点号
    mime_map = {
        "mp4": "video/mp4",
        "avi": "video/x-msvideo",
        "mov": "video/quicktime",
        "mkv": "video/x-matroska",
        "flv": "video/x-flv",
        "wmv": "video/x-ms-wmv"
    }
    return mime_map.get(ext, "video/mp4")  # 未知格式默认使用mp4
    

menu1 = 'upload'
menu2 = 'existing'
# state group
with st.sidebar:
    st.title("☝️🤓💡切片剪辑神器")
    if st.button("✅开始处理流程", disabled=st.session_state.raw_path is None):
        st.session_state.submit = True  # 点击时将状态设为 True

    menu = option_menu("视频读取方式", [menu1, menu2],
                    icons=['upload', "chat-square-text"],
                    menu_icon="wrench-adjustable", default_index=0)

    # 介绍选择
    selected_option = st.selectbox("🔘请选择一个当前的主播id", options, index=0)


    st.session_state.introduction = options_dict[selected_option]
    st.divider()  # 插入分割线

    if menu == menu1:
        # st.session_state.raw_path = None
        # 输入路径
        uploaded_file = st.file_uploader("🔼上传视频文件", type=["mp4", "avi", "mov"])

        if uploaded_file is not None:
            file_path = os.path.join(os.getcwd(), uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            if st.button("上传文件"):
                st.session_state.raw_path = upload_file_in_chunks(file_path)
                os.remove(file_path)
    else:
        raw_path_list = list_existing_file_list()
        # st.markdown(raw_path_list)
        st.session_state.raw_path = st.selectbox("👀请从已经存在的文件中选择", raw_path_list)
        
    
    
if st.session_state.raw_path is not None:

    fixed_height = "50px"
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f'**选定路径**： {st.session_state.raw_path if st.session_state.raw_path is not None else ""}'
        )
    with col2:
        st.markdown(
            f'**选定主播**： {selected_option}'
        )
if st.session_state.submit:
    if st.session_state.item_list is None:
        st.session_state.item_list = submit_root_processor()
    # st.success(st.session_state.item_list)
    for i, item in enumerate(st.session_state.item_list):
        # def callback(path=item["path"]):  # 使用默认参数捕获当前的 item["path"]
            
        with st.expander(f"{i}_{item['title']}"):
            sub_col1, sub_col2 = st.columns([9,1])
            
            with sub_col2:
                video_source_id = f"vid_{item['path']}"
                tog = st.toggle('📽️', key=video_source_id)
                # todo: 这里展示视频
            with sub_col1:
                if tog:
                    st.markdown(" ovo")
                else:
                    st.markdown(" x_x")
            if tog:
                st.session_state.video_path = item['path']
                video_format = get_video_mime_type(st.session_state.video_path)
                st.video(st.session_state.video_path, format=video_format)
            else:
                pass

    pass


