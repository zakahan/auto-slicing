import os
import json
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
    return "raw/upload_file.mp4"

def list_existing_file_list():
    return [
        "raw/existing_1.mp4",
        "raw/existing_2.mp4"
    ]
    

def submit_root_processor():
    print("刷新")
    return [
        {"id":1,"title": "1.mp4", "path": "xxx1"},
        {"id":2,"title": "2.mp4", "path": "xxx2"},
        {"id":3,"title": "3.mp4", "path": "xxx3"},
        {"id":4,"title": "4.mp4", "path": "xxx4"},
    ]

menu1 = 'upload'
menu2 = 'existing'
# state group
with st.sidebar:
    st.title("☝️🤓💡切片剪辑神器")
    if st.button("✅开始处理流程", disabled=st.session_state.raw_path is None):
        st.session_state.submit = True  # 点击时将状态设为 True
    # fixed_height = "50px"
    # border_style = "1px solid #ccc"
    # st.markdown(
    #     f'<div style="height: {fixed_height}; overflow-y: auto; border: {border_style};">'
    #     f'{st.session_state.raw_path if st.session_state.raw_path is not None else ""}'
    #     f'</div>',
    #     unsafe_allow_html=True
    # )

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
    # # st.button("这个时候才允许后续处理")
    # st.subheader("raw_video")
    # st.markdown(st.session_state.raw_path)
    # st.subheader("introduction")
    # st.markdown(st.session_state.introduction)

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
    st.success(st.session_state.item_list)
    for item in st.session_state.item_list:
        with st.expander(f"{item['id']}_{item['title']}"):
            sub_col1, sub_col2 = st.columns([9,1])
            with sub_col1:
                st.write(item['path'])
            with sub_col2:
                video_source_id = f"vid_{item['path']}"
                tog = st.toggle('📽️', key=video_source_id)
                # todo: 这里展示视频
                if tog:
                    st.markdown("ovo")
                else:
                    st.markdown("x_x")

    pass