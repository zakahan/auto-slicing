import os
import json
import streamlit as st
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()
from .parser.json_parser import json2dict, dict2json

options_dict = json2dict("introduction.json")
options = options_dict.keys()

st.set_page_config(
    page_title="☝️🤓💡切片神器（简陋版）",
    layout="wide",
)



# state group
with st.sidebar:
    st.title("🔥切片剪辑神器（破产版）")

    selected_option = st.selectbox("请选择一个选项", options, index=0)


